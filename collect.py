#!/usr/bin/env python3
"""
Collect candidate posts from r/math. ← UNIT 5, MILESTONE 4

Reddit now blocks anonymous access to its own JSON, so this reads r/math from
Arctic Shift (arctic-shift.photon-reddit.com), a public research archive of
Reddit. Same posts, same community — no account, no key. It writes a CSV in the
same `text,label,note` shape as `labels_template.csv` with the `label` column
left empty. Labelling is yours.

    python collect.py --help
    python collect.py                          # ~500 candidates from the last 6 months
    python collect.py --target 800 --months 12

The sample is spread across evenly spaced points in the window, with a cap per
thread, so one busy week or one big thread can't dominate. Collect more than
you need: junk gets dropped, and quips are rare here.

What gets skipped: [deleted]/[removed] and mod-removed posts, link and image
posts, AutoModerator and accounts ending in "bot", stickied and moderator
comments, exact duplicates, and anything shorter than --min-chars. Whitespace
is collapsed to single spaces so the file opens cleanly in a spreadsheet;
nothing else about the text is changed.

Run it again with the same --out and it appends, skipping posts it already has.
"""

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


SUBREDDIT = "math"
API = "https://arctic-shift.photon-reddit.com/api"
USER_AGENT = "ai201-takemeter-collector/1.0 (course project; low volume)"

# How many comments and text posts to pull at each point in the window. The
# archive caps a request at 100.
COMMENTS_PER_POINT = 100
POSTS_PER_POINT = 25

SKIP_BODIES = {"[deleted]", "[removed]", ""}


def fetch(kind, before, limit, delay):
    query = urllib.parse.urlencode(
        {"subreddit": SUBREDDIT, "limit": limit, "before": before, "sort": "desc"})
    url = f"{API}/{kind}/search?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    # The archive times out now and then under load and answers fine a moment
    # later, so a few retries with a growing wait before giving up.
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.load(response)
            break
        except urllib.error.HTTPError as e:
            error = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            error = f"couldn't reach the archive ({e.reason})"
        print(f"    {error}, retrying in {5 * (attempt + 1)}s")
        time.sleep(5 * (attempt + 1))
    else:
        sys.exit(f"Gave up on {url}: {error}. Run again later — it appends.")
    time.sleep(delay)
    if data.get("error"):
        sys.exit(f"Archive error: {data['error']}")
    return data["data"] or []


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def keep(item, text, min_chars):
    author = item.get("author")
    if text in SKIP_BODIES or author in (None, "[deleted]", "AutoModerator"):
        return False
    if author.lower().endswith("bot"):
        return False
    if item.get("distinguished") == "moderator" or item.get("stickied"):
        return False
    return len(text) >= min_chars


def from_post(post, min_chars):
    body = clean(post.get("selftext"))
    if not post.get("is_self") or post.get("removed_by_category") or not keep(post, body, min_chars):
        return None
    return clean(f"{post['title']} {body}"), post["id"], f"r/math post · {post['permalink']}"


def from_comment(comment, min_chars):
    body = clean(comment.get("body"))
    if not keep(comment, body, min_chars):
        return None
    kind = "comment" if comment.get("parent_id", "").startswith("t3_") else "reply"
    thread = comment.get("link_id", "").removeprefix("t3_")
    return body, thread, f"r/math {kind} · {comment['permalink']}"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", type=int, default=500,
                        help="how many new candidates to collect (default: 500)")
    parser.add_argument("--months", type=int, default=6,
                        help="how far back to spread the sample (default: 6)")
    parser.add_argument("--per-thread", type=int, default=12,
                        help="max posts kept from any one thread (default: 12)")
    parser.add_argument("--min-chars", type=int, default=15,
                        help="drop anything shorter (default: 15)")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="seconds between requests (default: 1)")
    parser.add_argument("--out", default="candidates.csv",
                        help="output file (default: candidates.csv)")
    args = parser.parse_args()

    out = Path(args.out)
    seen = set()
    new_file = not out.exists() or out.stat().st_size == 0
    if not new_file:
        with out.open(encoding="utf-8", newline="") as f:
            seen = {row["text"] for row in csv.DictReader(f)}
        print(f"{out} exists with {len(seen)} rows — appending, skipping duplicates")

    # Evenly spaced points from now back to --months ago. Each point takes an
    # equal share of the target, so the sample covers the whole window.
    now = int(time.time())
    span = args.months * 30 * 86400
    points = max(1, args.target // 50)
    share = -(-args.target // points)
    per_thread = {}
    added = 0

    with out.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["text", "label", "note"])

        for i in range(points):
            before = now - span * i // points
            items = ([from_post(p, args.min_chars) for p in fetch("posts", before, POSTS_PER_POINT, args.delay)]
                     + [from_comment(c, args.min_chars) for c in fetch("comments", before, COMMENTS_PER_POINT, args.delay)])
            kept = 0
            for item in filter(None, items):
                text, thread, note = item
                if kept >= share or added >= args.target:
                    break
                if text in seen or per_thread.get(thread, 0) >= args.per_thread:
                    continue
                writer.writerow([text, "", note])
                seen.add(text)
                per_thread[thread] = per_thread.get(thread, 0) + 1
                kept += 1
                added += 1
            day = time.strftime("%Y-%m-%d", time.gmtime(before))
            print(f"  [{i + 1}/{points}] before {day}: +{kept}")

    print(f"\nAdded {added} from {len(per_thread)} threads. {out} now has {len(seen)} candidates.")
    print("Label them, keep the ones you want, and save the result as labels.csv.")


if __name__ == "__main__":
    main()
