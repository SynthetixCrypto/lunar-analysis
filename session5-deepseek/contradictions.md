# Contradictions, corrections and documentation-consistency audit

Date: 2026-10-11. Session 5 (Deepseek). Static-only; no target execution. This file compares the claims of Codex (sessions 1–2), Opus (session 3) and SOL (session 4), and records inconsistencies with evidence. **Existing reports were not modified.** Where a later session already corrected an earlier one, the correction is marked as *resolved*; only genuinely unresolved or newly surfaced inconsistencies are raised as new.

Convention: **artifact → class.method @method-local decimal offset** for JVM facts; PE RVA/file offset for native metadata; "confirmed" = reproduced from bytes this session unless labelled otherwise.

## A. Already-resolved corrections (verified, no new action)

These were previously recorded as corrections by sessions 2–4. Session 5 re-checked them against fresh evidence and found **no contradiction**.

| # | Earlier claim | Correction already recorded | Session-5 check | Status |
|---|---|---|---|---|
| R-1 | `lunar$onInit` at `Minecraft.<init>` TAIL is the client init hook | Client singleton created at `Minecraft.run()` HEAD (`impl$run`, JV-01) | Not re-disassembled here (Modern Mixin); no contrary evidence | Resolved |
| R-2 | Bus subclass "thread-checked"/enforces affinity | Base class logs + `Thread.dumpStack`; no rejection (S4-BUS-01) | **Reproduced** from fresh `bus-base.javap-c.txt` (finding 1) | Resolved |
| R-3 | Mutations only affect the next event | Pending additions can run against the current event (S4-BUS-03) | **Reproduced** (finding 2) | Resolved |
| R-4 | RPC "no response leaves pending forever" | 10-minute write-expiry exists; expiry/disconnect silently abandon (S4-RPC-02/04) | **Reproduced** (findings 3–4) | Resolved |
| R-5 | Launcher "compares launch/installation identifiers" | Only `installation_id` compared; `launch_id` must be non-empty | Not re-opened (JS/minified); retained as-is | Resolved |
| R-6 | Native texture ownership/composition unresolved | Java owns textures; BGRA upload; framebuffer quad | Not re-opened; Java boundary consistent with finding 7 | Resolved |
| R-7 | "all 10 DLLs are x64" | Only the six-image snapshot is x64; `webp-imageio32.dll` is x86 (Machine `0x014c`) | Not re-parsed; retained | Resolved |
| R-8 | UI FPS-throttle identity tentative | `menuFpsLimit` drives texture refresh + `setFPS` (clamped 67–240) | Not re-opened | Resolved |

## B. Genuinely inconsistent or incomplete items (evidence-referenced)

### C-1 — Bus headline scope understates branch conditionality *(documentation nuance; SOL already scopes it in the report body)*

- **Claim location:** `session4-sol/README.md` "Key findings": *"Deferred additions can receive the current event."*
- **Report body:** `session4-sol/event-bus-threading.md` §"Exact class dispatch…" correctly limits this to the pending-add pass ("Indirectly via pending path"; "registering a listener from a handler can deliver the current event immediately in the deferred-add pass").
- **Observation (new evidence):** in fresh `evidence/bus-base.javap-c.txt`, the pending helper `COOCHIRORIICRCIIRIROHIIRIRICCH(Class,T,Supplier)` guard at `0–20` returns immediately when the event is null **or** the deferred list `isEmpty()`. Pending entries exist **only while dispatch depth ≠ 0** (private register/remove append only then). So the headline is true only on (a) the supplier posting path, (b) the paired PRE/POST path, and (c) when a mutation was queued during the current dispatch.
- **Severity:** Low. Not a technical error; a summary-brevity issue. **Recommended:** treat the report body as authoritative; the headline should be read as branch-scoped. Because the task forbids silently changing prior conclusions, this is **recorded, not edited**. Confidence: Confirmed (implementation).

### C-2 — `CLIENT_OVERRIDE` naming vs. actual priority *(already handled by SOL; retained as a standing caution)*

- **Observed:** override-category enum order is `SERVER → CLIENT_INTERNAL → CLIENT_REMOTE → CLIENT_CRITERIA → CLIENT_OVERRIDE` (`L._c8175c._cfe983._21aca6`: names at `$values` offsets 54–70 and ldc at 78–110). Under `EnumMap` iteration the **earliest** non-null category wins, so `CLIENT_OVERRIDE` — despite its name — has the **lowest** precedence.
- **Risk:** any reader (or future reimplementation) could invert this. SOL already warns against it (`S4-SUPPORT-05`). **Status:** resolved in SOL, restated here because it is the single most likely misreading in the whole corpus. Confidence: Confirmed.

### C-3 — "379 feature IDs" catalog vs. constructed features *(Codex vs. sessions 2–3; resolved, retained for lineage)*

