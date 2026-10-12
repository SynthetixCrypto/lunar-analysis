# RPC caller cleanup and remaining edge cases — Session 6

Static-only. No Lunar classes were executed, no service connections opened, and no personal settings or credential values read. Artifact: `C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar`, SHA-256 `bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9`. Fresh `javap -p -c` evidence was produced with the supplied JDK 21. Complete original class names are in [caller-manifest.json](evidence-rpc/caller-manifest.json); every original method signature and exact evidence filename is in [caller-audit.json](evidence-rpc/caller-audit.json). Aliases follow the earlier reports: a 30-character obfuscated token becomes underscore plus its first six MD5 hex digits. Offsets below are decimal JVM method-local bytecode offsets.

Confidence: **Confirmed** = directly shown in retained implementation; **Strong inference** = consequence of the shown control/data flow, not an observed run; **Unknown** = not established within this bounded static scope.

## S6-RPC-01 — G-13: no pending-completion UI latch in the 16 specified callers

**Confirmed within the requested 16-method scope.** The audit expanded Session 4's negative Future-symbol search into response-lambda bindings, same-class state handling, radio action entry points/HUD, checkout screen, and selected incoming-call references. There is no request-specific spinner/lock flag set before sending and released by these RPC completion lambdas. Every call supplies a null RpcController. Therefore silent expiry/disconnect does not strand a demonstrated *request-pending* latch in these bodies. That does **not** imply delivery, successful action, or universal UI recovery.

| Caller alias (evidence) | Exact method / RPC offset | Response and abandonment consequence |
|---|---|---|
| Transport `L._cb9292._cfe983` (caller-00) | `onOpen(ServerHandshake) @41–68`, updateFocus | UpdateFocusResponse lambda `_21aca6 @0` is a no-op. READY is written before sending, not on completion. |
| Same | `_6ee63a() @0–14 / @19–33`, checkTebexCapabilities / checkPayNowCapabilities | Response lambdas assign capability enum at `@0–55`; no pending flag. Missing reply leaves existing capability state. Constructor defaults it to UNSPECIFIED. |
| Same | `_26c4d4() @0–13`, checkPendingPromotion | Response lambda `_cfe983(CheckPendingPromotionResponse) @0–10` replaces promotion-list state; no latch. Independent PendingPromotionUpdatePush updates the same manager at `@11–21`. |
| Same | static `_d4ca6c(transport) @27–54`, updateFocus | Local focused-state setter runs at `@15–24` before RPC; response `_cfe983(UpdateFocusResponse) @0` no-op. A lost reply does not roll back local focus state. |
| `L._81676d._21aca6._d4ca6c._cfe983._c8175c` (caller-01) | `_cfe983(PromotionType,transport) @18–38`, playPromotion | Response `_cfe983(PlayPromotionResponse) @0–11` creates only the launcher-view notification. No completion means no notification; no pending field. |
| Radio `L._88f3cf._bb4487._6247d7._cfe983` (caller-02) | static `_cfe983(Boolean,transport) @0–23`, setMuted | Response `_cfe983(SetMutedResponse) @0` no-op. Local setting changes through `_e829e2 @0–28` and its observer, independently of acknowledgement. |
| Same | `_cfe983(transport) @0–36`, setVolume | Reads setting /100. Response `_cfe983(SetVolumeResponse) @0` no-op. |
| Same | `_21aca6(transport) @0–34`, setPlaying | Reads inverse cached playing state. Response `_cfe983(SetPlayingResponse) @0` no-op. |
| Same | static `_590f69(transport) @0–16`, openSelector | Response `_cfe983(OpenSelectorResponse) @0` no-op; station-list notification is issued immediately after send `@21–39`. |
| Same | `_1e73d7(transport) @0–16`, nextTrack | Response `_cfe983(NextTrackResponse) @0` no-op; skip notification uses cached remaining skips immediately `@21–99`. |
| Same | `_bb4487(transport) @16–36`, setPlaying | Response `_21aca6(SetPlayingResponse) @0` no-op; pause/resume notification follows send `@41–68`. |
| Same | `_1253fc(transport) @29–46`, fetchState | Nontrivial state synchronization; independent reset/poll paths detailed below. No outstanding-request guard. |
| `L._21aca6._cfe983` (caller-03) | `_cfe983(BroadcastLocationChangeResponse,InboundLocation,transport) @0–27`, updateLocation | Response `_cfe983(UpdateLocationResponse) @0` no-op. No state mutation in this IPC forwarding lambda. |
| `L.util._1253fc` (caller-04) | `_21aca6(String,Initiator,boolean) @82–130`, openUrl | Response `_cfe983(OpenUrlResponse) @0` no-op. Returns true immediately `@135–136`; this is acceptance for forwarding, not confirmed browser opening. |
| `L.util._252625` (caller-05) | `_5a1b50(String,String) @47–71`, openTebexJsCheckout | Response logs status and optionally schedules movement-blocking screen. No pre-send UI latch. |
| Same | `_ac25f2(String) @46–66`, openPayNowJsCheckout | Same response pattern; loss before completion prevents this callback from opening the screen. |

