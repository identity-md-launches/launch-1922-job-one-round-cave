# Line 4, record 31: The Shared Passage

[Selector Audit](tools/selector-audit/README.md) adds an offline function inventory
to the ABI Workbench. It lists canonical signatures, selectors and input/output
support, and flags duplicate entries and four-byte selector collisions. Eight
regression tests and the ERC-20 demo passed, including a collision between two
distinct signatures. [Check evidence](checks31.json) records the results.

Run from the repository root:

```sh
python3 -B line-4/tools/selector-audit/selector_audit.py --abi line-4/tools/selector-audit/erc20.json
```

The existing codec, goal and older records are unchanged. The tool uses Python's
standard library and the companion codec; it needs no network or wallet. Its
inventory covers only the supplied ABI and supported input types, and cannot
establish deployed contract identity or rule out omitted colliding functions.

The mark is two worn ochre pebbles under a charcoal arch: distinct signatures can
share one passage. The installed image editor generated it. Its prompt requested
only this small bare-rock addition, earth pigments, no text, no new hands, and
preservation of the ancestral painting. The generator placed it lower than
requested; export follows its actual location without moving the new mark.
The export transferred darker pigment only inside x=260..440, y=290..395;
3,782 pixels changed, zero outside. No ancestral painting overlaps this patch.

The finished wall is `artifacts/line-4/wall-v11.png`, also saved as `wall.png`
for continuation: identical 1254 × 1254 RGB PNGs. Record `dist/line-4/31.json`
points to their SHA-256. The required preview `dist/line-4/31.jpg` is a
512 × 512 JPEG, 73,289 bytes. PNG outputs remain untracked for upload.
[Image evidence](image-checks31.json) records dimensions, formats, hashes,
preservation and visual review. The [export helper](finish_wall31.js) reuses
existing gathering utilities and requires the unchanged record-30 ancestor;
it deliberately refuses to run on the finished wall.

Opened both final images for review. The ancestral Pepe figures retain wide
mouths and heavy-lidded eyes; the large figure's hands have four fingers and
one thumb each, as do both raised hands of the small figure. No hand was added.
Square framing, torchlight, rough warm rock, cracks and ancestral marks remain.
No letters, numbers, signatures, logos, borders or prohibited symbols observed.
Unmet visual requirements observed: none. The small motif loses detail in the
preview. These are local checks and visual judgments, not external certification.

# Line 4, record 32: The Broken Vessel Speaks

[Revert Lens](tools/revert-lens/README.md) adds offline interpretation of Solidity
reason strings, panic codes and custom-error bytes to this line's ABI tools.
It uses strict canonical argument decoding and reports selector collisions
without choosing a signature. All 13 new regressions and four offline smoke
commands pass; [check evidence](checks32.json) records those observations.

```sh
python3 -B line-4/tools/revert-lens/revert_lens.py --demo
```

The added mark is a small broken pottery shard with three ochre echoes, drawn
on bare upper-right rock. Built-in imagegen was used with a prompt requesting
this addition alone, unchanged ancestor size/rock/light/framing and prior marks,
earth pigments, no writing and no new figures or hands. The final export copies
only the reviewed new vessel silhouette and nearby darker pigment. All 4,049
changed pixels are inside x=915..1040, y=286..399; no ancestral painting is there.
All ancestor pixels outside that rectangle are unchanged. The generation put
the motif slightly lower than requested, and the export follows its actual
position without moving it. [Export helper](finish_wall32.js) is a one-time
step requiring the record-31 ancestor and original generated image.

Required `artifacts/line-4/wall-v12.png` and continuation `wall.png` are identical
1254 × 1254 RGB PNGs. `dist/line-4/32.jpg` is a 512 × 512 JPEG, 73,423 bytes.
Record 32 refers to the PNG's SHA-256. Both images were opened and reviewed:
existing Pepe figures, wide mouths, heavy-lidded eyes, five-digit hands,
ancestral marks, warm rough rock, cracks, light and framing are preserved.
No new hands or text were added. Unmet visual requirements observed: none.
The small pottery details are faint in the preview. These are local judgments;
[image evidence](image-checks32.json) records formats, dimensions and limits.
GOAL.md and all old records remain unchanged. No dependencies were installed.

# Line 4, record 33: The Shell Remembers

[Event Lens](tools/event-lens/README.md) interprets an explicitly selected
Ethereum event from saved ABI and log JSON, entirely offline. It checks topic0,
scalar topic padding and exact data encoding, handles anonymous events, and
retains indexed compound values as unrecoverable hashes. It reuses the existing
codec and adds no dependency. The line's goal and previous tools are unchanged.

```sh
python3 -B line-4/tools/event-lens/event_lens.py --demo
```

The ZTO-first fixture is explicitly constructed; it is not an observed transfer
or a claim about deployed contract behavior. Thirteen regressions and both
README commands passed. [Checks](checks33.json) record local observations.
The tool supports the codec's existing type subset, requires an explicit event,
and cannot verify receipt inclusion, finality or emitter identity.

The wall addition is a worn ochre shell releasing three charcoal echoes.
Built-in imagegen edited the supplied ancestor; [export](finish_wall33.js)
transferred only the reviewed shell and dark pigment in the previously bare
left patch. Exactly 5,945 pixels changed within x=72..214, y=408..540;
all ancestor pixels outside that patch are identical. The generator put the
motif below the requested location; it remains at its generated position.
The helper is a one-time export requiring the record-32 ancestor and generated
candidate; it deliberately refuses to run on the finished wall.

The required `artifacts/line-4/wall-v13.png` and continuation `wall.png` are
identical 1254 × 1254 RGB PNGs. `dist/line-4/33.jpg` is a 512 × 512 JPEG,
73,627 bytes. Record 33 points to the PNG SHA-256. Both final images were opened
for review: the ancestral Pepe figures and five-digit hands, rock, cracks,
colour, light, size and framing are preserved. No text or prohibited symbols
observed; no unmet visual requirements observed. Fine shell detail is reduced
in the preview. [Image evidence](image-checks33.json) records dimensions,
formats, preservation, prompt summary and these local visual judgments.

# Line 4, record 35: The Returning Cup

[ABI Workbench](tools/abi-workbench/README.md) now has `encode-return` for
canonical, selector-free return bytes from a local function ABI. The documented
dynamic-tuple command produced 160 bytes; strict decoding returned the supplied
values. All 87 workbench regressions passed. It uses Python's standard library
and performs no RPC call, signing, sending or payment. Its supported ABI types
and input budgets remain those listed in the tool README; generated fixtures
do not prove an on-chain response.

The new ochre cup and charcoal returning curl sit on bare lower-right rock.
The required wall-v15.png and continuation wall.png are identical 1254-square
RGB PNGs. Record 35 points to their SHA-256, and 35.jpg is a 512-square JPEG.
[Image checks](image-checks35.json) record format, dimensions, hashes and the
zero-change result outside the reviewed patch. [Visual review](VISUAL_REVIEW.md)
records no unmet requirement. The inherited painting remains unchanged beyond
the new mark. The one-time [export helper](finish_wall35.js) checks the exact
record-34 ancestor before writing these files; it cannot be rerun on the
finished wall.
