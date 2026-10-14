# File Integrity Monitor

A Python-based cybersecurity project that uses SHA-256 hashing to detect changes in files.

## Overview

The File Integrity Monitor scans a directory and calculates a SHA-256 hash for each file. It compares the current hashes against a previously saved baseline to identify added, modified, and removed files.

This project was developed as a hands-on learning exercise in Python programming, file integrity monitoring, and cybersecurity fundamentals.

## Features

- Calculate SHA-256 hashes for files.
- Scan directories recursively, including subdirectories.
- Detect newly added files.
- Detect modified files.
- Detect removed files.
- Save file hashes in a JSON baseline.
- Process files in chunks to avoid loading entire files into memory.

## Requirements

- Python 3.10 or later.
- No third-party packages required.

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Add test files to the `monitored_files/` directory.
4. Run the program:

```bash
python file_hash.py
```

On the first run, the program creates `baseline.json` containing the hashes of the monitored files.

On subsequent runs, the program compares the current file hashes with the saved baseline and reports any detected changes.

## Example Output

**First run:**

```text
Baseline created.
Recorded 1 file(s).
```

**No changes detected:**

```text
OK: No changes detected.
```

**Modified file:**

```text
MODIFIED: sample.txt
```

**Added file:**

```text
ADDED: new_file.txt
```

**Removed file:**

```text
REMOVED: sample.txt
```

## Technologies

- Python
- SHA-256
- JSON
- Git
- GitHub

## Limitations

The baseline is stored locally and is not protected against unauthorized modification. An attacker who can modify both the monitored files and the baseline may evade detection.

This project is intended for educational purposes and is not a replacement for a production-grade file integrity monitoring solution.

## Author

**Thiffanny Castro**

[GitHub Profile](https://github.com/thiffannycastro)
