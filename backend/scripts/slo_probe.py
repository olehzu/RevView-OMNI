"""Probe for the AVL-review-package-read SLO (specification section 9.5).

Loads one review package at a fixed interval, from outside the Application, and
counts good events: an HTTP 200 whose body is the section 8.2.3 envelope holding
the expected review package. Anything else is a bad event, including a refused
connection, a timeout, an error status, or another body, so the probe can fail.

Prints one line per probe, then a summary: good events, all events, and the ratio.
Standard library only.

    python scripts/slo_probe.py --interval 60            # until Ctrl+C
    python scripts/slo_probe.py --interval 5 --count 60  # 60 probes, 5 s apart
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime


def probe(url: str, review_id: str, timeout: float) -> tuple[bool, str]:
    """One probe: whether loading the review package succeeded, and why not."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            status = response.status
            body = json.loads(response.read())
    except urllib.error.HTTPError as error:
        return False, f"HTTP {error.code}"
    except (urllib.error.URLError, OSError) as error:
        return False, f"unreachable ({type(error).__name__})"
    except json.JSONDecodeError:
        return False, "body is not JSON"
    if status != 200:
        return False, f"HTTP {status}"
    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict) or data.get("review_id") != review_id:
        return False, "body is not the review package"
    return True, "ok"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--review-id", default="rev-0001")
    parser.add_argument("--interval", type=float, default=60.0, help="seconds")
    parser.add_argument("--count", type=int, default=0, help="0 runs until Ctrl+C")
    parser.add_argument("--timeout", type=float, default=5.0, help="seconds")
    args = parser.parse_args()

    url = f"{args.base_url}/api/v1/review-packages/{args.review_id}"
    good = total = 0
    started = datetime.now(UTC)
    try:
        while args.count == 0 or total < args.count:
            ok, detail = probe(url, args.review_id, args.timeout)
            total += 1
            good += ok
            stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"{stamp} {'good' if ok else 'BAD '} {detail}", flush=True)
            if args.count == 0 or total < args.count:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    ended = datetime.now(UTC)
    ratio = f"{good / total:.2%}" if total else "n/a"
    print(
        f"SLI {good}/{total} = {ratio} good loads of {args.review_id}, "
        f"{started:%Y-%m-%d %H:%M}Z to {ended:%H:%M}Z UTC"
    )


if __name__ == "__main__":
    main()
