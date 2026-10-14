
import hashlib
import json
from pathlib import Path

MONITORED_DIR = Path("monitored_files")
BASELINE_FILE = Path("baseline.json")


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_files():
    hashes = {}

    for file_path in MONITORED_DIR.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(MONITORED_DIR))
            hashes[relative_path] = calculate_hash(file_path)

    return hashes


def main():
    if not MONITORED_DIR.exists():
        print("Error: Monitored directory not found.")
        return

    current_hashes = scan_files()

    if not BASELINE_FILE.exists():
        BASELINE_FILE.write_text(
            json.dumps(current_hashes, indent=4),
            encoding="utf-8"
        )
        print("Baseline created.")
        print(f"Recorded {len(current_hashes)} file(s).")
        return

    original_hashes = json.loads(
        BASELINE_FILE.read_text(encoding="utf-8")
    )

    original_files = set(original_hashes)
    current_files = set(current_hashes)

    added = current_files - original_files
    removed = original_files - current_files
    common = current_files & original_files

    modified = [
        name for name in common
        if current_hashes[name] != original_hashes[name]
    ]

    if not added and not removed and not modified:
        print("OK: No changes detected.")
        return

    for name in sorted(added):
        print(f"ADDED: {name}")

    for name in sorted(modified):
        print(f"MODIFIED: {name}")

    for name in sorted(removed):
        print(f"REMOVED: {name}")


if __name__ == "__main__":
    main()
