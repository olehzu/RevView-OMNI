import { describe, expect, it } from "vitest";
import type { ApiError, Fetch } from "../api";
import { messageFor } from "../errors";
import {
  afterAssembleError,
  assembleMaterials,
  canAssemble,
  type Diff,
  evidenceLabel,
  formatBuildTime,
  getReviewPackage,
  groupDiffs,
  initialReviewId,
  noMatchingBuild,
  type ReviewPackage,
  reviewPackageMessages,
  safeLink,
} from "./reviewPackage";

// Synthetic Data, shaped like the API contract's example (design/rev.md).
function reviewPackage(overrides: Partial<ReviewPackage> = {}): ReviewPackage {
  return {
    review_id: "rev-0001",
    status: "In preparation",
    jira_ticket_key: "SYN-1",
    svn_branch: null,
    svn_evidence: null,
    jenkins_evidence: null,
    diffs: [],
    jenkins_builds: [],
    preselected_build: null,
    review_checklist: null,
    review_record: null,
    missing: [],
    ...overrides,
  };
}

function diff(platform: Diff["platform"], category: Diff["category"]): Diff {
  const path = `${category}/${platform}/branches/SYN-1-timer-fix/src/file`;
  return {
    platform,
    category,
    diff: `Index: ${path}`,
    changed_files: [
      {
        path,
        revision: "1042",
        repository_link: `https://svn.example.invalid/repo/${path}?p=1042`,
      },
    ],
  };
}

function error(code: string, message = "server message"): ApiError {
  return { code, message, source: null };
}

