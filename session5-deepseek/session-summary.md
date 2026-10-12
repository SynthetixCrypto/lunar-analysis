# Session 5 — summary

**Session:** 5 (Deepseek)
**Date:** 2026-10-11
**Scope:** Independent verification of Sessions 1–4 and research-gap analysis for Lunar Client.
**Boundary:** Static-only, read-only. No Lunar JAR/native/JS was executed or loaded; the installation was not modified; no credentials, tokens, account files, installation identifiers or personal settings values were read; no anti-cheat/integrity, protection-bypass or reimplementation work was performed.

## TL;DR

Sessions 1–4 are **technically reliable within their stated confidence labels**. I independently re-derived all seven Session-4 (SOL) headline findings from the shipped bytes and bytecode. **Six verified as stated; one partially verified (the six module traces are accurate but explicitly partial). Nothing was contradicted.**

The one structural weakness is unchanged and honestly disclosed by SOL: **native WebOSR internals remain unverifiable** because no deep native provider is configured (Ghidra/IDA unavailable, Hopper macOS-only on this Windows host). That is a tooling limitation, not an over-claim.

## Deliverables (this directory)

| File | Contents |
|---|---|
| [verification-audit.md](verification-audit.md) | Phase 1: method, tool reality, per-finding verdicts (VERIFIED / PARTIALLY VERIFIED / CONTRADICTED / INSUFFICIENT EVIDENCE) with class.method offsets |
| [contradictions.md](contradictions.md) | Phase 4: resolved corrections R-1…R-8, new items C-1…C-8, duplication audit, unsupported-conclusion audit, version-gating audit |
| [remaining-gaps.md](remaining-gaps.md) | Phase 2: open gaps G-01…G-33, blocked items B-01…B-05, and an explicit "do NOT re-investigate" list |
| [native-investigation-plan.md](native-investigation-plan.md) | Phase 3: exact native entry points, 16 questions, approval-gated execution plan N-0…N-8, free Java-side fallback J-A…J-D |
| [evidence-index.md](evidence-index.md) | New Session-5 evidence, class-identity map, claim→evidence→verdict table, provider state |
| `evidence/` | Fresh `javap` dump, PE-extraction reader, console outputs |

## Phase 1 verdicts

| # | SOL finding | Verdict |
|---|---|---|
| 1 | Wrong-thread event checks log rather than reject dispatch | **VERIFIED** |
| 2 | Deferred listener additions can receive the current event | **VERIFIED (branch-scoped)** |
| 3 | RpcChannel requests expire after ten minutes without notifying failure callbacks | **VERIFIED** |
| 4 | Disconnect cleanup does not notify pending callbacks | **VERIFIED** |
| 5 | Saved toggle intent, effective enablement, and event subscriptions are separate states | **VERIFIED** |
| 6 | The six additional feature traces accurately represent their implementations | **PARTIALLY VERIFIED** (sampled claims reproduced; reports self-labelled partial) |
| 7 | WebOSR JNI mappings and Java-side queue/lifetime behavior correctly documented | **VERIFIED (Java/PE) / native architecture INSUFFICIENT EVIDENCE** |

No finding was CONTRADICTED.

## Key verification facts

