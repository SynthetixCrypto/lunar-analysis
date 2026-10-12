# Session 7 — WebOSR rendering

## Main result

**Verified:** the inspected implementation has a native renderer worker and a custom three-buffer CPU surface. The worker produces completed pixel buffers; `Browser.getTexture()` drains the completed-buffer queue and synchronously invokes Java texture create/resize/upload callbacks. `invokeIteration0()` pumps actor queues on its calling thread. It is not the direct renderer-update/render function.

The word `gl` in a native namespace does not establish that these three buffers are GPU swapchain images. Their allocation and copying paths are CPU memory operations. GPU texture creation/upload occurs behind the supplied Java TextureHandler implementation.

Principal evidence: binding worker `0x18003b490` ([dossier](evidence/worker-run.json), `ev_7677cc52b19c1b0b0bfb6cbda416093ab83b24215bb18866b7433065390d8f2c`); supplier `0x18004bd60` ([dossier](evidence/swapchain-get-texture.json), `ev_6ebef923932659330d31e3035017765a1a8a0de62e49ce519fc6a73bc895516e`); [iteration target](evidence/engine-iteration.json).

## End-to-end static path

```text
Java createEngine
  -> native EngineImpl -> native worker -> Ultralight Renderer
Java createBrowser
  -> native BrowserImpl -> actor-0 view creation -> custom SurfaceFactory

worker cycle:
  pump actor-0 work
  update WebCore timers/run loop when update interval permits
  acquire available CPU pixel buffer / choose eligible views
  per-view operation + batched Painter submission
  supplier publish: completed CPU buffer + dirty regions

Java Browser.getTexture() on its caller:
  obtain browser's supplier
  drain completed queue (keep newest; return older buffers)
  create/resize Java texture if needed
  upload dirty rectangles through synchronous JNI callbacks
  recycle consumed CPU buffer
  return logical Java texture ID

Java framebuffer -> TexturedImageSource.update(directBuffer):
  address + capacity -> immediate native copy -> actor-0 task
  validate tight BGRA8 size -> replace native source data
```

This is a static call/data-flow model. It does not identify a live Minecraft thread, guarantee every callback's affinity, or measure frame cadence.

## Surface allocation and interfaces

**Verified / high confidence.** Engine's surface-factory subobject is at engine `+8`. Its factory method `0x180039c10` atomically consumes a one-shot flag at subobject `+0x150` (engine `+0x158`). Without the flag it delegates to imported `GetBitmapSurfaceFactory`; with the flag it allocates `0x1b8` bytes and constructs `webosr::ul::gl::surface::Swapchain` at `0x18004b130`. It retains the configured texture handler through shared ownership. Browser creation `0x18003a900` sets this flag before construction.

Evidence: [factory](evidence/surface-create.json), [browser factory](evidence/browser-factory-native.json), [constructor](evidence/swapchain-ctor.json), [worker view creation](evidence/browser-create-worker.json).

| Surface-relative location | Observed role |
|---|---|
| `+0` | Surface vtable `0x180062020` |
| `+0x18` | Texture-supplier interface/vtable `0x180062080` |
| `+0x24 / +0x28 / +0x2c` | Width / height / row-alignment parameter |
| `+0xd8` | Three pixel-buffer records, each `0x40` bytes |
| `+0x1a8 / +0x1b0` | Texture handler pointer / shared ownership control |

The supplier methods operate on `surface+0x18`, so their offsets cannot be mixed directly with Surface-relative offsets. [Raw tables](evidence/swapchain-tables.json).

### Allocation, stride and resize

Pixel-record initialization `0x18004bc00` allocates storage for all three records through `0x18004c1c0`, with byte size `height * alignedRowBytes`. For positive width and alignment:

```text
rowBytes = roundUp(width * 4, configuredAlignment)
byteSize = height * rowBytes
```

Surface row-byte method `0x18004c310` computes that same alignment-dependent value. An additional cached field at surface `+0x30` is rounded to 16 bytes by the constructor/resize body; that field must not be substituted for the callback's actual stride. Resize `0x18004b550` changes surface dimensions, resizes the currently acquired record if any and clears dirty history. Other records are reconciled to current dimensions when reacquired by `0x18004bfa0`.

Evidence: [pixel init](evidence/pixel-buffer-init.json), [allocation/grow](evidence/pixel-buffer-grow.json), [stride](evidence/swapchain-stride.json), [resize](evidence/surface-resize-correct.json), [reacquire](evidence/swapchain-ready.json).

**Unknown:** safe limits and validation for all zero/negative/overflowing dimension or alignment inputs. These equations describe the normal positive-input path, not a validated public API specification.

## Publication, dirty rectangles and latest-frame consumption

**Verified:** publication at `0x18004c360` reads the current surface dirty rectangle, combines it with two prior dirty rectangles, assigns the resulting region vector to the current pixel record, and inserts that record into a modulo-4 queue. It advances dirty history, clears the surface dirty state and clears the active-producer pointer.

The region helper `0x18004b740`:

1. Clips the three candidate rectangles to `[0,width] × [0,height]`.
2. Omits empty regions and removes exact duplicates.
3. Merges intersecting rectangles, and adjacent rectangles with the corresponding matching spans, into bounding rectangles until no more merges apply.
4. Passes the resulting vector through a final ordering helper.

