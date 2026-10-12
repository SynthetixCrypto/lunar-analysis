# Session 6 — JNI reconciliation and WebOSR data contracts

Static only. **Confirmed** = observed bytes/bytecode; **Derived/Strong inference** = consequence conditional on the shown code running; **Unknown** = not established. JVM offsets are decimal and method-local. All aliases in this report have original class names, artifact paths and class SHA-256 values in [class-manifest.json](evidence-native/class-manifest.json) or [lifecycle-manifest.json](evidence-native/lifecycle-manifest.json). Full fresh verbose javap and alias copies are retained next to them. No native decompiler was available; see [native-rendering-analysis.md](native-rendering-analysis.md).

## S6-WEB-01 — 56/58 means 55 shared, one Java-only and three DLL-only

[jni-reconciliation.json](evidence-native/jni-reconciliation.json) compares all 56 recovered native declarations with the 58 exact retained exports of the freshly digest-matched binding DLL. The arithmetic is **55+1 versus 55+3**, not simply two unnamed extra functions. This makes the earlier discrepancy explicit without repeating the completed PE inventory.

| Side | Exact symbol | Native RVA if present |
|---|---|---:|
| Java-only | Java_com_moonsworth_webosr_wrappers_Session_name | absent from retained named export table |
| DLL-only | Java_com_moonsworth_webosr_wrappers_Session_getName | 0x29690 |
| DLL-only | Java_com_moonsworth_webosr_wrappers_Browser_swapBuffers | 0x1fc10 |
| DLL-only | Java_com_moonsworth_webosr_wrappers_WebEngine_setTimers | 0x1c400 |

**Confirmed bounded negative:** [session-methodrefs.json](evidence-native/session-methodrefs.json) parses every class constant pool in lunar.jar (18,523 classes), modern JAR (1,368), common JAR (32) and genesis JAR (7,152): **27,075 class occurrences**. There is no Methodref/InterfaceMethodref to any method owned by `com/moonsworth/webosr/wrappers/Session`, including name(). Exact four artifact hashes are recorded. Session.name's own declaration has no Code attribute; a declaration is not a caller. This is stronger than an alias-text search, but excludes reflection, native invocation, external code and unscanned artifacts. Alternate registration and runtime linkage failure remain **Unknown**. DLL-only exports cannot be labelled dead/legacy based on this evidence.

## S6-WEB-02 — Java destination/source rectangle and byte-stride contract

Root TextureHandler `L._81676d._21aca6._590f69._cfe983._cfe983.uploadTexture(int id,ByteBuffer b,int x,int y,int w,int h,int stride) @0–49` forwards `(x,y,w,h,b,x,y,stride)` at @44 to the texture bridge. Width/height zero returns before map lookup. This root forwarding was known; the newly traced actual modern bridge supplies the units and conversion.

**Confirmed:** modern JAR `ML._d4ca6c._1e73d7._590f69._88f3cf._2f4182._cfe983.bridge$uploadBgra @0–190` splits at MC_VERSION 29:

| Gate | Concrete transfer |
|---|---|
| <29, @0–30 | Duplicates ByteBuffer and calls lunar$uploadOpenGl with format integer 32993 (0x80e1), destination rectangle, source x/y and byte stride. |
| >=29, @31–187 | Allocates/reuses w*h*4 staging bytes; source start=`memAddress(b)+sourceY*stride+sourceX*4 @54–75`; row start adds `row*stride @94–104`; reads each 32-bit source pixel, swaps the low and third bytes while retaining the other two, writes densely to destination @125–165; then lunar$uploadCompactRgba(destinationX,destinationY,w,h,staging) @179–187. |

The swap expression is `(pixel & 0xff00ff00) | ((pixel & 0x00ff0000) >>> 16) | ((pixel & 0x000000ff) << 16)`. Combined with the BGRA-named interface and RGBA write calls, it establishes the Java-side BGRA→RGBA conversion. There is **no alpha premultiply/unpremultiply operation in this method**; native premultiplication policy remains unknown.

`lunar$uploadOpenGl @12–42` reads old unpack skips/row length/alignment and texture binding; @48–78 sets source row skip, pixel skip, alignment=4, row length=`stride/4`; `_texSubImage2D @81–100` uses rectangle and unsigned-byte type 5121. The saved values and binding are restored on normal @103–137 and exceptional @143–184 paths. The numeric constants and division are directly observed; no external GL documentation was needed to establish stride units.

`lunar$uploadCompactRgba @28–226` selects GPU command encoders by version ordinals: >=39 uses v26_2 ByteBuffer overload, >=36 v26_1 ByteBuffer+RGBA, >=33 v1_21_9 ByteBuffer+RGBA, >=30 v1_21_6 IntBuffer+RGBA, else v1_21_5 IntBuffer+RGBA. Those are exact method suffixes/gates, not a claim of complete ordinal/version mapping. Destination x/y/w/h are carried through; source offset arguments are zero because staging is compact.

