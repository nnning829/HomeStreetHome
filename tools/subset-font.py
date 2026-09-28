"""重新擷取標題字型（jf open 粉圓）。

改過 index.html 的文字後執行一次，網站字型就會包含所有用到的字：
    pip install fonttools brotli
    python tools/subset-font.py

需要完整字型檔 jf-openhuninn-2.1.ttf（放在 tools/ 旁或以參數指定），
下載處：https://github.com/justfont/open-huninn-font/tree/master/font
"""
import sys
from pathlib import Path
from fontTools import subset

root = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "tools" / "jf-openhuninn-2.1.ttf"
html = (root / "index.html").read_text(encoding="utf-8")

# 頁面所有字元，外加常用標點與數字，避免小幅改字就缺字
extra = "０１２３４５６７８９，。、；：？！「」『』（）《》〈〉…—～・｜"
chars = set(html) | set(extra) | {chr(c) for c in range(0x20, 0x7F)}

opts = subset.Options()
opts.flavor = "woff2"
opts.layout_features = ["*"]
font = subset.load_font(str(src), opts)
sub = subset.Subsetter(opts)
sub.populate(text="".join(sorted(chars)))
sub.subset(font)
out = root / "assets" / "jf-openhuninn.woff2"
subset.save_font(font, str(out), opts)
print(f"已輸出 {out}（{out.stat().st_size // 1024} KB，{len(chars)} 字元）")
