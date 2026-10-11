# Session 4 — WebOSR interfaces and bounded native rendering analysis

## Scope and evidence

Static inspection only. No DLL loading, target execution, tooling installation or runtime attach. **Confirmed** means what the shipped bytes/bytecode implement, not an observed runtime result. **Strong inference** describes consequences conditional on those paths running; **Unknown** marks native internals not recovered.

New evidence: [PE export addresses/raw bytes](evidence-native/binding-pe-addresses.json), [full JVM class map](evidence-native/class-map.json), fresh verbose `javap` for five wrapper classes, and [REA availability result](evidence-native/rea-provider-status.json). Reproduce with `python native-static.py`; it reads the DLL and retained class cache and executes only the JDK disassembler. All generated evidence remains in this directory.

Artifact: `C:\Users\Admin\.lunarclient\offline\multiver\natives\WebOSR-Binding.dll`, SHA-256 `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf` — matches session 3. JVM artifact is `lunar.jar`; original obfuscated class identities are in the mapping above. Bytecode offsets below are decimal and method-local; PE offsets/RVAs are hexadecimal.

REA successfully opened and identified the x64 PE without executing it. Its only advertised deep provider, Ghidra, is **unavailable / not_configured** (`GHIDRA_INSTALL_DIR` unset). Target support is separate and reported supported. No Ghidra setup was attempted. `rea-evidence-session4.json` is a retained export of the **four inherited session-3 PE-resource records**, not four new native analyses; no fabricated REA ID is assigned to our Python/manual evidence.

## 1. The 56/58 discrepancy: concrete entry points, not a resolved failure

**Confirmed — S4-NATIVE-01.** The fresh PE export reader records actual code destinations for the previously identified DLL-only names. They are not export-directory forwarders:

| Export suffix | Entry RVA | File offset | `.pdata` end RVA (exclusive) |
|---|---:|---:|---:|
| `Browser_swapBuffers` | `0x1fc10` | `0x1f010` | `0x1fc37` |
| `Session_getName` | `0x29690` | `0x28a90` | `0x29868` |
| `WebEngine_setTimers` | `0x1c400` | `0x1b800` | `0x1c471` |
| `WebEngine_invokeIteration0` | `0x1c3b0` | `0x1b7b0` | `0x1c3cb` |
| `WebOSR_createEngine` | `0x10a30` | `0xfe30` | `0x11132` |

Full symbols begin `Java_com_moonsworth_webosr_wrappers_`. These ranges are Windows RUNTIME_FUNCTION entries, **not** proof of complete semantic body extent. The reader retains all 58 export destinations and matching unwind-table records.

**Confirmed, bounded negative.** The complete named export table has no `JNI_OnLoad`, `JNI_OnUnload` or `Java_com_moonsworth_webosr_wrappers_Session_name`. Java `Session.name()` remains native (Code offset **N/A**; declaration in retained wrapper dump). This narrows ordinary JNI name lookup; it does **not** rule out registration performed by a different function/library, a non-exported JNI-table call or an unexamined call site. **Strong inference:** wrapper/binding version skew remains plausible. **Unknown:** actual `UnsatisfiedLinkError`, whether `name()` is called, and alternate native registration. Session 3’s caution is retained, not upgraded to an observed defect.

## 2. One small native stub can be decoded without claiming a native architecture

**Confirmed — S4-NATIVE-02, analyst manual instruction decode.** The export `WebEngine_invokeIteration0` has these exact 27 bytes, wholly inside its RUNTIME_FUNCTION range:

```text
RVA       bytes                 x64 instruction
0x1c3b0   48 83 ec 28            sub rsp,0x28
0x1c3b4   e8 07 d6 ff ff         call 0x199c0
0x1c3b9   48 8b 88 e8 00 00 00  mov rcx,[rax+0xe8]
0x1c3c0   48 8b 01               mov rax,[rcx]
0x1c3c3   48 83 c4 28            add rsp,0x28
0x1c3c7   48 ff 60 08            jmp qword ptr [rax+0x8]
```

Source: PE file offsets `0x1b7b0–0x1b7ca`; exact hex is retained in the export row. The relative call target is calculated from the signed displacement plus next-instruction RVA. **Strong inference:** this is a forwarding stub with a tail dispatch through an object/vtable, rather than the implementation of the iteration algorithm. **Unknown:** semantics of helper `0x199c0`, pointee at `+0xe8`, virtual slot `+8`, scheduling, locking, paint cadence and callback thread. Do not assign these to Ultralight `Render()`/`Update()` by name alone.

## 3. Java iteration ownership is a queue gate, not a thread rejection

