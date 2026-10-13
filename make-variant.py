#!/usr/bin/env python3
"""
LPのバリエーション（ファーストビューのコピー違い）を作るスクリプト。

utage-embed.html を元に、1枚目のキャッチコピーだけを差し替えた別バージョンを
書き出します。本体を直接編集しないので、元のLPはそのまま残ります。

  python3 make-variant.py          … すべてのバリエーションを書き出す
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "utage-embed.html")

# ------------------------------------------------------------------
# バリエーションの定義（ここの文字を書き換えれば新しい版が作れます）
#   lead  … 小さいリード文
#   main  … 大きいキャッチ（<br> で改行）
#   size  … 大きいキャッチの文字サイズ（vw, 最大px）
#   top   … 文字ブロックを置く位置（画像の高さに対する％）
# ------------------------------------------------------------------
VARIANTS = {
    "eye": {
        "file": "utage-embed-eye.html",
        "lead": "夕方になると、目の奥が重い。",
        "main": "その頭痛、<br>眼精疲労から？",
        "size": ("7.8vw", "47px"),
        "top": "18.4%",
        "og": "A＋salon｜その頭痛、眼精疲労から？",
        "alt": "A＋salon／その頭痛、眼精疲労から？ 40代女性のための上質なヘッドマッサージ（完全予約制・女性専用／宗像市）",
    },
}


def swap(s, v):
    """1枚目のキャッチコピーまわりだけを差し替える"""
    old_lead = '<span class="aps-lp__hero-lead">頭が重い、眠りが浅い。そんな毎日に。</span>'
    old_main = '<span class="aps-lp__hero-main">ふわっと、<br>頭が空っぽになる時間。</span>'
    assert old_lead in s and old_main in s, "キャッチコピーが見つかりません"
    s = s.replace(old_lead, f'<span class="aps-lp__hero-lead">{v["lead"]}</span>', 1)
    s = s.replace(old_main, f'<span class="aps-lp__hero-main">{v["main"]}</span>', 1)

    vw, px = v["size"]
    s = s.replace("font-size:min(7.0vw,42px);", f"font-size:min({vw},{px});", 1)
    if v.get("top"):
        s = s.replace("    top:19.0%;", f"    top:{v['top']};", 1)

    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               f'<meta property="og:title" content="{v["og"]}">', s, count=1)
    s = re.sub(r'(<div class="aps-lp__hero">\s*\n\s*<img src="[^"]*" alt=")[^"]*(")',
               lambda m: m.group(1) + v["alt"] + m.group(2), s, count=1)
    return s


def build(name, v):
    out = os.path.join(ROOT, v["file"])
    open(out, "w", encoding="utf-8").write(swap(open(SRC, encoding="utf-8").read(), v))

    # 画像を埋め込んだ版（UTAGEに貼るのはこちら）。本体の埋め込み済みファイルを使うので
    # 画像の圧縮具合は元のLPとまったく同じになります。
    emb_src = os.path.join(ROOT, "utage-embed-with-images.html")
    emb_out = out.replace(".html", "-with-images.html")
    open(emb_out, "w", encoding="utf-8").write(swap(open(emb_src, encoding="utf-8").read(), v))

    for f in (out, emb_out):
        print(name, "->", os.path.basename(f), f"({os.path.getsize(f)//1024}KB)")


if __name__ == "__main__":
    for name, v in VARIANTS.items():
        build(name, v)
