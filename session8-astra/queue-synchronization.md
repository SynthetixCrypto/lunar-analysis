# Native queue synchronization and shutdown

**Result: partially resolved.** Fresh assembly identifies publication instructions and acknowledgment primitives. It supports a constrained producer/consumer model, not a proof of multi-producer safety or recovery from partial initialization.

All binding addresses and S8 record aliases are indexed in [evidence](evidence-index.md). Background rendering remains statically verified by the [Session 7 worker trace](../session7-astra/native-threading-lifecycle.md).

## Actors and scheduling

- Engine constructor `0x180038ac0` registers its caller as actor 1 and starts the native worker. Worker initialization registers actor 0; the worker loop `0x18003b490` pumps it and schedules renderer update/submission.
- `invokeIteration0()` reaches `0x180036320`, which drains actors registered in the calling thread's TLS. It is not the renderer itself.
- `0x180036380` compares the current thread ID against the destination actor's registered thread. A match invokes the callable inline; otherwise the inspected route uses a ring of 64-byte callable slots.
- Java texture callbacks run synchronously on the `getTexture()` caller. Renderer production and graphics consumption are distinct roles; OS thread names and actual cadence were not observed.

## Fresh assembly findings

| Mechanism | Verified instructions / layout | Interpretation and boundary |
|---|---|---|
| Actor ring publication | Producer loads write index `+0x40048`, tests next index against read index `+0x40040`, transfers callable, then `MOV` publishes write index at `0x180036484` | Modulus `0x1001`; one slot reserved implies 4096 usable entries. No producer index reservation/CAS in this route |
| Full ring | Yields, then rereads indices and retries | Backpressure can block a producer; this is not a drop/coalesce policy |
| Actor ring consumption | Moves callable into local storage, publishes advanced read index at `0x1800361ff`, then invokes it | Slot reuse follows the move; invocation may occur after space becomes available |
| Alternate batch/list route | Consumer includes memory `XCHG` of pointer `+0x40060` at `0x180036058` | Must not conflate this synchronization with the ring's producer index |
| Surface completed queue | Writes record pointer then completed index at `0x18004c4bb`; consumer reads corresponding indices | Three CPU records, four ring slots; intended worker-producer / Java-consumer relationship |
| Engine stop acknowledgment | Stop flag store, then `XCHG byte ptr [ack]` at `0x18003a174` | Atomic acknowledgment publication in the inspected Windows x64 binary |
| Source cleanup acknowledgment | `XCHG byte ptr [ack]` at `0x180049a41` | Acknowledges provider removal before temporary-reference epilogue |

Evidence: `actor-send-assembly`, `actor-consume-assembly`, `swapchain-publish-asm`, `shutdown-assembly`, `source-dtor-task-asm`. **Confidence: high** for instructions; **medium** for intended SPSC usage; **unknown** for all-callsite producer cardinality and race freedom.

## Memory visibility: what can and cannot be concluded

An x86-64 `MOV` can implement a language-level acquire/release atomic; the lack of an explicit fence is not evidence of absent synchronization. Conversely, disassembly does not recover the complete original C++ memory model, establish every object alignment/lifetime, or prove that multiple callers never concurrently write the same ring slot. The observed ring producer has no atomic reservation mechanism, so general MPSC safety requires additional serialization not demonstrated here. Locked reference counts protect those control blocks, not automatically queue admission or source objects.

## Stop ordering and failure-before-ready

Engine destructor `0x1800396e0` sends stop, waits while pumping/yielding, then joins via `0x18003aec0`. Source destructor uses its own worker acknowledgment; browser destruction pumps caller actors while waiting. These are different wait protocols and should not be summarized as one uniform close method.

Fresh `engine-constructor-assembly` corroborates the ready-byte wait. `worker-entry` (`0x180039990`) performs initialization then the run loop; the inspected normal body does not establish a ready-failure result delivered back to the constructor. Exception tables, outer thread boundary, allocation/thread-creation failure and all unwind paths are not fully traced. Therefore:

1. orderly stop/join is verified;
2. a timeout, guaranteed failure notification or queue cancellation protocol is not verified;
3. concurrent shutdown with newly admitted work, constructor failure and close after worker exit remain open;
4. no deadlock, UAF or saturation incident was reproduced under this static-only scope.

## Independent architecture decision

Use Minecraft's client thread as the single owner of modules, input state and HUD state. Send immutable disk-I/O results back through the supported client executor. Avoid reproducing this native actor transport. If an asynchronous subsystem is later introduced, use a maintained queue/executor with a specified producer model and explicit `STARTING → RUNNING → STOPPING → CLOSED/FAILED` lifecycle. These are design recommendations, not claims about Lunar's source.
