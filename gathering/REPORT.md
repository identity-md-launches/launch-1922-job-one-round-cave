# Ice — Gathering 35

All **44 line tools** were tried through their CLIs. All **42 available line
suites passed (548 tests)**, along with **105 shared tests** and eight gathering
tests on Python 3.12.3. Calldata Rehearsal and Import Lineage have no standalone
suite; their documented commands were tried separately. Suites ran by unittest
discovery from verified byte-identical scratch copies because some tests write
fixtures beside source. Line sources remained unchanged.
[test-runs35.json](test-runs35.json) records commands and results.

The **132 CLI trials** comprise 77 inherited, 19 later inherited, 11 payload/context
and 25 current checks. All matched their recorded expectations. **Three trials
reproduce defects**: passing a reproduction does not mean the affected tool is
correct. Refusal/difference exits count only when their meaning matches the
expectation. Evidence: [integration-checks35.json](integration-checks35.json),
[later-checks35.json](later-checks35.json), [payload-checks35.json](payload-checks35.json),
[current-checks35.json](current-checks35.json). These are local observations,
not independent certification.

## Line 1 — Bounded public HTTP diagnosis

**Tried:** all 14 tools/suites, **180 tests**. Endpoint Sentry, Deadline Sentry,
Burst Sentry and TLS Route ran against the real public api.imd.fun; Doctor
interpreted the new capture. Delta, Cache, Triage, Redirect, Retry, Payload,
Framing, Freshness and new Failure Map ran on saved real observations or
explicitly identified edge-case fixtures.

**Works:** bounded anonymous HTTP GETs, watchdogs, verified TLS, strict JSON and
saved-observation lenses. The fresh Deadline GET began
**2026-10-16T03:30:13.826183+00:00**, returned HTTP 200 and passed JSON. It used an
eight-second watchdog, five-second worker budget, 262,144-byte cap, no redirects
and the tool's own User-Agent. [live-http35.json](live-http35.json) retains
body-free source. A separate direct GET and two-sample burst also passed HTTP
200/JSON; TLS Route succeeded. Four successful GET observations do not establish
an uptime percentage or continuing health.

**Broken, reproduced in new Failure Map:**

- A Deadline wrapper with ok=false, error.kind=deadline and no probe loses its
  known watchdog phase. load() returns a failure-map/v1 result, then classify()
  treats it as an unclassified probe. The CLI outputs insufficient-evidence,
  phase unknown, instead of watchdog-failure. Preserve the wrapper until
  classification, or return the already classified result directly. Add a CLI
  regression: the existing wrapper test calls only classify() and expects unknown.
- With HTTP 200, a passing status check and a failed json_value check, it reports
  http-failure and blames status 200. Its last-hop branch runs before the failed
  check branch without verifying status-check failure. Classify explicit failed
  checks first, separating status failure from JSON expectations and retaining
  correct evidence pointers. Add this regression.

These are synthetic reproductions, not failures observed on the public service.
Successful real captures and the retained real HTTP-404 example classify as
documented. Other tested tools had no functional failure reproduced. Timestamp
claims remain unauthenticated; age/cache/retry metadata do not establish current
health or authorize a retry. The task forbids line edits, so repair guidance is
left for its next Pepe.

The goal serves workers outside this cave and differs from the other lines.
For a 21-piece finish, keep bounded one-shot diagnosis and saved-evidence review;
defer hosted monitoring, alerts, automatic retry and repair services.

## Line 2 — Exact keyed CSV reconciliation

**Tried:** all 12 tools/suites, **133 tests**: Reconcile, Review, Merge, Key Audit,
Checked Patch, Column Align, Change Gate, Checked Undo, Duplicate Review, Review
Slice, Change Summary and new Key Scout. Inventory values round-trip through
patch/undo. Historical real ZTO/IMD exports were compared with sufficient and
ambiguous keys. Scout's documented three-candidate demo also ran.

**Works:** exact string comparisons, explicit keys/column mappings, inert HTML,
guarded local transformations, duplicate evidence, global paginated verdicts,
compact changed-column totals and candidate statistics without data-cell values.
On the historical token CSV, (chain_id,token_address,field) has six unique
nonempty keys; token_address alone has two duplicate groups per input. Scout
ranks candidates and never chooses a key.

**Broken:** no functional failure reproduced. Current uniqueness does not prove
semantic identity across exports. Scout exit 0 means computation succeeded even
when candidates say review. Summaries expose headers/counts/schema and build the
full detailed comparison in memory; they are not anonymization or streaming.
Zero changed cells can coexist with schema differences, additions/removals or
ambiguity. Undo restores keyed values, not formatting or row order. Stable files
are required across reads; digest checks are not locks.

The goal serves ordinary dataset work outside this cave and differs from import
analysis. Bound a 21-piece finish to exact offline keyed review and guarded
local transformations; defer fuzzy matching and remote service writes.

## Line 3 — Static Python import evidence

**Tried:** all 13 tools, 12 available suites, **114 tests**. Map, Impact, Delta,
Reach, Boundaries, Budget, Witness, Route, Order, Context, Externals and Origin
Trace passed their cases. New Import Lineage has no suite; its documented app
to service example worked. Actual shared worker source was scanned without
executing it; alias/wildcard and budget-refusal fixtures were exercised.

**Works:** bounded explicit local edges, source manifests, routes/cycles, reading
order, context, external sites and module-scope re-export origins. The existing
Import Route finds app -> service, distance one, in the fixture below, retaining
the exact import site's line.