**Java memory ownership:** `L.util._2f4182._13ea87._8cc4be @0–41` holds one static ByteBuffer, grows it via BufferUtils.createByteBuffer when absent/too small, resets position=0 and limit=capacity, and returns it. Upload sets limit=w*h*4. No synchronization or per-engine staging ownership appears. **Conditional inference:** concurrent calls can share/overwrite this Java staging memory unless callers/native/GPU layers serialize or copy it. No live overlap, GPU retention or use-after-free is proven. Input buffer directness/size and native row-stride correctness are not validated by this Java method.

**Native limit:** callback strings and RTTI in the binding support a candidate JNI texture-handler path (prior file offsets 0x5e878–0x5e8b8 and 0x7ff80), but neither this Java contract nor strings proves which native method calls them or how long native input pixels remain valid.

## S6-WEB-03 — reverse transfer: Minecraft framebuffer to native image source

This is distinct from browser pixels uploaded into Minecraft textures. Artifact lunar.jar, `L._81676d._21aca6._13ea87._cfe983`:

- Constructor(String,boolean,int) @47–73 creates native `WebEngine.createImageSourceTextured(name)` when engine is available and registers this wrapper. Lazy `_26a15d @0–59` repeats creation when a previously unavailable engine becomes usable.
- `_21aca6(renderContext,w,h) @0–181` indexes owned framebuffer objects by the image-source Java object's hashCode; dimension mismatch deletes the previous framebuffer @68–75, allocates a replacement @80–101, installs it in the map @118–134 and clears/binds it. Native `TexturedImageSource.size(w,h)` is called only when dimensions change (`_d930e6 @16–48`). Object hash is a map key here; it is not claimed to be a native texture pointer or GL name.
- `_2ce426(framebuffer) @8–45` obtains dimensions and the color texture, then requests readback of `(0,0,w,h,RGBA8)` with a Consumer. The callback binds to private `update(ByteBuffer)` (verbose BootstrapMethods binding retained).
- `update @8–53` swaps byte 0 and byte 2 in each four-byte group in place; @56–61 calls **native** TexturedImageSource.update(ByteBuffer); @65 invokes bind notification. There is no additional Java copy, synchronization, directness check or size guard in this callback. Its loop uses absolute indexes from zero and remaining() as the bound; correctness relies on the readback buffer contract (in particular position/layout).
- `_941bc2 @0–54` binds the native image source once and emits gameTexture notification; `delete @0–140` releases owned framebuffers, unbinds/closes the image source and then emits removal notification when previously bound. See native-rendering-analysis.md for shutdown order/failure boundaries.

**Unknown:** whether the native update copies or borrows this buffer, synchronization with the browser, native image/surface ownership and image-release timing. The binding's TextureSourceImpl size-mismatch string @file 0x604a0 is consistent with an inbound BGRA image, but is not the implementation proof of copy/lifetime. A future native pass must trace this direction as well as TextureHandler uploads.

## S6-WEB-04 — G-32 Java PromiseJS codec consequence narrowed

Session 4 established that FunctionBus.subscribe @300–308 captures `Parameter.getParameterizedType().getClass()` rather than the generic T. The new continuation traces its actual effect:

- `FunctionBus.buildInvocationParameters @257–273` binds that Class and the bus codec to PromiseJS when non-null.
- `PromiseJS.bindBridgeCodec @0–7` stores those references. `resolve(T) @19–31` forwards null directly to `_resolve(String)`; @32–61 passes non-null values plus the captured Class to codec.objectToString. Without a codec/type, only String is accepted @65–100.
- Base `FunctionBus.objectToString @0–231` selects String, primitives/boxes, enum and UUID **by the supplied Class**; unsupported Class throws IllegalArgumentException @232–248.
- Lunar subclass `L._81676d._21aca6._590f69._cfe983.objectToString @0–15` catches Exception from the base and returns Gson.toJson(object), using no supplied Type in the fallback.

**Derived static consequence:** when the captured class is a reflection type implementation rather than T, the base scalar branches do not match. Lunar's codec then uses its Gson fallback for non-null values; a String can consequently cross as JSON-quoted string text rather than the base raw String path. Exact runtime reflection implementation classes were not observed, and native parsing of the returned text remains unknown. The bytecode does not provide faithful generic-T recovery. Null uses the separate null-string completion path; no native JS null/undefined distinction is asserted.

G-32's Java data flow is now traced through completion; native marshalling parity remains open. The subsequent [G-33 caller follow-up](functionbus-followup.md) establishes that the annotated invoke router and three Java iteration callers add no local queue guard/promise recovery; it extends rather than repeats the prior queue-full/unknown-routine branches. No runtime queue-saturation claim is made.
