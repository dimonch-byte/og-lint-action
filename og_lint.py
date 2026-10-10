#!/usr/bin/env python3
"""og-lint: check Open Graph / Twitter card tags in HTML files or a live URL. Markup only; stdlib only."""
import sys, re, glob, argparse, urllib.request
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.meta={}; s.title=False
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=="meta":
            k=(a.get("property") or a.get("name") or "").lower()
            if k: s.meta.setdefault(k,a.get("content") or "")
        if t=="title": s.title=True
def lint(html, where):
    p=P(); p.feed(html); m=p.meta; issues=[]
    for k in ("og:title","og:image","og:url"):
        if not m.get(k): issues.append(f"missing {k}")
    img=m.get("og:image","")
    if img and not re.match(r"https?://",img): issues.append(f"og:image is relative ({img}); crawlers need an absolute https URL")
    if img.startswith("http://"): issues.append("og:image uses http://; some crawlers refuse mixed content")
    if not m.get("twitter:card"): issues.append("missing twitter:card (X falls back to a small card or none)")
    if img and not (m.get("og:image:width") and m.get("og:image:height")): issues.append("no og:image:width/height (first share on LinkedIn/Facebook may render without image)")
    return [f"{where}: {i}" for i in issues]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("targets",nargs="+",help="HTML globs or https URLs"); ap.add_argument("--warn-only",action="store_true")
    a=ap.parse_args(); out=[]
    for t in a.targets:
        if t.startswith("http"):
            req=urllib.request.Request(t,headers={"User-Agent":"og-lint/1.0 (+https://github.com/dimonch-byte/og-lint-action)"})
            out+=lint(urllib.request.urlopen(req,timeout=20).read(2_000_000).decode("utf-8","replace"),t)
        else:
            for f in glob.glob(t,recursive=True): out+=lint(open(f,encoding="utf-8",errors="replace").read(),f)
    for o in out: print("::warning::"+o if a.warn_only else "::error::"+o)
    if out:
        print(f"\n{len(out)} share-card issue(s). This checks markup only; crawlers can still be blocked by your host/WAF.")
        print("To see what each real crawler gets back from your live page (free check, paid fix pack optional): https://sharepack.adjudi.com/?utm_source=github&utm_medium=action&utm_campaign=sharepack-intent-w2&utm_content=og-lint-action")
    else: print("og-lint: no markup issues found.")
    sys.exit(1 if out and not a.warn_only else 0)
if __name__=="__main__": main()
