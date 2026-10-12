# Lunar Client static RE — session 4 (SOL)

Date: 2026-10-11. This directory contains new work only. Reports and evidence outside this directory are inputs and must not be overwritten.

## Boundaries

- Do not execute or load Lunar JARs, natives, JavaScript or other target code.
- Installation files are read-only. Do not access credentials, accounts.json, installation-id, tokens, or personal settings values.
- No anti-cheat/integrity investigation, protection bypass, reimplementation, runtime attach, or tooling installation/configuration.
- Use static javap/disassembly, archive parsing and available REA static operations.
- Label findings Confirmed / Strong inference / Tentative / Unknown, with actual artifact, class, method and method-relative bytecode offset (or native RVA/file offset). Bounded negative searches are not universal proofs.

## Investigation checklist

1. Event-bus thread checks, locking, nested dispatch, deferred mutations and cancellation.
2. RpcChannel tracking, timeouts, error paths and cleanup.
3. Server/support/restriction/intercept transitions and propagation to children/subscriptions.
4. Six additional modules: ARMORSTATUS, POTION_EFFECTS, TOGGLE_SNEAK, REACH_DISPLAY, COMBO and PACK_DISPLAY.
5. New WebOSR/JNI/native rendering evidence beyond the session-3 metadata and mismatch inventory.
6. Contradiction checks, an evidence ledger, preservation checks and remaining questions.

## Starting evidence

The parent directory's session-3 ledger closes registration filtering, HUD global math/snapping, migration-list/load algorithm and UI throttle identity. It structurally catalogs events and traces FPS/CPS/ZOOM/Coordinates/Keystrokes/Waypoints. Those investigations will not be repeated.

Retained static dumps and extracted class files are in:
`C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad`.

## Report index and completion status

| Area | Report | Status |
|---|---|---|
| Event bus | [Threading, dispatch and mutation](event-bus-threading.md) | Selected overloads resolved statically; runtime thread identities unknown |
| RpcChannel | [Tracking, expiration and cleanup](rpc-channel.md) | Channel policy resolved; transitive caller deadlines unknown |
| Feature transitions | [Support, flipping and overrides](feature-support-transitions.md) | Selected state transitions resolved; all override producers not exhausted |
| ARMORSTATUS / POTION_EFFECTS | [Module traces](modules-armor-potions.md) | Partial; data/filter/durability/duration paths recovered |
| TOGGLE_SNEAK / REACH_DISPLAY | [Module traces](modules-toggle-reach.md) | Partial; tap thresholds, key state and reach correlation recovered |
| COMBO / PACK_DISPLAY | [Module traces](modules-combo-pack.md) | Partial; count/reset and pack/texture/formatting paths recovered |
| WebOSR/native rendering | [Java contracts and bounded native analysis](native-rendering.md) | Java-side advanced; native architecture still partial |
| Cross-check and next steps | [Status and corrections](status-and-corrections.md) | Supersedes named older inferences without editing their reports |
| Finding provenance | [Local evidence ledger](evidence-ledger.md), [citation table](finding-locations.tsv) | Local S4 IDs, not fabricated REA IDs |
| Document verification | [Validation result](session4-validation.json), [validator](validate-session4.py) | Link/hash/Git checks, not runtime tests |

## Key findings

- The event bus's wrong-thread check is in its base class and logs/dumps a stack rather than refusing dispatch. Deferred additions can receive the current event.
- RpcChannel uses a ten-minute expire-after-write cache; expiry and disconnect do not complete callbacks with failure. Tracking expiration is not a caller timeout API.
- Parent/server/dynamic allowance gates precede effective overrides. Server flip intent, stored toggle, effective enablement and subscribed handlers are distinct states.
- TOGGLE_SNEAK uses separate <=200 ms sneak and <=400 ms sprint tap thresholds. REACH_DISPLAY and COMBO use bridge counters—not wall-clock timers—in their correlation/reset paths.
- WebEngine drains the shared Java callback queue only on its owner thread but calls native iteration regardless. Native paint/dirty-rectangle/threading behavior remains unknown.

## Evidence layout

`evidence-bus/`, `evidence-rpc/`, `evidence-support/`, `evidence-modules-a/`, `evidence-modules-b/`, `evidence-modules-c/` and `evidence-native/` retain disassembly, mappings and bounded searches. Original JVM names are in each area's mapping/manifest. Full/verbose dumps are authoritative; shortened/compact views are reading aids. Some PowerShell-generated `.txt` files are UTF-16 and need an encoding-aware reader.

Reports cite artifact/class/method and decimal method-local JVM offsets or hexadecimal native RVA/file offsets. Abstract/native declarations and schema inventories have offsets N/A. **Confirmed** is static implementation evidence; **Strong inference** is conditional; **Tentative** is weak attribution; **Unknown** is unestablished. `S4-*` labels are local findings. The REA bundle contains four inherited PE-resource records, not new native decompilations.

## Verification and reproduction

From the repository root, with Python 3:

```powershell
python .\session4-sol\validate-session4.py
```

The validator checks local Markdown links, citation evidence paths, retained evidence SHA-256s, prior-report Git comparisons and historical ledger-prefix hashes. It reads only research files/Git metadata and writes `session4-validation.json` in this directory. On its first run it creates `evidence-files.sha256.tsv`; subsequent runs compare, rather than replace, that evidence baseline. It does not run target code or prove behavioral completeness. Without Git/history it records preservation comparisons as unavailable rather than claiming success. Raw byte and CRLF-normalized comparisons are separate because the repository uses `text=auto`.

Evidence digests bind the exact retained bytes. A later Git checkout's newline conversion or other filters can change text-file digests even without changing readable content; retain an original-byte evidence copy for forensic verification. The validator reports such differences and does not silently regenerate the baseline.

Optional static class verification, using a locally authorized extracted class tree and JDK disassembler:

```powershell
$Javap = 'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe'
$Classes = 'C:\path\to\authorized\extracted\lunar'
& $Javap -p -c -v -classpath $Classes 'com.moonsworth.webosr.wrappers.WebEngine'
```

`javap` disassembles class bytes; do not substitute `java`, launch the client or load JNI. Follow mapping files for obfuscated classes. Original artifacts/extracted trees are not a required part of a public documentation checkout.

`native-static.py` is a local-session capture helper, **not portable setup**: it hardcodes the retained cache, DLL and JDK paths and writes into `evidence-native/`. It uses only stdlib PE parsing plus javap, but loads an analyst-created pickle; never substitute an untrusted cache. Re-running can replace generated session-4 evidence. Review paths/source and work in a new analysis copy before optional recapture. No provider installation is automated.

## Git and publication

The repository-level [README](../README.md) provides the main index and publication checklist. No Git staging/commit/push is included. Keep earlier reports and private evidence unchanged; review distribution rights and sensitive fields before copying any evidence to a public remote. Do not publish Lunar artifacts, extracted packages, caches, credentials, personal settings, or proprietary assets. Absolute local paths in retained evidence are provenance, not portable requirements; redact only a separate publication copy.

## Remaining questions

The original checklist has deliverables for every area, but **the investigation is not complete**. All six modules retain narrowly stated unfinished branches. Native architecture requires an approved static provider; real ordering/threading/timing requires separate runtime authorization. Prior Ichor, launcher, dormant-service and actual launch-response questions retain their earlier status unless specifically updated in [status-and-corrections.md](status-and-corrections.md).
