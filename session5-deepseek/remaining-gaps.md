# Remaining implementation gaps

Date: 2026-10-11. Session 5 (Deepseek). Static-only; no target execution. This file consolidates the open questions after sessions 1–4, marks which are **genuinely open** vs. **already resolved** (so no one re-investigates closed items), and prioritizes the next static work.

**Reading rule.** An item is listed as *open* only if I could not find a session-1–4 conclusion that closes it. Where a prior session closed an item, it appears under "Resolved — do not repeat".

Priorities: **P1** high-value and statically reachable now; **P2** valuable, larger or multi-class; **P3** blocked on tooling/approval or out of scope.

## A. Open — feature algorithms (incomplete)

| # | Question | Why still open | Next legitimate static step | Pri |
|---|---|---|---|---|
| G-01 | ARMORSTATUS full list spacing, individually-positioned equipment, protection-enchantment aggregation, custom bars-layout formula | SOL recovered update/source/preview split, durability math and overlay bars, but explicitly left these sub-branches (S4-MOD-01) | Disassemble the retained element/list helpers in `evidence-modules-a/L__88f3cf__bb4487__21aca6__1e73d7__*`; follow the protection child (`_590f69._cfe983`) and bars child (`_cfe983._21aca6`) constructors | P1 |
| G-02 | POTION_EFFECTS three-mode tile spacing, ordering, blink alpha curve, inventory-hook cancellation | SOL recovered mode routing, duration conversion, icon/text boundaries; left spacing/ordering/blink/inventory (S4-MOD-02) | Disassemble the three renderer instances `_590f69/_21aca6/_d4ca6c` and the blink tick; trace the inventory-hook producer annotation | P1 |
| G-03 | TOGGLE_SNEAK exact fly-speed/motion formula + all special-version sync/reset paths + producer cancellation | SOL recovered thresholds and the state-writing bridge; flight math and special-version paths partial (S4-MOD-03) | Disassemble flight callback `_cfe983(_00e05b) @0–347` fully; enumerate `_3a14e3` tick producers | P2 |
| G-04 | REACH_DISPLAY: actual attack-event producer for `getDistance`; identity of bridge counter `_0be1fc`; `_1eb51c` producer timing | SOL recovered clamp/correlation/reset but not the bridge field identity (S4-MOD-04) | Trace `bridge$entityAttackRange` and `_0be1fc` implementation in the modern bridge; map `_1eb51c` producers | P1 |
| G-05 | COMBO: Minecraft implementation of attacker/time/counter; whether every hit (vs. correlated status event) increments | SOL flags bridge semantics partial (S4-MOD-05) | Trace the same `bridge$getLastAttacker*`/`_0be1fc` family as G-04 (shared) | P1 |
| G-06 | PACK_DISPLAY: full custom width/height formula, child HUD role, mode color propagation, reload producer sequence, texture teardown | SOL recovered selection/texture/wrap/format; left these (S4-MOD-06) | Disassemble `…59b0c6…_cfe983$_21aca6` layout and the child `…_21aca6`; trace texture-manager release | P2 |
| G-07 | Remaining ~113 unmodeled feature IDs (of the ~119 constructed / 379 catalogued) | Only FPS/CPS/ZOOM/Coordinates/Keystrokes/Waypoints (s3) + Armor/Potions/ToggleSneak/Reach/Combo/Pack (s4) traced in depth | Apply the proven method (getId string → ctor → handlers → HUD) to the highest-value remaining features; reuse framework knowledge | P2 |

## B. Open — event-threading behavior

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-08 | Runtime value of the diagnostic check flag (`ORCHIOIHCIRHOROOOIHCRCOCCHIIOI`) and which subclasses select the debug bus | SOL: base `<clinit>` selects debug subclass when production flag false; effective state Unknown; no settings read | Static: enumerate `<clinit>` selection branches; do **not** read user settings values | P1 |
| G-09 | Real producer thread identities and lock contention/deadlock behavior | Requires runtime observation (not authorized) | Static only: map which producers post on which documented thread; contention needs approval | P3 |
| G-10 | Whether error-policy/depth imbalance **(conditional risk)** can actually leave positive depth / an uncleared deferred list | SOL: Strong inference, not reproduced | Static: audit all callers of wrapper/paired APIs for exception paths between depth begin/end; check `OHCRIICRROCCIORHCCICIOOCOCHHI` (replay) and the reporting helper for throwing paths | P1 |
| G-11 | Audit callers of the exposed mutable map (`COCRHRICOOHCCCCHCORIRICIIRRIIC`) and of wrapper/paired APIs for duplicate-production expectations | SOL recommends this explicitly | Static: xref the mutable-map getter and the wrapper overloads; classify call sites | P1 |
| G-12 | Whether PRE-only-pending cancellation (no PRE listener array) ever skips the paired operation in practice | SOL: branch exists (`_cfe983 @216–229`); runtime reachability Unknown | Static: find paired-overload callers whose PRE class has only deferred listeners | P2 |

