# Unresolved implementation questions (after session 2)

Study date: 2026-10-11. This list replaces nothing in [missing-evidence.md](missing-evidence.md); it records what remains open after the session-2 bytecode work. Each item says why it is open and what the next *legitimate* step would be. Next steps are static unless explicitly marked as needing approval.

## A. Phase 1 validation summary

| Codex claim | Re-verified how | Result |
|---|---|---|
| Artifact hashes (lunar, genesis, modern, common, `main.js`, preload) | `sha256sum` | Match |
| Genesis two-stage bootstrap, reflective `main` | javap of `ClientGameBootstrap.apply` | Confirmed, and the `main` target is now resolved (JV-27) |
| Mixin hook inventory | Joined with javap post sites | Confirmed and extended into an event map (JV-38) |
| WebOSR Browser/FunctionBus binding | javap of the GameUI ctor and constant pool | Confirmed, and the push direction resolved (JV-33) |
| Launcher WebSocket server and `--ipcPort` | `main.js` text (`bLe`, `gLe`) | Confirmed, with corrected details (JS-06/07) |
| Launch pipeline (`lRe` → `LUe` → `bRe`/`yRe` → spawn) | `main.js` text | Confirmed; the full argument set was added (JS-04/05) |
| 379 feature IDs as a "feature catalog" | `FeatureManager._de9126` | Clarified: about 119 classes are constructed at top level; the rest are children or IDs used only in localization |
| REA launcher graph coverage limits | Re-ran on extracted `dist-electron` | Still limited: heap exhaustion on `main.js` with a 4 GB worker |

## B. Open questions, prioritized

| # | Question | Why it is still open | Next legitimate step |
|---|---|---|---|
| U-01 | What the `removeIf` predicate in `FeatureManagerBase._535838()` filters out (which constructed features are dropped, and why) | The lambda target was not resolved from `BootstrapMethods` | `javap -v` on `L._02d7ad._cfe983` to resolve invokedynamic #0, then disassemble the synthetic method. **Static.** |
| U-02 | Full semantics of the trait keys `panel`, `page`, `index`, `display`, `label`, `staff_mod`, `ichor_keybind` and `toggle_keybind` | Only the key creation was traced | Grep for `getstatic L/_88f3cf/_02d7ad.<key>` consumers. **Static.** |
| U-03 | Which features attach `support`, `restriction` or `intercept` traits (server/Apollo gating), and the server data that drives them | The precedence is known; the attachments were not enumerated | Search for `putTrait(_02d7ad._290b8b/_ced4d4/_9a425c, …)` call sites, then follow the Apollo module classes. **Static.** No server interaction. |
| U-04 | Exact global Lunar HUD scale formula (`ALL`/`MODS`/`AUTO`) and the per-element scale range | Arithmetic partly decoded | Disassemble `L._2f4182._1253fc._bb4487.getScale/_22e64f` fully and the interface defaults `_b667ba/_0f113a`. **Static.** |
| U-05 | HUD editor snapping thresholds and the anchor-reassignment algorithm | Only signatures and strings were read | Disassemble `L._2f4182._6c713e._cfe983._cfe983(Rectangle,Rectangle)` and `_a140a8(point)`. **Static.** |
| U-06 | Event class semantics: which payload fields each of the 211 posted event types carries | Classes are obfuscated; roles are inferred from hooks | Per-event constructor descriptor plus hook-site arguments (the map is already in `mixin-event-post-map.tsv`). **Static.** |
| U-07 | Thread affinity: the behavior of the thread-checked bus subclass and of GameUI pumping (`invokeIteration`) relative to the render thread | Subclass body untraced; native side unavailable | Disassemble `L._d4ca6c._cfe983`. Native threading needs a native disassembler; **Ghidra is not configured** (set `GHIDRA_INSTALL_DIR` for REA if approved). |
| U-08 | Ultralight/WebOSR native internals: paint scheduling, dirty-rect generation, JS context, `bindFunction` marshalling | `WebOSR-Binding.dll` / `Ultralight.dll` are native, and REA's deep providers are unavailable | Configure Ghidra for REA (user approval for installation and configuration), then `open_binary` on `WebOSR-Binding.dll` and trace the JNI exports. **Static after setup.** |
| U-09 | Ichor transformation pipeline order: when Lorenz remapping, version pruning and Mixin application run, and which mapping files are opened | Only the transformer class was examined | Disassemble the ServiceLoader-registered Ichor services listed in `genesis!META-INF/services/*` and `Genesis.run`. **Static.** |
| U-10 | ~~Mapping of `--uiDir`/`--webosrDir` to the `L.util._038392` fields~~ | **Resolved in this session.** `lunar$main$parse` stores `lunar$uiDir` → `_8d6c5d` and `lunar$webosrDir` → `_155716` | — |
| U-11 | Game-side RPC timeout and failure handling when the launcher ignores a request (unknown service or method) | `L._cb9292._21aca6` (RpcChannel) was not disassembled | Disassemble the RpcChannel's `callMethod` / pending map. **Static.** |
| U-12 | Whether `ChatService` (launcher service and protos) is used by any game build | No Java stub exists in this build | Search other installed builds or profiles. Otherwise record it as dormant. **Static.** |
| U-13 | Settings migration (`L._2b0ee0._cfe983._bb4487`) rules and the version constant | Not traced | Disassemble the migrator. **Static.** |
| U-14 | Apollo `ModSettingModule` broadcast semantics (what servers receive or override) | Only the call site was seen | Trace `com.lunarclient.apollo.module.modsetting.*` within `lunar.jar`. **Static.** No server contact. |
| U-15 | Launcher `main.js` handlers beyond the launch path (profiles DB schema, installs, mod compatibility solver; ME-06/07) | REA semantic analysis runs out of heap; minified | Targeted text inspection per handler, or REA on smaller extracted slices of `main.js`. **Static.** |
| U-16 | The actual `POST /launch` response (`mainClass`, artifacts, JRE) for this installation | It requires a live service call | **Requires user approval:** a sanitized observation of an owned launch, or reading a cached response if one exists locally, without credentials. |
| U-17 | Crash classification rules (`bWe`) and the solutions database | Not traced | Text inspection of `bWe` and its metadata source. **Static.** |
| U-18 | Feature algorithms beyond FPS, CPS and ZOOM (Keystrokes, Coordinates, Armor Status and so on) | Out of scope for depth-first work | Apply the same per-feature method (`getId` string → constructor → handlers → HUD). **Static.** |

