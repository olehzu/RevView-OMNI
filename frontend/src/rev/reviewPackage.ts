/**
 * The review package page's API calls, error messages, and logic
 * (UC-REV-assemble-materials; design/rev.md, the review package page).
 * Types mirror backend/app/rev/models.py; field names are the API contract.
 */
import {
  API_UNREACHABLE,
  type ApiError,
  type ApiResult,
  type Fetch,
  request,
} from "../api";
import type { AreaMessages } from "../errors";

export type ReviewPackageStatus =
  "In preparation" | "Materials assembled" | "Pending build validation";

/** Whether an external system answered; `null` means it was not asked yet. */
export type Evidence = "available" | "unavailable" | null;

export type Platform = "common" | "falcon" | "phoenix";
export type Category = "code" | "tools" | "tests";

export interface ChangedFile {
  path: string;
  revision: string | null;
  repository_link: string;
}

export interface Diff {
  platform: Platform;
  category: Category;
  diff: string;
  changed_files: ChangedFile[];
}

export interface JenkinsBuild {
  build_number: number;
  name: string;
  result: string;
  /** UTC, ISO 8601 with `Z`. */
  built_at: string;
}

export interface ReviewChecklistTab {
  platform: Platform;
  changed_files: string[];
}

export interface ReviewRecord {
  id: string;
  review_id: string;
  jira_ticket_key: string;
}

/** A gap flagged for the Author (extension 2a1). */
export interface MissingMaterial {
  path: string;
  missing: "revision";
}

export interface ReviewPackage {
  review_id: string;
  status: ReviewPackageStatus;
  jira_ticket_key: string;
  svn_branch: string | null;
  svn_evidence: Evidence;
  jenkins_evidence: Evidence;
  diffs: Diff[];
  /** Newest first. */
  jenkins_builds: JenkinsBuild[];
  preselected_build: number | null;
  review_checklist: { tabs: ReviewChecklistTab[] } | null;
  review_record: ReviewRecord | null;
  missing: MissingMaterial[];
}

export const IN_PREPARATION: ReviewPackageStatus = "In preparation";

/** The review id is already trimmed by the page, where it is read from the input. */
function resource(reviewId: string): string {
  return `/review-packages/${encodeURIComponent(reviewId)}`;
}

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isStringOrNull(value: unknown): boolean {
  return value === null || isString(value);
}

function isArrayOf(value: unknown, item: (v: unknown) => boolean): boolean {
  return Array.isArray(value) && value.every(item);
}

const STATUSES: readonly unknown[] = [
  "In preparation",
  "Materials assembled",
  "Pending build validation",
];
const EVIDENCE: readonly unknown[] = ["available", "unavailable", null];

function isChangedFile(v: unknown): boolean {
  return (
    isObject(v) &&
    isString(v.path) &&
    isStringOrNull(v.revision) &&
    isString(v.repository_link)
  );
}

function isDiff(v: unknown): boolean {
  return (
    isObject(v) &&
    isString(v.platform) &&
    isString(v.category) &&
    isString(v.diff) &&
    isArrayOf(v.changed_files, isChangedFile)
  );
}

function isJenkinsBuild(v: unknown): boolean {
  return (
    isObject(v) &&
    typeof v.build_number === "number" &&
    isString(v.name) &&
    isString(v.result) &&
    isString(v.built_at)
  );
}

function isChecklist(v: unknown): boolean {
  return (
    v === null ||
    (isObject(v) &&
      isArrayOf(
        v.tabs,
        (t) =>
          isObject(t) &&
          isString(t.platform) &&
          isArrayOf(t.changed_files, isString),
      ))
  );
}

/**
 * Whether a 2xx `data` is a review package the page can show. A body of another
 * shape is a failure, never shown as success or as a blank page (section 8.2.1).
 */
export function isReviewPackage(v: unknown): v is ReviewPackage {
  return (
    isObject(v) &&
    isString(v.review_id) &&
    STATUSES.includes(v.status) &&
    isString(v.jira_ticket_key) &&
    isStringOrNull(v.svn_branch) &&
    EVIDENCE.includes(v.svn_evidence) &&
    EVIDENCE.includes(v.jenkins_evidence) &&
    isArrayOf(v.diffs, isDiff) &&
    isArrayOf(v.jenkins_builds, isJenkinsBuild) &&
    (v.preselected_build === null || typeof v.preselected_build === "number") &&
    isChecklist(v.review_checklist) &&
    (v.review_record === null ||
      (isObject(v.review_record) && isString(v.review_record.id))) &&
    isArrayOf(v.missing, (m) => isObject(m) && isString(m.path))
  );
}

async function reviewPackageResult(
  pending: Promise<ApiResult<unknown>>,
): Promise<ApiResult<ReviewPackage>> {
  const result = await pending;
  if (!result.ok) {
    return result;
  }
  if (isReviewPackage(result.data)) {
    return { ok: true, data: result.data };
  }
  return {
    ok: false,
    error: {
      code: API_UNREACHABLE,
      message: "The response was not a review package.",
      source: null,
    },
  };
}