**Confirmed — S4-NATIVE-03.** `com.moonsworth.webosr.wrappers.WebEngine.<init>(long) @5–9` records `Thread.currentThread()` in final `owner`. `invokeIteration() @0–13` drains `FunctionBus.consumeMainActorQueue()` only when current thread equals owner. Regardless of the comparison, `@16–17` calls native `invokeIteration0()`. Thus the Java wrapper does **not** throw for a foreign thread, and does **not** skip native iteration on it. Native-side restrictions remain **Unknown**.

**Confirmed.** `FunctionBus` owns a **static shared** `ArrayBlockingQueue<Runnable>` of capacity **4096** (`<clinit> @0–10`). Its maps of children/routines/cache are `ConcurrentHashMap`s (`<init> @4–34`). `consumeMainActorQueue @0–20` polls and runs until empty; it has no per-runnable catch in that method.

**Strong inference:** independent engines share this Java queue; an owner-thread iteration of one engine can drain queued callbacks originating from another. An exception from one task aborts that drain invocation before native iteration in the wrapper; unpolled tasks remain queued. This follows the direct uncaught call chain, not a runtime measurement. Multi-engine native ownership and external callers’ handling remain **Unknown**.

## 4. JS callback dispatch and conversion are recoverable on the Java side

**Confirmed — S4-NATIVE-04.** `FunctionBus.subscribe(Object)` inspects public methods (`getMethods @105–106`), requires `@CallbackJS @133–150`, unreflects methods `@183–190`, and registers annotation-named routines `@335–423`. Static callbacks can register via a `Class`; instance callbacks without an instance are skipped `@153–180`. The `async` annotation value is captured `@351–358`.

`FunctionBus.invoke(PromiseJS,Browser,String,String[])`:

- `@7–42`: a first JS argument that names an existing child/routine becomes an explicit target and is removed from arguments (`isExplicitTarget @0–31`).
- `@44–76`: delegate to a child first; `@77–98`: return silently for an unknown routine. No promise rejection appears in that branch.
- `@99–127`: build parameters; argument errors become `RuntimeException`.
- `@128–171`: **async=true executes the MethodHandle immediately on the calling thread** and completes its promise; it does not start an executor/thread.
- `@172–189`: **async=false queues a runnable via `add`, not blocking `put` or checked `offer`**. Queue-full handling is absent here.

**Strong inference:** queue saturation can surface `IllegalStateException` under ordinary `ArrayBlockingQueue.add` semantics. Unknown-target calls can leave a promise without Java-side completion. Native rejection/exception translation is **Unknown**; the Java body does not establish it.

**Confirmed.** `buildInvocationParameters @0–70` checks required argument count and permits extras only with a `String[]` parameter. It injects instance `@101–119`, Browser `@158–174`, PromiseJS `@177–193`, remaining-string array `@196–225`, and converted scalars `@229–247`. Multiple PromiseJS parameters are rejected during subscription `@275–296`.

Primitive/boxed conversions, enum `toString` case-insensitive matching and UUID parsing are explicit (`stringToObject @0–290`; reverse `objectToString @0–248`). Lunar’s subclass `L._81676d._21aca6._590f69._cfe983.stringToObject @0–19` additionally maps literal `"null"` and `"undefined"` to Java null; on base conversion exception it falls back to Gson `@27–36`. Reverse conversion falls back to Gson `objectToString @7–15`. No browser/JS code was executed to test coercion parity.

**Confirmed — important caveat.** Subscription’s `promiseValueType` capture uses `Parameter.getParameterizedType().getClass()` (`subscribe @300–308`), not extraction of the generic value argument. `buildInvocationParameters @257–273` binds that captured class to a supplied promise. Exact generic codec behavior is **Unknown** and must not be described as correctly recovering `PromiseJS<T>`’s T.

`completePromiseIfNeeded @0–7` leaves completion to routines that take PromiseJS; otherwise it handles void, null and converted return values `@8–53`. Both immediate and queued callback failures are wrapped as RuntimeException (`invoke @160–171`; `lambda$invoke$0 @21–32`) with no Java promise-reject call on those paths. Fresh verbose evidence binds BootstrapMethods #0 to `lambda$invoke$0`.

## 5. Native object lifetime and future semantics have narrow guarantees

**Confirmed — S4-NATIVE-05.** `NativeHandle.handle` is a plain private long. `close @0–18` checks nonzero, calls virtual native destroy, then writes zero. No synchronized modifier, monitor or CAS appears. Sequential successful closes avoid repeated destroy; if destroy throws, the zero write is not reached. **Unknown:** concurrent-close safety, native validation after close, Cleaner/finalizer behavior outside this class and allocation ownership.

