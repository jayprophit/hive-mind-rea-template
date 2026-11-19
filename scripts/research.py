#!/usr/bin/env python3
"""
research.py - search and read the web without an API key or paid billing.

Why this exists
---------------
The hosted search tool billed per query and stopped working when the balance
ran out. Scraping Google/DuckDuckGo/Bing from a script does not work either:
they serve bot challenges or ignore the query (verified 2026-11).

Marginalia (marginalia.nu) is a real independent index that answers plain HTTP
requests with no key and no challenge, so it is the primary engine here.
Wikipedia and Hacker News are used as secondary sources because both have
stable public JSON endpoints.

Commands
--------
  research.py "query"                 search the web
  research.py "query" -n 12           more results
  research.py --hn "query"            search Hacker News (technical discussion)
  research.py --wiki "query"          Wikipedia summary
  research.py --url URL               fetch a page and print readable text
  research.py --url URL --chars 8000  longer extract

Examples
--------
  python scripts/research.py "ideapad 3 15iil05 memory upgrade"
  python scripts/research.py --url https://psref.lenovo.com/...
  python scripts/research.py --hn "opencode mcp server"

Exit codes
----------
  0 results returned
  1 nothing found or network error

No third-party packages. Python 3.8+.
"""

import argparse
import gzip
import html
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)


def fetch(url, timeout=25, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", UA)
    req.add_header("Accept-Language", "en-GB,en;q=0.9")
    req.add_header("Accept-Encoding", "gzip")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        charset = r.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|li|h[1-6]|tr)>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


# ---------------------------------------------------------------- engines

def search_marginalia(query, limit):
    url = "https://search.marginalia.nu/search?query=" + urllib.parse.quote(query)
    page = fetch(url)
    hits = []
    seen = set()
    for m in re.finditer(
        r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', page, re.S
    ):
        href, label = m.group(1), strip_tags(m.group(2))
        if not label or len(label) < 8:
            continue
        host = urllib.parse.urlparse(href).netloc
        if "marginalia" in host or "patreon" in host:
            continue
        if href in seen or label.startswith("http"):
            continue
        seen.add(href)
        hits.append({"title": label[:120], "url": href, "source": "marginalia"})
        if len(hits) >= limit:
            break
    return hits


def search_hn(query, limit):
    url = (
        "https://hn.algolia.com/api/v1/search?query="
        + urllib.parse.quote(query)
        + f"&hitsPerPage={limit}"
    )
    data = json.loads(fetch(url, headers={"Accept": "application/json"}))
    out = []
    for h in data.get("hits", []):
        title = h.get("title") or h.get("story_title")
        link = h.get("url") or (
            "https://news.ycombinator.com/item?id=" + str(h.get("objectID"))
        )
        if not title:
            continue
        points = h.get("points")
        out.append({
            "title": title[:120],
            "url": link,
            "source": "hn",
            "meta": (f"{points} points" if points else "") + (
                f" by {h.get('author')}" if h.get("author") else ""
            ),
        })
    return out


def search_wiki(query, limit):
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json"
        "&srsearch=" + urllib.parse.quote(query) + f"&srlimit={limit}"
    )
    data = json.loads(fetch(url, headers={"Accept": "application/json"}))
    return [
        {
            "title": r["title"],
            "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(r["title"].replace(" ", "_")),
            "source": "wikipedia",
            "meta": f"{r.get('wordcount', 0)} words",
        }
        for r in data.get("query", {}).get("search", [])
    ]


def wiki_summary(query):
    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + urllib.parse.quote(query.replace(" ", "_"))
    )
    data = json.loads(fetch(url, headers={"Accept": "application/json"}))
    return data.get("extract", "") or "(no summary)"


# ---------------------------------------------------------------- fetch

def readable_text(url, limit):
    page = fetch(url)
    if "<html" not in page[:2000].lower():
        return page[:limit]
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    if m:
        title = strip_tags(m.group(1))[:120]
    body = re.sub(r"(?is)<(script|style|nav|footer|header|svg)[^>]*>.*?</\1>", " ", page)
    text = strip_tags(body)
    text = re.sub(r"[ \t]+", " ", text)
    return (f"# {title}\n\n" + text)[:limit]


# ---------------------------------------------------------------- output

def emit(query, hits):
    if not hits:
        print(f"No results for: {query}")
        print("Tip: Marginalia has a small index. Try shorter, more distinctive words,")
        print("     or fetch a known URL directly with --url.")
        return 1
    print(f"{len(hits)} result(s) for: {query}\n")
    for i, h in enumerate(hits, 1):
        print(f"{i:2}. [{h['source']}] {h['title']}")
        print(f"    {h['url']}")
        if h.get("meta"):
            print(f"    {h['meta']}")
        print()
    return 0


def main():
    p = argparse.ArgumentParser(
        description="Key-free web research: search, fetch, and read pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("query", nargs="*", help="words to search for")
    p.add_argument("-n", "--limit", type=int, default=8, help="max results (default 8)")
    p.add_argument("--url", help="fetch this URL and print readable text")
    p.add_argument("--chars", type=int, default=4000, help="max characters for --url")
    p.add_argument("--hn", action="store_true", help="search Hacker News instead")
    p.add_argument("--wiki", action="store_true", help="Wikipedia summary for the query")
    p.add_argument("--all", action="store_true", help="combine all engines")
    args = p.parse_args()

    q = " ".join(args.query).strip()

    try:
        if args.url:
            print(readable_text(args.url, args.chars))
            return 0

        if not q:
            p.print_help()
            return 1

        if args.wiki:
            print(wiki_summary(q))
            return 0

        if args.hn:
            return emit(q, search_hn(q, args.limit))

        if args.all:
            hits = []
            for fn in (search_marginalia, search_hn, search_wiki):
                try:
                    hits += fn(q, max(3, args.limit // 2))
                except Exception:
                    pass
            seen, uniq = set(), []
            for h in hits:
                if h["url"] not in seen:
                    seen.add(h["url"])
                    uniq.append(h)
            return emit(q, uniq[: args.limit])

        return emit(q, search_marginalia(q, args.limit))

    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} from the source. Try --hn or --url instead.", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main())
