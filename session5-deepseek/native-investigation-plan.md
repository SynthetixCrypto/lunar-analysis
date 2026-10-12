# Native investigation plan — next stage

Date: 2026-10-11. Session 5 (Deepseek). Planning only. **No native tooling was installed, configured, downloaded or executed in this session or any prior session.** No Lunar binary was loaded or run. Every action below is a *proposal* requiring separate, explicit owner approval before it is attempted.

This file reviews `native-analysis-preparation.md` (session 3) and `session4-sol/native-rendering.md` (session 4) and defines exactly what a Ghidra-assisted pass should investigate next.

## 1. Why this stage is not yet done

Independently re-observed this session via `rea.binary_session`:

| Provider | Status | Reason |
|---|---|---|
| Ghidra | **unavailable / `not_configured`** | `GHIDRA_INSTALL_DIR` unset; `analyzeHeadless` missing; matching win32/x64 native decompiler missing |
| Hopper | unavailable / `unsupported_host` | Hopper integration is macOS-only; host is win32 |
| IDA | unavailable / `not_configured` | `REA_IDA_MCP_CONFIG` unset |

**Tool anomaly (new this session):** the live probe reports the REA server's Ghidra candidate `java_home = C:\Program Files\Java\jre1.8.0_461` (`unsupported_version`), whereas `provider-availability.json` (session 3) recorded `java_home = C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot` (accepted). See [contradictions.md](contradictions.md) C-6. Either way Ghidra stays unavailable because the install dir is unset. **Pin both `GHIDRA_INSTALL_DIR` and `JAVA_HOME` before any attempt.**

**Boundary:** Java-side bytecode work continues to be doable with the standalone JDK 21 `javap` (as used in this session). Only *native* decompilation is blocked.

## 2. Target inventory (from sessions 3–4, re-checked)

Artifacts under `C:\Users\Admin\.lunarclient\offline\multiver\natives` (read-only):

| DLL | Size | Arch | Role (labelled) |
|---|---:|---|---|
| `WebOSR-Binding.dll` | 565,752 | x64 | **Primary JNI glue target.** 58 `Java_com_moonsworth_webosr_wrappers_*` exports |
| `Ultralight.dll` | 613,880 | x64 | engine facade (Strong inference) |
| `UltralightCore.dll` | 2,503,672 | x64 | engine core / Bitmap+Surface (Strong inference) |
| `WebCore.dll` | 48,295,416 | x64 | JavaScriptCore C API host (Strong inference) |
| `MumbleLink.dll` | 19,968 | x64 | unknown in scope |
| `webp-imageio64.dll` | 919,045 | x64 | WebP decoder |
| `webp-imageio32.dll` | 753,368 | **x86** (Machine `0x014c` @ file `0x84`) | WebP decoder (32-bit) |

Primary target SHA-256 (unchanged, matches session 3): `WebOSR-Binding.dll` = `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf`.

Dependencies seen in the binding import table (sessions 3–4): `jvm.dll` (`JNI_GetCreatedJavaVMs`), `Ultralight.dll` (Renderer/ViewListener/LoadListener/NetworkListener/KeyEvent), `UltralightCore.dll` (Bitmap/Surface/GetBitmapSurfaceFactory), `WebCore.dll` (JSValue*/JSObjectMakeFunctionWithCallback/JSObjectMakeDeferredPromise/JSEvaluateScript), `DWrite.dll`, `USER32.dll` (`SetWindowLongPtrA`/`CallWindowProcA` → window subclassing). **No OpenGL import** in the retained normal table (bounded negative).

## 3. Exact entry points to trace

Session 4 recovered these as real code destinations (reproduced this session — see [verification-audit.md](verification-audit.md) §finding 7). These are the seeds, not conclusions:

| Export | RVA | File offset | Note |
|---|---:|---:|---|
| `WebOSR_createEngine` | `0x10A30` | `0x0FE30` | engine construction; primary seed |
| `WebEngine_invokeIteration0` | `0x1C3B0` | `0x1B7B0` | 27-byte forwarding stub: `sub rsp,0x28; call 0x199C0; mov rcx,[rax+0xE8]; mov rax,[rcx]; jmp qword ptr [rax+0x8]` |
| `WebEngine_setTimers` | `0x1C400` | `0x1B800` | timer installation |
| `Browser_swapBuffers` | `0x1FC10` | `0x1F010` | present/swap |
| `Session_getName` | `0x29690` | `0x28A90` | paired with the Java `Session.name()` skew question |

Internal helper to resolve: **`0x199C0`** (called by the iteration stub) and the virtual slot at object offset `+0xE8` → vtable `+0x8`.

## 4. Questions the Ghidra pass must answer (grouped)

### 4.1 Native paint callback and frame production
1. What does `0x199C0` return, and what is the object at `[rax+0xE8]`?
2. Which vtable slot (`+0x8` of that object) is dispatched, and what does the callee do (update? render? paint?)?
3. Where is the frame produced — does the engine call back into Java `TextureHandler.createTexture/uploadTexture`, or does Java pull via `Browser.getTexture`?
4. Is there a distinct "paint" callback, or only the TextureHandler pixel-transfer path?

