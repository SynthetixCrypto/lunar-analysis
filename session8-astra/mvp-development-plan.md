# Independent client — MVP development plan

Date: 2026-10-12. **Proposed implementation work, not completed development.** Contracts and subsystem acceptance live in [architecture](independent-client-architecture.md); blockers and release gates live in [readiness](development-readiness.md).

## Release slice and stack

Build an original client-only Fabric mod containing four HUD modules, module/event/settings infrastructure, keybinds, movable HUD editor, native settings GUI and local configuration profiles. First support one locked Minecraft version and Windows x64. Launch through an existing launcher. This narrows the earlier [roadmap](../development-roadmap.md), which placed a new launcher near the start: the playable mod now comes first.

| Layer | Provisional choice | Lock requirement |
|---|---|---|
| Game/runtime | Minecraft 1.21.11; JDK 21 | Pin Minecraft exactly; record JDK vendor and full patch/build for CI and release verification. Official 1.21.11 docs require JDK 21. |
| Loader/API | Fabric Loader and Fabric API for 1.21.11 | Resolve exact compatible versions through generator and official metadata; no `latest`, `+` wildcard or version range in build dependencies. The literal `+1.21.11` in an API artifact version is a version suffix, not a wildcard. |
| Build | Fabric Loom, Gradle Wrapper, Java toolchain 21, Groovy Gradle scripts | Keep generator-compatible Loom/Gradle pairing, choose a released Loom version, pin plugin/wrapper and wrapper SHA-256. Verify the Gradle daemon's JDK requirement separately from Java compilation target. |
| Mappings | Mojang official mappings for 1.21.11 | One naming namespace, locked to the selected game artifact; no mixing Yarn and official-name examples. |
| UI/render | Minecraft Screen/widgets/fonts and Fabric HUD API | Versioned docs and generated source are authoritative; verify callbacks, method descriptors and render/extraction lifetime in a spike. |
| Data/tests | Explicit Gson dependency; JUnit Jupiter; small injected clock/storage adapters | Pin resolved versions, dependency locks and verification hashes. No UI framework, service container or network stack required. |

## Gate 0 — lock the toolchain

