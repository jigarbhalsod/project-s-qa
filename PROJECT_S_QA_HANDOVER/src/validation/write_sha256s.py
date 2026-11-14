"""Write a size/SHA-256 manifest for a completed handover folder."""
import hashlib
from pathlib import Path

def write_manifest(root):
    root = Path(root).resolve()
    target = root / "SHA256SUMS.txt"
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p != target):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.stat().st_size}  {path.relative_to(root).as_posix()}")
    target.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument("root"); args = parser.parse_args()
    print(f"Manifest entries: {write_manifest(args.root)}")
