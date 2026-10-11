# Native/runtime inventory supplement

## Method and coverage

Confirmed observations below come from read-only file bytes. REA `inspect_pe_resources` was available and used directly for MumbleLink.dll and WebOSR-Binding.dll. Ghidra and IDA were not configured; Hopper does not support this Windows host. No native disassembly or target execution was performed. PE header/import/export parsing and ZIP central-directory/member-header inspection supplemented REA. Native ZIP members were decompressed only into memory, never executed or extracted to Lunar directories.

Evidence: `native-runtime-evidence.json` contains file SHA-256 digests, PE header and section locations, declared import names and their file offsets, exported names/RVAs, native ZIP member headers/digests, JRE release metadata, and complete inline REA resource evidence. These supplemental observations are analyst-produced static evidence, not REA decompilation. Import tables do not prove runtime loading, function calls, or communication. Delay imports, forwarded-export resolution, dependency search resolution, signatures, and actual runtime behavior were not examined.

REA resource evidence IDs:

- `ev_ce47b2c1768f5fdd35a762b2fc69b9cf8694d50d1f53e0fce8c7b185c6153001`: `C:\Users\Admin\.lunarclient\offline\multiver\natives\MumbleLink.dll`; pe32-plus, machine 0x8664; complete bounded resource inventory.
- `ev_1754d1892de23136481a3896993038130ace56740dd41b5f11c0f502fb1b7a0e`: `C:\Users\Admin\.lunarclient\offline\multiver\natives\WebOSR-Binding.dll`; pe32-plus, machine 0x8664; complete bounded resource inventory.

## JREs

Confirmed: three locally stored Azul Zulu runtime installations have release metadata declaring `OS_NAME="Windows"`, `OS_ARCH="x86_64"`, and the following versions. All three `bin/java.exe` files independently have machine `0x8664`, PE32+ headers. They declare imports from `jli.dll`, `KERNEL32.dll`, Microsoft VC runtime and Windows CRT API sets. None was launched.

| Runtime path under `C:/Users/Admin/.lunarclient/jre/` | Release JAVA_VERSION | JAVA_RUNTIME_VERSION |
|---|---|---|
| `515e47c1d532181677af445d76add9cabc2317de/zulu25.30.17-ca-jre25.0.1-win_x64` | 25.0.1 | 25.0.1+8-LTS |
| `56e53accb20696f802d92bd011174126b5e3154e/zulu21.30.15-ca-jre21.0.1-win_x64` | 21.0.1 | 21.0.1+12-LTS |
| `d093c370fc8eaa3e6743d7f61fb633adac4344f2/zulu21.48.17-ca-jre21.0.10-win_x64` | 21.0.10 | 21.0.10+7-LTS |

Inference: these provide locally cached alternative Java runtimes. Their presence alone does not establish which game version selects each runtime or which runtime last executed.

## Extracted Minecraft-side native directory

All entries below are under `C:/Users/Admin/.lunarclient/offline/multiver/natives/`. Architecture is confirmed from the PE COFF machine field, not inferred from filenames.

| File | Architecture | Format | Named exports |
|---|---|---|---|
| `msvcp140.dll` | x86_64 (0x8664) | PE32+ | 1515 |
| `msvcp140_1.dll` | x86_64 (0x8664) | PE32+ | 7 |
| `msvcp140_2.dll` | x86_64 (0x8664) | PE32+ | 44 |
| `msvcp140_atomic_wait.dll` | x86_64 (0x8664) | PE32+ | 32 |
| `msvcp140_codecvt_ids.dll` | x86_64 (0x8664) | PE32+ | 4 |
| `MumbleLink.dll` | x86_64 (0x8664) | PE32+ | 2 |
| `Ultralight.dll` | x86_64 (0x8664) | PE32+ | 541 |
| `UltralightCore.dll` | x86_64 (0x8664) | PE32+ | 543 |
| `vcruntime140.dll` | x86_64 (0x8664) | PE32+ | 71 |
| `vcruntime140_1.dll` | x86_64 (0x8664) | PE32+ | 3 |
| `WebCore.dll` | x86_64 (0x8664) | PE32+ | 14173 |
| `WebOSR-Binding.dll` | x86_64 (0x8664) | PE32+ | 58 |
| `webp-imageio32.dll` | x86 (0x14c) | PE32 | 101 |
| `webp-imageio64.dll` | x86_64 (0x8664) | PE32+ | 101 |

Confirmed: the native directory includes both x86 and x86_64 WebP libraries. All other inspected DLLs in this directory are x86_64. Native media resource filenames include `resources/icudt67l.dat`, `resources/mediaControls.css`, `resources/mediaControls.js`, `resources/mediaControlsLocalizedStrings.js`, and `resources/cacert.pem`; their contents were not examined in this pass.

## JNI and rendering/input boundary

Confirmed: `WebOSR-Binding.dll` declares imports from `jvm.dll` (including `JNI_GetCreatedJavaVMs`), `Ultralight.dll`, `UltralightCore.dll`, `WebCore.dll`, `DWrite.dll`, Windows libraries and Microsoft C++ runtimes. All 58 named exports follow the `Java_com_moonsworth_webosr_wrappers_...` JNI naming pattern. Examples:

