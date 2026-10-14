
import argparse
import hashlib
import json
import sys
from pathlib import Path

MONITORED_DIR = Path("monitored_files")
BASELINE_FILE = Path("baseline.json")
CHUNK_SIZE = 4096


def calculate_hash(file_path):
    """Calculate a file's SHA-256 hash using chunked reads."""
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_files():
    """Return file hashes and any scanning errors."""
    hashes = {}
    errors = []

    try:
        paths = sorted(MONITORED_DIR.rglob("*"))
        for file_path in paths:
            try:
                if file_path.is_file():
                    relative_path = file_path.relative_to(MONITORED_DIR).as_posix()
                    hashes[relative_path] = calculate_hash(file_path)
            except OSError as error:
                errors.append(f"{file_path}: {error}")
    except OSError as error:
        errors.append(f"Could not scan directory: {error}")

    return hashes, errors


def save_baseline(hashes):
    """Save a baseline in JSON format."""
    try:
        BASELINE_FILE.write_text(
            json.dumps(hashes, indent=4) + "\n",
            encoding="utf-8",
        )
    except OSError as error:
        print(f"Error: Could not save baseline: {error}")
        return False

    return True


def load_baseline():
    """Load and validate the saved baseline."""
    try:
        data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error: Could not read baseline: {error}")
        return None

    if not isinstance(data, dict):
        print("Error: Baseline must contain a JSON object.")
        return None

    for name, file_hash in data.items():
        if (
            not isinstance(name, str)
            or not isinstance(file_hash, str)
            or len(file_hash) != 64
            or any(char not in "0123456789abcdef" for char in file_hash)
        ):
            print("Error: Baseline contains an invalid file path or SHA-256 hash.")
            return None

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Detect file changes using SHA-256 hashes."
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Replace the saved baseline with the current file hashes.",
    )
    args = parser.parse_args()

    if not MONITORED_DIR.is_dir():
        print("Error: Monitored directory not found.")
        return 1

    current_hashes, errors = scan_files()

    if errors:
        print("Error: Some files could not be scanned:")
        for error in errors:
            print(f"  - {error}")
        print("Scan incomplete. Baseline was not changed.")
        return 1

    if args.update_baseline:
        if save_baseline(current_hashes):
            print("Baseline updated.")
            print(f"Recorded {len(current_hashes)} file(s).")
            return 0
        return 1

    if not BASELINE_FILE.exists():
        if save_baseline(current_hashes):
            print("Baseline created.")
            print(f"Recorded {len(current_hashes)} file(s).")
            return 0
        return 1

    original_hashes = load_baseline()
    if original_hashes is None:
        print("No comparison performed. Fix the baseline before continuing.")
        return 1

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
        return 0

    for name in sorted(added):
        print(f"ADDED: {name}")

    for name in sorted(modified):
        print(f"MODIFIED: {name}")

    for name in sorted(removed):
        print(f"REMOVED: {name}")

    print("\nReview the reported changes before updating the baseline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