## C. Explicitly out of scope / not attempted

- Anti-cheat and integrity code paths (for example `INTEGRITY`/`OWEINTEGRITY` resources and launcher hosts-file checks). Their existence is noted; they were not analyzed.
- Account and auth flows. Only message *names and field types* were recorded. No accounts file, tokens or `installation-id` value was read.
- Any execution or loading of Lunar code, natives or JavaScript. No runtime capture.

## D. Recommended next investigation (priority order)

1. **Close the remaining static gaps cheaply:** U-01 (feature filter), U-11 (RPC timeout), U-13 (migration) and U-04 (HUD scale). Each is a single javap trace and upgrades an inference to Confirmed.
2. **Trace two or three more representative features** with the proven method: Keystrokes (input + multi-element HUD), Coordinates (child HUD composition) and Waypoints (3D render event + persistence file). This turns the framework understanding into broader feature coverage.
3. **Enable native analysis**, with user approval to configure Ghidra for REA. Then trace `WebOSR-Binding.dll` JNI exports into Ultralight for U-07/U-08.
4. **Only if approved:** a bounded, credential-free runtime observation of one launch, to confirm the `mainClass`, the stdout marker sequence and the IPC handshake ordering (U-16).

## Session 3 — status update (2026-10-11)

This section is an append-only update. The session-2 questions above remain as a historical record; the statuses below supersede their earlier open/partial classifications where specified. **Confirmed / Strong inference / Tentative / Unknown** have the same meanings as in the six linked reports. Static inspection only: no target execution, install-file changes, credential/settings-value reads, anti-cheat/integrity analysis or reimplementation.

### Six deliverables and resolved questions

| Topic / question | Current status | Result and evidence |
|---|---|---|
| Feature registration — U-01 | **Resolved; Confirmed** | The generic `removeIf` removes candidates with a present support trait whose static `_951ef4()` is false. Server gating is separate enablement, not registration. `lunar.jar`, `L._02d7ad._cfe983._535838 @5–16`, `_81676d @0–30`, `_cfe983(Support) @0–17`; JV-39–42. [feature-registration-deep-dive.md](feature-registration-deep-dive.md). |
| Event payloads — U-06 | **Partially resolved; Confirmed structural catalog, Unknown complete semantics** | 279 classes, 211 posted types, 90 cancellable; 31 posted SkyBlock types. Cancellation audit: 154/31 of 185 mapped cancellable Mixin rows do/do not read the flag. Catalog/constructor/hook/audit TSVs provide original classes, method signatures and Code ranges; JV-43/44, FS-08/09. [event-payloads.md](event-payloads.md). This is not a complete listener-effect or runtime-sequence specification. |
| HUD math — U-04 and U-05 | **Resolved for global/framework scale and snap algorithm; Confirmed** | Global scale and early-return modes, integer HiDPI ratio, framework scale-setting range 0.25–5.0, thirds-based anchors, screen/center/neighbour snapping. Exact physical input-button mapping remains **Tentative**. `lunar.jar`, global `L._2f4182._1253fc._bb4487.getScale @0–155`, `_22e64f @0–62`; editor draw `@1691–2140`, helper `@58–1059`, rectangle metric `@0–60`; JV-45/46. [hud-math.md](hud-math.md). |
| More module algorithms — U-18 | **Partially resolved; Confirmed selected code paths** | Coordinates, Keystrokes and Waypoints defaults/input/data/render/persistence paths traced; JV-47–49, FS-11. Exact class/method/offset tables in [additional-module-traces.md](additional-module-traces.md). Remaining features and unexpanded branches remain open. |
| Migration — U-13 | **Resolved for ordered ledger/load algorithm; Confirmed** | 31 steps, lazy lookup, context-version update before applying each target-specific rewrite, post-load re-save; effective setting reads separate from stored sparse saves. `lunar.jar`, migrator `L._2b0ee0._cfe983._bb4487._cfe983 @0–83`, `<clinit> @0–18`; setting `get @0–39`, serializer `@21–98`; JV-50–52, FS-10. [settings-persistence.md](settings-persistence.md). Exhaustive migration outcome for every personal/inactive profile is **Unknown** and was not tested. |
| Native preparation and UI FPS throttle | **Throttle identity resolved; Confirmed. Native model still Unknown** | `menuFpsLimit` default 120/range 30–500 drives texture refresh and the `setFPS` listener; engine argument additionally clamped 67–240. `lunar.jar`, performance ctor `@359–390`, `_eeb804 @0–4`, GameUI `_bb4487(Integer) @0–62`, blitter `@11–61`; JV-53–55, FS-12–15. [native-analysis-preparation.md](native-analysis-preparation.md). JNI 56/58 mismatch confirmed; version-skew interpretation and normal-lookup error are **Strong inference**, not observed failure. |

