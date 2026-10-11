# Minecraft-side Lunar Client architecture

Study date: 2026-10-11. Static, read-only analysis of local packaged code. No application/JAR/native execution, runtime attachment, protected-code recovery, account-data inspection or network connection was performed.

## Evidence and boundaries

All relative JAR paths refer to **C:\Users\Admin\.lunarclient\offline\multiver**. Exact SHA-256 identities, manifests and package summaries are in [minecraft-artifacts.json](minecraft-artifacts.json).

- **REA-G1 — confirmed archive evidence:** REA open_binary identified genesis-0.1.0-SNAPSHOT-all.jar as ZIP, SHA-256 c188afc0d9efd61eb994c23883b70e942dbd2d88777550edae24649849a1f046. inspect_artifact Evidence **ev_3dfa373be43e21b36815c27464dbd7b08fa52a525ac0995bc2cfc9a6c7e378a7**, linked inventory **ev_abd81f72db9d0318d3f5953315cfdcb138c8462fdbbea1dca5ed840efb52cb24**. Complete records are in [rea-evidence-through-genesis.json](rea-evidence-through-genesis.json). Its producer exceeded the MCP response budget; retained export succeeded. REA establishes central-directory inventory, not Java behavior.
- **S1 — supplemental static evidence:** ordinary Node ZIP/classfile parsing read 14 JARs and 28,992 class entries, zero parser errors. This includes shaded dependencies and duplicates between archives; it is not 28,992 unique Lunar classes. Inheritance/interfaces are in [minecraft-class-relationships.tsv](minecraft-class-relationships.tsv).
- **S2:** [minecraft-bootstrap-metadata.json](minecraft-bootstrap-metadata.json), selected class signatures and bytecode reference operations for Genesis and bootstraps.
- **S3:** [minecraft-mixin-metadata.json](minecraft-mixin-metadata.json), 184 Mixin configurations and 2,332 class-level Mixin annotations, including member injection/accessor declarations.
- **S4:** [minecraft-webosr-metadata.json](minecraft-webosr-metadata.json) and [minecraft-ui-bridge-metadata.json](minecraft-ui-bridge-metadata.json), browser signatures, native flags, CallbackJS annotations and bridge call sites.
- **S5:** [minecraft-ipc-metadata.json](minecraft-ipc-metadata.json), local WebSocket IPC inheritance and bytecode references.

S1–S5 are analyst parsers, **not REA decompiler output**. Bytecode offsets are within the named Java method's Code byte array. Obfuscated symbols are preserved. [minecraft-parser-methods.json](minecraft-parser-methods.json) preserves helper implementations; these parse metadata/reference operands without recovering source, executing targets or decrypting anything. JEB/JADX and deep native providers were unavailable in the parent REA capability check. Conditional path selection, full reflection targets and native implementations therefore remain partially understood.

## Packaged components

| Artifact | Confirmed facts | Architectural interpretation |
|---|---|---|
| genesis-0.1.0-SNAPSHOT-all.jar | 7,152 class entries; manifest Main-Class com.moonsworth.lunar.genesis.Genesis; Implementation-Version 9.10.1; Multi-Release true | Bootstrap/classloading layer, supported by S2 calls |
| lunar.jar | 18,523 classes; 6,448 under com/moonsworth/lunar, 2,445 under com/lunarclient/websocket, 1,378 under com/lunarclient/apollo, 382 under com/lunarclient/gameipc | Shared client feature code, protocol models and browser bindings; no standalone manifest Main-Class |
| common-0.1.0-SNAPSHOT-all-nomappings.jar | 32 classes under com/moonsworth/lunar/ichor; lunar/minecraft.accesswidener | Common integration declarations; exact broad responsibility inferred |
| modern-0.1.0-SNAPSHOT-all-nomappings.jar | 1,368 classes; 12 Mixin configurations; versioned bridge packages | Minecraft adaptation/feature-injection layer |
| lunar-fabric-mixins-0.1.0-SNAPSHOT-all.jar | 566 classes; versioned Fabric/OptiFabric configs; tiny-remapper/mapping classes | Fabric compatibility/version adaptation |
| lunar-sodium-mixins-0.1.0-SNAPSHOT-all.jar | 635 classes; versioned Sodium configs | Rendering-mod compatibility; activation unobserved |
| lunar-replaymod-fabric-mixins-0.1.0-SNAPSHOT-all.jar | 697 classes; versioned ReplayMod configs | Replay integration; activation unobserved |
| Flashback / Mod Menu / SkyHanni Mixin JARs | 9 / 5 / 5 classes and corresponding versioned configs | Separate compatibility components; activation unobserved |
| lunar-lang.jar | 34 resources, zero classes | Language/resource bundle |
| Three lunar-platform-mappings-v*.jar archives | Zero classes; v1_21_11 has 5 entries, v26_1_2 and v26_2 have 1 each | Mapping-data carriers; not applied to defeat obfuscation |

