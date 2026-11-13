/**
 * The review package page's API calls, error messages, and logic
 * (UC-REV-assemble-materials; design/rev.md, the review package page).
 * Types mirror backend/app/rev/models.py; field names are the API contract.
 */
import { type ApiError, type ApiResult, type Fetch, request } from "../api";
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

function resource(reviewId: string): string {
  return `/review-packages/${encodeURIComponent(reviewId.trim())}`;
}

/** Loads the stored review package, so the Author sees its state (PRE-1). */
export function getReviewPackage(
  reviewId: string,
  fetchFn?: Fetch,
): Promise<ApiResult<ReviewPackage>> {
  return request<ReviewPackage>("GET", resource(reviewId), fetchFn);
}

/** Assembles the review materials (steps 1 to 6). */
export function assembleMaterials(
  reviewId: string,
  fetchFn?: Fetch,
): Promise<ApiResult<ReviewPackage>> {
  return request<ReviewPackage>(
    "POST",
    `${resource(reviewId)}/assembly`,
    fetchFn,
  );
}

function asSentence(text: string): string {
  const trimmed = text.trim();
  return /[.!?]$/.test(trimmed) ? trimmed : `${trimmed}.`;
}

/** The area's rows of the Error messages table, for the package with this review id. */
export function reviewPackageMessages(reviewId: string): AreaMessages {
  return {
    SVN_UNAVAILABLE: () =>
      "SVN did not respond, so the Changed Files could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    JENKINS_UNAVAILABLE: () =>
      "Jenkins did not respond, so the Jenkins Builds could not be read. Nothing was assembled and the package is still In preparation. Try Assemble again later.",
    ASSEMBLY_INCOMPLETE: (error: ApiError) =>
      `The materials could not be assembled: ${asSentence(error.message)}`,
    REVIEW_PACKAGE_NOT_IN_PREPARATION: () =>
      "Materials can be assembled only while the package is In preparation. This package is already past that.",
    REVIEW_PACKAGE_NOT_FOUND: () =>
      `There is no review package with the id ${reviewId.trim()}. Check the id and load it again.`,
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
  return new URLSearchParams(search).get("review")?.trim() ?? "";
}

/** Assemble is offered only while the package is "In preparation" (PRE-1, a convenience, section 8.2.5). */
export function canAssemble(pkg: ReviewPackage | null): boolean {
  return pkg !== null && pkg.status === IN_PREPARATION;
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

/** A build time as `YYYY-MM-DD HH:MM:SS UTC`, read with UTC methods only. */
export function formatBuildTime(iso: string): string {
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
