# Native WebOSR evidence and preparation for deeper static analysis

Study date: 2026-10-11, session 3. No DLL, JAR or JavaScript target code was executed. No native decompiler was installed/configured. **Confirmed / Strong inference / Tentative / Unknown** label direct evidence, interpretation, provisional attribution and missing evidence. JVM offsets are method-relative decimal values; native metadata has no JVM class or Code offset, so PE tables/resources or file offsets are cited instead. The Java bytecode citation appendix is [session3-bytecode-locations.tsv](session3-bytecode-locations.tsv); wrapper/native declarations are separately retained below.

## 1. Files, architecture and identity (FS-12)

**Confirmed.** Native files are under `C:\Users\Admin\.lunarclient\offline\multiver\natives`. [native-pe-session3.json](native-pe-session3.json) retains sizes, SHA-256, PE Machine, imports, exports, certificate-table presence and PDB-string search results for six DLLs. All six recorded images have Machine `0x8664` (x64). The missing 32-bit WebP image was checked narrowly without executing it; its metadata/hash is in [native-jni-session3-verification.json](native-jni-session3-verification.json).

| DLL | Confirmed size / architecture | Role and classification |
|---|---|---|
| `WebOSR-Binding.dll` | 565,752 B / x64 | **Strong inference:** Lunar JNI glue, supported by 58 `Java_com_moonsworth_webosr_wrappers_*` exports and the Java wrapper declarations |
| `Ultralight.dll` | 613,880 B / x64 | **Confirmed:** Ultralight API exports/import relationship; **Strong inference:** engine facade |
| `UltralightCore.dll` | 2,503,672 B / x64 | **Confirmed:** bitmap/surface/platform API symbols; **Strong inference:** shared engine-core component |
| `WebCore.dll` | 48,295,416 B / x64 | **Confirmed:** JavaScriptCore C API symbols; **Strong inference:** web engine/JavaScript component |
| `MumbleLink.dll` | 19,968 B / x64 | **Unknown:** detailed implementation not traced in this scope |
| `webp-imageio64.dll` | 919,045 B / x64 | **Unknown:** detailed decoder/JNI algorithm not traced |
| `webp-imageio32.dll` | 753,368 B / **x86** | **Confirmed:** Machine `0x014c` at file offset `0x84`; **Unknown:** whether any owned launch uses it |

Source for each table row: that image's record in the PE snapshot, except WebP32's separate verification. Class/method/JVM offset: N/A for PE metadata. **Correction:** “all natives are x64” is true only for the six-image saved snapshot, not both WebP filenames on disk. WebP32 SHA-256 is `04d9da8790fe6ef5d9fc006381b23574ceea85c3178eac1e364c7d40e76aa114`; the other hashes remain unchanged in the existing snapshot.

**Confirmed.** `Ultralight.dll` embeds `Ultralight/1.4.0` in its user-agent string at file offset `0x711ab` and `1.4.0` at `0x711e5`, together with `AppleWebKit/615.1.18.100.1` and `Version/16.4.1`. Retained in [native-signatures-session3-verification.json](native-signatures-session3-verification.json). **Strong inference:** this engine distribution identifies as Ultralight 1.4.0; it is not an independent VERSIONINFO result for every component or evidence that Safari itself is embedded.

## 2. Binding imports and the rendering path (FS-13, JV-53)

**Confirmed.** The binding's 58 JNI exports cover Browser, NativeFuture, PlatformInterface, PromiseJS, Session, WebEngine/WebOSR and image wrappers. Selected entry names include `WebOSR_createEngine`, `WebEngine_invokeIteration0`, `Browser_getTexture`, `Browser_bindFunction`, and `PlatformInterface_setScrollCallback`. Source: `native-pe-session3.json`, WebOSR-Binding export table; native code address/JVM offset N/A, export names—not analyzed function bodies.

**Confirmed.** Its normal PE imports include:

| Dependency | Retained imported symbols / families | Evidence boundary |
|---|---|---|
| `jvm.dll` | `JNI_GetCreatedJavaVMs` | Import table, not proof of thread attach/detach policy |
| `Ultralight.dll` | `Renderer::Create`, ViewListener, LoadListener, NetworkListener, KeyEvent | Demangled interpretations of the retained C++ symbol names |
| `UltralightCore.dll` | Bitmap, Surface, `GetBitmapSurfaceFactory`, Platform and associated destruction/string APIs | The snapshot attributes FileSystem/Clipboard/Logger constructors to WebCore and destructors to Core; do not collapse DLL attribution |
| `WebCore.dll` | `JSValue*`, `JSObjectMakeFunctionWithCallback`, `JSObjectMakeDeferredPromise`, property/function/context/string operations, `JSEvaluateScript` | JavaScriptCore C API imports; marshalling algorithms untraced |
| `DWrite.dll` | DirectWrite API dependency | No text-rendering implementation inferred from presence alone |
| `USER32.dll` | `SetCursor`, `GetWindowLongPtrA`, `SetWindowLongPtrA`, `CallWindowProcA` | **Strong inference:** window-procedure subclassing is used for cursor/scroll integration; native call sequence not decompiled |