**Confirmed dependencies (S1):** Genesis includes SpongePowered Mixin, MixinExtras, ASM, Gson, Typesafe Config, SnakeYAML, JCTools, Sentry and Cadix packages. Lunar includes Protobuf, Apollo APIs/models, WebSocket/gameipc models, Adventure, Caffeine, graph and audio packages. Presence establishes inclusion, not runtime activation or exhaustive dependency resolution/version compatibility.

## Bootstrap and class relationships

**Confirmed (S2):** Genesis, ClientGameBootstrap and PreLaunchLibraryBootstrap have classfile major 61 (Java 17 bytecode). Shaded dependencies include older versions. This establishes those classes' Java 17 requirement; launcher/runtime evidence separately determines the selected JVM.

**Confirmed (S2):** Genesis.main(String[]) calls genesis.IRCROOHIIOOHIRCRRHOHIORHCOHIOR.init() at bytecode 40 and Genesis.run(String[]) at 44. Exception handling references Sentry. This is compiled behavior, not an observed report or network request.

**Confirmed (S2):** Genesis.run declares options version, classpathDir, workingDirectory, ichorClassPath, ichorExternalFiles, integrationTest, partialJar and dumpClasses. No dump option was invoked. It constructs genesis.RROHOCRCCHCIORHICIHCOHRIRCIHCI classloaders at 609 and 802, accompanied by Prelaunch and Game literals. It constructs PreLaunchLibraryBootstrap's argument record at 629 and ClientGameBootstrap's at 843, then invokes a loader helper at 640 and 854. Literal bootstrap class identities occur alongside these calls. This supports a two-stage prelaunch/game bootstrap design; branches and every reflective dispatch remain unverified.

**Confirmed relationships (S1/S2):**

- PreLaunchLibraryBootstrap implements Function<PreLaunchLibraryBootstrap$COOCHIRORIICRCIIRIROHIIRIRICCH,List<Path>>. Its record holds mcVersionName, mxCacheDir, classpathDir, overridesDir and extraLibsDir. It declares download overloads and keys ichor.launch.libraries, ichor.fabricLoaderVersion and FABRIC_LOADER.
- ClientGameBootstrap implements Function<ClientGameBootstrap$COOCHIRORIICRCIIRIROHIIRIRICCH,Void>. Its record holds args, working/classpath/cache/override directories, version, Ichor classpath/external files, integration-test flag and optional partial-JAR/class-dump metadata.
- genesis.RROHOCRCCHCIORHICIHCOHRIRCIHCI extends URLClassLoader and declares findClass, addURL and the reflective bootstrap helper.
- genesis.OHRORRHCHCRICORRRCIRIOCCIRCRII extends URLClassLoader and implements two ichor.api interfaces and an Ichor utility interface. Overrides include loadClass, findClass, findResource(s), getResourceAsStream, isExcluded and close.

**Confirmed (S2):** ClientGameBootstrap.apply calls Class.forName(String,boolean,ClassLoader) at 1101, Class.getMethod at 1119 with literal main, and Method.invoke at 1456. Its exact runtime-resolved game main class remains unknown. Its launch argument builder contains --gameDir, --assetsDir, --texturesDir, --uiDir, --jitDir and --webosrDir. Compiled path/property contracts include lunar.dataDir, java.library.path, ichor.prelaunchLibDir, overrides and mx-cache. These are code contracts, not personal settings values.

**Integration inference:** Genesis is a packaged executable entry candidate and statically leads toward the game main method. The launcher's effective mainClass is supplied by launch metadata; the manifest alone does not prove that this exact installed launcher selected Genesis in any particular session.

## Minecraft rendering, UI, input and configuration integration

**Confirmed (S3):** modern Mixin JSON files declare target CLIENT, minVersion 0.8, required true, compatibilityLevel JAVA_17, mixinPriority 200 and injectors.defaultRequire 1. The combined bridge list has 475 mixins, combined lunar 405 and OptiFine 29. These are declarations, not observed successful transformations. Version-suffixed methods and min/max annotations establish version-conditioned metadata; condition implementation remains unverified.

Exact obfuscated class paths and complete annotations are retained in S3; search by target/method below.

| Subsystem | Confirmed annotation target/symbol | Supported conclusion |
|---|---|---|
| Lifecycle | Minecraft: lunar$onInit at constructor TAIL; lunar$onTick at runTick HEAD | Construction/tick hooks; onInit's visible bytecode registers resource reload listeners, so its name does not prove full client initialization |
| Browser/frame | Minecraft: lunar$webosr$runTick$head, tail variants, lunar$webosr$renderFrame$head | Browser integration points within frame/tick lifecycle |
| Rendering | GameRenderer, Gui and render targets; lunar$renderTargetOverride, bridge$overrideMainRenderTarget; crosshair/vignette/camera-overlay bridges | Rendering access/injection boundaries; no output/performance capture |
| Keyboard | KeyboardHandler: lunar$onKeyPress$v1_21_9 and older variant inject HEAD with cancellable=true; character/setup and lunar$webosr$cancelKeyPress methods | Keyboard/browser input integration |
| Mouse | MouseHandler: lunar$onPress, lunar$onScroll, lunar$onMove and drag/release families | Mouse/scroll hooks; full dispatch semantics unverified |
| Screens | Screen: webosr$keyPressed variants, render/tick/init; Minecraft screen-change callbacks | UI lifecycle/browser input bridges |
| Configuration | Options: lunar$preSaveOptions at save HEAD; lunar$saveOptionsOverwrite at save TAIL; load/process/save setting methods | Options persistence integration; exact filenames/settings semantics unresolved |