## C. Open — RPC edge cases

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-13 | Caller-side pending-state cleanup after silent abandonment (expiry/disconnect) | SOL resolved channel policy; caller UI state not traced | Static: trace the 16 non-auth caller method bodies' pending/completion handling; find any UI spinner/lock released only on callback | P1 |
| G-14 | Real close/error ordering and the `onError` null-message NPE reachability | Requires runtime or careful library reasoning; SOL flags Strong inference | Static: bound the WebSocket library's error paths that can pass null messages | P2 |
| G-15 | Exact Guava cache maintenance timing (when logical expiry becomes physical removal/notification) | Library-semantics dependent, not channel code | Cite Guava version behavior; no target execution | P3 |
| G-16 | Whether simultaneous accepts of the same request ID can schedule duplicate callbacks | SOL: non-atomic lookup+invalidate; transport is a single receive stream | Static: confirm transport is single-threaded receive; else treat as open | P2 |
| G-17 | Reconnect race: pending entries left in a discarded transport's cache | SOL: new transport does not migrate old callbacks | Static: confirm per-transport cache ownership and old-transport GC | P2 |

## D. Open — dynamic feature-support transitions

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-18 | Enumerate **every** override producer and classify which invoke normal toggle lifecycle vs. effective recompute only | SOL: "all producers/broadcast/reset cases not exhausted" | Static: xref `L._88f3cf._1e73d7._a140a8._cfe983(feature,category,Boolean)` and `setEnabled`; build a producer table | P1 |
| G-19 | Metadata removal/reset paths and specialized setting interceptors | SOL: partial | Static: trace `_0ee36d` clear and `_cfe983(Predicate,T)`; enumerate setting-interceptor subclasses | P1 |
| G-20 | Producer ordering between brand arrival, world-ready, Apollo update and disconnect | Runtime ordering; SOL: "no live order collected" | Static: enumerate event registrations and note documented Minecraft-side ordering only | P3 |
| G-21 | Dynamic allowance dependency (`_a1dd3a`) live trigger ordering | SOL: dependency-driven transitions proven, order Unknown | Static: trace `_ba7d98._bb4487` dependency registration | P2 |

## E. Open — settings / configuration interactions

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-22 | Complete Apollo/server/option source precedence beyond the Boolean interceptor | SOL: complete precedence for other setting types Unknown | Static: trace per-type interceptors; do not read personal files | P2 |
| G-23 | Migration outcomes for every personal/inactive profile | Requires personal data (out of scope) | None; implementation is version-31 ordered ledger (resolved) | P3 |
| G-24 | Grouped-format parity of Coordinates decimal/format handling | s3: grouped-format parity Unknown | Static: trace the grouped formatter branch | P2 |

## F. Open — Minecraft-version-specific differences

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-25 | Full per-version matrix of gated branches (armor slot map, potion IDs, sneak special-version tick, reach/custom formatting) | Only point-gates recovered | Static: enumerate `MC_VERSION`/`_21aca6`-style version predicates and their thresholds into one table | P2 |
| G-26 | `versions.conf` ordinals → concrete Minecraft versions mapping | s2: ordinals 0–39 recorded; concrete names only partly mapped | Static: map `launch-class`/family to ordinal table | P2 |
| G-27 | Which profile/version an owned launch actually selects | Requires launch metadata/observation (approval) | None without approval | P3 |

## G. Open — Java↔native rendering boundary

| # | Question | Why still open | Next step | Pri |
|---|---|---|---|---|
| G-28 | Native engine thread model, paint scheduling, dirty-rectangle cadence | **No deep native provider configured** | See [native-investigation-plan.md](native-investigation-plan.md) (requires approval to configure Ghidra) | P3 |
| G-29 | `WebOSR_createEngine` @0x10A30, helper `0x199C0`, virtual slot `+0x8` semantics | Same | Same | P3 |
| G-30 | Texture-handler native callback path, BGRA stride units, teardown order | Same | Same | P3 |
| G-31 | `Session.name()` alternate registration / actual callers | Same (JNI resolution) | Same | P3 |
| G-32 | JS↔Java marshalling parity, `PromiseJS<T>` generic codec | Java side partially recovered; native conversion Unknown | Java-side static is doable now; native needs provider | P2 (Java) / P3 (native) |
| G-33 | `FunctionBus` queue-full (`add` → `IllegalStateException`) and unknown-routine unresolved-promise behavior in practice | SOL: conditional risk | Static: audit `invoke` call paths and any queue-depth guards | P2 |

