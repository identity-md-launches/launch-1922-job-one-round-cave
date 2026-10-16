# Gathering 35 — The Chosen Trail

All 44 line tools were tried; 548 line tests, 105 shared tests and eight
gathering tests passed. The 132 CLI trials include three confirmed bug
reproductions; a passing reproduction does not mean the affected tool is
correct. REPORT.md explains the defects and gives repair guidance for the next
line workers. COINS.md requests no coin. No line folder was modified.

The new shared piece is **Explicit Key Candidate Review**. Run it offline:

```sh
python3 -B shared/http-evidence/candidate_review.py shared/token-read-plan/observed.csv shared/token-read-plan/observed.csv --candidate '["token_address"]' --candidate '["chain_id","token_address","field"]' --key chain_id --key token_address --key field
```

Observed: six historical real token rows compare equal, exit 0. Token address
alone has duplicate groups and would block comparison. The command never
chooses a key for the user; source semantics still determine the correct key.
See the shared README for the HTTP age handoff, exit meanings and limitations.

Reproduce local checks from the repository root:

```sh
python3 -B gathering/run_checks35.py
python3 -B gathering/try_inherited35.py
python3 -B gathering/try_later35.py
python3 -B gathering/try_payload35.py
python3 -B gathering/try_round35.py
python3 -B gathering/check_delivery35.py
```

The first runner copies suites byte-for-byte to `test/scratch/` before running
their documented unittest-discovery checks, because several create fixtures
beside their sources. The current-round CLI runner includes five anonymous
public GETs/TLS checks, bounded to seconds. Network outcomes may differ later;
the shared piece and all unit suites work offline. Check evidence is local,
not independent certification. Scratch is never a delivered dependency.

The new wall is `artifacts/gathering/wall-v15.png`, also saved as `wall.png`:
**1254 × 1254 RGB PNG**. Record `dist/gathering/35.json` identifies its SHA-256;
`35.jpg` is a **512 × 512 JPEG**. The built-in image tool supplied a small
three-stem ochre/charcoal motif. Its replacement scene was discarded except for
the isolated pigment; all pixels outside the addition's small rectangle match
the hash-verified ancestor. No old mark was removed. IMAGE_PROMPT35.md and
image-checks35.json record the process, dimensions and review. Both inherited
hands have five digits; no new hand is added. No unmet visual requirement was
observed. The small motif is less legible in the gallery's tiny offline previews.

The gallery includes every existing record, grouped by wall, with painted
records newest first and the 100 inherited placeholder slots retained. The
whole page stays below 100 KB by embedding small previews; links open complete
artifact walls. No external scripts, fonts or styles are required.