All caller filenames above mean `evidence-rpc/caller-NN.javap.txt` plus its `.aliases.txt`; BootstrapMethods files independently bind each invokedynamic response callback to the stated method. The old 16 count counts call-containing methods, not RPC invocations: the capability method contains two calls.

### Radio state is independently refreshed/reset, not completed per request

**Confirmed.** Radio `_88f3cf(event _3a14e3) @0–31` checks the time source minus `_040090` strictly greater than 2000 ms, invokes `_1253fc` through the current Optional transport, and refreshes the timestamp after the Optional call. This is an event opportunity age gate, not a dedicated two-second timer. It has no in-flight gate: a slow/lost fetch does not prevent later fetches.

`_1253fc(transport) @0–26` checks WebSocket ReadyState.OPEN. If not OPEN, it sets track null (also clearing joined artist text), controls null and progress null, then calls `_7fde47`, before still attempting fetchState. An absent Optional transport skips this body, so absence alone is **not** proof of reset. An open connection with a silently expired request also does not enter the reset branch; old radio state can remain until a later fetch/push/reset.

`_cfe983(FetchStateResponse) @0–157` updates track, controls, progress, volume/mute settings and submits `_7fde47`. Incoming StyngrTrackControlsUpdate independently sets controls and volume/mute `@0–47`; StyngrTrackProgressUpdate sets progress `@0–2`. The IPC-ready event handler `_cfe983(event _1253fc._590f69) @5–38` registers all three push handlers. The radio boolean `_9b9f23` and timestamps `_2b71e5`, `_324554` are HUD text-scroll direction/time/offset, not request flags: see [radio-hud.aliases.txt](evidence-rpc/radio-hud.aliases.txt), render `_cfe983(event,float,float,boolean) @487–679 / @788–803`.

### Checkout screen has a separate close-push dependency

**Confirmed.** Both checkout response callbacks in caller-05 inspect getOpenMinecraftScreen `@21–25`, then bridge$submit a Runnable `@39–47`. The scheduled methods `_6183b8() / _581846() @0–20` instantiate `L._2f4182._2f4182._cfe983` and display it. The [checkout screen](evidence-rpc/checkout-screen.aliases.txt) has empty init, update, render, mouse, key and close methods (each `@0 return`) and no own disconnect/timeout recovery. Its [base](evidence-rpc/checkout-screen-base.aliases.txt) declares the key and close methods abstract.

Transport `_cfe983(TebexJsCheckoutClosed) @0–4` clears the current screen via bridge$displayScreen(null); constructor `@177–186` registers that push. Transport onClose clears RPC tracking and marks DISCONNECTED, but does not clear the screen. This dependency is separate from pre-response silent abandonment. **Strong inference:** once a checkout callback has installed this screen, losing the close push/disconnecting does not cause cleanup through these shown methods. **Unknown:** all Minecraft adapter/inherited OS/focus paths that can replace or dismiss it; a permanent movement lock is not proven. See [transport-full.aliases.txt](evidence-rpc/transport-full.aliases.txt).

## S6-RPC-02 — G-14: a concrete static path delivers a null-message exception

**Confirmed implementation path; runtime occurrence unobserved.** Embedded `org.java_websocket.drafts.Draft_6455.processFrameContinuousAndNonFin @69–104` has an invalid-text branch that constructs `InvalidDataException(1007)` using the int-only constructor. [InvalidDataException.javap.txt](evidence-rpc/InvalidDataException.javap.txt), constructor(int) `@0–6`, delegates to Exception() and does not set a message. This library constructor analysis is corroborated by local JDK 21 [Exception.javap.txt](evidence-rpc/Exception.javap.txt), constructor() @0–1, and [Throwable.javap.txt](evidence-rpc/Throwable.javap.txt), constructor() @0–28 / getMessage() @0–4: the no-argument path never assigns detailMessage, and getMessage returns that field. These two files are JDK evidence, not Lunar JAR entries. [WebSocketImpl.javap.txt](evidence-rpc/WebSocketImpl.javap.txt), decodeFrames `@106–132`, catches InvalidDataException and calls onWebsocketError **before** close(exception). [WebSocketClient.javap.txt](evidence-rpc/WebSocketClient.javap.txt), onWebsocketError `@0–2`, forwards the same exception to Lunar's onError. Lunar transport onError `@0–6` calls getMessage().startsWith without guarding null.

