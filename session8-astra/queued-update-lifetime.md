# Queued image-source lifetime

**Result: normal serialized destruction is substantially better understood; arbitrary concurrency remains unproved.** Payload copying and object lifetime are different contracts. The newly recovered destructor provides an actor-0 cleanup acknowledgment, rather than making every update capture a strong source reference.

Native target identity and exact Evidence IDs: [evidence index](evidence-index.md). All addresses below are in the binding DLL.

## Verified chain

| Stage | Static observation | Evidence alias / address |
|---|---|---|
| Java input | JNI reads direct buffer address and capacity; positive capacity is the copied extent, not Java `remaining()` | Session 7 `image-update-jni`, `0x180027cd0` |
| Queue submission | Allocate and copy the input bytes, capture adjusted source pointer plus owned byte range, then dispatch actor 0 | S8 `source-update-asm`, `0x18004a530`; Session 7 `image-update-copy` |
| Worker update | Requires exact tightly packed `width * height * 4` BGRA8 payload size | Session 7 `image-upload-work`, `0x180049510` |
| Handle close | JNI destroy releases the handle wrapper's shared ownership | S8 `image-destroy-jni`, `0x1800278f0`; `source-handle-cleanup`, `0x180027610` |
| Last shared-owner disposal | Refcount control-block vtable leads through `0x18003a130` to the actual source destructor | S8 `source-refcount-table`, `source-refcount-destroy` |
| Source destructor | Dispatch actor-0 cleanup, yield until an acknowledgment byte changes, then release child/container/bitmap members | S8 `source-dtor-body`, `source-dtor-asm`, `0x180049400` |
| Worker cleanup | Look up image-provider entry by source identity, remove it only if it matches this source's stored object, then atomically acknowledge | S8 `source-dtor-task`, `source-dtor-task-asm`, `0x1800499e0` |

Confidence is **high** for these observed bodies and table edges. The closure's invocation table and assembly are the authority; earlier exploratory filenames are not semantic names.

## What the destructor protects

**Verified:** source memory and members are retained while the destructor waits for actor-0 cleanup. Worker acknowledgment uses memory `XCHG` at `0x180049a41`. Provider removal is identity-checked so that destruction does not simply remove whatever object currently has the same name.

**Inferred / medium:** with one serialized producer, FIFO ring delivery and a live actor-0 consumer, updates submitted before close finish their actor work before the cleanup acknowledgment, allowing ordinary update-then-close use. The same-actor dispatch path runs inline rather than waiting for a future queue iteration.

This inference has important bounds:

- The update closure itself captures a raw adjusted source pointer. Its copied byte range is independently owned, but that does not make the destination immortal.
- A racing producer could enqueue after close's barrier or access the handle during destruction. The inspected Java `NativeHandle.close()` zeroes the handle after native destruction; that is not a universal concurrent-close guard.
- The alternate actor batch/list path prevents assuming a universal FIFO across every route.
- The cleanup closure writes acknowledgment **before** releasing its temporary provider reference. Thus the acknowledgment is not proof that all closure epilogue work has ended.
- The source destructor yields without pumping the caller actor loop, unlike the browser destructor. No timeout/cancellation was found in this body. Closing after actor-0 exit may lack forward progress; no runtime hang was observed.

## Unbind, resize and reconfiguration

S8 `source-unbind-adjust` and `source-base-unbind` resolve the inspected unbind implementation to a state-byte write (`0x18004cc50`) after subobject adjustment. That does not establish cancellation of all previously queued work. Size/update operations and child references still require a cross-method ordering contract if called concurrently. The destructor's child/container releases do not by themselves prove every child-held backpointer is safe under every interleaving.

## Correction and independent design implication

Session 7 correctly left destination lifetime unknown. This session adds a concrete destructor barrier and identity-checked provider removal; it would now be incomplete to describe the implementation as merely “raw pointer queued with no cleanup coordination.” It would also be incorrect to declare it race-free.

For a future independently written asynchronous image service, specify immutable payload ownership, a generation/closed state, admission control before shutdown, one proven queue model and a completion future for destruction. The MVP avoids this native subsystem entirely; [development readiness](development-readiness.md) explains why this gap is non-blocking.