- Thread check (finding 1): `RORCICOHRIOIIIOIOHIIIICRCIHRII.RHCCHHHHIHHRIICRIHRRIHRORIIOHO(Class)` has three return sites and **no throw / no queue / no dispatch rejection**; failure path logs and calls `Thread.dumpStack`.
- Pending additions (finding 2): the pending helper feeds the **current event object** to queued consumers and re-reads its own growing list; pending entries exist only while dispatch depth ≠ 0 (supplier and paired paths).
- RPC (findings 3–4): `expireAfterWrite(10, MINUTES)` + a removal listener that **returns immediately on `RemovalCause.EXPLICIT`**; `invalidateAll` on disconnect is therefore silent.
- States (finding 5): `updateEnabled` gate order and the override enum order `SERVER → CLIENT_INTERNAL → CLIENT_REMOTE → CLIENT_CRITERIA → CLIENT_OVERRIDE` reproduced; `CLIENT_OVERRIDE` is **lowest** priority.
- Modules (finding 6): armor integer durability `(max−dmg)*100/max`; potion 20.0f division + 3600/600 thresholds; sneak 200 ms / sprint 400 ms; reach status-byte 2 + Δ≤4 + `Math.min(attackRange, dist)`; combo reference identity + Δ≤4; pack FIRST = last list element — all reproduced.
- WebOSR (finding 7): `WebEngine.owner` compare then **unconditional** `invokeIteration0()`; `FunctionBus.MAIN_ACTOR_QUEUE` static `ArrayBlockingQueue(4096)` via `add`; `NativeHandle.close` not synchronized; the five PE export RVAs (`0x1FC10/0x29690/0x1C400/0x1C3B0/0x10A30`) and the 27-byte iteration stub reproduced byte-for-byte.

## Phase 2 highlights (open gaps)

Highest-value, statically reachable, low-cost:

1. **G-04/G-05** — trace the shared bridge field `_0be1fc` and `bridge$getLastAttacker*`/`entityAttackRange` (closes reach + combo bridge semantics together).
2. **G-18/G-19** — enumerate all override producers; classify normal-toggle-lifecycle vs. effective-recompute.
3. **G-13** — RPC caller pending-state cleanup after silent abandonment.
4. **G-10/G-11** — bus depth/replay exception path + mutable-map caller audit.
5. **G-01/G-02** — finish ARMORSTATUS and POTION_EFFECTS to remove their "partial" status.

## Phase 3 highlights (native)

Primary target `WebOSR-Binding.dll` (`4368a692…`). Seeds: `WebOSR_createEngine @0x10A30`, helper `0x199C0`, iteration stub `invokeIteration0 @0x1C3B0`, texture callbacks, `Session_getName @0x29690`. Plan: approve Ghidra 12.1.x + JDK 21 setup (N-0…N-8); meanwhile do the free Java-side tasks J-A…J-D. No native internals are claimed until observed.

## Phase 4 highlights (consistency)

- **Resolved corrections** R-1…R-8 re-checked, none contradicted.
- **Newly recorded:** C-1 (a README one-liner is broader than the report body — documentation-only), C-6 (**REA server `java_home` drift**: live probe resolves `jre1.8.0_461` while the session-3 record has JDK 21 — tooling, not Lunar), C-8 (ASAR-helper integrity discrepancy is outside the research-evidence manifest — reading caution).
- **Standing cautions restated:** `CLIENT_OVERRIDE` lowest priority; RPC completion is not atomic; cache expiry ≠ timeout; 56/58 JNI skew cause Unknown.
- **No session universalized a version-specific finding** in the sampled corpus; no inference was presented as a runtime fact.

## Tool reality (recorded honestly)

`rea.binary_session` is reachable. **Ghidra is `not_configured`** (`GHIDRA_INSTALL_DIR` unset); Hopper is `unsupported_host`; IDA is `not_configured`. Session 5 therefore verified only what Java bytecode and PE metadata permit, using the standalone **JDK 21 `javap`** against the same extracted class tree sessions 3–4 used, plus Python reads of retained session-4 evidence.

## Recommended immediate next step

Run the four free, static Java-side traces in [remaining-gaps.md](remaining-gaps.md) §"Highest-value next static pass" (G-04/G-05, G-18/G-19, G-13, G-10/G-11). They close the most unknowns without any tooling install, and they directly de-risk the eventual native pass by removing Java-side ambiguity.

## Integrity statement

Existing reports under `lunar-analysis/**` were **not modified**. All Session-5 output is confined to `session5-deepseek/`. No Git staging/commit/push was performed. No Lunar artifact, credential or personal value is included.