## H. Blocked on approval (explicitly not performed)

| # | Question | Blocker |
|---|---|---|
| B-01 | Actual `POST /launch` response, selected `mainClass`/JRE/artifacts | Live service call (U-16; ME-01). Requires sanitized observation + approval |
| B-02 | Live stdout-marker / IPC handshake ordering | Requires owned-launch observation + approval |
| B-03 | Launch performance parity / FPS / startup timing | Requires runtime measurement + approval (ME-17) |
| B-04 | Replay/Reverse internals, service/social semantics | Out of scope / remote services (ME-12/14) |
| B-05 | Anti-cheat/integrity code paths | Explicitly out of scope |

---

## Resolved — do NOT re-investigate

These were closed by sessions 2–4. Listed so the next pass does not repeat them.

- **Registration filtering** (`removeIf` static-unsupported trait): JV-40.
- **Global HUD scale + snap algorithm** (integer HiDPI ratio, thirds anchors, inclusive ±2 neighbour gate): JV-45/46.
- **Migration ledger/load algorithm** (31 steps, lazy lookup, context update before apply, re-save): JV-50/51.
- **Effective vs. stored setting reads**: JV-52.
- **UI FPS-throttle identity** (`menuFpsLimit` → texture refresh + `setFPS` clamped 67–240; distinct from ≥5 ms engine pump): JV-55.
- **Event-bus thread-check semantics** (base logs, no reject): S4-BUS-01 (re-verified in Session 5).
- **Deferred add/remove + current-event pending path**: S4-BUS-03 (re-verified).
- **Bus lock/reentrancy/priority structure**: S4-BUS-02.
- **Paired PRE/POST cancellation branches**: S4-BUS-05.
- **RpcChannel tracking/expiration/cleanup/disconnect/reconnect**: S4-RPC-01..05 (3–4 re-verified).
- **Support gates + server flip intent + override precedence/restoration**: S4-SUPPORT-01..06 (5 re-verified).
- **Six module headline mechanisms**: S4-MOD-01..06 (6 re-verified).
- **WebOSR Java wrapper contracts + PE export mapping**: S4-NATIVE-01..06 (7 re-verified Java/PE).
- **Event catalog (279 classes / 211 posted / 90 cancellable / 31 SkyBlock)**: FS-08/JV-43/44.
- **gameipc protobuf schemas + handshake + close 4401**: PB-01/JV-34.
- **Launcher port policy, stdout markers, quick-join, exit classification**: JS-01..09.

## Genuine-unknown vs. already-resolved (quick reference)

| Topic | Status |
|---|---|
| Feature algorithms | **Genuine unknown**, largely statically reachable → G-01…G-07 |
| Event threading (runtime flags/thread identities) | **Genuine unknown**, runtime-gated → G-08/G-09; static caller audits → G-10…G-12 feasible |
| RPC edge cases | **Partly genuine unknown**; caller cleanup is statically reachable → G-13 |
| Dynamic support transitions | **Partly genuine unknown**; producer enumeration statically reachable → G-18/G-19 |
| Settings/config interactions | **Mostly resolved**; only non-Boolean precedence + grouped formatting open → G-22/G-24 |
| Version-specific differences | **Open matrix**, statically reachable → G-25/G-26 |
| Java↔native rendering boundary | **Genuine unknown**, blocked on native provider → G-28…G-31, G-33 |

## Highest-value next static pass (cheap wins)

1. **G-04/G-05** shared bridge field (`_0be1fc`, `bridge$getLastAttacker*`, `entityAttackRange`) — closes reach + combo bridge-semantics unknowns in one trace.
2. **G-18/G-19** override-producer enumeration — completes the support-state model.
3. **G-13** caller pending-state cleanup — closes the RPC story end-to-end.
4. **G-10/G-11** bus depth/replay + mutable-map caller audit — converts a conditional risk into a stated fact.
5. **G-01/G-02** armor/potion finish — turns two "partial" module reports into complete ones.
