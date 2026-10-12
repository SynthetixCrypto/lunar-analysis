# JNI attachment, references and exceptions

**Result: partially resolved.** The attachment ABI and callback/reference paths are verified. Full Environment ownership and all detach/thread-exit paths remain unknown.

Target and evidence: [index](evidence-index.md); [prior JNI reconciliation](../session7-astra/native-jni-mapping.md). Native addresses refer to the binding DLL.

## Attachment and Environment acquisition

Fresh `env-attach-assembly` establishes that `0x180001f60` loads JavaVM slot `+0x38` and calls it with an output `JNIEnv*` pointer and null attachment arguments. Against the independently enumerated JDK JNI table, this is **AttachCurrentThreadAsDaemon**, not `GetEnv` or `DetachCurrentThread`.

On success it allocates `0x58` bytes for an Environment wrapper, transfers a cleanup callable and stores the acquired environment at `+0x50` (`environment-actual-ctor`, `0x1800014c0`). `jni-env-access` (`0x1800021d0`) is just that field accessor. An attach failure constructs and throws a native exception. The inspected attach body itself has no per-thread cache lookup before allocation.

The cleanup callable's invoke entry `0x180001cf0` was verified in Session 7 as a no-op. Releasing that callable is not evidence of JVM detachment. Fresh `vm-actual-ctor`, `vm-refcount-release` and `vm-environment-map-release` trace a VM-owned container and shared-reference disposal, but do not establish where every Environment is inserted, destroyed or detached. The earlier speculative `vm-ctor`/`vm-release` record names referred to generic callable/vector helpers; their actual contents are classified in the index.

**Verified / high:** daemon attachment, allocation, field ownership transfer and accessor. **Unknown:** complete Environment owner graph, caching outside this helper, all TLS/thread-exit hooks and balanced detachment for native-created threads. No global “never detaches” or memory-leak claim follows from this bounded trace.

## Reference ownership and callbacks

| Boundary | Verified contract | Evidence |
|---|---|---|
| Java objects retained past JNI entry | Global-reference creation and deleter wrapper exist | Session 7 `jni-refs-global`, reference lambda tables |
| Global release | Fresh `0x180001a60` obtains an Environment then invokes JNI table `+0xb0` = `DeleteGlobalRef` | S8 `global-delete-helper` |
| Pixel callback buffer | `NewDirectByteBuffer` wraps native memory; synchronous `CallVoidMethodA`; local reference then deleted | Session 7 `upload-call-assembly`, `jni-upload`; binding `0x18002d910` |
| Delete callback | Uses acquired environment and `(I)V` argument array; calls exception checker | S8 `jni-delete-asm`, `0x18002d630` |
| Reverse update | Copies bytes before actor dispatch; does not retain the Java direct-buffer object for later worker reads | S8 `source-update-asm`; Session 7 input JNI trace |

`JNIEnv*` is thread-associated by the JNI contract. Calling the acquisition helper on the current callback thread is consistent with that contract; no permission to move an Environment to another thread is established. The Java upload callback must not retain the borrowed pixel buffer beyond the synchronous call.

## Exception behavior

`0x1800020e0` checks for a pending Java exception and describes/clears it on the inspected callback path. Thus a thrown Java upload/delete exception is not automatically delivered as a structured failure to a waiting worker. Fresh create/delete assembly confirms this checker is used on those callbacks as well. It does not imply that all JNI exports share the same policy, nor that every native C++ exception is translated to a Java exception.

Failed attachment throws before a usable Environment is returned. Failed callback lookup, allocation failures, worker exceptions and shutdown with references outstanding require broader unwind evidence. Their practical frequency was not measured.

## Development consequence

The independent MVP has no JNI component, so these remaining questions do not block implementation. If native integration is later justified, independently specify thread-owned environments, attach-only-if-needed ownership, detach on owned native-thread exit, explicit global/local reference wrappers and callback failure propagation. Do not reuse the observed no-op cleanup as a desired design.
