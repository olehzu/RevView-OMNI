import { describe, expect, it } from "vitest";
import { API_UNREACHABLE, type ApiError } from "./api";
import { type AreaMessages, messageFor } from "./errors";

function error(code: string, message = "server message"): ApiError {
  return { code, message, source: null };
}

// Page: every extension's error code (the shared rows of the Error messages table)
describe("messageFor, shared codes", () => {
  it("gives the VALIDATION_FAILED message, which names no page's field", () => {
    expect(messageFor(error("VALIDATION_FAILED"))).toBe(
      "The request was not valid.",
    );
  });

  it("gives the INTERNAL_ERROR message", () => {
    expect(messageFor(error("INTERNAL_ERROR"))).toBe(
      "Something went wrong in RevView/OMNI. Try again. If it keeps happening, report the code shown below.",
    );
  });

  it("gives the API_UNREACHABLE message", () => {
    expect(messageFor(error(API_UNREACHABLE))).toBe(
      "RevView/OMNI could not be reached. Check that the application is running.",
    );
  });

  it.each([
    "NOT_FOUND",
    "METHOD_NOT_ALLOWED",
    "REQUEST_FAILED",
    "SOME_FUTURE_CODE",
  ])("gives the fallback naming the code for %s", (code) => {
    expect(messageFor(error(code))).toBe(
      `The request could not be completed (${code}).`,
    );
  });

  it("never shows the server's message for an unknown code", () => {
    expect(
      messageFor(error("SOME_FUTURE_CODE", "Traceback ...")),
    ).not.toContain("Traceback");
  });
});

describe("messageFor, area messages", () => {
  const area: AreaMessages = {
    SOME_AREA_CODE: (e) => `Area says: ${e.message}`,
    INTERNAL_ERROR: () => "The area's own wording.",
  };

  it("uses the area's message for the area's code", () => {
    expect(messageFor(error("SOME_AREA_CODE", "detail"), area)).toBe(
      "Area says: detail",
    );
  });

  it("lets the area's message win over a shared one", () => {
    expect(messageFor(error("INTERNAL_ERROR"), area)).toBe(
      "The area's own wording.",
    );
  });

  it("still gives shared messages and the fallback with area messages passed", () => {
    expect(messageFor(error("VALIDATION_FAILED"), area)).toBe(
      "The request was not valid.",
    );
    expect(messageFor(error("NOT_FOUND"), area)).toBe(
      "The request could not be completed (NOT_FOUND).",
    );
  });

  it("does not treat inherited object keys as codes", () => {
    expect(messageFor(error("toString"), area)).toBe(
      "The request could not be completed (toString).",
    );
  });
});