### 4.2 Frame-buffer ownership
5. Who allocates and owns the bitmap/surface (UltralightCore `Bitmap`/`Surface` vs. a Java-side `RGBA8` allocation)?
6. What is the lifetime of the surface relative to the engine and to the Java texture ID?
7. Confirm the pixel format/stride units implied by `TextureSourceImpl::update size mismatch … ({}x{} BGRA8)` (string @ file `0x604A0`) and match them to the Java `uploadTexture` argument list.

### 4.3 Thread synchronization
8. On which thread does `invokeIteration0`'s dispatched callee run? Does the binding create worker threads, or is everything owner-thread driven?
9. What synchronisation (mutex/atomic) guards the engine update vs. the Java owner-thread queue drain?
10. Does the native side enforce a thread affinity the Java wrapper does *not* (the Java wrapper calls native iteration unconditionally)?

### 4.4 Texture upload behavior
11. Trace the JNI callback into `com/moonsworth/webosr/TextureHandler` (names at file `0x5E878…0x5E8B8`; RTTI `JniTextureHandler@binding@webosr` @ `0x7FF80`).
12. Does the native side call `createTexture/resizeTexture/uploadTexture/deleteTexture`, or are those Java-called-from-Java only?
13. Determine whether uploads are dirty-rect region-based (the Java side forwards x/y/width/height + a stride-like arg to `bridge$uploadBgra`).

### 4.5 Resource cleanup
14. What does engine destruction / `WebOSR_destroy…` do: surface release order, callback unregistration, thread joins?
15. Does `Session.name()`'s missing export imply a `RegisterNatives` call somewhere in the binding (search for `RegisterNatives`/`FindClass`/`GetMethodID` descriptors)?
16. Are `Browser_swapBuffers` / `WebEngine_setTimers` (DLL-only, no Java declaration) dead code, legacy, or registered by name externally?

## 5. Proposed execution plan (approval-gated)

Each step is static; none executes Lunar code.

| Step | Action | Approval needed |
|---|---|---|
| N-0 | Decide host for Ghidra (Windows native Ghidra 12.1.x + JDK 21, **or** a Linux analysis host). Record the decision | Owner |
| N-1 | Install/extract Ghidra 12.1.x at a chosen path (no target execution) | Owner |
| N-2 | Set `GHIDRA_INSTALL_DIR` **and** `JAVA_HOME` in the REA MCP server environment; restart REA | Owner |
| N-3 | Re-probe `rea.binary_session`; confirm a deep provider is `available` and record the diagnostics | — |
| N-4 | `open_binary` on the exact `WebOSR-Binding.dll` path; do not modify install files | — |
| N-5 | Resolve and analyze `WebOSR_createEngine` (`0x10A30`) → `0x199C0` → vtable slot; export an Evidence bundle | — |
| N-6 | Analyze the TextureHandler JNI callbacks; reconcile with Java `uploadTexture` | — |
| N-7 | Analyze `Session_getName` and search for `RegisterNatives`/`FindClass` | — |
| N-8 | Record address-based citations + REA Evidence IDs; `close_binary` with a snapshot | — |

**Acceptance criteria.** Each question in §4 is answered with an address-based citation (and REA Evidence where the provider returns it), or explicitly marked Unknown with the reason. A forwarding stub or an unnamed vtable slot may **not** be renamed to "Render()" without observing the callee.

## 6. What remains runtime-only (separate approval)

Even with a full static native pass, these cannot be answered statically and need a separately authorized, credential-free live observation:

- Actual native paint cadence and callback thread at runtime.
- Queue-full behavior under real load (`FunctionBus` `ArrayBlockingQueue.add`).
- Real close/error races and IPC ordering.
- FPS/startup performance parity (ME-17).

None of these were performed; none is authorized.

## 7. Cheaper Java-side alternative that advances the same boundary (no approval)

If native tooling stays unavailable, the following Java-side work is doable now with `javap` alone and materially reduces the native unknowns:

- **J-A:** fully trace `L._81676d._21aca6._590f69._cfe983._cfe983` (TextureHandler impl) and its `bridge$uploadBgra` call site arguments → documents the exact Java-side upload contract the native side must match.
- **J-B:** trace `L._81676d._21aca6._21aca6._cfe983._cfe983(int,int,double,Listener)` (browser factory) and `_16aefb` (engine config) → confirms the installed-handler wiring.
- **J-C:** enumerate every `native` declaration in `com.moonsworth.webosr.**` and diff against the retained 58-export table (already 56 vs 58; extend to attribute each of the 2 unaccounted exports).
- **J-D:** statically determine whether any code path can call `Session.name()` (xref its declaration) — narrows whether the skew is live-reachable.

**Recommendation:** do J-A…J-D first (free, static, no approval), then N-0…N-8 only after the owner approves Ghidra setup.

## 8. Explicit non-goals

- No anti-cheat/integrity analysis, no protection bypass, no reimplementation.
- No execution of `WebOSR-Binding.dll`, `Ultralight.dll`, `WebCore.dll`, `MumbleLink.dll` or any Lunar binary.
- No credentials, no account/installation identifiers, no personal data.
- No download or installation without owner approval.