- Engine lifecycle/scheduling: `WebOSR_createEngine`, `WebEngine_createBrowser`, `WebEngine_createSession`, `WebEngine_destroy`, `WebEngine_invokeIteration0`, `WebEngine_setFPS`, `WebEngine_setTimers`.
- Browser/UI: `Browser_loadURL`, `Browser_eval`, `Browser_evalNoResult`, `Browser_bindFunction`, `Browser_unbindFunction`, `Browser_getTexture`, `Browser_swapBuffers`, `Browser_triggerResize`.
- Input/focus: `Browser_triggerKeyEvent`, `Browser_triggerMouseEvent`, `Browser_triggerScrollEvent`, `Browser_setFocus`, `PlatformInterface_setCursor0`, `PlatformInterface_setScrollCallback`.
- Async and textures: `NativeFuture_get0`, `NativeFuture_isDone`, `PromiseJS_resolve0`, `PromiseJS_reject0`, `image_TexturedImageSource_update`, `image_TexturedImageSource_bind`.

Each name above abbreviates the common JNI prefix; full export names and RVAs are in the JSON evidence. Confirmed native dependency edges: `WebOSR-Binding.dll -> Ultralight.dll / UltralightCore.dll / WebCore.dll`; `Ultralight.dll -> UltralightCore.dll / WebCore.dll`; `WebCore.dll -> UltralightCore.dll`.

Inference: the JNI exports describe an embedded web rendering interface with Java-controlled browser lifecycle, URL/script interaction, textures, keyboard/mouse input, and asynchronous responses. This strongly supports a game-side web UI boundary, but does not establish which specific screens call it or the ordering/threading of those calls. The import declarations establish build-time native boundaries; actual runtime dispatch remains unobserved.

Confirmed: `WebCore.dll` declares `WS2_32.dll`, `CRYPT32.dll`, and `bcrypt.dll` imports. Inference: this is consistent with socket/cryptography capabilities in the web component. No destination URLs, active network connections, TLS traffic or credentials were collected.

## Mumble boundary and candidate local IPC

Confirmed: `MumbleLink.dll` exports `Java_com_moonsworth_lunar_client_mumble_MumbleLink_init` (RVA 5600) and `Java_com_moonsworth_lunar_client_mumble_MumbleLink_update` (RVA 5856). Its KERNEL32 import table declares `OpenFileMappingW` (name file offset 15728) and `MapViewOfFile` (15748), as well as synchronization APIs.

Inference: these declarations are consistent with a Java-to-native Mumble link using Windows mapped shared memory. The mapping name, memory schema, participants, call sites and runtime use were not established. This is not evidence of launcher-to-game IPC.

## WebP boundary

Confirmed: `webp-imageio32.dll` is machine 0x14c/PE32; `webp-imageio64.dll` is machine 0x8664/PE32+. Both expose 101 named JNI exports for `com.luciad.imageio.webp`, including `WebP_decode`, `WebP_encodeRGB`, `WebP_encodeRGBA`, and encoder/decoder option methods. Inference: they supply platform-specific WebP image decoding/encoding through Java ImageIO integration. Loading-selection behavior was not traced.

## Native archives and misleading architecture labels

| Archive under `offline/multiver/` | Members | Confirmed PE member architectures |
|---|---|---|
| `client-natives-win-x86-v1_21_11.zip` | 3 | x86_64, x86 |
| `client-natives-win-x86-v26_1_2.zip` | 3 | x86_64, x86 |
| `client-natives-win-x86-v26_2.zip` | 3 | x86_64, x86 |
| `ul-natives-x86-win.zip` | 10 | x86_64 |
| `webosr-natives-x86-win.zip` | 1 | x86_64 |

Confirmed: `ul-natives-x86-win.zip` contains ten DLLs and every member has x86_64 PE machine headers; `webosr-natives-x86-win.zip` contains an x86_64 WebOSR-Binding.dll. Each `client-natives-win-x86-*.zip` contains MumbleLink.dll (x86_64), webp-imageio32.dll (x86), and webp-imageio64.dll (x86_64). Therefore `x86` in these archive filenames cannot be used to conclude that the package is exclusively 32-bit.

Confirmed: `client-natives-win-x86-v26_1_2.zip` and `client-natives-win-x86-v26_2.zip` are byte-identical by SHA-256 (`a0c526513091c7feb64e223b8f84be9891b89a6ffb0a8962fdfed8edcfca58b8`). Their WebP member hashes match the currently extracted native-directory WebP files; the older `v1_21_11` archive has different, smaller WebP files. The Mumble member hash is shared among all three. Every member of the Ultralight and WebOSR native archives matches the same-named extracted native file by SHA-256.

Inference: the extracted native directory is consistent with materialization of the current cached native packages. Hash agreement does not identify when extraction happened, which process performed it, or which version last used the files.

## Remaining limits

This pass covers the three cached Java launchers/release files, the 14 DLLs found in `offline/multiver/natives/`, and five native ZIPs. It does not examine JVM internals, all launcher native modules, all libraries embedded in every JAR, anti-cheat/protection internals, or live processes. Import declarations, JNI symbol names and archive membership support boundaries; they do not substitute for callers, function bodies or permitted runtime observation.