- **Earlier framing:** Codex listed “379 feature IDs as a feature catalog” (`unresolved-implementation.md` §A).
- **Later correction:** only ~119 classes are constructed at top level; the rest are children/IDs used only in localization (`unresolved-implementation.md` §A; `feature-registration-deep-dive.md` JV-39). `missing-evidence.md` ME-03 independently says IDs "include child/auxiliary/server/scope-excluded items".
- **Status:** resolved and consistent across sessions 2–4. No contradiction found. Confidence: Confirmed (inventory scope).

### C-4 — "ID must match / pending invalidated before parse" ordering vs. duplicate-callback risk *(internal SOL caution; consistent, worth flagging for implementers)*

- **Claim:** `session4-sol/rpc-channel.md` S4-RPC-03 says the matched pending entry is invalidated **before** the response is decoded, and that lookup+invalidate are two operations (so a concurrent duplicate accept could schedule two callbacks).
- **Observed:** channel `COOCHIRORIICRCIIRIROHIIRIRICCH(IPCRpcResponse)` does `getIfPresent` (bytecode 4–16), then `invalidate` (48), then `newBuilder/mergeFrom/build` (53–76), then schedules the callback (99–104). Confirms both the ordering and the non-atomicity.
- **Status:** SOL is internally consistent; this is **not** a contradiction, but it is the kind of "conditional risk" that a later implementation must not read as "the channel guarantees exactly-once". No change needed. Confidence: Confirmed.

### C-5 — Terminology drift: "cache expiration" vs. "timeout API"

- **Risk:** `ipc-deep-dive.md` (session 2) and the README phrase the RPC policy loosely; SOL's `rpc-channel.md` explicitly corrects it ("The 10-minute setting is a **cache expiration policy**, not evidence of a timer…"). A reader who reads only session 2 could describe the RPC layer as having a caller timeout.
- **Status:** resolved by SOL; restated as a **cross-report reading-order caution**. Confidence: Confirmed.

### C-6 — REA provider `java_home` differs between Session 3's record and this session's live probe *(new observation)*

- **Session 3 record** (`provider-availability.json`): Ghidra check `java` = **ok**, `"21.0.10; 64-bit; JDK; C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot; accepted a 64-bit full JDK 21 or newer"`.
- **Session-5 live `rea.binary_session` probe (this run):** the same Ghidra candidate reports `java_home = C:\Program Files\Java\jre1.8.0_461`, `java_version = 1.8.0_461`, check `java` = **ok:false / `unsupported_version`** ("accepted a 64-bit full JDK 21 or newer").
- **Interpretation:** the two observations disagree about which JRE the **REA server process** currently resolves. This is an **environment/tooling inconsistency, not a Lunar finding**. Possible causes: a different `JAVA_HOME` in the MCP server's environment now, PATH ordering, or a stale `provider-availability.json`. It does **not** affect Java bytecode verification (I used the standalone JDK 21 `javap.exe` directly), and it does **not** change the Ghidra `not_configured` verdict (both observations agree Ghidra is unavailable because `GHIDRA_INSTALL_DIR` is unset).
- **Recommended:** before any future native pass, re-record provider diagnostics and pin `JAVA_HOME`/`GHIDRA_INSTALL_DIR` in the MCP server environment. Confidence: Confirmed (both observations recorded); cause Unknown. Source: this session's `rea.binary_session` output vs `provider-availability.json`.

### C-7 — Native "56 declarations vs 58 exports" skew: still open, correctly *not* over-claimed

- **Claim lineage:** Opus (JV-54) found 56 Java `native` declarations vs 58 DLL exports; SOL confirmed the discrepancy and reproduced non-forwarder entry RVAs (`Session_getName` @0x29690, `Browser_swapBuffers` @0x1fc10, `WebEngine_setTimers` @0x1c400).
- **Session-5 check:** export RVAs and entry bytes reproduced exactly (`evidence/pe_rva.py`; finding 7). Java `Session.name()` remains `native` with no Code offset (retained `Session.javap.txt`).
- **Status:** the *observation* is solid; the *cause* (version skew vs. alternate `RegisterNatives`) is **Unknown** and both sessions correctly avoid claiming an observed `UnsatisfiedLinkError`. No contradiction. Confidence: Confirmed (discrepancy); Unknown (cause).

### C-8 — ASAR helper integrity discrepancy (F-19) vs. Session-4 validator "all pass"

- **F-19** (`findings.md`): three unpacked 7za helpers have observed hashes that differ from ASAR metadata declarations; cause not established.
- **`session4-validation.json`** reports `document_and_evidence_checks_passed: true` and an evidence manifest with `changed: []`.
- **These are not in conflict:** SOL's validator checks *its own* retained research evidence against *its own* baseline, not the original Lunar ASAR integrity. A reader could misread "checks passed" as "the install is internally consistent". **Recommended:** keep F-19's unresolved status visible; it is an install-side observation outside the research-evidence manifest. Confidence: Confirmed (both records); no Lunar conclusion changed.