**Confirmed (S1):** [lunar/minecraft.accesswidener](minecraft-accesswidener-metadata.json) starts “accessWidener v2 lunar” and declares accessible Minecraft/Blaze3D types, including OpenGL command/device/state classes, render-target support and Vulkan shader-compilation keys. These are shipped declarations; nothing was applied during this study.

## Embedded game UI and feature registry

**Confirmed (S4):** com.moonsworth.webosr.wrappers.Browser extends NativeHandle; NativeHandle implements AutoCloseable. Browser declares native loadURL, getTexture, eval, evalNoResult, bindFunction, resize/focus, keyboard/mouse/scroll and destroy methods. WebOSR.createEngine(Logger,UltralightConfig,ThreadConfig) is native. This establishes a Java/native browser boundary; native implementation and initialization order remain partial.

**Confirmed (S4):** FunctionBus implements handler.FunctionJS and exposes registerChild, subscribe(Object), invoke(PromiseJS,Browser,String,String[]), codec conversion and promise handling. The class **com/moonsworth/lunar/client/OHOORCCRHHHHROIICHOCRHOCRICROH/RROHOCRCCHCIORHICIHCOHRIRCIHCI/RROHOCRCCHCIORHICIHCOHRIRCIHCI/COOCHIRORIICRCIIRIROHIIRIRICCH**, method COOCHIRORIICRCIIRIROHIIRIRICCH, loads lunarInternalInvoke at 58, obtains its FunctionBus at 61 and calls Browser.bindFunction at 64. A sibling listener onDocumentReady contains a literal IIFE defining window.lunar, lunarReady, lunarInternalAccept, event subscriptions and forwarding to lunarInternalInvoke. This corroborates the game UI JavaScript bundle's host contract.

**Confirmed (S4):** the provider class ending .../COOCHIRORIICRCIIRIROHIIRIRICCH/IRCROOHIIOOHIRCRRHOHIORHCOHIOR has CallbackJS annotations requestPayload, unregisterPayload, setScreen, setActiveRoute, setActiveOverlay, hideOverlay and invoke. Its OHROHICCCHIOIOOCHCCOHHCOOHRICC uses ImmutableMap.builder/put to register settings, profiles, mods, hudModProperty, hudModMetadata, waypoints, cosmetics, friends, rewind and associated namespaces. These establish feature-facing UI boundaries. A complete core mod manager, event bus and persistence model were not reconstructed; registry names do not establish individual feature algorithms.

## Launcher IPC and remaining unknowns

**Confirmed (S5):** com.moonsworth.lunar.client.COOIOIRCCICRCCIHCCRHRCIHROHCCI.COOCHIRORIICRCIIRIROHIIRIRICCH extends org.java_websocket.client.WebSocketClient. Its constructor takes a gameipc Handshake, forms a URI with the constant-pool concat recipe ws://127.0.0.1:<runtime integer>, calls URI.create at 9 and WebSocketClient constructor at 37. No runtime port or handshake payload was collected. It creates protobuf RPC stubs for launch, location, browser and other service families. onMessage(ByteBuffer) calls GameboundIPCMessage.parseFrom at 1 and distinguishes RPC_RESPONSE/PUSH_NOTIFICATION, referencing IPCRpcResponse. onOpen registers PlayServerPush, ExitGamePush and FocusGamePush. This establishes compiled loopback WebSocket/protobuf behavior, not an observed connection. The launcher architecture report independently identifies its paired loopback WebSocket server and --ipcPort argument.

**Confirmed limitation (S1):** 4,421 of 4,439 com/moonsworth/lunar/client class entries have final segments matching the shipped uppercase CHIORS alphabet, optionally followed by inner-class suffixes. This is a descriptive pattern, not authoritative obfuscator identification. No renaming, deobfuscation, mapping application or protection bypass was attempted.

**Partially answered:** classloading sequence, selected Mixin/version activation, complete feature/mod relationships, native rendering and configuration schemas. **Unresolved:** runtime-resolved Minecraft main class, complete core initialization call graph and active network/IPC state. Anti-cheat internals were not examined. Static package/symbol presence must not be described as observed execution. Native inventory and embedded UI analysis appear in companion reports.
