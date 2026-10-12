# Lunar Client architecture research

An independent, evidence-backed study of Lunar Client's shipped launcher, Java client, feature framework and native WebOSR boundary. The goal is to understand architectural ideas and inform an **original, independently implemented Minecraft client**.

This project is **unofficial and unaffiliated with Lunar Client**. It is a research repository: the proposed independent client has not been implemented or released here. No rights to Lunar Client software, branding or assets are granted by these reports.

## Start here

| Topic | Reading |
|---|---|
| Overall findings and coverage | [Findings](findings.md), [component map](component-map.md), [missing evidence](missing-evidence.md) |
| Latest investigation | [Session 8 summary](session8-astra/session-summary.md), [all 16 native question statuses](session8-astra/native-question-status.md) |
| Independent client development | [Architecture](session8-astra/independent-client-architecture.md), [MVP implementation plan](session8-astra/mvp-development-plan.md), [readiness](session8-astra/development-readiness.md) |
| Historical evidence and unresolved questions | [Evidence index](evidence-index.md), [unresolved implementation](unresolved-implementation.md) |
| Launcher and startup | [Launcher architecture](launcher-architecture.md), [launcher internals](launcher-internals.md), [startup flow](startup-flow.md) |
| Java client and features | [Java internals](java-internals.md), [feature registration](feature-registration-deep-dive.md), [module lifecycle](module-lifecycle.md) |
| Events, settings and rendering | [Event payloads](event-payloads.md), [settings persistence](settings-persistence.md), [HUD math](hud-math.md), [rendering](rendering-and-hud.md) |
| IPC | [IPC deep dive](ipc-deep-dive.md), [session-4 RpcChannel policy](session4-sol/rpc-channel.md) |
| Native rendering and ownership | [Session 7 rendering](session7-astra/webosr-rendering.md), [GPU cleanup](session8-astra/gpu-resource-lifecycle.md), [queued image lifetime](session8-astra/queued-update-lifetime.md), [JNI lifecycle](session8-astra/jni-lifecycle.md) |
| Public repository status | [Session 8 audit and required cleanup](session8-astra/repository-audit.md), [sanitized evidence index](session8-astra/evidence-index.md) |

Historical reports are preserved. Read later corrections before relying on an older inference; a completed investigation pass does not mean every technical question is resolved.

## Research completed through Session 8

- **Sessions 1–4:** artifact/launcher architecture, Java features, lifecycle/events, settings/HUD, IPC and corrected wrapper-level findings. Start with the [Session 4 guide](session4-sol/README.md).
- **Sessions 5–6:** deeper Java reachability, compatibility and native-boundary preparation; [Session 6 gaps](session6-sol/remaining-unknowns.md) retain the unresolved-question definitions.
- **Session 7:** working Ghidra analysis established worker-driven rendering, three CPU pixel buffers, actor pumping, pull-triggered Java texture uploads, dirty-region processing and JNI reconciliation. See the [summary](session7-astra/session-summary.md).
- **Session 8:** targeted source-destruction acknowledgment, queue publication instructions, Java texture-release routes, JNI ownership and JS/promise contracts; all sixteen inherited native questions classified; an implementation-ready Fabric MVP and public-repository audit delivered.

Complete browser-to-GPU shutdown, arbitrary concurrent close/update safety, failed initialization, all JNI detach paths, alpha/color-space and `Session.name()` linkage remain open. They do not block the proposed native-Minecraft-UI MVP.

## Methodology and evidence

Research uses static artifact inventory, independent PE/class-file parsing, JDK `javap`, REA MCP and Ghidra decompilation/disassembly. Artifact hashes, function addresses, exact REA Evidence IDs and bounded search scopes support findings. Assembly and verified table layouts take precedence over guessed prototypes or exploratory filenames.

- **Verified / Confirmed:** directly supported within the cited static scope; not automatically runtime-observed.
- **Inferred:** a supported interpretation with assumptions stated.
- **Unknown:** evidence does not establish the behavior.

Session-specific finding aliases are not REA Evidence IDs. Native addresses must be qualified by binary, because dependencies can share image bases. Obfuscated Java aliases are analyst shorthand. Raw local records may contain proprietary disassembly or machine paths; Session 8 publishes a sanitized index and retains its raw evidence outside the Git publication set.

## Development roadmap

1. Lock a supported Fabric toolchain and verify startup/input/HUD integration. The provisional target is **Minecraft 1.21.11 / Java 21**, chosen for a bounded initial implementation, not claimed to be the latest release.
2. Build a pure-Java core: module lifecycle, typed events/settings, safe persistence and keybinds.
3. Deliver a restart-persistent FPS vertical slice, then CPS, coordinates and keystrokes HUDs.
4. Add a movable HUD editor, in-game settings and local profiles; test the packaged mod in a clean instance.
5. Consider a launcher and additional Minecraft versions after the first playable milestone.

Use Fabric APIs and Minecraft screens/rendering, with narrow version adapters where needed. A native browser renderer is unnecessary for this MVP. Exact dependency versions, build/launch checks and all product tests are future implementation work detailed in the [plan](session8-astra/mvp-development-plan.md).

## Repository layout and validation

Root reports contain historical architecture and inventories; `session2-tools`/`session3-tools` hold earlier helpers; `session4-sol` through `session8-astra` hold successive research. Session 8's twelve reports are linked from its [summary](session8-astra/session-summary.md).

Read the reports without a Lunar installation. With Python 3 and Git:

```powershell
python .\session8-astra\validate_documentation.py
python .\session8-astra\audit_repository.py
```

These checks read documentation/Git metadata and write only ignored local audit output. The documentation validator checks local link targets, fragments and evidence-index membership; it does not contact linked websites or prove semantics. Private raw evidence and target-hash checks are additional local validation described in the [evidence index](session8-astra/evidence-index.md).

## Research boundaries

- Installed target artifacts remain read-only; target code is not executed during these static investigations.
- Credentials, personal runtime data and private services are outside scope.
- Authentication, licensing and anti-cheat protections are not bypassed.
- New implementations must use original code/assets and supported APIs.

## Public-repository cleanup status

**The repository is already public and still contains tracked material requiring review.** Session 8 found extracted Minecraft class files, raw disassembly, machine-specific paths and oversized evidence blobs. New ignore rules prevent future accidental additions but do not remove tracked files or historical objects.

See the [audit](session8-astra/repository-audit.md) for counts, exact local review manifests and follow-up commands. Existing evidence is preserved; no untracking, commit, push or history rewrite was performed. Any future publication cleanup must also update affected documentation citations and preserve a private evidence archive.
