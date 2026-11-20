import { type SubmitEvent, useState } from "react";
import type { ApiError } from "../api";
import { messageFor } from "../errors";
import {
  afterAssembleError,
  assembleMaterials,
  canAssemble,
  type ChangedFile,
  type Evidence,
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

/** A message shown to the Author, with its code in small text for support. */
interface ShownError {
  message: string;
  code: string;
}

function shown(error: ApiError, reviewId: string): ShownError {
  return {
    message: messageFor(error, reviewPackageMessages(reviewId)),
    code: error.code,
  };
}

/**
 * The review package page (UC-REV-assemble-materials; design/rev.md). Everything
 * from the server is rendered as text, never as HTML.
 */
function ReviewPackagePage() {
  const [reviewId, setReviewId] = useState(() =>
    initialReviewId(window.location.search),
  );
  const [pkg, setPkg] = useState<ReviewPackage | null>(null);
  const [errors, setErrors] = useState<ShownError[]>([]);
  const [busy, setBusy] = useState(false);

  async function load(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = reviewId.trim();
    if (id === "" || busy) {
      return;
    }
    setBusy(true);
    setErrors([]);
    const result = await getReviewPackage(id);
    // On a failed Load the package on screen would not be the one asked for.
    setPkg(result.ok ? result.data : null);
    if (!result.ok) {
      setErrors([shown(result.error, id)]);
    }
    setBusy(false);
  }

  async function assemble() {
    if (pkg === null || !canAssemble(pkg) || busy) {
      return;
    }
    // Assemble acts on the package shown, not on whatever the input now holds.
    const id = pkg.review_id;
    setBusy(true);
    setErrors([]);
    const result = await assembleMaterials(id);
    if (result.ok) {
      setPkg(result.data);
    } else {
      const messages = [shown(result.error, id)];
      const next = afterAssembleError(result.error.code);
      if (next === "clear") {
        setPkg(null);
      } else if (next === "reload") {
        const reload = await getReviewPackage(id);
        if (reload.ok) {
          setPkg(reload.data);
        } else {
          // Never leave stale evidence on screen.
          messages.push(shown(reload.error, id));
          setPkg(null);
        }
      }
      setErrors(messages);
    }
    setBusy(false);
  }

  return (
    <>
      <h1>Review package</h1>
      <form className="review-id-form" onSubmit={load}>
        <label htmlFor="review-id">Review id</label>
        <input
          id="review-id"
          value={reviewId}
          onChange={(e) => setReviewId(e.target.value)}
          autoComplete="off"
        />
        <button type="submit" disabled={busy || reviewId.trim() === ""}>
          Load
        </button>
      </form>

      {errors.map((e, i) => (
        <div className="error" role="alert" key={i}>
          <p>{e.message}</p>
          <small>{e.code}</small>
        </div>
      ))}

      {pkg && (
        // Keyed by review id, so another package starts on its first checklist tab.
        <PackageView
          key={pkg.review_id}
          pkg={pkg}
          busy={busy}
          onAssemble={() => void assemble()}
        />
      )}
    </>
  );
}

function PackageView({
  pkg,
  busy,
  onAssemble,
}: {
  pkg: ReviewPackage;
  busy: boolean;
  onAssemble: () => void;
}) {
  return (
    <section aria-label="Review package">
      <dl className="facts">
        <dt>Review id</dt>
        <dd>{pkg.review_id}</dd>
        <dt>Status</dt>
        <dd>
          <strong>{pkg.status}</strong>
        </dd>
        <dt>Jira Ticket</dt>
        <dd>{pkg.jira_ticket_key}</dd>
        <dt>SVN Branch</dt>
        <dd>{pkg.svn_branch ?? "none yet"}</dd>
        <dt>SVN evidence</dt>
        <dd>
          <EvidenceBadge evidence={pkg.svn_evidence} />
        </dd>
        <dt>Jenkins evidence</dt>
        <dd>
          <EvidenceBadge evidence={pkg.jenkins_evidence} />
        </dd>
        <dt>Review Record</dt>
        <dd>{pkg.review_record?.id ?? "none yet"}</dd>
      </dl>

      <button
        type="button"
        onClick={onAssemble}
        disabled={busy || !canAssemble(pkg)}
      >
        Assemble
      </button>

      {pkg.missing.length > 0 && (
        <div className="alert" role="alert">
          <p>
            These Changed Files have no Revision. Correct them in SVN, then
            assemble again:
          </p>
          <ul>
            {pkg.missing.map((m) => (
              <li key={m.path}>
                <code>{m.path}</code>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Diffs pkg={pkg} />
      <Builds pkg={pkg} />
      <Checklist pkg={pkg} />
    </section>
  );
}

function EvidenceBadge({ evidence }: { evidence: Evidence }) {
  return (
    <span className={`evidence evidence-${evidence ?? "none"}`}>
      {evidenceLabel(evidence)}
    </span>
  );
}

function FileLine({ file }: { file: ChangedFile }) {
  const link = safeLink(file.repository_link);
  return (
    <li>
      <code>{file.path}</code>{" "}
      {file.revision === null ? (
        <span className="missing">no Revision</span>
      ) : (
        <>Revision {file.revision}</>
      )}{" "}
      {link === null ? (
        <span>{file.repository_link}</span>
      ) : (
        <a href={link} target="_blank" rel="noreferrer noopener">
          repository link
        </a>
      )}
    </li>
  );
}

function Diffs({ pkg }: { pkg: ReviewPackage }) {
  const groups = groupDiffs(pkg.diffs);
  if (groups.length === 0) {
    return null;
  }
  return (
    <section>
      <h2>Diffs</h2>
      {groups.map((group) => (
        <section key={group.platform}>
          <h3>{group.platform}</h3>
          {group.diffs.map((d) => (
            <div className="diff" key={d.category}>
              <h4>{d.category}</h4>
              <ul>
                {d.changed_files.map((f) => (
                  <FileLine key={f.path} file={f} />
                ))}
              </ul>
              <details>
                <summary>
                  Diff ({group.platform}, {d.category})
                </summary>
                <pre>{d.diff}</pre>
              </details>
            </div>
          ))}
        </section>
      ))}
    </section>
  );
}

function Builds({ pkg }: { pkg: ReviewPackage }) {
  if (noMatchingBuild(pkg)) {
    return (
      <section>
        <h2>Jenkins Builds</h2>
        <p className="alert">No matching Jenkins Build for this SVN Branch.</p>
      </section>
    );
  }
  if (pkg.jenkins_builds.length === 0) {
    return null;
  }
  return (
    <section>
      <h2>Jenkins Builds</h2>
      <table>
        <thead>
          <tr>
            <th>Build</th>
            <th>Name</th>
            <th>Result</th>
            <th>Built at</th>
            <th>Preselected</th>
          </tr>
        </thead>
        <tbody>
          {pkg.jenkins_builds.map((b) => {
            const preselected = b.build_number === pkg.preselected_build;
            return (
              <tr
                key={b.build_number}
                className={preselected ? "preselected" : undefined}
              >
                <td>{b.build_number}</td>
                <td>{b.name}</td>
                <td>{b.result}</td>
                <td>{formatBuildTime(b.built_at)}</td>
                <td>{preselected ? "Preselected" : ""}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}

function Checklist({ pkg }: { pkg: ReviewPackage }) {
  const tabs = pkg.review_checklist?.tabs ?? [];
  const [chosen, setChosen] = useState(0);
  if (tabs.length === 0) {
    return null;
  }
  const current = Math.min(chosen, tabs.length - 1);
  const tab = tabs[current];
  return (
    <section>
      <h2>Review Checklist</h2>
      <div role="tablist" aria-label="Review Checklist Platforms">
        {tabs.map((t, i) => (
          <button
            key={t.platform}
            type="button"
            role="tab"
            id={`checklist-tab-${t.platform}`}
            aria-selected={i === current}
            aria-controls="checklist-panel"
            className={i === current ? "tab tab-selected" : "tab"}
            onClick={() => setChosen(i)}
          >
            {t.platform}
          </button>
        ))}
      </div>
      <div
        role="tabpanel"
        id="checklist-panel"
        aria-labelledby={`checklist-tab-${tab.platform}`}
      >
        <ul>
          {tab.changed_files.map((path) => (
            <li key={path}>
              <code>{path}</code>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default ReviewPackagePage;