1. Generate a **Java, client-only, Minecraft 1.21.11** project using the [official Fabric template generator](https://fabricmc.net/develop/template/). Keep split client sources; remove sample gameplay/content code when creating the new product repository.
2. Check the generator's exact values against [Loader metadata for 1.21.11](https://meta.fabricmc.net/v2/versions/loader/1.21.11) and [Fabric API Maven metadata](https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml). Record exact Loader, API, Loom, Gradle, mappings choice and JDK build with source URLs/date in the new repository's `docs/toolchain-lock.md`.
3. Metadata checked in this planning pass listed stable Loader **0.19.5** for 1.21.11 and API **0.141.6+1.21.11** among published matching artifacts. These are **candidates**, not a jointly tested lock. Loader metadata's own `min_java_version` is not Minecraft's runtime requirement. Do not infer a working combination from publication alone.
4. Resolve dependencies, generate sources, run tests/build and start a development client. If the generator selects a snapshot Loom, select and validate a released compatible version before declaring the lock complete. If build tooling needs a newer daemon JDK, record it separately while keeping the game/toolchain at Java 21; do not silently change Minecraft targets.
5. Commit exact coordinates, wrapper, checksum and dependency verification/lock files in the future implementation repository. Restrict `fabric.mod.json` to the validated game target and client environment. Record release dependency requirements for Loader/API/Java.

**Gate output:** reproducible clean build plus title-screen launch on the recorded toolchain. No exact Loom/Gradle/JDK-patch tuple was generated or tested during this report. Minecraft 1.21.11 is provisional and is not described as current/latest: [official docs](https://docs.fabricmc.net/1.21.11/develop/) currently advertise 26.2 as the default track.

## Proposed repository structure

Create this as a new implementation repository; paths below are a proposal, not files added to the research workspace. `dev.example.client` is a temporary package prefix to replace with the product's owned namespace at bootstrap.

```text
independent-client/
  settings.gradle
  build.gradle
  gradle.properties
  gradlew / gradlew.bat / gradle/wrapper/
  gradle/verification-metadata.xml
  gradle.lockfile
  core/
    build.gradle
    src/main/java/dev/example/client/
      lifecycle/ event/ module/ setting/ input/ metrics/ hud/ profile/ persistence/
    src/test/java/dev/example/client/
    src/test/resources/config-fixtures/
  fabric-client/
    build.gradle
    src/main/resources/fabric.mod.json
    src/client/java/dev/example/client/
      FabricClientEntrypoint.java
      runtime/                       # composition and bridge ownership
      adapter/minecraft/             # tick, input, snapshots, drawing
      module/                        # FPS, CPS, coordinates, keystrokes
      screen/                        # settings, editor, profiles
      mixin/client/                  # only verified missing input hooks
    src/client/resources/
      independent-client.client.mixins.json
      assets/independent-client/lang/en_us.json
    src/test/java/dev/example/client/
  docs/
    toolchain-lock.md
    config-schema.md
    manual-acceptance.md
    performance-baseline.md
  .github/workflows/build.yml
```

Start with two Gradle projects only: `core` is plain Java and `fabric-client` is Loom. Package the core classes into the distributed client artifact using the chosen Loom-compatible configuration; test the release JAR in a clean instance so a development-only project dependency cannot hide missing classes. Core tests must run without a game installation.

## Implementation order and exit criteria

Dependencies form a vertical slice: **toolchain → adapters → lifecycle/events/settings → persistence → FPS → input/CPS/other HUDs → editor/settings → profiles → release verification**. Complete each gate before expanding scope.

| Gate | Concrete deliverable and dependencies | Exit check |
|---|---|---|
| 0. Toolchain/repository | Generator-derived build, exact dependency lock, CI, client entrypoint | Clean build/test and title-screen launch; record all versions. |
| 1. Integration spike | One tick callback, one HUD element, one open-screen key, world/focus snapshot and physical mouse press observation. Verify rendering API and input hook availability; keep any necessary Mixin within adapter. | Development client displays fixed text, opens/closes a screen, captures two rapid clicks between ticks and survives join/disconnect. Record callback threads and concrete hook descriptors. |
| 2. Core ownership | Runtime state machine, resource scope, typed event bus, module manager and typed settings definitions | Failure-injection tests cover lifecycle rollback/cleanup, ordering, reentrancy and owner faults. One test module toggles 100 times with stable listener count. |
| 3. Durable config | Schema 1, default profile, ConfigStore, revisioned autosave, lock and recovery modes | Temporary-directory fault tests cover corruption and each write stage; restart restores a valid full state. UI-independent save diagnostics exist. |
| 4. FPS vertical slice | Real FPS module, HUD registry/geometry, one boolean/color setting and temporary development toggle action | Enable → render → change setting → save → restart → disable. No ghost HUD/listener after disable. Remove temporary action once the real GUI is ready. |
| 5. Input and HUD suite | InputRouter, binding validation/capture, CPS clock/deques, coordinates, keystrokes | Metric semantics and focus/reset tests pass; all four widgets work in-world; menu clicks and held-key repeats are excluded. |
| 6. Editor/settings | Native screens, typed controls/drafts, search/category, HUD drag/scale/grid/reset and Done/Cancel | Keyboard-only settings path; drag/save/restart; cancel restores prior layout/settings; GUI-scale/fullscreen tests pass. |
| 7. Profile workflows | CRUD/clone/activate, whole-root persistence, safe-tick transition and degraded-module feedback | Two visibly different profiles remain independent across switches/restarts; failed modules and unsaved active state are explicit. |
| 8. Release candidate | Remapped/package-appropriate distribution artifact, installation instructions, diagnostics, performance/soak record | Clean launcher instance with only declared dependencies passes the release checklist in readiness. |

Each gate ends with a runnable increment or a deterministic core/storage contract test. Runtime checks are against this original client only. A speculative launcher or browser bridge is not on the critical path.

## First implementer tasks

1. **T01 — Bootstrap and record lock.** Generate project; settle owned mod/package IDs; record exact versions; implement Gate 0. Output: reproducible wrapper commands and clean title-screen smoke result.
2. **T02 — Isolate integration.** Implement `MinecraftAdapter`, one HUD layer and screen-opening binding. Verify official-mapping class names from generated sources. Output: documented callback/thread/input contract.
3. **T03 — Define durable IDs and values.** Add module/setting/profile/widget IDs, result types, schema-1 DTOs and clock abstraction. Output: defaults for all four module descriptors with bounded typed settings.
4. **T04 — Own resources and dispatch.** Implement `ResourceScope`, EventBus and ModuleManager, then listener-failure tests. Output: one managed fake module with enable/disable/fault recovery behavior.
5. **T05 — Persist a single default profile.** Implement validator, ConfigStore, lock and revision writer using temporary-directory fixtures. Output: load/save/recovery status consumable by screens.
6. **T06 — Complete FPS slice.** Bind the game FPS source, widget measurement, original appearance setting and autosave. Output: first restart-persistent user-visible feature.

T01/T02 establish the adapter risks early; T03–T05 must remain testable without Minecraft. Do not build a general plugin loader, dependency-injection framework or multi-version abstraction beyond the single adapter seam.

## Verification commands and records

After the proposed multi-project build exists, its expected Windows entry points are:

```powershell
.\gradlew.bat --version
.\gradlew.bat :core:test :fabric-client:test :fabric-client:build
.\gradlew.bat :fabric-client:runClient
```

Confirm task names against the chosen Loom version. CI runs the build/tests on the locked toolchain; interactive client smoke and clean release-JAR installation are separately recorded. Retain test results, toolchain identity, manual matrix, known defects and measurements in the implementation repository. These commands were not run for this planning-only delivery.

## After the MVP

1. Measure and fix release defects before adding platforms or versions.
2. Add launcher architecture only after the mod's artifact/config boundaries are stable: independent launch metadata, Java/runtime preparation, process lifecycle and installation profiles.
3. Consider a second Minecraft adapter only with a new compatibility/test matrix.
4. Revisit browser rendering only for a concrete feature that native screens cannot satisfy; it would require new frame/texture/queue ownership tests, not resolution of proprietary implementation details as a prerequisite.