### Corrections and evidence boundaries

- **Confirmed:** neighbour snap interval is inclusive `[-2,+2]`, not open; only center/neighbour helper needs exactly one selected element. Screen-edge snapping precedes that gate. Sources: editor draw `@1797–2083`, helper `@588–600` (JV-46).
- **Confirmed:** HiDPI ratio uses `idiv`, not a floating-point division. Source: `_22e64f @57–61` (JV-45).
- **Confirmed:** separate-child decimal Coordinates formatting truncates toward zero; clipboard uses integer-cast `posY`, whereas the HUD supplier uses bounding-box `minY`. Sources: Coordinates `_133367 @0–40`, `_76bef3 @16–90`, `_ec6c75 @0–17` (JV-47). Grouped-format parity remains **Unknown**.
- **Confirmed:** WebP32 is x86, not x64. Source: PE Machine at file offset `0x84`, `native-jni-session3-verification.json` (FS-12). The six images in the old PE snapshot are x64.
- **Tentative:** personal profile scalar version observations are retained from the handoff only, not independently re-read under the keys/types-only rule. The implementation's current version 31 is **Confirmed** from the step list (FS-10/JV-50).
- **Confirmed structural observation / Strong inference interpretation:** the handoff's saved Default key order is a registry subsequence; absence of `REPLAYMOD` is consistent with module gating but cannot prove the cause because empty feature objects are omitted (FS-07).

### Still open and resolvable statically

| Question | Status and next bounded static step |
|---|---|
| U-11 — RpcChannel timeout/pending failure handling | **Unknown.** Inspect `L._cb9292._21aca6.callMethod` and pending-map completion/error/timeout code; do not make RPC requests. Prior JV-34 establishes transport, not this policy. |
| U-07 — thread-check event-bus subclass | **Unknown.** Disassemble `L._d4ca6c._cfe983`; Java WebEngine owner/queue behavior now has a separate confirmed trace (`WebEngine.<init> @5–9`, `invokeIteration @0–20`), but it does not answer bus checks. |
| Support trait `_83eb1a` / `setFlipped` | **Unknown.** Trace those consumers and their BootstrapMethods bindings. Static-supported and server-gate semantics in JV-40/41 do not establish all mutation/flip behavior. |
| U-18 — remaining feature algorithms | **Unknown beyond the named traces.** Continue constructor → settings → handlers → suppliers/renderers for a specifically selected feature; preserve limits on Credentials/anti-cheat/integrity. |
| U-03/U-14 — Apollo/option override sources | **Unknown.** Trace source-declared `lunar_option_overrides.json` parsing and intercept producers, key names/types only for any settings file. Setting.get's fallback is known, but complete precedence and producer semantics are not. |

Other historical items not expressly resolved above—such as trait-key consumers, Ichor pipeline order, dormant ChatService use, broader launcher handlers and crash metadata—remain at their prior statuses. No completed catalog is being treated as completion of the entire client study.

### Requires native tooling or separately authorized runtime evidence

- **Unknown — U-07/U-08:** Ultralight native thread/paint model, dirty-rect cadence, full TextureHandler callback route, and JS↔Java marshalling. Proposed Ghidra 12.1.x setup is documented, **not performed**. Installing/configuring it needs user approval; the approved follow-on can remain static.
- **Unknown — U-16:** actual `POST /launch` response and launcher-selected `mainClass`. Existing shipped-code mappings and Genesis/vanilla bootstrap facts do not establish an actual response. A suitably sanitized cached response or an authorized observation would be needed.
- **Unknown:** live stdout-marker sequence and IPC handshake/push ordering. Static contracts already cited in launcher/IPC reports are not a runtime trace. Any owned-launch observation needs separate user approval and credential exclusion.

No approval for setup, target execution or runtime observation is inferred from this write-up request.
