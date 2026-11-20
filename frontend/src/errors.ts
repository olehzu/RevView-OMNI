import { API_UNREACHABLE, type ApiError } from "./api";

/**
 * An area's messages for its own error codes (design/rev.md, Error messages).
 * Each area keeps its own; only the shared codes and the fallback live here.
 */
export type AreaMessages = Readonly<
  Record<string, (error: ApiError) => string>
>;

const SHARED_MESSAGES: AreaMessages = {
  VALIDATION_FAILED: () => "The request was not valid.",
  INTERNAL_ERROR: () =>
    "Something went wrong in RevView/OMNI. Try again. If it keeps happening, report the code shown below.",
  [API_UNREACHABLE]: () =>
    "RevView/OMNI could not be reached. Check that the application is running.",
};

/**
 * The message the Author sees for an error. An area's own message wins for its
 * codes; an unknown code gets the fallback naming the code, never a blank.
 */
export function messageFor(
  error: ApiError,
  areaMessages: AreaMessages = {},
): string {
  if (Object.hasOwn(areaMessages, error.code)) {
    return areaMessages[error.code](error);
  }
  if (Object.hasOwn(SHARED_MESSAGES, error.code)) {
    return SHARED_MESSAGES[error.code](error);
  }
  return `The request could not be completed (${error.code}).`;
}
