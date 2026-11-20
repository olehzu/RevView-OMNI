const API_PREFIX = "/api/v1";

/** Builds the URL of an application API resource, e.g. apiPath('/health'). */
export function apiPath(resource: string): string {
  return resource.startsWith("/")
    ? `${API_PREFIX}${resource}`
    : `${API_PREFIX}/${resource}`;
}

/**
 * The client-side code for "no envelope came back": a refused connection, a body
 * that is not JSON, or a body that is not the section 8.2.3 envelope. The server
 * never sends it.
 */
export const API_UNREACHABLE = "API_UNREACHABLE";

/** The `error` of the section 8.2.3 envelope; `source` names an unavailable external system. */
export interface ApiError {
  code: string;
  message: string;
  source: string | null;
}

/** Either the envelope's `data` or its `error`, never both. */
export type ApiResult<T> =
  { ok: true; data: T } | { ok: false; error: ApiError };

/** The `fetch` the client calls; tests pass their own. */
export type Fetch = (input: string, init?: RequestInit) => Promise<Response>;

function unreachable(): { ok: false; error: ApiError } {
  return {
    ok: false,
    error: {
      code: API_UNREACHABLE,
      message: "No response envelope came back from the application.",
      source: null,
    },
  };
}

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function asApiError(value: unknown): ApiError | null {
  if (
    !isObject(value) ||
    typeof value.code !== "string" ||
    typeof value.message !== "string"
  ) {
    return null;
  }
  const source = value.source ?? null;
  if (source !== null && typeof source !== "string") {
    return null;
  }
  return { code: value.code, message: value.message, source };
}

/**
 * Reads the section 8.2.3 envelope once. `data` is taken only from a 2xx and
 * `error` only from a non-2xx; anything else is API_UNREACHABLE, so a failure is
 * never shown as success (section 8.2.1).
 */
export function parseEnvelope<T>(status: number, body: unknown): ApiResult<T> {
  if (!isObject(body)) {
    return unreachable();
  }
  const success = status >= 200 && status < 300;
  if (success && "data" in body && !("error" in body)) {
    return { ok: true, data: body.data as T };
  }
  if (!success && "error" in body && !("data" in body)) {
    const error = asApiError(body.error);
    if (error !== null) {
      return { ok: false, error };
    }
  }
  return unreachable();
}

const browserFetch: Fetch = (input, init) => fetch(input, init);

/**
 * Calls an API resource and reads its envelope. A rejected fetch or a body that
 * is not JSON gives API_UNREACHABLE.
 */
export async function request<T>(
  method: string,
  resource: string,
  fetchFn: Fetch = browserFetch,
): Promise<ApiResult<T>> {
  let response: Response;
  try {
    response = await fetchFn(apiPath(resource), {
      method,
      headers: { Accept: "application/json" },
    });
  } catch {
    return unreachable();
  }
  let body: unknown;
  try {
    body = await response.json();
  } catch {
    return unreachable();
  }
  return parseEnvelope<T>(response.status, body);
}