`PromiseJS.handle` is **volatile**, but resolve/reject use check-then-call-then-zero rather than atomic arbitration: `_resolve @0–33`, `resolve() @0–32`, `reject(String) @0–33`, `reject() @0–32`. A later successful completion attempt throws `"Future already completed"`; this is not a JVM guarantee against two racing completions. Codec references clear after successful native completion (`clearBridgeCodec @0–10`). Native concurrency protection is **Unknown**.

`NativeFuture.get(long,TimeUnit) @0–9` converts the duration to nanoseconds and delegates to `get0(long)`; no-argument `get @0–5` passes zero. Both `cancel(boolean)` and `isCancelled @0–7` throw `UnsupportedOperationException`. **Unknown:** meaning of native zero timeout, waiting/timeout/error implementation, exception delivery and cancellation outside these wrappers. This Future is unrelated to game-IPC RpcChannel futures.

## 6. Rendering ABI: what crosses the Java boundary

**Confirmed — S4-NATIVE-06.** `TextureHandler` declares create, resize, upload, read and delete; descriptors/Code offsets **N/A** for abstract methods. Lunar implementation `L._81676d._21aca6._590f69._cfe983._cfe983`:

| Method | Actual bytecode behavior |
|---|---|
| `<init> @4–17` | Plain HashMap; integer logical ID starts at 1. |
| `createTexture @0–88` | Registers `webosr` texture resource, inserts next logical ID, allocates RGBA8 and returns logical ID; **not demonstrated to return a GL object name**. Third argument is unused. |
| `resizeTexture @0–34` | Looks up logical ID, reallocates RGBA8 width/height; fourth argument unused. |
| `uploadTexture @0–49` | Returns if width or height arguments are zero; looks up ID and forwards x/y/width/height/buffer/x/y/final stride-like argument to `bridge$uploadBgra`. Last argument’s actual native unit/meaning remains Unknown here. |
| `readTexture @0–7` | Always throws UnsupportedOperationException. |
| `deleteTexture @0–23` | Removes ID and invokes bridge release; no missing-ID null guard. |

**Confirmed.** Browser factory `L._81676d._21aca6._21aca6._cfe983._cfe983(int,int,double,Listener) @9–43` selects nonaccelerated, transparent browser with supplied dimensions/scale/listener, then `@46–64` creates it and binds `lunarInternalInvoke` to FunctionBus. Engine config `_16aefb @15–22` installs the Java texture handler. This corroborates earlier reports; it does not independently recover native paint-to-upload calls.

**Confirmed native bytes / Strong inference relationship.** The DLL contains `com/moonsworth/webosr/TextureHandler` at file offset `0x5d4e0`, callback names `createTexture`, `resizeTexture`, `uploadTexture`, `readTexture`, `deleteTexture` at `0x5e878`, `0x5e888`, `0x5e898`, `0x5e8a8`, `0x5e8b8`; RTTI name `JniTextureHandler@binding@webosr` at `0x7ff80`; and `TextureSourceImpl::update size mismatch: got {} bytes, expected {} ({}x{} BGRA8)` at `0x604a0`. These corroborate a JNI texture-handler/BGRA pathway but are **not** a recovered call graph or measured upload format. The direct Java `bridge$uploadBgra` call is stronger evidence than the string alone.

Browser$Listener contains default no-op load/document/history/title/URL/tooltip/close callbacks and child creation returning the supplied Browser; cursor integer overload translates `Mouse.Cursor.fromValue` (`onCursorChange(Browser,int) @0–11`). The DLL stores those names in file range `0x5dd40–0x5de4f`; native descriptor lookups, actual callback threads, pixel callbacks and teardown sequence remain **Unknown**. No paint callback is declared on this Listener; pixel transfer is represented separately by TextureHandler.

## 7. What should be investigated next

1. With explicit approval to configure a static native engine, follow `WebOSR_createEngine @RVA 0x10a30`, iteration helper `0x199c0`/virtual slot, texture-handler callbacks and PromiseJS completion lambdas. Recover JNI method/field lookup descriptors and exception conversion before asserting ABI compatibility.
2. Resolve whether `Session.name()` has alternate registration or actual callers. Export presence alone neither resolves compatibility nor demonstrates failure.
3. Trace native EngineImpl update/render/timers, buffer ownership/dirty rectangles, stride units and destroy order. Java owner queue gating does not establish a native single-thread architecture.
4. Runtime paint cadence, foreign-thread behavior, shutdown races and exception effects require separate approval; none were tested.

**Status:** Java-side wrapper/dispatch/lifetime contracts materially advanced; native PE entry mapping and one forwarding stub recovered; **native implementation architecture still partial** because no deep provider is configured.
