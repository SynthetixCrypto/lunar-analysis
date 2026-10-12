# Independent client — development readiness

Date: 2026-10-12. **Decision: ready to begin an original Fabric MVP, subject to the toolchain and integration spikes. Not implemented, built or release-ready.** See [architecture](independent-client-architecture.md) for subsystem contracts and [development plan](mvp-development-plan.md) for tasks/order.

## What is ready and what is still a gate

| Area | Status | Evidence or next action |
|---|---|---|
| Product scope | Specified | Four local HUD modules, native GUI/editor, typed infrastructure, profiles and persistence; launcher deferred. |
| Architecture/contracts | Proposed and implementation-ready | Each subsystem has responsibilities, dependencies, interfaces, failure policy and acceptance criteria in the architecture. These are new design decisions. |
| Minecraft/Java target | Provisional: 1.21.11 / Java 21 | Versioned official docs explicitly require JDK 21; target is not latest. |
| Exact dependency/build tuple | **Open Gate 0** | Generator + official metadata + clean build/launch must lock Loader/API/Loom/Gradle/mappings/JDK build. Published candidates alone do not prove compatibility. |
| Input/render integration | **Open Gate 1** | Verify raw click hook, remapping semantics, callback threads, layer ordering and current drawing/extraction API against pinned sources/runtime. |
| Native proprietary gaps | Nonblocking for MVP | No embedded browser, custom JNI or proprietary texture/service contract is needed. |
| Code, tests and artifact | Not delivered by these reports | Implementation tasks begin in a new repository. Every acceptance item below is prospective. |
| Performance and compatibility | Unmeasured | Establish a baseline and test the original client; no parity claim follows from static research. |
| Future launcher | Deferred design boundary | Its metadata/authentication/process/install contracts need separate development verification. |

## Evidence versus design

