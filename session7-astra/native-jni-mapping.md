# Session 7 — Native/JNI mapping

All native addresses below refer to `WebOSR-Binding.dll` unless stated otherwise. Static findings are **Verified / high confidence** within the cited functions; unresolved linkage and lifetime conclusions are explicitly marked.

## Independent declaration/export reconciliation

`verify_artifacts.py` parses the PE export directory and Java class constant pools/access flags independently. It does not reuse the prior export list as its authority. The matching set uses ordinary short JNI symbol mangling for the observed declarations; it is an export/declaration comparison, not proof of every runtime binding mechanism.

| Result | Fresh count / symbol |
|---|---|
| Java native declarations under `com/moonsworth/webosr/` in `lunar.jar` | 56 |
| `Java_` exports in binding DLL | 58 |
| Shared short symbols | 55 |
| Java-only | `Java_com_moonsworth_webosr_wrappers_Session_name` |
| DLL-only | `Java_com_moonsworth_webosr_wrappers_Session_getName` |
| DLL-only | `Java_com_moonsworth_webosr_wrappers_Browser_swapBuffers` |
| DLL-only | `Java_com_moonsworth_webosr_wrappers_WebEngine_setTimers` |

Full declarations/descriptors/class hashes: [fresh reconciliation](evidence/jni-reconciliation-fresh.json). Full export locations: [PE identities](evidence/pe-identities.json).

**Verified:** `Session_getName` at `0x180029690` gets a native session pointer, calls session virtual `+8` to obtain string data, then JNI `NewStringUTF` at table offset `0x538`. This is a real string-returning implementation, not an empty compatibility stub. **Unknown:** whether `Session.name()` is dynamically bound to it in any actual launch. See [body](evidence/session-name.json) and [fresh Session bytecode](evidence/com.moonsworth.webosr.wrappers.Session.javap.txt).

`swapBuffers` and `setTimers` also contain working bodies. Absence from this JAR's declarations is insufficient to call them dead, unused or registered aliases.

## ABI verification from the installed JDK header

The 64-bit table offsets were independently enumerated from `jni.h`, including reserved entries, and asserted at key indices. [Complete offsets and header digest](evidence/jni-abi-offsets.json).

| JNIEnv offset | Entry | Used to establish |
|---|---|---|
| `0x80 / 0x88` | `ExceptionDescribe / ExceptionClear` | Callback error handling |
| `0xa8 / 0xb0 / 0xb8` | `NewGlobalRef / DeleteGlobalRef / DeleteLocalRef` | Reference ownership |
| `0xf8` | `GetObjectClass` | Handle lookup setup |
| `0x108` | `GetMethodID` | Texture callback method lookup |
| `0x1f8` | `CallVoidMethodA` | Upload/resize/delete callback invocation |
| `0x2f0 / 0x328` | `GetFieldID / GetLongField` | `NativeHandle.handle:J` |
| `0x338` | `GetDoubleField` | Thread timers |
| `0x538` | `NewStringUTF` | Session name return |
| `0x6b8` | `RegisterNatives` | Bounded registration search |
| `0x720` | `ExceptionCheck` | Callback exception check |
| `0x728 / 0x730 / 0x738` | `NewDirectByteBuffer / GetDirectBufferAddress / GetDirectBufferCapacity` | Both transfer directions |

JavaVM is a different table: `+0x38` is **AttachCurrentThreadAsDaemon**, while `+0x28` is **DetachCurrentThread**. They must not be interpreted using JNIEnv indices.

## Texture callback object and methods

Constructor `0x18002d360` installs `JniTextureHandler` vtable `0x1800602d0`, caches method descriptors/IDs, and retains the supplied object wrapper at handler `+0x80`. The configuration path includes global-reference creation before this constructor. The destructor at `0x18002d470` invokes the retained reference's deleter and releases its associated ownership. Global creation/deletion helpers use JNI `0xa8/0xb0`.

Evidence: [constructor](evidence/jni-texture-ctor.json), [configuration](evidence/binding-config-texture.json), [vtable](evidence/texture-handler-vtable.json), [NewGlobalRef](evidence/jni-refs-global.json), [DeleteGlobalRef](evidence/jni-delete-global-body.json), [destructor](evidence/texture-handler-dtor.json).

| Handler slot | Native target | Java contract |
|---|---|---|
| `+8` | `0x18002d580` | `createTexture(III)I` |
| `+0x10` | `0x18002d840` | `resizeTexture(IIII)V` |
| `+0x18` | `0x18002d910` | `uploadTexture(ILjava/nio/ByteBuffer;IIIII)V` |
| `+0x20` | `0x18002d6c0` | `readTexture(ILjava/nio/ByteBuffer;III)V` |
| `+0x28` | `0x18002d630` | `deleteTexture(I)V` |