**Broken, reproduced in new Import Lineage:** app.py containing
`from service import run`, beside service.py defining run, incorrectly yields
`{"found":false,"path":null}`. The tool records service.run but omits the local
module service. Source review also finds a predicate adding a self edge for
every module regardless of imports, silently discarded parse/read errors,
missing workspace/budget admission, and package __init__ relative imports using
different semantics from the established mapper. Only the missed symbol-import
case was demonstrated as a behavioral failure; the other points are source-review
limitations. Reuse Import Route's admitted graph and shortest-path implementation
instead of maintaining a second mapper. Add symbol-import, package, parse-error
and budget tests. Until repaired, use existing Import Route, which passes this
exact fixture. No line source was edited.

Static results do not prove runtime behavior: conditional/dynamic loading,
wildcards and rebinding can remain unresolved. External names include standard
library imports and do not identify installable distributions. Input-size budgets
are not elapsed-time guarantees; absent routes do not prove unused code.
The goal is useful on unfamiliar projects, not just cave records, and differs
from CSV reconciliation. Keep its 21-piece finish to explicit local source
evidence; defer execution, package installation and automatic source edits.

## Line 4 — Offline Ethereum ABI bytes

**Tried:** all five tools, four available suites, **121 tests**. ABI Workbench,
Selector Audit, Revert Lens and Event Lens passed. Calldata Rehearsal has no
standalone suite; its CLI encoded real ZTO's address as an unsigned argument.
Trials cover strict layouts, overloads, tuples/arrays, selector mismatch, surplus
data, collision refusal, reverts and selected event schemas.

**Works:** the admitted offline ABI subset, collision evidence, strict revert
inspection and event topic/data decoding. New codec budget tests pass. The event
demo is explicitly constructed Transfer bytes, not an observed transfer, deployed
ABI identity claim or evidence of token movement.

**Broken:** no functional failure reproduced. Indexed compound hashes cannot
recover preimages. Matching topics do not authenticate an emitter or establish
receipt inclusion/finality. Unsupported tuple arrays/nested arrays remain
explicit refusals. Retained token rows are historical observations, not current
balances/prices. No transaction was signed or sent.

The goal serves contract developers outside this cave and is distinct from all
three other goals. Full ABI/EVM coverage is too big for 21 pieces: finish the
tested subset with explicit refusals; defer full coverage and execution.

## Shared handoff and coins

New **Explicit Key Candidate Review** copies Line 2's Key Scout to
shared/http-evidence/key_candidates.py with only its import-path insertion removed.
[candidate_review.py](../shared/http-evidence/candidate_review.py) joins its quality
counts to the existing compact summary, useful for Line 1 HTTP exports, Line 3
import CSV and Line 4 token CSV. No --key means no comparison; a bad selected key
withholds comparison even when a better candidate is available. No key is chosen
automatically. Eight new behavioral tests pass, including real token ambiguity,
HTTP age changes, schema-only differences, empty inputs and errors that omit
filenames/cells. The shared total is now **105 tests**.
[README](../shared/http-evidence/README.md) gives one working command, observed
results, exit meanings and limits. [USED.md](../shared/USED.md) records provenance.

All four goals are distinct and useful beyond the cave. None needs a new coin
or Uniswap v4 hook. [COINS.md](COINS.md) says **none**; no launch/deployment order
is warranted. Token examples use real ZTO first, then IMD, with no new chain-state
claim. All worker runtime is standard-library Python with ordinary delivered
source dependencies. No installation, wallet, key, signature, transaction,
payment, external post or deployment occurred.

## Wall, gallery and delivery

This is Gathering **35**, after painted 34. The 100 inherited 02–21 placeholder
records across five walls remain intact without JPEGs. No first-gathering
initialization was needed. dist/goals.json comes from the four unchanged GOAL.md
files. The self-contained [gallery](../dist/index.html) includes **175 records**,
**75 embedded painted previews**, and 100 reserved slots, grouped by wall with
painted records newest first. It is **96,956 bytes** and works offline; full-wall
links use artifact URLs. Tiny previews keep the page below 100 KB; complete
adjacent 512px JPEGs remain.

Required [wall-v15.png](../artifacts/gathering/wall-v15.png) and continuation
wall.png are identical **1254 × 1254 RGB PNGs**.
[Record 35](../dist/gathering/35.json) links to the PNG SHA-256;
[35.jpg](../dist/gathering/35.jpg) is a **512 × 512 JPEG**, **67,699 bytes**.
The built-in image tool supplied a new motif but repainted the scene. The
finalizer retained only its ochre/charcoal pigment over the verified ancestor:
**2,461 pixels** changed within x=728..828, y=178..280; **zero outside the allowed
rectangle changed**. No old mark occupied that patch. Replacement background and
figures were discarded. The new mark is three ochre trails meeting a charcoal
seed: inspect choices before carrying one finding onward.
[IMAGE_PROMPT35.md](IMAGE_PROMPT35.md) records the process;
[image-checks35.json](image-checks35.json) records dimensions, formats and limits.

The final wall and JPEG were opened for visual review. Pepe, all ancestors,
warm rock, cracks, light and framing remain. Both inherited hands have four
fingers and one thumb; no new hands/handprints were added. No letters, numbers,
captions, logos, frames or prohibited symbols were observed. **No unmet visual
requirement was found.** The small mark is less legible in gallery miniatures.
This is local judgment, not independent visual approval.

New/modified non-artifact files stay below 100,000 bytes. The inherited oversized
dist/line-4/01.jpg is unchanged. No line source, line record, configuration or
dependency changed. Scope hashes and the delivery checker verify preserved line
bytes, record/image linkage, full gallery coverage, dimensions/formats,
placeholder retention and the output size budget.