// Page: every extension's error code (the area's rows of the Error messages table)
describe("messageFor with the review package messages", () => {
  const messages = reviewPackageMessages("rev-0001");
  const shown = (code: string, message?: string) =>
    messageFor(error(code, message), messages);

  it("gives the SVN_UNAVAILABLE message", () => {
    expect(shown("SVN_UNAVAILABLE")).toBe(
      "SVN did not respond, so the Changed Files could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    );
  });

  it("gives the JENKINS_UNAVAILABLE message", () => {
    expect(shown("JENKINS_UNAVAILABLE")).toBe(
      "Jenkins did not respond, so the Jenkins Builds could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    );
  });

  it("includes the server's message for ASSEMBLY_INCOMPLETE, the only place the gap is named", () => {
    expect(
      shown(
        "ASSEMBLY_INCOMPLETE",
        "No SVN Branch name contains the Jira Ticket key SYN-1.",
      ),
    ).toBe(
      "The materials could not be assembled: No SVN Branch name contains the Jira Ticket key SYN-1.",
    );
  });

  it("ends an ASSEMBLY_INCOMPLETE message with one period", () => {
    expect(shown("ASSEMBLY_INCOMPLETE", "no Changed Files")).toBe(
      "The materials could not be assembled: no Changed Files.",
    );
  });

  it("leaves no dangling colon when the server names no gap", () => {
    expect(shown("ASSEMBLY_INCOMPLETE", "  ")).toBe(
      "The materials could not be assembled.",
    );
  });

  it("gives the REVIEW_PACKAGE_NOT_IN_PREPARATION message", () => {
    expect(shown("REVIEW_PACKAGE_NOT_IN_PREPARATION")).toBe(
      "Materials can be assembled only while the package is In preparation. This package is already past that.",
    );
  });

  it("names the review id for REVIEW_PACKAGE_NOT_FOUND", () => {
    expect(
      messageFor(
        error("REVIEW_PACKAGE_NOT_FOUND"),
        reviewPackageMessages("rev-9999"),
      ),
    ).toBe(
      "There is no review package with the id rev-9999. Check the id and load it again.",
    );
  });

  it("adds the review id hint to VALIDATION_FAILED", () => {
    expect(shown("VALIDATION_FAILED")).toBe(
      "The request was not valid. Check the review id.",
    );
  });

  it("gives the shared INTERNAL_ERROR message", () => {
    expect(shown("INTERNAL_ERROR")).toBe(
      "Something went wrong in RevView/OMNI. Try again. If it keeps happening, report the code shown below.",
    );
  });

  it("gives the fallback naming an unknown code", () => {
    expect(shown("METHOD_NOT_ALLOWED")).toBe(
      "The request could not be completed (METHOD_NOT_ALLOWED).",
    );
  });
});

describe("afterAssembleError", () => {
  it.each([
    "SVN_UNAVAILABLE",
    "JENKINS_UNAVAILABLE",
    "ASSEMBLY_INCOMPLETE",
    "REVIEW_PACKAGE_NOT_IN_PREPARATION",
  ])("reloads the package after %s", (code) => {
    expect(afterAssembleError(code)).toBe("reload");
  });

  it("clears the package after REVIEW_PACKAGE_NOT_FOUND", () => {
    expect(afterAssembleError("REVIEW_PACKAGE_NOT_FOUND")).toBe("clear");
  });

  it.each([
    "VALIDATION_FAILED",
    "INTERNAL_ERROR",
    "API_UNREACHABLE",
    "NOT_FOUND",
  ])("does nothing more after %s", (code) => {
    expect(afterAssembleError(code)).toBe("nothing");
  });
});

// Page: step 3 grouping
describe("groupDiffs", () => {
  it("orders Platforms common, falcon, phoenix and Categories code, tools, tests", () => {
    const groups = groupDiffs([
      diff("phoenix", "tests"),
      diff("falcon", "tests"),
      diff("common", "tools"),
      diff("falcon", "code"),
      diff("phoenix", "code"),
      diff("falcon", "tools"),
    ]);
    expect(
      groups.map((g) => [g.platform, g.diffs.map((d) => d.category)]),
    ).toEqual([
      ["common", ["tools"]],
      ["falcon", ["code", "tools", "tests"]],
      ["phoenix", ["code", "tests"]],
    ]);
  });

  it("keeps each Diff's Changed Files", () => {
    const input = diff("falcon", "code");
    expect(groupDiffs([input])[0].diffs[0].changed_files).toEqual(
      input.changed_files,
    );
  });

  it("gives nothing for no Diffs", () => {
    expect(groupDiffs([])).toEqual([]);
  });
});

// Page: evidence (section 8.2.1)
describe("evidenceLabel", () => {
  it("reads available, unavailable, and not read yet", () => {
    expect(evidenceLabel("available")).toBe("available");
    expect(evidenceLabel("unavailable")).toBe("unavailable");
    expect(evidenceLabel(null)).toBe("not read yet");
  });

  it("never gives a passing word for unavailable", () => {
    expect(evidenceLabel("unavailable")).not.toMatch(
      /^available|pass|ok|success/i,
    );
  });
});

// Page: choosing the package
describe("initialReviewId", () => {
  it("reads the review query parameter", () => {
    expect(initialReviewId("?review=rev-0001")).toBe("rev-0001");
  });

  it("is empty with no parameter; there is no default", () => {
    expect(initialReviewId("")).toBe("");
    expect(initialReviewId("?other=1")).toBe("");
  });
});

describe("getReviewPackage and assembleMaterials", () => {
  function recording(): { fetchFn: Fetch; calls: string[][] } {
    const calls: string[][] = [];
    const fetchFn: Fetch = (input, init) => {
      calls.push([init?.method ?? "", input]);
      return Promise.resolve(
        new Response(JSON.stringify({ data: reviewPackage() }), {
          status: 200,
        }),
      );
    };
    return { fetchFn, calls };
  }

  it("calls the two endpoints of the API contract", async () => {
    const { fetchFn, calls } = recording();
    await getReviewPackage("rev-0001", fetchFn);
    await assembleMaterials("rev-0001", fetchFn);
    expect(calls).toEqual([
      ["GET", "/api/v1/review-packages/rev-0001"],
      ["POST", "/api/v1/review-packages/rev-0001/assembly"],
    ]);
  });

  it("encodes the review id in the path", async () => {
    const { fetchFn, calls } = recording();
    await getReviewPackage("rev/1?x#y", fetchFn);
    expect(calls[0][1]).toBe("/api/v1/review-packages/rev%2F1%3Fx%23y");
  });

  it("returns a well-shaped package as success", async () => {
    const { fetchFn } = recording();
    expect(await getReviewPackage("rev-0001", fetchFn)).toEqual({
      ok: true,
      data: reviewPackage(),
    });
  });

  function respondingWithData(data: unknown): Fetch {
    return () =>
      Promise.resolve(new Response(JSON.stringify({ data }), { status: 200 }));
  }

  // A malformed 2xx is a failure, never success or a blank page (section 8.2.1).
  it.each([
    ["null data", null],
    ["no missing list", { ...reviewPackage(), missing: undefined }],
    ["no Diffs list", { ...reviewPackage(), diffs: "none" }],
    ["an unknown status", reviewPackage({ status: "Done" as never })],
    [
      "an evidence value that is not one of the three",
      { ...reviewPackage(), svn_evidence: "passing" },
    ],
    [
      "a Diff without its Changed Files",
      reviewPackage({
        diffs: [
          { ...diff("common", "code"), changed_files: undefined as never },
        ],
      }),
    ],
    [
      "a build without a time",
      reviewPackage({
        jenkins_builds: [
          { build_number: 57, name: "SYN-1", result: "SUCCESS" } as never,
        ],
      }),
    ],
    [
      "a checklist without tabs",
      reviewPackage({ review_checklist: {} as never }),
    ],
    // An unknown value would make groupDiffs drop the Diff and its files (#54 review).
    [
      "a Diff with an unknown Platform",
      reviewPackage({
        diffs: [{ ...diff("common", "code"), platform: "typo" as never }],
      }),
    ],
    [
      "a Diff with an unknown Category",
      reviewPackage({
        diffs: [{ ...diff("common", "code"), category: "docs" as never }],
      }),
    ],
    [
      "a checklist tab with an unknown Platform",
      reviewPackage({
        review_checklist: {
          tabs: [{ platform: "typo" as never, changed_files: [] }],
        },
      }),
    ],
  ])("gives API_UNREACHABLE for %s", async (_, data) => {
    for (const call of [getReviewPackage, assembleMaterials]) {
      expect(await call("rev-0001", respondingWithData(data))).toMatchObject({
        ok: false,
        error: { code: "API_UNREACHABLE", source: null },
      });
    }
  });

  it("passes an error envelope through unchanged", async () => {
    const notFound = {
      code: "REVIEW_PACKAGE_NOT_FOUND",
      message: "No review package has that id.",
      source: null,
    };
    const fetchFn: Fetch = () =>
      Promise.resolve(
        new Response(JSON.stringify({ error: notFound }), { status: 404 }),
      );
    expect(await getReviewPackage("rev-9999", fetchFn)).toEqual({
      ok: false,
      error: notFound,
    });
  });
});

describe("canAssemble (PRE-1, a convenience)", () => {
  it("is true only while the package is In preparation", () => {
    expect(canAssemble(reviewPackage())).toBe(true);
    expect(canAssemble(reviewPackage({ status: "Materials assembled" }))).toBe(
      false,
    );
    expect(
      canAssemble(reviewPackage({ status: "Pending build validation" })),
    ).toBe(false);
  });
});

describe("noMatchingBuild (4a1)", () => {
  it("is shown when Jenkins answered with no builds, whatever the status", () => {
    expect(
      noMatchingBuild(
        reviewPackage({
          status: "Pending build validation",
          jenkins_evidence: "available",
        }),
      ),
    ).toBe(true);
    // 2a1 and 4a1 together leave "In preparation".
    expect(
      noMatchingBuild(
        reviewPackage({
          status: "In preparation",
          jenkins_evidence: "available",
        }),
      ),
    ).toBe(true);
  });

  it("is not shown when Jenkins was unavailable or not asked", () => {
    expect(
      noMatchingBuild(reviewPackage({ jenkins_evidence: "unavailable" })),
    ).toBe(false);
    expect(noMatchingBuild(reviewPackage({ jenkins_evidence: null }))).toBe(
      false,
    );
  });

  it("is not shown when a build matched", () => {
    expect(
      noMatchingBuild(
        reviewPackage({
          jenkins_evidence: "available",
          jenkins_builds: [
            {
              build_number: 57,
              name: "SYN-1 timer fix",
              result: "SUCCESS",
              built_at: "2026-11-05T14:02:11Z",
            },
          ],
        }),
      ),
    ).toBe(false);
  });
});

describe("formatBuildTime", () => {
  it("shows the UTC time, labelled UTC", () => {
    expect(formatBuildTime("2026-11-05T14:02:11Z")).toBe(
      "2026-11-05 14:02:11 UTC",
    );
  });

  it("converts an offset time to UTC, never local time", () => {
    expect(formatBuildTime("2026-11-05T23:30:00-05:00")).toBe(
      "2026-11-06 04:30:00 UTC",
    );
  });

  it.each(["2026-11-05T14:02:11", "2026-11-05"])(
    "shows %s, which has no Z or offset, as it came and never labelled UTC",
    (naive) => {
      expect(formatBuildTime(naive)).toBe(naive);
    },
  );

  it("shows an unreadable time as it came", () => {
    expect(formatBuildTime("not a time")).toBe("not a time");
  });
});

describe("safeLink", () => {
  it("keeps a web address", () => {
    const link =
      "https://svn.example.invalid/repo/tools/common/branches/SYN-1-timer-fix/src/timer.py?p=1042";
    expect(safeLink(link)).toBe(link);
  });

  it.each(["javascript:alert(1)", "data:text/html,x", "not a url"])(
    "refuses %s",
    (link) => {
      expect(safeLink(link)).toBeNull();
    },
  );
});
