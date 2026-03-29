"""
embed_photo.py
--------------
Run this once to bake your house photo into the HTML as base64.
Usage:  python embed_photo.py "C:\\path\\to\\your\\photo.jpg"
The script updates house_showcase.html so it becomes truly self-contained.
"""

import sys, base64, pathlib, re, shutil

def embed(image_path: str):
    img = pathlib.Path(image_path)
    if not img.exists():
        print(f"❌ File not found: {image_path}")
        sys.exit(1)

    # Copy to folder as house.jpg too (for convenience)
    dest = pathlib.Path(__file__).parent / "house.jpg"
    if img.resolve() != dest.resolve():
        shutil.copy(img, dest)
        print(f"✅ Copied photo → {dest}")

    # Determine MIME type
    suffix = img.suffix.lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(suffix.strip("."), "image/jpeg")

    # Encode
    b64 = base64.b64encode(img.read_bytes()).decode()
    data_uri = f"data:{mime};base64,{b64}"

    # Patch HTML
    html_path = pathlib.Path(__file__).parent / "house_showcase.html"
    html = html_path.read_text(encoding="utf-8")

    # Replace src value
    patched = re.sub(
        r'src="house\.jpg"',
        f'src="{data_uri}"',
        html
    )
    html_path.write_text(patched, encoding="utf-8")
    print("✅ Photo embedded into house_showcase.html successfully!")
    print("🌐 Open house_showcase.html in your browser — it is now fully self-contained.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python embed_photo.py \"C:\\path\\to\\your\\photo.jpg\"")
        sys.exit(1)
    embed(sys.argv[1])
