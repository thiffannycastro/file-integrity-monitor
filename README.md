

\# File Integrity Monitor



A Python project that uses SHA-256 hashes to detect changes in files.



\## Overview



The File Integrity Monitor scans a directory and calculates a SHA-256

hash for each file. It compares the current hashes with a previously

saved baseline to identify added, modified, and removed files.



This project was created as a hands-on learning exercise in Python

programming and cybersecurity fundamentals.



\## Features



\- Calculate SHA-256 hashes.

\- Scan files in a directory, including subdirectories.

\- Detect added files.

\- Detect modified files.

\- Detect removed files.

\- Save a baseline in JSON format.



\## Requirements



\- Python 3.10 or later

\- No third-party packages required



\## How to Run



1\. Clone or download this repository.

2\. Open a terminal in the project directory.

3\. Add test files to `monitored\_files/`.

4\. Run the program:



&#x20;  ```bash

&#x20;  python file\_hash.py

&#x20;  ```



On the first run, the program creates `baseline.json`.

On subsequent runs, it compares the current files with the saved baseline.



\## Example Output



```text

Baseline created.

Recorded 1 file(s).

```



If no files have changed:



```text

OK: No changes detected.

```



If a file is modified:



```text

MODIFIED: sample.txt

```



\## Technologies



\- Python

\- SHA-256

\- JSON

\- Git and GitHub



\## Limitations



The baseline is stored locally and is not protected against unauthorized

modification. An attacker who can modify both the monitored files and

the baseline may evade detection.



This is a learning project and is not intended to replace a

production-grade file integrity monitoring solution.



\## Author



Thiffanny Castro