## C. Duplicated investigations (coverage overlap, not contradiction)

| Topic | Sessions covering it | Assessment |
|---|---|---|
| Event bus structure/priorities | 2 (JV-05), 4 (S4-BUS-*) | 4 refines 2; no duplication in conclusion; 2's thread-check inference superseded |
| HUD math / snapping | 3 (JV-45/46), 4 (reuses) | 4 explicitly reuses; correct de-duplication |
| RPC transport/handshake | 2 (JV-34), 4 (S4-RPC-*) | 2 = transport/envelope; 4 = policy/lifetime; complementary, not duplicated |
| WebOSR Java wrapper | 3 (JV-53/54), 4 (S4-NATIVE-*) | 4 extends 3; the 56/58 item is re-verified, not re-derived |
| Feature support gating | 2 (JV-07/09), 3 (JV-40/41), 4 (S4-SUPPORT-*) | Layered; each adds a distinct state; no contradiction |
| Module algorithms | 3 (Coordinates/Keystrokes/Waypoints), 4 (Armor/Potions/Toggle/Reach/Combo/Pack) | Disjoint module sets; no overlap |

**Verdict:** the corpus is well de-duplicated. No session re-investigated a completed inventory, and where work is reused it is cited as reuse.

## D. Unsupported / weakly-supported conclusions found

| Item | Where | Assessment |
|---|---|---|
| ProGuard attribution | JV / `findings.md` F-18 | Correctly labelled **Strong inference** from `proguardUuid`; not asserted as fact. Fine. |
| `lunar-platform-mappings` = Ichor's Lorenz mappings | JV-25 | **Strong inference** as labelled. Fine. |
| Launcher-cached Zulu JREs = "selected runtime" | F-07 | F-07 already says "cached alternatives, not proof of selection". Fine. |
| Mumble shared-memory IPC | F-14 / component map | Labelled **inference** (imports only). Fine. |
| "×2 HUD UI coordinate space" | JV-19 | Labelled S. Fine. |
| Any native "Render()/Update()" identity | `session4-sol/native-rendering.md` | **Not** claimed by SOL ("Do not assign… by name alone"). Good. |

**No session presented an inference as a confirmed runtime fact in the sampled corpus.** The consistent discipline is the strongest reliability signal in this study.

## E. Missing evidence references (*spot audit*)

I spot-checked citation resolvability rather than re-linking every one:

- SOL's `finding-locations.tsv` primary-evidence and mapping columns point at files that exist under `session4-sol/evidence-*/` (verified for all 28 S4-* rows: `evidence-bus/…aliases.txt`, `evidence-rpc/…javap.txt`, `evidence-support/…short.javap.txt`, `evidence-modules-*/…`, `evidence-native/…`).
- `session4-validation.json` reports `missing_relative_links: []`, `missing_citation_paths: []`, 1011-file evidence manifest with 0 missing.
- **Minor gap:** the REA export `session4-sol/rea-evidence-session4.json` is, by SOL's own statement, four inherited session-3 PE-resource records — so S4-NATIVE findings have **no dedicated REA Evidence ID**. This is honestly disclosed and is the reason those findings rest on analyst PE parsing rather than REA Evidence. Not an error; a traceability limitation. Confidence: Confirmed.

## F. Version-specific findings presented as universal *(audit)*

| Item | Risk | Assessment |
|---|---|---|
| ARMORSTATUS slot ordering `3-slotId` for `MC_VERSION>=29` | version-specific mapping | SOL explicitly gates it by version. Fine. |
| POTION EFFECT ID numbers / `excludeBreathOfTheNautilus` at `MC_VERSION>=35` | version-specific | SOL flags version gates. Fine. |
| TOGGLE_SNEAK "extra tick callback only for a specific version enum" | version-specific | SOL says the enum's human-readable version is **not** asserted. Good discipline. |
| Six-image "all x64" | corrected (R-7) | Resolved. |
| `Session.name()` absence | bounded negative | SOL calls it a bounded negative, not universal; correct. |

**Verdict:** session-4 version-conditioned findings are consistently gated rather than universalized. Earlier (session-2) reports are occasionally version-agnostic, but sessions 3–4 supply the gates. No silent universalization found.

## G. Summary

- **Resolved previously:** R-1…R-8.
- **Newly recorded inconsistencies:** C-1 (headline scope, documentation-only), C-6 (REA `java_home` environment drift — tooling, not Lunar), C-8 (ASAR-integrity vs. research-validator scope — reading caution).
- **Standing cautions restated (already flagged by SOL):** C-2 (`CLIENT_OVERRIDE` lowest priority), C-4 (RPC non-atomic completion), C-5 (cache expiry ≠ timeout), C-7 (56/58 skew cause Unknown).
- **No contradiction was found that requires changing a resolved technical conclusion.** No earlier conclusion was silently altered by this session.
