import { describe, expect, it } from "vitest";
import {
  API_UNREACHABLE,
  apiPath,
  type Fetch,
  parseEnvelope,
  request,
} from "./api";

describe("apiPath", () => {
  it("prefixes a resource with the API version", () => {
    expect(apiPath("/health")).toBe("/api/v1/health");
  });

  it("adds the slash when the resource has none", () => {
    expect(apiPath("health")).toBe("/api/v1/health");
  });
});

const svnUnavailable = {
  code: "SVN_UNAVAILABLE",
  message: "SVN is unavailable, so its evidence could not be read.",
  source: "SVN",
};

// Page: envelope success (section 8.2.3)
describe("parseEnvelope, success", () => {
  it("returns the data of a 200", () => {
    const data = { review_id: "rev-0001", status: "In preparation" };
    expect(parseEnvelope(200, { data })).toEqual({ ok: true, data });
  });
});

// Page: envelope error (section 8.2.1)
describe("parseEnvelope, error", () => {
  it("returns a 503 error envelope's code, message, and source unchanged", () => {
    expect(parseEnvelope(503, { error: svnUnavailable })).toEqual({
      ok: false,
      error: svnUnavailable,
    });
  });

  it("keeps a null source", () => {
    const error = {
      code: "ASSEMBLY_INCOMPLETE",
      message: "The SVN Branch SYN-1-timer-fix has no Changed Files.",
      source: null,
    };
    expect(parseEnvelope(409, { error })).toEqual({ ok: false, error });
  });
});

// Page: API unreachable
describe("parseEnvelope, no envelope", () => {
  const unreachable = { ok: false, error: { code: API_UNREACHABLE } };

  it.each([
    ["neither data nor error", 200, { status: "ok" }],
    [
      "neither data nor error, on an error status",
      502,
      { detail: "Bad gateway" },
    ],
    ["not an object", 200, "Materials assembled"],
    ["null", 200, null],
    ["an array", 200, [{ data: {} }]],
    [
      "data on an error status",
      503,
      { data: { status: "Materials assembled" } },
    ],
    ["error on a success status", 200, { error: svnUnavailable }],
    ["both data and error", 200, { data: {}, error: svnUnavailable }],
    [
      "an error without a code",
      500,
      { error: { message: "Boom", source: null } },
    ],
    [
      "an error whose source is not a string",
      503,
      { error: { ...svnUnavailable, source: 7 } },
    ],
  ])("gives API_UNREACHABLE for %s", (_, status, body) => {
    expect(parseEnvelope(status, body)).toMatchObject(unreachable);
  });
});

function respondWith(status: number, body: string): Fetch {
  return () => Promise.resolve(new Response(body, { status }));
}

describe("request", () => {
  it("calls the versioned resource with the method and reads the envelope", async () => {
    const calls: Array<[string, RequestInit | undefined]> = [];
    const fetchFn: Fetch = (input, init) => {
      calls.push([input, init]);
      return Promise.resolve(
        new Response(JSON.stringify({ data: { id: 1 } }), { status: 200 }),
      );
    };
    expect(
      await request("POST", "/review-packages/rev-0001/assembly", fetchFn),
    ).toEqual({
      ok: true,
      data: { id: 1 },
    });
    expect(calls).toHaveLength(1);
    expect(calls[0][0]).toBe("/api/v1/review-packages/rev-0001/assembly");
    expect(calls[0][1]?.method).toBe("POST");
  });

  it("returns an error envelope as an error", async () => {
    const result = await request(
      "POST",
      "x",
      respondWith(503, JSON.stringify({ error: svnUnavailable })),
    );
    expect(result).toEqual({ ok: false, error: svnUnavailable });
  });

  // Page: API unreachable
  it("gives API_UNREACHABLE when the fetch rejects", async () => {
    const refused: Fetch = () =>
      Promise.reject(new TypeError("Failed to fetch"));
    expect(await request("GET", "x", refused)).toMatchObject({
      ok: false,
      error: { code: API_UNREACHABLE, source: null },
    });
  });

  it("gives API_UNREACHABLE when the body is not JSON", async () => {
    const proxyPage = respondWith(502, "<html><body>Bad gateway</body></html>");
    expect(await request("GET", "x", proxyPage)).toMatchObject({
      ok: false,
      error: { code: API_UNREACHABLE },
    });
  });

  it("gives API_UNREACHABLE when the body has neither data nor error", async () => {
    expect(await request("GET", "x", respondWith(200, "{}"))).toMatchObject({
      ok: false,
      error: { code: API_UNREACHABLE },
    });
  });
});
