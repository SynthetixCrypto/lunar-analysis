# RpcChannel tracking, timeout and cleanup — session 4

Static-only; no connections opened or target code executed. Artifact: `lunar.jar`. Original classes in [class-map.tsv](evidence-rpc/class-map.tsv); fresh complete channel and pending-entry disassembly, verbose BootstrapMethods, selected transport/library bodies and bounded caller search are in [evidence-rpc](evidence-rpc/). JVM citations below use decimal method-local offsets. Confidence: **Confirmed** code structure; **Strong inference** conditional consequence; **Unknown** uncollected behavior.

## Tracking is callback/cache-based, not a channel-owned Future

**Confirmed — S4-RPC-01.** `L._cb9292._21aca6.<init> @4–26` creates a Guava Cache with **expireAfterWrite(10, MINUTES)** and a RemovalListener. Pending value `L._cb9292._21aca6$_cfe983.<init> @4–16` holds diagnostic method name, response Message prototype and RpcCallback. No CompletableFuture, RpcController or timeout task is stored in that object. `callMethod` never reads its RpcController argument.

`callMethod @0–40` returns immediately if transport is not open, optionally logging; it neither registers a request nor invokes the callback nor sets controller failure. If open: UUID.randomUUID → UUID.toString → ByteString.copyFromUtf8 (`@41–50`), build envelope (`@52–116`), cache pending callback/prototype **before send** (`@118–150`), then transport `send(byte[]) @155–164`. IDs are textual UUID bytes, not a sequential integer or raw 16-byte UUID. Envelope fields use actual service/method/input descriptors, not a synthesized service lookup.

**Confirmed.** There is no catch/rollback around send in this method. **Strong inference:** a connection-close race after isOpen can throw through send while leaving its cache entry; neither the callback nor RpcController is failed by this channel. Library selected `WebSocketImpl.send` confirms open-state rejection; actual races are **Unknown**.

## Expiration is not an error completion

**Confirmed — S4-RPC-02; U-11 resolved at channel level.** Static RemovalListener `_cfe983(RemovalNotification) @0–42` ignores EXPLICIT removals and only logs the method/cause for other removal causes. It does **not** call RpcCallback, complete a Future, set controller failure, retry or emit a wire cancellation. `<clinit> @0–5` BootstrapMethods #3 binds this listener.

The 10-minute setting is a **cache expiration policy**, not evidence of a timer that completes callers exactly at ten minutes. No scheduler or explicit `Cache.cleanUp` appears in this channel. Under normal Guava semantics, entries become logically expired by age and physical removal/notifications occur during maintenance/access, not a guaranteed dedicated timer. **Strong inference:** timed-out requests can abandon their callback without any failure notification, and retention can outlast the logical expiry until maintenance. **Unknown:** transitive caller-specific timeout wrappers or another subsystem’s maintenance. The bounded search found no Future/timeout symbols in **16 non-auth IPC call-containing method bodies**; this is not a whole-program proof.

An unknown launcher service can therefore have its pending entry expire; the older phrase “no response leaves pending forever” is wrong as a cache-lifetime claim. “Callback might never be called” remains correct for these paths.

## Responses remove tracking before decoding or scheduling completion

**Confirmed — S4-RPC-03.** `L._cb9292._21aca6._cfe983(IPCRpcResponse)` (original `COOCHIRORIICRCIIRIROHIIRIRICCH`) gets by request ID `@0–16`. Missing/late/duplicate IDs log and return `@17–39`. Matched entry is invalidated `@40–48` **before** response prototype `newBuilderForType.mergeFrom(output).build @53–76`. InvalidProtocolBufferException is logged/printed `@80–98`; no callback or controller failure follows, and the request has already been removed. Other build/scheduling exceptions are not caught by this decode handler.

Success submits callback through `L.util._d930e6._cfe983(Object,RpcCallback) @0–15`, which wraps callback in a Runnable and calls Minecraft `bridge$submit`. The queued helper `_cfe983(RpcCallback,Object) @0–17` catches **Exception**, not Error, and reports PacketUtil. Transport `onMessage(ByteBuffer) @0–24` similarly logs malformed outer envelopes; `@25–46` delegates RPC responses; text-message overload is a no-op. This does not establish exact game-thread execution timing; it establishes the scheduling boundary.

**Confirmed limit.** Cache lookup and invalidation are two separate operations, not atomic remove-and-return. **Strong inference:** simultaneous accepts of the same ID could both retain a pending object before invalidation and schedule duplicate callbacks; the shown transport normally processes a receive stream, but a universal concurrent exactly-once guarantee cannot be attributed to this channel.

Protocol metadata contains request ID/output response fields, not a structured error result; offsets **N/A** for schema declaration (retained `protocol-common-proto.javap.txt` and prior schema). Local decode/send/callback failures still exist even without a wire error field.

## Disconnect drops pending callbacks; onError is not cleanup

**Confirmed — S4-RPC-04.** Channel original cleanup method `ORIRHCHRRHRCCOCIHCOOCHHOHCCCIO() @0–9` calls **invalidateAll**. Transport `L._cb9292._cfe983.onClose @0–4` invokes it, then updates disconnect state `@60–64`. Those EXPLICIT removals are ignored by the listener, so disconnect is **silent abandonment**, not exceptional completion. Push registrations and service stubs are not cleared in onClose. Cache is per channel/transport instance, not global.

`onError(Exception) @0–58` only conditionally logs/prints; it does not invalidate pending entries or change disconnect state. It dereferences `exception.getMessage().startsWith` without a null guard `@0–6`: **Strong inference** null messages can themselves produce NPE. A WebSocket library error may separately trigger close, but that is not the same as cleanup inside this callback.

## Reconnection is a new transport, with a surprising bounded backoff

**Confirmed — S4-RPC-05.** Transport event callback (original `COCCCORHOHRORRICOOHOCHOOCHHICR(event)`) checks absent/disconnected transport `@7–34`, lazily creates backoff `@34–51`, then calls its elapsed test `@54–66` before client restart. Client original `IHHHRCROHRCIRICROICCHOOHCRCOIO @0–16` starts a background thread. Worker `HHICRRORCCHCRRHHIIIRCHHIHCROII @0–23` closes an existing **open** transport via closeBlocking, then creates/stores a new transport and calls connect `@45–61`; it does not migrate old pending callbacks. A null setup object returns `@29–44`; no personal handshake/identifier value was accessed.

The null-input backoff constructor `L._21aca6._bb4487.<init> @101–122` sets current interval **15,000 ms**, records time, and stores caller-supplied cap. IPC supplies **5,000 ms** (`onClose @14–25` when state is null; periodic callback `@40–51`). Elapsed test `CIHHCOHOIHIRRRHICHICRHHRICRRHR @0–47` waits until current interval, then sets interval `min(old*2,cap)` and refreshes timestamp. **Strong inference:** that IPC null-input path first waits at least 15 seconds, then uses a 5-second interval, not monotonically increasing exponential backoff. Reconnect checks occur on event opportunities, so these are minimum age gates, not exact timers. onOpen clears static backoff `@0–1` and sets READY `@4–8`.

## Verification / remaining scope

- Earlier service/envelope/handshake inventory is reused, not repeated. Controller/callback policy, expiration and cleanup are newly resolved.
- **Correction:** timeout policy exists, but it only expires tracking and logs; do not promise failure completion or cancellation.
- **Unknown:** transitive caller deadlines, real close/error order, bridge queue execution timing and reconnect races. No networking/target execution is authorized.
- Next static work should trace caller UI pending-state cleanup after silent abandonment and library maintenance semantics if exact retention timing is needed; it should not revisit the service catalog.