Reacquisition `0x18004bfa0` can copy rows from the previous produced buffer over dirty-history regions before new painting, using `row * stride + x * 4` and `(right-left) * 4` bytes. **Inferred / medium confidence:** historical damage maintains valid content as buffers rotate and intermediate frames are skipped. Full correctness for all producer/consumer interleavings was not proved.

Evidence: [publication](evidence/swapchain-present.json), [region selection](evidence/dirty-regions.json), [reacquire/copy](evidence/swapchain-ready.json). Region helper Evidence ID: `ev_dbff08c73303e8781a0028212c70026cfde9f0c12e71138d2795842a86e7d35f`.

The two queues use modulo-4 indices with an empty-slot convention, consistent with three usable entries and three CPU records. The consumer `0x18004bd60` drains all available completed records, recycling any superseded current record, then processes the last one. **Verified:** newest available frame is retained within that drain pass. **Unknown:** actual drop frequency, publication memory-order guarantees and race behavior; this is not a proof of a general lock-free multi-producer queue.

## `getTexture()` and JNI upload

`Browser.getTexture` at `0x18001f7b0` obtains the wrapper's Browser pointer at `+0x20`, invokes Browser virtual `+0xb8` (`0x180047760`) to get the supplier, then invokes supplier `+8` (`0x18004bd60`). Supplier acquisition waits while Browser `+0x50` is null, pumping caller actors and yielding.

Once a completed record exists:

- If texture ID is zero, invoke handler create; retain its returned logical ID.
- If width/height differ from the remembered texture dimensions, invoke resize.
- Following create or resize, replace dirty regions with the full frame rectangle.
- For each nonempty region, invoke upload with the **whole pixel buffer** pointer/size and region `(x,y,w,h,stride)`.
- Clear the record's dirty vector and return it to the available-buffer queue.
- Return cached logical texture ID, even on a call with no newly completed record.

Evidence: [JNI getTexture](evidence/get-texture.json), [supplier wait](evidence/browser-texture-supplier.json), [consumer](evidence/swapchain-get-texture.json), [callsite assembly](evidence/swapchain-upload-assembly.json), [JNI upload assembly](evidence/upload-call-assembly.json).

**Verified static thread consequence:** create/resize/upload on this chain execute synchronously on the `getTexture()` caller; the inspected chain does not enqueue them to actor 0. The independent native worker performs the painting/publication work. Which real application thread calls this API is not established by native code alone.

The DLL-only `Browser.swapBuffers` calls supplier `+0x10`, the same publication role called by the worker after rendering. It is not established as a Java-accessible GPU swap/present API in the shipped JAR. [Export body](evidence/swap.json).

## Pixel format and Java conversion

**Verified:** Java's handler forwards the callback as BGRA upload. The modern bridge consumes rows at `base + sourceY*byteStride + sourceX*4`, swaps red/blue byte positions in its newer-backend staging path, and writes compact RGBA. Its older branch forwards a duplicated ByteBuffer to the OpenGL upload path using BGRA format constant `32993`. Fresh bytecode and class hashes match the previous research.

Evidence: [handler](evidence/L._81676d._21aca6._590f69._cfe983._cfe983.javap.txt), [modern bridge, `bridge$uploadBgra`](evidence/ML._d4ca6c._1e73d7._590f69._88f3cf._2f4182._cfe983.javap.txt), [hash check](evidence/java-hash-verification.json).

Native stride and four-byte pixel arithmetic now corroborate the Java interpretation. The reverse worker's explicit size diagnostic names BGRA8 as well. **Unknown:** end-to-end alpha premultiplication, color-space conversion, full rasterizer layout guarantees and every backend's selected runtime version. A channel swap alone does not prove any of those properties.

## Reverse transfer: copied before asynchronous work

The texture-image interface's real update body is `0x18004a530`, reached through virtual-inheritance thunk `0x18004a51c`. It allocates native memory, zero-fills it, copies the supplied byte range, captures the copy, then dispatches actor 0. Worker body `0x180049510` accepts exact size `width*height*4` for nonzero dimensions, moves the copied vector into source storage and sets a dirty flag; mismatch logs expected/received dimensions and size.

Evidence: [JNI capacity read](evidence/image-update-jni.json), [interface/thunk](evidence/texture-source-update-thunk.json), [copy body](evidence/image-update-copy.json), [task invoke](evidence/image-update-task-invoke.json), [size validation](evidence/image-upload-work.json), [task release](evidence/image-update-task-release.json).

**Verified:** the Java direct buffer is not retained as borrowed input for that queued update. **Unknown:** the lifetime guarantee for the captured native `TextureSourceImpl` pointer relative to queued resize/unbind/destroy; successful byte copying does not prove source-object ownership safety.

## Ownership and cleanup boundary

Surface destruction `0x18004b480` releases the retained handler and destroys all three CPU records; record cleanup frees storage and region vectors. Engine's surface destroy method performs virtual deletion. This establishes CPU-buffer ownership.

The inspected surface destructor contains no obvious `deleteTexture` invocation. Although the native-to-Java delete callback exists, its complete call chain from normal browser shutdown is unresolved. **Unknown:** which path releases the cached Java/GPU texture, whether the Java owner has a separate cleanup path, and all exceptional lifecycle behavior. No leak or complete GPU cleanup is claimed. [Destructor](evidence/swapchain-dtor.json), [record release](evidence/pixel-buffer-release.json), [delete callback](evidence/jni-delete-texture.json).