Source: WebOSR-Binding record, `imports` object. These are PE metadata claims; no JVM bytecode offset exists.

**Confirmed, bounded negative.** No OpenGL DLL/API appears in that retained normal import table. **Unknown:** dynamic loading, resolved function pointers, or graphics used by other components are not excluded by this observation.

**Confirmed.** Java browser configuration explicitly sets `BrowserConfig.accelerated=false`: `lunar.jar`, `L._81676d._21aca6._21aca6._cfe983._cfe983(int,int,double,Browser.Listener) @9–12`. Its engine config installs the Java texture handler in `_16aefb @15–22`. The handler `L._81676d._21aca6._590f69._cfe983._cfe983` allocates RGBA8 textures and calls `bridge$uploadBgra` on upload (JV-30; exact methods in the bytecode appendix).

**Strong inference.** The nonaccelerated view and Bitmap/Surface imports produce CPU-backed pixels that Java uploads through TextureHandler and composites as the existing fullscreen quad (JV-30/31). This strengthens but does not turn the unobserved native callback path, dirty-rectangle cadence or native thread model into Confirmed behavior. See [rendering-and-hud.md §5](rendering-and-hud.md#5-textures).

## 3. Signatures and resources (FS-14)

**Confirmed.** Windows `Get-AuthenticodeSignature` reports `Valid`, signer CN **Moonsworth, LLC**, for WebOSR-Binding, Ultralight, UltralightCore and WebCore. It reports `NotSigned` for MumbleLink and both WebP imageio files. Results are recorded separately in `native-signatures-session3-verification.json`; this is static signature metadata, not analysis of Lunar's integrity mechanisms or a safety conclusion.

**Confirmed, search-bound.** The saved PE parser records `pdb:null` for the six snapshot images; no PDB path was found by that parser. That does not prove symbols cannot exist separately. Source: each `native-pe-session3.json` record, metadata/JVM offset N/A.

**Confirmed.** The four WebOSR/Ultralight images each have one resource of type 24 (manifest), name 2, language 1033, and no VERSIONINFO resource in their complete resource trees. REA portable resource inspection requires no configured Ghidra and did not load these libraries. Full inline records and limitations are preserved in [rea-evidence-session3.json](rea-evidence-session3.json).

| Image | REA Evidence ID | Manifest payload file offset / bytes |
|---|---|---|
| WebOSR-Binding | `ev_1754d1892de23136481a3896993038130ace56740dd41b5f11c0f502fb1b7a0e` | 552032 / 381 |
| Ultralight | `ev_99d6f9e19db301702248dd3d31a16c69fc358a0fafc95f4f0d894aebddcb626a` | 598624 / 323 |
| UltralightCore | `ev_db8a8cff158fc7524fa171d357c3aa138aae3e21100d0b39942d19cd8aeb1a29` | 2481248 / 323 |
| WebCore | `ev_0ef9f04a55e935408a7dd6cdd3d1c14a23adaaf975ea4ca520d68be5bdc72bf7` | 47837280 / 323 |

For resource claims, class/method/bytecode offset is N/A. Resource coverage is complete within REA's bounded parser; manifest contents remain opaque in its result.

## 4. JNI declaration/export mismatch (JV-54)

**Confirmed.** A fresh `javap -p -c` static read of all extracted `com.moonsworth.webosr` classes reproduces **56 Java native declarations versus 58 DLL exports**, with 55 expected JNI names shared. [session3-tools/verify-jni.py](session3-tools/verify-jni.py) records the full declarations in [webosr-native-declarations.javap.txt](webosr-native-declarations.javap.txt) and the comparison in `native-jni-session3-verification.json`.

| Side only | Declaration / export | Classification |
|---|---|---|
| Java | `com.moonsworth.webosr.wrappers.Session.name()` → expected `Java_com_moonsworth_webosr_wrappers_Session_name` | **Confirmed:** declaration has `native`, no Code attribute, offset N/A; expected name absent from binding exports |
| DLL | `Java_com_moonsworth_webosr_wrappers_Session_getName` | **Confirmed:** no matching Java `Session.getName()` declaration in this inspected package |
| DLL | `Java_com_moonsworth_webosr_wrappers_Browser_swapBuffers` | **Confirmed:** no matching Browser declaration |
| DLL | `Java_com_moonsworth_webosr_wrappers_WebEngine_setTimers` | **Confirmed:** no matching WebEngine declaration |

**Strong inference.** This is Java/native version skew. Calling `Session.name()` using ordinary JNI name-based resolution against this DLL would produce `UnsatisfiedLinkError`. **Unknown:** alternate `RegisterNatives` registration or another loaded library could supply that method; the native bodies have not been decompiled and no call was made. Therefore the unconditional runtime error must not be presented as observed or fully proven.

**Confirmed partial Java thread evidence.** `WebEngine.<init>(long) @5–9` records `Thread.currentThread()` as owner; `invokeIteration @0–20` drains `FunctionBus.consumeMainActorQueue` only on that owner thread, then calls `invokeIteration0` regardless. This narrows the Java-side behavior but does not establish Ultralight's native worker/thread or paint model.

## 5. UI FPS throttle is identified (JV-55)

**Confirmed.** In `lunar.jar`, performance settings `L._02d7ad._1253fc._1253fc._bb4487.<init>` declare:

| Setting | Constructor default / allowed range | Offsets |
|---|---|---|
| `menuFpsLimit` | 120 / 30–500 | `@359–390` |
| `limitFps` | 30 / 15–300 | `@325–356` |
| `shouldLimitUnfocusedFps` | true | `@303–322` |

These are code defaults, not user's settings values. `_eeb804 @0–4` returns the `menuFpsLimit` setting (`_05d444`). GameUI `L._81676d._21aca6._21aca6.<init> @392–412` registers its setting listener; the callback target is `_bb4487(Integer)` (bytecode appendix contains class methods; [webosr-fps-listener-binding.json](webosr-fps-listener-binding.json) retains BootstrapMethods #1 and its callsite at 404).

**Confirmed.** `_bb4487(Integer) @0–62` optionally substitutes Minecraft's frame-rate limit under the REWIND-related predicate (`@0–31`), then calls:

```text
WebEngine.setFPS(max(67, min(argument.shortValue(), 240)))
```

The constants 67 and 240 are at `@32` and `@38`, with the call at `@59`. **Correction:** the UI setting's 30–500 range does not mean the engine always receives that same number. **Unknown:** actual observed FPS, the complete native meaning of `setFPS`, and all REWIND predicate conditions remain untraced here.

**Confirmed.** Separately, the blitter `L._81676d._21aca6._21aca6._cfe983._21aca6._cfe983(DrawContext,float,float,resolution) @11–51` reads the same `_eeb804()` setting and tests elapsed milliseconds against `1000.0/menuFpsLimit` before refreshing from `Browser.getTexture @54–61`. Thus the previously Tentative redraw-throttle setting identity is resolved. Engine pumping still has the previously traced ≥5 ms gate (JV-32), which is not identical to the blitter refresh cap or proof of native paint scheduling.

## 6. Ghidra checklist — proposal only

**Confirmed recorded tooling state.** [provider-availability.json](provider-availability.json) reports Ghidra unavailable because `GHIDRA_INSTALL_DIR` is not set, while its Java check accepts the preinstalled Microsoft JDK 21.0.10. Source: `providers[ghidra].availability.diagnostics.checks`, metadata/class/method/bytecode offset N/A. This continuation reused that diagnosis rather than installing or repairing anything.

The following are **proposed actions, not findings and not performed**. Installation/configuration needs user approval:

1. Install/extract Ghidra **12.1.x** at a chosen location.
2. Set `GHIDRA_INSTALL_DIR` in the **REA MCP server's environment**.
3. Restart REA, check `binary_session` provider/tool availability and the JDK result.
4. Use `open_binary` on the explicit `WebOSR-Binding.dll` path in a new analysis workspace; leave install artifacts unchanged.
5. Trace `WebOSR_createEngine`, `WebEngine_invokeIteration0`, `Browser_getTexture`, `Browser_bindFunction`, and `PlatformInterface_setScrollCallback` into the imported Ultralight/JSC calls.
6. Record address-based citations and retained REA Evidence for each result; close the analysis session afterward.

**Unknown questions for that authorized static pass:** native engine thread model, paint/dirty-rectangle cadence, the complete TextureHandler callback path, JS↔Java value/string/promise marshalling, and possible alternate JNI registration relevant to `Session.name()`. Native tooling may answer some; runtime-only claims still require separate approval.

**Unknown runtime-only items:** the actual `POST /launch` response and chosen `mainClass`, and live stdout-marker/IPC ordering. Nothing in this native metadata pass establishes them. See [unresolved-implementation.md](unresolved-implementation.md).
