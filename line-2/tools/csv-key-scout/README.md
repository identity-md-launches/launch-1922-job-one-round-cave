# CSV Key Scout

Compare explicit candidate column sets across two CSV exports before choosing a key for CSV Reconcile. The scout reports row counts, empty key rows, duplicate groups, unique nonempty keys, and keys that can be paired uniquely across the two files. It prints no cell values and never selects or applies a key.

Python 3.9+, standard library only. It imports the existing bounded UTF-8 CSV reader from `../csv-reconcile/`; keep that sibling tool in place. Run from the workspace root. Inputs must resolve inside the current working directory. No network, coin, wallet, or file writes are used.

## One command to see it working

```sh
python3 -B line-2/tools/csv-key-scout/scout.py line-2/tools/csv-key-scout/demo-before.csv line-2/tools/csv-key-scout/demo-after.csv --candidate '["record_id"]' --candidate '["source_code"]' --candidate '["area","record_id"]' --format text
```

Observed: all three candidates are evaluated. `record_id` has four unique nonempty keys on the left and three on the right; one right-side row has an empty ID, so the result says `review`. Two eligible keys are shared. `source_code` has a duplicate group on each side. The command exits **0** because scoring completed; `review` is not an error. The fixtures are synthetic.

## Input and ranking

Repeat `--candidate` with a JSON array of one to four exact header names. For example, `--candidate '["account","region"]'` represents a composite key. Supply one to twenty distinct candidates. The default text report can be changed to JSON with `--format json`.

Candidates are ordered by: no missing/empty/duplicate keys in either nonempty file, descending count of shared uniquely eligible keys, descending total uniquely eligible keys, fewer columns, then column names. The report retains each candidate's original index. A key is eligible only when every component is nonempty and that tuple occurs once in that file. Duplicates and empty tuples are excluded from overlap counts.

Exit **0** means the candidate statistics were computed, even when a candidate needs review. Exit **2** means an input, candidate, or I/O error; no partial report is printed. Column names and counts are included, but cell values and file paths are not.

The scout loads both tables in memory through CSV Reconcile's existing parser, which bounds each file to 16 MiB and 100,000 rows and refuses malformed UTF-8 CSV, duplicate/empty headers, ragged records, and paths resolving outside the workspace. At most 20 candidates and four columns per candidate are accepted. It compares exact strings: no trimming, normalization, fuzzy matching, or inferred key combinations. Ranking describes only these two exports. A column can be unique today and still fail to identify the same real-world record later; choose keys from the source system's identity contract, then use CSV Key Audit and CSV Reconcile.

## What happened when tried

All **5 focused behavioral tests passed**. They check the demo counts, duplicate and empty-key handling, missing columns without cell-value output, candidate validation, refusal to produce a partial result after an input failure, and the text caution. The documented command also produced the counts above.

```sh
python3 -B -m unittest discover -s line-2/tools/csv-key-scout -v
```