/** Loads the stored review package, so the Author sees its state (PRE-1). */
export function getReviewPackage(
  reviewId: string,
  fetchFn?: Fetch,
): Promise<ApiResult<ReviewPackage>> {
  return reviewPackageResult(request("GET", resource(reviewId), fetchFn));
}

/** Assembles the review materials (steps 1 to 6). */
export function assembleMaterials(
  reviewId: string,
  fetchFn?: Fetch,
): Promise<ApiResult<ReviewPackage>> {
  return reviewPackageResult(
    request("POST", `${resource(reviewId)}/assembly`, fetchFn),
  );
}

/** The ASSEMBLY_INCOMPLETE message: the server's text names the gap, ending in one period. */
function assemblyIncomplete(serverMessage: string): string {
  const gap = serverMessage.trim();
  if (gap === "") {
    return "The materials could not be assembled.";
  }
  const sentence = /[.!?]$/.test(gap) ? gap : `${gap}.`;
  return `The materials could not be assembled: ${sentence}`;
}

/** The area's rows of the Error messages table, for the package with this review id. */
export function reviewPackageMessages(reviewId: string): AreaMessages {
  return {
    SVN_UNAVAILABLE: () =>
      "SVN did not respond, so the Changed Files could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    JENKINS_UNAVAILABLE: () =>
      "Jenkins did not respond, so the Jenkins Builds could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    ASSEMBLY_INCOMPLETE: (error: ApiError) => assemblyIncomplete(error.message),
    REVIEW_PACKAGE_NOT_IN_PREPARATION: () =>
      "Materials can be assembled only while the package is In preparation. This package is already past that.",
    REVIEW_PACKAGE_NOT_FOUND: () =>
      `There is no review package with the id ${reviewId}. Check the id and load it again.`,
    // The shared message names no field; this page's only input is the review id.
    VALIDATION_FAILED: () => "The request was not valid. Check the review id.",
  };
}

/** What the page does after an Assemble error (the Error messages table, "Then the page"). */
export type AfterError = "reload" | "clear" | "nothing";

const RELOAD_AFTER = new Set([
  "SVN_UNAVAILABLE",
  "JENKINS_UNAVAILABLE",
  "ASSEMBLY_INCOMPLETE",
  "REVIEW_PACKAGE_NOT_IN_PREPARATION",
]);

export function afterAssembleError(code: string): AfterError {
  if (RELOAD_AFTER.has(code)) {
    return "reload";
  }
  return code === "REVIEW_PACKAGE_NOT_FOUND" ? "clear" : "nothing";
}

const PLATFORM_ORDER: readonly Platform[] = ["common", "falcon", "phoenix"];
const CATEGORY_ORDER: readonly Category[] = ["code", "tools", "tests"];

export interface PlatformDiffs {
  platform: Platform;
  diffs: Diff[];
}

/** The Diffs by Platform (common, falcon, phoenix), then Category (code, tools, tests). Step 3. */
export function groupDiffs(diffs: readonly Diff[]): PlatformDiffs[] {
  return PLATFORM_ORDER.map((platform) => ({
    platform,
    diffs: diffs
      .filter((d) => d.platform === platform)
      .sort(
        (a, b) =>
          CATEGORY_ORDER.indexOf(a.category) -
          CATEGORY_ORDER.indexOf(b.category),
      ),
  })).filter((group) => group.diffs.length > 0);
}

/** How a system's evidence reads; "unavailable" is never shown as passing (section 8.2.1). */
export function evidenceLabel(evidence: Evidence): string {
  if (evidence === null) {
    return "not read yet";
  }
  return evidence;
}

/** The review id from the `review` query parameter, or empty; there is no default. */
export function initialReviewId(search: string): string {
  return new URLSearchParams(search).get("review") ?? "";
}

/** Assemble is offered only while the package is "In preparation" (PRE-1, a convenience, section 8.2.5). */
export function canAssemble(pkg: ReviewPackage): boolean {
  return pkg.status === IN_PREPARATION;
}

/**
 * Jenkins answered and no build matched (4a1). Shown whatever the status, because
 * 2a1 and 4a1 together leave "In preparation".
 */
export function noMatchingBuild(pkg: ReviewPackage): boolean {
  return (
    pkg.jenkins_evidence === "available" && pkg.jenkins_builds.length === 0
  );
}

function pad(n: number): string {
  return String(n).padStart(2, "0");
}

/**
 * A build time as `YYYY-MM-DD HH:MM:SS UTC`, read with UTC methods only. A time
 * with no `Z` or offset would be read as local time, so it is shown as it came,
 * never labelled UTC.
 */
export function formatBuildTime(iso: string): string {
  if (!/(?:Z|[+-]\d{2}:?\d{2})$/i.test(iso.trim())) {
    return iso;
  }
  const t = new Date(iso);
  if (Number.isNaN(t.getTime())) {
    return iso;
  }
  return (
    `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())} ` +
    `${pad(t.getUTCHours())}:${pad(t.getUTCMinutes())}:${pad(t.getUTCSeconds())} UTC`
  );
}

/** The repository link if it is a web address; anything else is shown as text only. */
export function safeLink(url: string): string | null {
  try {
    const { protocol } = new URL(url);
    return protocol === "https:" || protocol === "http:" ? url : null;
  } catch {
    return null;
  }
}
