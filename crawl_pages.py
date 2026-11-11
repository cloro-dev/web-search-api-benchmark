# /// script
# requires-python = ">=3.10"
# dependencies = ["trafilatura==2.0.0"]
# ///
"""Fetch the organic result pages of saved cloro responses and save them as markdown.

Usage: uv run crawl_pages.py <run folder> <results file with the question ids> [--workers 16]

For each question id in the results file, reads <run folder>/raw/cloro/<id>.json
and fetches the page-1 organic links. A page is fetched only if the robots.txt of
its host allows our user agent. The main text is extracted as markdown with
trafilatura and saved to <run folder>/pages/<sha1 of the url>.json with the
fields url, status (ok, robots_disallowed, fetch_error, no_text), and markdown.
A re-run skips the pages that are saved. This file needs trafilatura, so it is
separate from benchmark.py, which uses the standard library only.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import sys
import threading
import urllib.parse
import urllib.request
import urllib.robotparser

import trafilatura

USER_AGENT = "benchmark-crawler/1.0"
TIMEOUT_S = 20
MAX_BYTES = 5_000_000
_robots, _lock = {}, threading.Lock()


def page_path(out, url):
    return os.path.join(out, "pages", hashlib.sha1(url.encode()).hexdigest() + ".json")


def allowed(url):
    p = urllib.parse.urlparse(url)
    root = f"{p.scheme}://{p.netloc}"
    with _lock:
        rp = _robots.get(root)
    if rp is None:
        rp = urllib.robotparser.RobotFileParser()
        try:
            req = urllib.request.Request(root + "/robots.txt", headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                rp.parse(r.read(MAX_BYTES).decode("utf-8", "ignore").splitlines())
        except urllib.error.HTTPError as e:
            # Same rule as the robots.txt standard: 4xx means no rules, 5xx means do not crawl.
            rp.parse([] if e.code < 500 else ["User-agent: *", "Disallow: /"])
        except Exception:
            rp.parse([])
        with _lock:
            _robots[root] = rp
    return rp.can_fetch(USER_AGENT, url)


def crawl(url):
    if not allowed(url):
        return {"url": url, "status": "robots_disallowed", "markdown": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.5"})
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            html = r.read(MAX_BYTES).decode(r.headers.get_content_charset() or "utf-8", "ignore")
    except Exception as e:
        return {"url": url, "status": "fetch_error", "error": repr(e)[:200], "markdown": None}
    md = trafilatura.extract(html, output_format="markdown", include_links=False, include_comments=False)
    return {"url": url, "status": "ok" if md else "no_text", "markdown": md}


def main():
    run, ids_file = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 16
    os.makedirs(os.path.join(run, "pages"), exist_ok=True)
    ids = {json.loads(line)["id"] for line in open(ids_file)}
    urls = []
    for i in sorted(ids):
        d = json.load(open(os.path.join(run, "raw", "cloro", f"{i}.json")))
        urls += [o["link"] for o in (d.get("result") or {}).get("organicResults") or [] if o.get("page", 1) == 1 and o.get("link")]
    todo = sorted({u for u in urls if not os.path.exists(page_path(run, u))})
    print(f"{len(ids)} questions, {len(urls)} links, {len(todo)} to fetch", file=sys.stderr)
    with cf.ThreadPoolExecutor(workers) as ex:
        for k, rec in enumerate(ex.map(crawl, todo), 1):
            json.dump(rec, open(page_path(run, rec["url"]), "w"), ensure_ascii=False)
            if k % 100 == 0:
                print(f"{k}/{len(todo)}", file=sys.stderr)


if __name__ == "__main__":
    main()