The table and fresh [Java interface](evidence/com.moonsworth.webosr.TextureHandler.javap.txt) establish all five contract slots. Create/resize/upload bodies and their supplier callers were followed. The read/delete entries are identified; a complete normal-shutdown caller chain to delete remains **Unknown**.

### Upload: pointer, arguments and exception behavior

At `0x18002d050`, lookup assembly passes method name and descriptor to `GetMethodID` at `0x108`; descriptor builder `0x18002bea0` yields the same signature as Java.

At `0x18002d910`, the native source pointer is wrapped by `NewDirectByteBuffer`; the byte size is passed from a 32-bit native argument. A seven-element `jvalue` argument array carries `texture ID, ByteBuffer, x, y, width, height, byte stride`. Assembly at `0x18002da29–0x18002da3c` supplies the cached method ID, retained Java handler object and array to `CallVoidMethodA`. The original local buffer reference is deleted at `0x18002da5e`.

The pointer remains native-owned. **Inferred / high confidence contract:** consume or copy the bytes synchronously during the callback; holding the Java ByteBuffer object does not extend the native pixel storage's lifetime. The supplier returns that pixel buffer to its reusable pool after the callback path. JNI reference lifetime and backing memory lifetime are separate.

At `0x1800020e0`, `ExceptionCheck` leads to `ExceptionDescribe`, `ExceptionClear`, and stderr logging/flushing. **Verified:** exceptions on this inspected callback-check path are cleared. This is not evidence that every JNI entry catches native C++ exceptions or that application cleanup always succeeds.

Evidence: [lookup assembly](evidence/jni-upload-method-assembly.json), [descriptor](evidence/upload-descriptor.json), [upload body](evidence/jni-upload.json), [upload assembly](evidence/upload-call-assembly.json), [exception checker](evidence/jni-invoke-check.json).

### Reverse image update

`0x180027cd0` reads direct-buffer address and **capacity**, not Java `remaining()`. It forwards only a nonnull address and positive capacity. Correct virtual thunk `0x18004a51c` reaches `0x18004a530`, which allocates native storage and copies the bytes before dispatching actor 0. The worker accepts exactly `width * height * 4` bytes for nonzero dimensions; mismatch logs a BGRA8 size diagnostic.

Evidence: [JNI entry](evidence/image-update-jni.json), [thunk](evidence/texture-source-update-thunk.json), [copy](evidence/image-update-copy.json), [worker validation](evidence/image-upload-work.json). This resolves Java-buffer borrow-versus-copy for this path. Lifetime of the native source object captured by queued work remains a separate question.

## Attachment and registration bounds

`0x180001e60` enumerates created Java VMs and expects one. `0x180001f60` invokes **AttachCurrentThreadAsDaemon** and creates an Environment wrapper. The `attachShared` cleanup callable's invoke slot is `0x180001cf0`, a no-op/guard stub. **Verified:** that callback does not call `DetachCurrentThread`. **Unknown:** complete wrapper disposal, thread-exit handling, and other detach sites. This does not establish a leak.

Evidence: [VM lookup](evidence/java-vm.json), [attachment](evidence/jni-thread-state.json), [callable table](evidence/jni-ref-lambda-tables.json), [invoke body](evidence/jni-detach-task.json).

Registration search was explicitly bounded:

1. Fresh exports and exact ASCII names were searched in the four identified DLLs.
2. Binding `.text` was scanned for little-endian displacement bytes `b8 06 00 00` corresponding to JNIEnv `+0x6b8` in a conventional displacement encoding.
3. Four byte candidates were found. Ghidra resolves them to `MOV EAX,6` at `0x18002fd08` and `0x1800405c0`, and `MOV [RBP-0x48],6` at `0x180043a74` and `0x180043ae2`, not RegisterNatives calls.
4. The binding entry/registry constructor and the directly analyzed JNI paths supplied no alternate `Session.name` registration proof.

Evidence: [bounded scan](evidence/registration-bounded-scan.json), [candidate 1 corrected](evidence/registration-candidate-1-correct.json), [candidate 2](evidence/registration-candidate-2.json), [candidate 3](evidence/registration-candidate-3.json), [candidate 4](evidence/registration-candidate-4.json), [registry constructor](evidence/binding-registry-ctor.json).

**Unknown:** computed table indexing, transformed names, registration from other modules, reflection or launch-dependent linkage. A negative byte/string search is not a whole-program exclusion of dynamic registration. Session 6's separate four-JAR symbolic caller scan remains historical evidence, not a fresh all-JAR scan performed here.
