"""Build Arabic IPTV playlists (general + kids) from the iptv-org database.

Usage: python build.py [--min 480] [--hd 720] [--no-check]
Output: playlists/arabic_{general,kids}.m3u and ..._720p.m3u (HD only)
"""
import argparse, json, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "playlists"
API = "https://iptv-org.github.io/api/"

ARAB_COUNTRIES = {"SA","AE","EG","QA","KW","BH","OM","JO","LB","SY","IQ","PS","YE","LY","TN","DZ","MA","SD","MR","SO","DJ","KM"}
KIDS_CATS = {"kids", "animation"}
SKIP_CATS = {"xxx"}


def load(name):
    p = DATA / f"{name}.json"
    if not p.exists():
        DATA.mkdir(exist_ok=True)
        urllib.request.urlretrieve(API + f"{name}.json", p)
    return json.loads(p.read_text(encoding="utf-8"))


def height(q):
    m = re.match(r"(\d+)", q or "")
    return int(m.group(1)) if m else 0


def check(url, ua=None, ref=None):
    """Return (alive, best_height) by fetching the m3u8 and reading variant RESOLUTIONs."""
    h = {"User-Agent": ua or "Mozilla/5.0"}
    if ref:
        h["Referer"] = ref
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=8) as r:
            body = r.read(200_000).decode("utf-8", "ignore")
        if "#EXTM3U" not in body:
            return False, 0
        res = [int(m) for m in re.findall(r"RESOLUTION=\d+x(\d+)", body)]
        return True, max(res) if res else 0
    except Exception:
        return False, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=480, help="min height for the standard lists; 0 keeps everything")
    ap.add_argument("--hd", type=int, default=720, help="min height for the *_720p lists; 0 skips them")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()

    channels = {c["id"]: c for c in load("channels")}
    feeds = {(f["channel"], f["id"]): f for f in load("feeds")}
    streams = load("streams")

    floor = min(x for x in (a.min, a.hd) if x) if (a.min or a.hd) else 0
    items = []
    for s in streams:
        cid = s.get("channel")
        c = channels.get(cid)
        if not c or c.get("is_nsfw") or c.get("closed"):
            continue
        if set(c["categories"]) & SKIP_CATS:
            continue
        f = feeds.get((cid, s.get("feed")))
        langs = set(f["languages"]) if f else set()
        if "ara" not in langs and c["country"] not in ARAB_COUNTRIES:
            continue
        if f and langs and "ara" not in langs:
            continue
        q = height(s.get("quality"))
        if floor and q and q < floor:
            continue
        kids = bool(set(c["categories"]) & KIDS_CATS)
        items.append(dict(id=cid, name=c["name"], country=c["country"], cats=c["categories"],
                          logo=None, url=s["url"], q=q, kids=kids,
                          ua=s.get("user_agent"), ref=s.get("referrer")))

    print(f"{len(items)} candidates")
    if not a.no_check:
        with ThreadPoolExecutor(40) as ex:
            res = list(ex.map(lambda i: check(i["url"], i["ua"], i["ref"]), items))
        alive = []
        for i, (ok, h) in zip(items, res):
            if not ok:
                continue
            if h:
                i["q"] = h
            if floor and i["q"] and i["q"] < floor:
                continue
            alive.append(i)
        print(f"{len(alive)} alive")
        items = alive

    OUT.mkdir(exist_ok=True)
    logos = {l["channel"]: l["url"] for l in load("logos")}
    variants = [(a.min, "")] + ([(a.hd, f"_{a.hd}p")] if a.hd else [])
    for level, suffix in variants:
        # unknown quality (0) only allowed in the standard lists; HD lists need proof
        pool = [i for i in items if i["q"] >= level or (i["q"] == 0 and level <= 480)]
        # best stream per channel, highest quality first
        best = {}
        for i in pool:
            k = (i["id"], i["kids"])
            if k not in best or i["q"] > best[k]["q"]:
                best[k] = i
        final = sorted(best.values(), key=lambda i: (-i["q"], i["name"].lower()))
        for base, kids in (("arabic_kids", True), ("arabic_general", False)):
            fname = f"{base}{suffix}.m3u"
            lines = ["#EXTM3U"]
            sel = [i for i in final if i["kids"] == kids]
            for i in sel:
                grp = "Kids" if kids else (i["cats"][0].title() if i["cats"] else "General")
                lines.append(f'#EXTINF:-1 tvg-id="{i["id"]}" tvg-logo="{logos.get(i["id"], "")}" '
                             f'group-title="{grp}",{i["name"]} [{i["q"] or "?"}p]')
                if i["ua"]:
                    lines.append(f'#EXTVLCOPT:http-user-agent={i["ua"]}')
                if i["ref"]:
                    lines.append(f'#EXTVLCOPT:http-referrer={i["ref"]}')
                lines.append(i["url"])
            (OUT / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(fname, len(sel), "channels")


if __name__ == "__main__":
    main()