- **Observed in prior static research:** [Session 7 summary](../session7-astra/session-summary.md) reports worker-driven native rendering, three CPU surface records and synchronous caller-side texture callbacks; [cross-language contracts](../session7-astra/cross-language-contracts.md) distinguishes copied input from borrowed upload storage and partial cleanup evidence.
- **Still unknown in that research:** [remaining gaps](../session7-astra/remaining-gaps.md) explicitly leaves important native lifetime, queue, JNI and JS/promise questions open. Static analysis did not establish real FPS, contention, failure frequency or complete cleanup.
- **New proposal here:** pure-Java core, deterministic typed dispatch, scoped module resources, one revisioned JSON root, client-thread mutation, native Minecraft UI and independently specified HUD metrics/layout.
- **Verified external guidance in this pass:** [Fabric 1.21.11 setup](https://docs.fabricmc.net/1.21.11/develop/getting-started/setting-up) specifies JDK 21; [HUD docs](https://docs.fabricmc.net/1.21.11/develop/rendering/hud) recommend `HudElementRegistry` and discourage deprecated `HudRenderCallback`; [versioned guide navigation](https://docs.fabricmc.net/1.21.11/develop/) shows 26.2 as the default documentation track. The [generator](https://fabricmc.net/develop/template/) and metadata were consulted, but no project was generated/built.

## Remaining native unknowns: disposition

| Research gap | Why it does not block this MVP | When it becomes relevant |
|---|---|---|
| Complete native → Java GPU texture deletion | Native Minecraft drawing primitives own their engine resources; MVP creates no browser textures. | A future embedded/offscreen browser or custom texture provider needs a new explicit resource-lifetime design and tests. |
| Queued source-object lifetime and queue memory ordering | No native actor/surface queue is used; mutable core stays client-thread-owned. | A future asynchronous renderer must specify leases, bounded queues, publication and close-with-pending-work. |
| Worker failed initialization/unwind and JNI attach/detach | Client startup uses Java scopes and one ordinary I/O executor. | Custom native integration requires independent construction/unwind/attachment verification. |
| Alpha, premultiplication, padded stride and rasterizer details | HUD uses engine text and rectangle rendering. | Pixel uploads require synthetic color/alpha/stride tests of the chosen new renderer. |
| `Session.name` dynamic registration and unmatched JNI exports | No proprietary API or binary linkage is part of the MVP. | Relevant only to continued artifact research; an original client can define its own names/interfaces. |
| Native JS codec, promise retention/retry/timeout | No JavaScript bridge or browser screen exists in this design. | A future bridge requires its own typed messages, completion/cancellation and ownership contracts. |
| Original runtime speed, contention and cleanup failures | No parity target or original-runtime baseline is assumed. | Measure the new product directly before making performance claims. |

**Research can continue independently, but implementation should not wait for these answers.** The transferable lesson is explicit ownership and failure handling, not reproduction of native queues or proprietary contracts.

## Actual implementation risks and resolution gates

| Risk | Concrete mitigation | Gate/acceptance |
|---|---|---|
| Reading default 26.2 docs while targeting 1.21.11 | Use versioned pages and generated sources; keep all Minecraft names in adapters. | Gate 0/1 builds on exact pinned tuple and records descriptors. |
| Missing fast clicks with tick polling | Observe physical press transitions at the game input boundary; use a narrow Mixin only if the API lacks the hook. | Two clicks occurring between consecutive ticks are counted independently. |
| Incorrect rendering lifetime/thread assumption | Record callback/extraction ownership in the integration spike; pass immutable snapshots/draw descriptions. | No retained drawing context; no game calls from I/O thread. |
| Listener leaks or duplicate toggles | One Fabric bridge; module-scoped subscriptions; deferred lifecycle mutation. | 100 toggle cycles preserve baseline listener count; disabled owner receives no callbacks. |
| Config corruption or out-of-order saves | One writer, revision ordering, same-directory atomic replacement, validated backup and read-only recovery. | Fault-injection/restart suite always recovers a complete valid root or clearly reports recovery failure. |
| Focus loss and binding conflicts | Explicit release/reset, context gating and conflict validation against vanilla/global/module bindings. | Alt-Tab/chat/inventory/capture tests cause no stuck key or unintended toggle. |
| Profile transition inconsistency | Safe-tick switch, clear transient input/metrics, whole-root persistence and explicit degraded status. | No old listeners or mixed settings; failed save does not falsely mark selected profile durable. |
| Scaling or editor drift | One GUI coordinate system and normalized free-space layout with inverse tests. | Placement remains reachable across the documented resolutions/scales. |
| Core missing from distributed JAR | Package dependency deliberately and verify a clean instance. | Release artifact runs without development classpath/project files. |

## MVP acceptance checklist

All items are **not yet executed**. Tick them only with implementation test/manual evidence.

- [ ] **Toolchain:** exact Minecraft/Loader/API/Loom/Gradle/mappings/JDK tuple recorded; clean checkout builds; packaged JAR runs with declared dependencies only.
- [ ] **Startup:** empty directory creates defaults; restart restores settings; no world is needed to open settings; stop during load cannot re-enable modules.
- [ ] **Lifecycle/events:** deterministic ordering, listener mutation and reentrancy policy tested; failure during enable/disable/render isolates its module; 100 toggles leak no subscriptions.
- [ ] **Settings:** typed controls enforce ranges/types, reset uses current defaults, Done commits and Cancel discards; same validators apply to loaded config.
- [ ] **Persistence:** root/backup corruption, denied writes, simulated full disk, unsupported atomic move, stale completion, future schema and second-instance lock cases verified; failed writes remain visibly unsaved.
- [ ] **Input:** repeat/hold gives one toggle; rebinding does not trigger gameplay actions; conflicts are surfaced; typing/menu clicks do not toggle modules or count CPS; Alt-Tab resets highlights.
- [ ] **FPS:** game counter source and refresh lag documented; missing value handled.
- [ ] **CPS:** left/right counts pass deterministic exact-boundary tests including between-tick presses; holds and repeats excluded; saturation indicated.
- [ ] **Coordinates:** negatives floor correctly; dimension changes update; disconnect clears world snapshot.
- [ ] **Keystrokes:** vanilla remapping reflected in labels/highlights, including mouse-bound actions; no stale pressed state.
- [ ] **HUD/editor:** drag/hit-test/z-order/scale/reset work; disabled previews do not activate modules; Done persists and Cancel restores; F1 respected outside editor.
- [ ] **Settings/navigation:** keyboard traversal, narration labels, search, nested Back/Escape and title-screen settings work; all MVP options accessible in GUI.
- [ ] **Profiles:** create/clone/rename/delete/switch survive restart; clone edits are independent; last-profile deletion rejected; faulted modules and failed saves visibly distinguished.
- [ ] **Recovery/soak:** repeated join/disconnect, resource reload, resize, profile switch and close/reopen produce no accumulating resources or repeated error spam.

## Manual matrix and proposed performance gates

Initial manual platform: Windows x64 with the locked JDK/driver/game tuple recorded. Check title screen, singleplayer and a permitted multiplayer session; chat/inventory/settings/editor; focus loss; F1; resource reload; window/fullscreen; 854×480 and 1920×1080. Test every GUI scale valid at each resolution, including Auto. Support claims extend only to combinations actually tested.

Use the same world, viewpoint, graphics settings, FPS cap and warm-up for disabled/enabled comparisons. Record hardware, software versions, screen resolution and sample length. These are **proposed budgets**, not measured results:

- Combined four-widget client CPU work: p95 below **0.5 ms per rendered frame** in a five-minute post-warm-up sample on the recorded baseline machine. Measure the client's own callbacks/extraction work, not GPU time inferred from FPS.
- No file access in tick/HUD callbacks; configuration writes execute on the single I/O worker. Format/cache strings only when values change.
- 30-minute soak with at least 100 module toggles, 20 profile switches and 10 world reconnects: subscriber/widget counts return to expected baselines; click buffers stay bounded; retained client objects show no monotonic growth attributable to these actions.
- Shutdown flush finishes within the proposed **2-second** deadline under healthy storage; injected stalls time out with an unsaved diagnostic and preserve the last durable revision.

Investigate regressions against the baseline rather than claiming this client improves Minecraft FPS. Revise budgets only with recorded measurements and rationale.

## Go/no-go decision

**Go now:** Gate 0 toolchain lock, Gate 1 integration spike, then the restart-persistent FPS vertical slice. The specified modules, profiles and native GUI are sufficiently bounded to implement without further proprietary research.

**Hold release:** until the actual tuple is locked, original code exists, failure-path tests pass and the packaged artifact completes the acceptance matrix. **Hold launcher work:** until its own metadata/process/authentication contracts and acceptance slice are specified and verified. The previous research remains useful context, not a substitute for testing this implementation.
