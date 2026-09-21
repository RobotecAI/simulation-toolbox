#!/usr/bin/env python3
"""Generate the QR code that goes on the slides and on the page itself.

Usage:
    python3 tools/make_qr.py https://<user>.github.io/<repo>/

Writes static/img/qr.png (page, shown automatically in the Q&A box) and
static/img/qr.svg + qr-slides.png at 2048 px (drop into the slides).
Requires: pip install "qrcode[pil]"
"""
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.image.svg import SvgPathImage
except ImportError:
    sys.exit('Missing dependency. Run: pip install "qrcode[pil]"')

if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit(__doc__)

url = sys.argv[1]
out = Path(__file__).resolve().parent.parent / "static" / "img"
out.mkdir(parents=True, exist_ok=True)

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
qr.add_data(url)
qr.make(fit=True)

qr.make_image(fill_color="#1b2330", back_color="white").resize((640, 640)).save(out / "qr.png")
qr.make_image(fill_color="black", back_color="white").resize((2048, 2048)).save(out / "qr-slides.png")
qr.make_image(image_factory=SvgPathImage).save(out / "qr.svg")

print(f"QR for {url}")
for f in ("qr.png", "qr-slides.png", "qr.svg"):
    print("  wrote", out / f)
print("Rebuild the site; the page picks up static/img/qr.png automatically.")