**Strong inference:** when this library branch is reached in this transport, Lunar's error handler throws NPE; decodeFrames' intended close call at `@130–132` is skipped on that pass. The receive-loop RuntimeException handler `WebSocketClient.run @439–459` calls onError again before closeConnection. Whether that second error has a non-null helpful-NPE message depends on the actual launch JVM; terminal ordering and cleanup remain unobserved. This establishes an artifact-contained precursor, stronger than merely saying an arbitrary external exception might have a null message. It does not justify running malformed input against the client.

Other shown orders differ: run's connection-setup catch calls onWebsocketError before closeConnection `@262–281`; read IOException routes through handleIOException, which only calls onError for SSLException `@0–9` then eot `@12–16`; a normal EOF invokes eot directly `run @418–422`. Do not assign one universal error→close ordering.

## S6-RPC-03 — G-16: normal transport receives serialize response acceptance

**Confirmed.** WebSocketClient.connect `@17–65` creates one thread running this client and refuses reuse when connectReadThread is already non-null. WebSocketClient.run `@377–415` reads one InputStream chunk, synchronously calls engine.decode, and loops. WebSocketImpl.decodeFrames `@9–59` iterates frames and calls draft.processFrame synchronously; Draft_6455.processFrameBinary `@0–11` invokes onWebsocketMessage directly; WebSocketClient.onWebsocketMessage(ByteBuffer) `@0–2` invokes Lunar onMessage directly. Lunar onMessage `@35–43` invokes channel response accept. The retained whole-class search [response-accept-callers.txt](evidence-rpc/response-accept-callers.txt) found that sole Lunar acceptance call-containing method.

**Strong inference for this shown receive path:** consecutive duplicate responses cannot overlap the cache lookup/invalidate interval, because response acceptance completes on the same receive thread before decoding the next frame/chunk. Scheduling the successful callback to Minecraft occurs after invalidation. The channel still has a non-atomic API and no universal concurrent exactly-once contract; unmodeled reflective/external/manual concurrent invocation is outside this proof. [WebSocketClient$WebsocketWriteThread.javap.txt](evidence-rpc/WebSocketClient$WebsocketWriteThread.javap.txt) contains output-queue writing/error handling, not a parallel response decoder.

## S6-RPC-04 — G-17: ownership resolved; discarded-instance collection remains conditional

**Confirmed.** Transport constructor `@40–49` allocates a new channel with this transport; all stubs in `@63–148` bind that channel. Callback cache is a channel field (Session 4 rpc-channel constructor `@4–26`). Each successful reconnect replacement creates a new transport then stores it in main-client field `_a75959 @45–54`; no cache transfer occurs. The bootstrap tick consumer is static and resolves the current Optional transport each time, rather than permanently capturing an old transport: transport-full `bootstrap @0–10`, `_429bf0(event) @69–77`, BootstrapMethods #13/#14.

**Confirmed limitation / Strong inference.** Main-client worker `_a61e7a @0–21` closes the old transport only when isOpen; a CONNECTING/CLOSING old instance can be replaced without this worker closing it. The inherited receive thread Runnable references its client, and the write Runnable also holds a client. Thus clearing the main-client field alone does not prove that an active old instance/cache is garbage-collectable. A completed normal close invalidates all pending entries, but late old activity/references/queued bridge callbacks and exact GC timing are **Unknown**. G-17 is partially closed, not a static proof of prompt collection or leak.

## S6-RPC-05 — Capability replies share one field

**Confirmed.** The Tebex and PayNow capability response methods both write the same `EmbeddedCheckoutSupport _5e258b` field at `@55`; constructor `@158–162` initializes it UNSPECIFIED. The two requests are issued sequentially by `_6ee63a` but no response-order enforcement is present there. **Strong inference:** if their returned support enums differ, the last processed response wins the shared field. This is an implementation detail, not proof that deployed providers actually return different capabilities.

## Remaining limits and implementation guidance

G-13 is closed for the specifically requested 16 callers and their traced state/callback boundaries. No whole-program absence of pending UI state is claimed. G-14 and G-16 now have concrete static paths; real error/close timing remains runtime-gated. G-17 retains lifecycle/GC uncertainty. G-15 exact Guava maintenance timing was not re-investigated.

For an independent implementation, explicitly distinguish fire-and-forget forwarding from acknowledged actions, keep radio state refresh separate from command acknowledgement, and make checkout screen release react to transport loss as well as the normal close signal. These are suggested design choices, not claims about additional Lunar behavior. No live-service implementation or compatibility bypass is supplied.
