#!/usr/bin/env python3
"""
画像を埋め込まず、URLで読み込む版のUTAGEコードを作るスクリプト。

埋め込み版（data URI）はコードが1MB近くになりUTAGEで保存できないため、
画像は assets/lp/*.webp をCDN（jsDelivr）から読み込む形にする。

  python3 build-cdn.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "utage-embed.html")

# 画像を置いているコミット。assets/lp/ の画像を更新したら、
# push後のコミットハッシュに書き換えてください。
COMMIT = "81e4e7c75356ec982f7130e8cdc6355efdb54669"
BASE = f"https://cdn.jsdelivr.net/gh/3844akemi3844-ship-it/note-kit@{COMMIT}/assets/lp/"

# IMAGE_n_URL のプレースホルダ
PLACEHOLDERS = {"1": "lp-01", "2": "lp-02", "4": "lp-04", "5": "lp-05", "8": "lp-08"}

# 本文に直接埋め込まれている画像（HTMLに出てくる順番）
INLINE = ["feel-01", "feel-02", "feel-03",
          "before-after-01", "before-after-02",
          "therapist-photo", "salon-01"]


def to_cdn(s):
    for n, name in PLACEHOLDERS.items():
        s = s.replace(f"IMAGE_{n}_URL", BASE + name + ".webp")
    assert "IMAGE_" not in s, "差し替えできていないプレースホルダがあります"

    uris = re.findall(r'data:image/(?:jpeg|webp);base64,[A-Za-z0-9+/=]+', s)
    assert len(uris) == len(INLINE), f"埋め込み画像の数が合いません（{len(uris)} 件）"
    for uri, name in zip(uris, INLINE):
        s = s.replace(uri, BASE + name + ".webp", 1)
    assert "data:image" not in s, "埋め込み画像が残っています"
    return s


if __name__ == "__main__":
    src = open(SRC, encoding="utf-8").read()
    out = to_cdn(src)
    p = os.path.join(ROOT, "utage-embed-cdn.html")
    open(p, "w", encoding="utf-8").write(out)
    print(os.path.basename(p), f"{len(out)//1024}KB")

    # コピー違い（目の疲れ版）も同じ方式で作る
    sys.path.insert(0, ROOT)
    from importlib import import_module
    mv = import_module("make-variant".replace("-", "_")) if False else None
    import runpy
    g = runpy.run_path(os.path.join(ROOT, "make-variant.py"), run_name="not_main")
    for name, v in g["VARIANTS"].items():
        o = g["swap"](out, v)
        q = os.path.join(ROOT, v["file"].replace(".html", "-cdn.html"))
        open(q, "w", encoding="utf-8").write(o)
        print(os.path.basename(q), f"{len(o)//1024}KB")
