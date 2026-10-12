# GPU resource lifecycle

**Result: partially resolved.** Creation, resize and the Java deletion implementation are established. An unconditional browser-close → cached supplier ID → deletion callback chain is still unproved. The available evidence establishes neither a GPU leak nor complete leak freedom.

All native addresses here refer to `WebOSR-Binding.dll`, SHA-256 `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf`. Evidence aliases resolve in the [index](evidence-index.md); static conclusions do not describe an observed launch.

## Ownership and normal operations

| Resource | Verified owner / operation | Evidence; confidence |
|---|---|---|
| Three CPU pixel records | Custom surface constructs and destroys three records; these are not OpenGL textures | Session 7 `swapchain-ctor`, `swapchain-dtor`, `pixel-buffer-free`; high |
| Logical texture ID | Supplier caches the Java-returned ID at supplier `+0x180` (surface `+0x198`) | `0x18004bd60`, Session 7 `swapchain-get-texture`; high |
| Graphics texture object | Java TextureHandler maps logical IDs to texture bridge objects and registers texture objects through Minecraft's texture manager | Fresh S8 `java-10`, methods `createTexture`, `deleteTexture`; high for bytecode, selected runtime bridge unknown |
| Handler wrapper | Surface retains shared native handler ownership; JNI handler retains Java reference ownership | Session 7 `swapchain-dtor`, `texture-handler-dtor`, `jni-refs-global`; high |

`Browser.getTexture()` reaches supplier `0x18004bd60` on its caller. With completed pixels available, zero cached ID triggers handler virtual `+8` (create); changed dimensions trigger `+0x10` (resize); dirty rectangles invoke `+0x18` (upload). It records the new dimensions and forces full damage after create/resize. JNI upload borrows the CPU storage for the synchronous callback. This is a pull-driven Java graphics update, separate from worker rasterization.

The `JniTextureHandler` vtable at `0x1800602d0` contains delete at `+0x28` → `0x18002d630`. Fresh `handler-vtable-correct` and `jni-delete-asm` verify the edge. The deletion wrapper obtains an Environment, calls the Java `(I)V` method and checks/describes/clears an exception. The native reference search (`delete-incoming`) returns data references, including the vtable slot, not a resolved shutdown caller. Virtual calls are not disproved by this result.

## Newly traced Java cleanup

Fresh class-byte hashes and `javap` results are indexed as `java-10`, `cleanup-0` and `cleanup-1`:

1. `TextureHandler.deleteTexture(int)` removes the logical-ID map entry and invokes bridge method `CRRIHIOIHRIOICIIOHHCCOIIHHCCHI()`. The inspected body does not null-check a missing map entry before invoking it. This is not a universal idempotent-delete contract.
2. A shipped modern `ReloadableTexture` bridge implements that method using a version branch: its newer branch restores the underlying texture/view/sampler state when needed, then calls the superclass close method; the older branch restores a saved ID and calls superclass release-ID. Its cleanup callback can schedule work onto Minecraft's render/client machinery when off-thread.
3. A separate `AbstractTexture` bridge implements the same method through `release()`, restores a saved texture ID when necessary, calls superclass release-ID and then its owner callback.
4. The previously inspected modern resize bridge closes existing `GpuTexture` and `GpuTextureView` objects before replacement. See [Session 7 rendering contracts](../session7-astra/webosr-rendering.md).

**Verified / high:** graphics-resource release mechanisms exist beyond the native CPU destructor. **Inferred / medium:** these bridge implementations provide the downstream cleanup route for compatible selected versions. **Unknown:** actual transformed Minecraft superclass implementation/backend in a launch, the selected bridge instance, and whether every WebOSR browser shutdown invokes this route. The trace stops at shipped bridge/superclass calls; it does not establish a specific `glDeleteTextures` instruction for every supported version.

## Browser and renderer shutdown

Browser destructor `0x180042860` moves its view into an actor-0 closure, waits for acknowledgment while pumping the caller's actors, then releases members. Surface destructor `0x18004b480` releases handler ownership and the three CPU records. The inspected body does not pass its cached texture ID to handler `+0x28`. Handler destructor `0x18002d470` releases reference-wrapper ownership, which is not itself a per-ID texture deletion.

Engine destruction dispatches a stop request, waits for acknowledgment and joins the worker before releasing remaining resources. That demonstrates a worker stop boundary, not that all browsers and Java graphics resources have already been closed in a safe order. See [queue synchronization](queue-synchronization.md).

## Failure and remaining boundary

- Zero-ID creation may be retried on a later completed frame. A Java exception is described/cleared by the inspected JNI wrapper; this does not prove the native caller receives a structured graphics-allocation failure.
- Java resize closes old GPU objects before replacement on the examined branch. Full allocation-failure rollback and manager registration cleanup remain unknown.
- Partial browser/engine construction, close after worker exit, graphics-context loss and shutdown with callbacks outstanding remain unproved.

**Next evidence if this subsystem is ever needed:** recover callsites using the exact handler pointer and supplier cached ID, and the Java browser owner's explicit close/texture-manager release ordering. A broad direct-xref search alone cannot close this gap. This work is non-blocking for the independent Fabric HUD MVP, which uses Minecraft-managed rendering resources.
