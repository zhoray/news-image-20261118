"""picture.jpg stored next to this script holds JPEG bytes that must be delivered byte for byte under the required output name entry.png; the write is a plain write_bytes because the grading output directory rejects renames."""
import sys
import os
from pathlib import Path

JPEG_MAGIC = b'\xff\xd8'  # it is the first two bytes of every JPEG file

def read_picture():
    script_dir = Path(__file__).resolve().parent
    pic_path = script_dir / "picture.jpg"
    try:
        data = pic_path.read_bytes()
    except Exception as exc:
        raise ValueError(f"Failed to read picture.jpg from {pic_path}") from exc
    if len(data) == 0:
        raise ValueError("picture.jpg is empty")
    if not data.startswith(JPEG_MAGIC):
        raise ValueError("picture.jpg does not start with JPEG_MAGIC")
    return data
def write_entry(data):
    out_dir = os.getenv("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        raise ValueError(f"Failed to create output directory {out_dir}") from exc
    out_path = Path(out_dir) / "entry.png"
    try:
        out_path.write_bytes(data)
    except Exception as exc:
        raise ValueError(f"Failed to write {out_path}") from exc
    if out_path.stat().st_size != len(data):
        raise ValueError(f"Written file {out_path} size mismatch")
    return out_path

def main():
    try:
        data = read_picture()
        out_path = write_entry(data)
        print(f"entry.png {len(data)}")
        return 0
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
