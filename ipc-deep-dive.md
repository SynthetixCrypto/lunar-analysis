# IPC and WebOSR deep dive

Study date: 2026-10-11. This report is static only. No socket was opened, no message was captured, and no handshake or account value was read.

Lunar has three independent communication boundaries:

| Boundary | Transport | Section |
|---|---|---|
| A. Launcher ↔ game | Loopback WebSocket carrying protobuf | 1 |
| B. Game Java ↔ in-game web UI | Ultralight JS bridge (WebOSR) | 2 |
| C. Game ↔ launcher via the process | stdout status markers and CLI arguments | 3 |

A fourth, the launcher renderer ↔ Electron main IPC, was covered by Codex. It is summarized in [launcher-internals.md](launcher-internals.md).

---

## 1. Launcher ↔ game: WebSocket and protobuf

### 1.1 Message schemas, recovered exactly (PB-01)

The game's generated protobuf classes embed their `FileDescriptorProto` as string literals in each `*Proto` class's static initializer. I read the literal order with `javap` and the bytes from the class-file constant pool, then parsed them with the Python `protobuf` 7.35.1 `descriptor_pb2` module. **No Lunar code was executed.** 21 of 21 gameipc `*Proto` classes decoded. The full dump is in [gameipc-protobuf-schema.txt](gameipc-protobuf-schema.txt) and the decoder is [session2-tools/protox.py](session2-tools/protox.py).

The envelope is `lunarclient/gameipc/protocol/v1/common.proto`:

```
message LauncherboundIPCMessage {      // game → launcher (RPC request)
  bytes  request_id      = 1;
  string service         = 2;
  string method          = 3;
  bytes  input           = 4;          // serialized request message
  string full_method     = 6;
  string input_name      = 7;
  string input_full_name = 8;          // used by launcher to pick the decoder
}
message GameboundIPCMessage {          // launcher → game
  IPCRpcResponse      rpc_response      = 1;
  google.protobuf.Any push_notification = 2;
}
message IPCRpcResponse { bytes request_id = 1; bytes output = 2; }
```

The handshake is `lunarclient/gameipc/handshake/v1/common.proto`:

```
message Handshake { string launch_id = 1; string process_id = 2; string installation_id = 3; }
```

**Services the game calls on the launcher** (descriptor `service` blocks). `Java stub` means the game client creates a stub for that service.

| Service | Methods | Java stub |
|---|---|---|
| AuthService | RefreshAccount, AddAccount (also NotifySwitchAccount and OpenMicrosoftPopup messages) | yes |
| LaunchService | LaunchGame(version, module, auto_join_server_ip, launch_source{MAIN_MENU_SWITCHER, SERVER_KICK_PROMPT, SERVER_MODPACK_RECOMMENDATION}, modpack) | yes |
| LocationService | UpdateFocus(focused), UpdateLocation(location, inbound_location) | yes |
| BrowserService | OpenUrl(url, initiator enum ×10, open_type {FORCE_EMBEDDED, FORCE_EXTERNAL}) | yes |
| TebexService / PayNowService | Check…Capabilities, Open…JsCheckout | yes |
| PromotionService | CheckPendingPromotion, PlayPromotion | yes |
| StyngrRadioService | FetchState, FetchPlaylists, StartPlaylist, NextTrack, SetPlaying/Muted/Volume, ToggleLiked, OpenSelector | yes |
| ChatService | ReceiveMessage(sender, content) | **no** |

**Pushes from the launcher** (`Any` payloads): `PlayServerPush{auto_join_server_ip}`, `ExitGamePush{}`, `FocusGamePush{}`, `PendingPromotionUpdatePush`, `TebexJsCheckoutClosed`, `PayNowJsCheckoutClosed`, `StartStorePreviewSessionPush{basket_ident, package_id}`, and `SendChatPush{message}`.

Auth message schemas are listed only by name and field type. Nothing about credentials was inspected.

**Discrepancy found.** The launcher registers a `chat` service (`../services/chat.ts`) and the protos define `ChatService`, but the Java client constructs only 8 stubs and none is for chat (JV-34). The chat service may be used by another client build, or be dormant. Not resolved.

### 1.2 Connection initialization: both ends confirmed

**Launcher server** (`bLe`, JS-07):

- `new WebSocketServer({host: "127.0.0.1", port: 28190 + k, verifyClient: () => true})`.
- On `EADDRINUSE` it retries the same port up to 5 times at 1,000 ms intervals, then moves to the next port, for at most **30 ports** (28190–28219). It then logs "Failed to find an available port after trying 30 ports."
- The bound port is stored in `this.port` and passed to the game as `--ipcPort` (fallback `28190`).

**Game client** (`L._cb9292._cfe983 extends org.java_websocket.client.WebSocketClient`, JV-34):

- URI `ws://127.0.0.1:<L.util._038392._0e3e07>`, where that field comes from `--ipcPort` (JV-26), using `Draft_6455`.
- It sends the **HTTP upgrade header** `lc-handshake: Base64(Handshake.toByteArray())`.
- Normally `launch_id = --launchId` and `installation_id = --installationId`, both parsed by the `Main` Mixin into `L.util._038392._539ac8` / `._37ebd5` (JV-26).
- If `--launchId` is `"not supplied"`, one of two things happens. When the flag `L._1e73d7._cfe983._c1461e` is set, no handshake is built and the method returns `null`. Otherwise `launch_id` falls back to `00000000-0000-0000-0000-000000000000` and `installation_id` is read from the `installation-id` file in the Lunar data directory. Its value was not read.
- `process_id` is `ProcessHandle.current().pid()`.
- The client singleton's constructor calls `_555303()`, which starts a `Thread` running `_a61e7a()`. That method closes any existing open client (`closeBlocking`), rebuilds the handshake, constructs a new `L._cb9292._cfe983`, and calls `connect()`. The same method is reused to (re)connect.

**Launcher identification** (`gLe.attemptToIdentify`, JS-06). The connection is closed with **code 4401** if any of these hold:

1. the header is missing;
2. Base64 or protobuf decoding fails;
3. `launch_id` is empty;
4. `installation_id !== this launcher's installation id`.

> **Correction to prior reports.** The `launch_id` is required to be non-empty, but it is **not** compared with the active session's ID at identification time. It is stored on the connection and used later to target pushes (`getConnectionByLaunchId`). Only `installation_id` is compared.

### 1.3 Message routing

**Game → launcher RPC** (`mLe`, JS-06):

1. `LauncherboundIPCMessage.decode`.
2. Look up the service with `services.get(service)`. The services are registered from 9 modules: auth, browser, chat, launch, location, paynow, promotion, styngr and tebex.
3. Decode the input with `messageTypeRegistry.get(input_full_name).decode(input)`.
4. Call `service[method](input)`.
5. Encode the result through its `$type`.
6. Reply with `GameboundIPCMessage{rpc_response{request_id, output}}`.

**Launcher → game push** (`sendPush`): `Any{type_url: "type.googleapis.com/<$type>", value}`, either broadcast to all clients or sent only to the connection matching a `launchId`. Pushes queued while no game is connected (`queuePush`) are flushed on the next connection.

**Game receive path** (`onMessage(ByteBuffer)`): `GameboundIPCMessage.parseFrom`, then a branch:

- `RPC_RESPONSE` completes the pending call (channel `L._cb9292._21aca6`);
- `PUSH_NOTIFICATION` unpacks the `Any` and dispatches by message class through `Map<Class, Consumer>`.

The handlers registered on open include `FocusGamePush` (focus the window), `PendingPromotionUpdatePush`, `ExitGamePush` ("Received exit game push, shutting down") and `PlayServerPush` ("connecting to %s", which needs an available session).

### 1.4 Observable error handling

| Side | Condition | Behavior |
|---|---|---|
| Launcher | Unknown service, method or response type | A warning is logged and the message is ignored. **No error response is sent**, so the game's pending RPC never completes. Strong inference: the game relies on timeouts or ignores the result. |
| Launcher | Exception in a service method | Not caught in `mLe`. It becomes an async rejection, with no reply. |
| Game | Parse failure | `"Failed to parse clientbound WebSocket message"`. |
| Game | Unexpected envelope | `"Unknown response type to consume"`. |
| Game | Close | `"Connection closed (%d, \"%s\")"`. |
| Game | Connection refused | Handled distinctly. |

---

## 2. Game Java ↔ in-game web UI (WebOSR)

### 2.1 Engine, URL and root selection: resolved (JV-28, JV-29)

`GameUI` (`L._81676d._21aca6._21aca6`) reads system properties in its static initializer:

| Property | Default | Meaning |
|---|---|---|
| `lunar.webosr.url` | `file:///index.html` | Normalized, then used as the page URL |
| `lunar.webosr.bundlePath` | `.` | Bundle path |
| `lunar.webosr.debug` | — | Debug flag |
| `lunar.webosr.noFilter` | — | Disables filtering |

Its constructor then:

1. creates a `Browser` sized to the display through an engine factory, logging "Browser Create [w, h, lh, sd, sf]";
2. calls `FunctionBus.subscribe(provider)` for the root providers;
3. calls `FunctionBus.registerChild(namespace, childBus)` for each namespaced provider;
4. calls `Browser.loadURL(url)`. Under an Ichor flag it loads `file:///none` instead;
5. starts a file-watcher helper when the URL is `file:`, which suggests hot reload in development.

**The `file:///` scheme is served by Lunar's own `FileSystem` handler** (`L._81676d._21aca6._590f69._1253fc implements com.moonsworth.webosr.handler.FileSystem`). It resolves a request path against an ordered set of root directories:

1. `L.util._038392._8d6c5d` (= `--uiDir`) and `._155716` (= `--webosrDir`). These field assignments are **confirmed** in `lunar$main$parse`, where the OptionSpec `lunar$uiDir` is stored to `_8d6c5d` and `lunar$webosrDir` to `_155716`;
2. two other launch-argument directories;
3. settings and Rewind data directories;
4. `<mcDataDir>/resourcepacks` and `<mcDataDir>/assets`.

For each request:

- a path ending in **`.imgsrc`** returns a `text/plain` payload of the form `IMGSRC-V1\n<id>`. This is the Ultralight image-source handshake used by `gameTexture` (section 2.3);
- if a root file is a **ZIP**, the entry is read from inside it, so a zipped UI bundle can be served directly;
- otherwise the file is served if it exists, then Minecraft's `ResourceManager` is tried (`bridge$getResource`);
- if all fail, it logs `WebOSR-REQ` and returns an empty `application/octet-stream` payload.

The launcher passes `--uiDir = <uiRoot>/<launch response ui.sourceSha1>` (JS-05). Combining the two sides gives the full chain:

`launch response ui.sourceSha1` → `--uiDir .lunarclient/ui/<sha1>` → FileSystem root → `file:///index.html` → `.lunarclient/ui/<sha1>/index.html`.

This chain was flagged as unresolved by Codex. Every link is now **confirmed statically**: the launcher argument, the Java option-to-field store, the FileSystem root registration and the URL default. Only the server-chosen `sourceSha1` value for a particular launch is unobserved.

### 2.2 JS → Java calls (confirmed both ends)

1. The JS `c0.invoke` calls `window.lunarInternalInvoke(namespace, method, ...args)`.
2. That function is bound by Java with `Browser.bindFunction("lunarInternalInvoke", FunctionBus)` (Codex F-11).
3. `FunctionBus` routes `namespace` to its child bus, then to the method annotated `@CallbackJS("<method>")`.
4. The return value is codec-converted, and the JS side `JSON.parse`s it.

**Settings example.** `settings.update(scope, ownerId, settingId, value)` reaches the `@CallbackJS("update")` static method (JV-16), then `Setting._d2c28f(String)`, then a save-on-change of the profile JSON file.

### 2.3 Java → JS pushes: format confirmed (JV-33)

Payloads are kept in a dirty-tracked store, `L._81676d._21aca6._d4ca6c._590f69`. Producers write into it with `_2f4182(key, value)`. Examples:

- `FeatureManager` writes `"details"` and `"features"`;
- `SettingsManager` writes `"general"`, `"performance"` and `"controls"`.

On flush, each payload is serialized with Gson and **compared with the last value sent for that key**, so unchanged payloads are not re-sent. Changed payloads are evaluated in the page with:

```
Browser.evalNoResult("window.lunarInternalAccept('" + event + "', " + json + ");")
```

The `event` value uses the template `data:<name>`. That exactly matches the JS subscription names `data:<name>` / `data:<name>-<argument>` that Codex recorded from the UI bundle (GUI-02/03). The **round-trip contract is therefore confirmed on both sides.** For a full settings update:

`JS update → Java setter → file save → payload store → lunarInternalAccept("data:features" …) → React store`

**Images.** `gameTexture` and `.imgsrc` requests are answered with `IMGSRC-V1\n<id>`. Logs such as `"Created ImageSource for …"` and `WebEngine.createImageSourceTextured` (Codex S4) show that game textures are exposed to the page as Ultralight image sources, not copied as files.

### 2.4 Input routing into the UI

`MouseHandler.onPress` first posts the Lunar mouse event (which is cancellable), then forwards the click to `GameUIRenderer._dcf582(button, action, mods)`. If the GameUI reports that it consumed the input (`_ea1304()`), the vanilla handler is cancelled (JV-23). Keyboard input follows the `KeyboardHandler` and `Screen.keyPressed` Mixins that Codex listed (`webosr$…`).

---

## 3. Process-level contract (stdout and CLI)

- **CLI:** the key set is listed in [launcher-internals.md](launcher-internals.md). `--ipcPort`, `--launchId`, `--uiDir` and `--webosrDir` connect boundaries A and B.
- **Stdout:** `LUNARCLIENT_STATUS_{PREINIT, BUILD_CACHE, SAVING_CACHE, INIT, STARTED}` are printed by Genesis and the Minecraft Mixins. The launcher's log parser uses them for progress, window hiding, success telemetry and exit classification (JS-01).

## 4. Settings synchronization summary

| Path | Mechanism | Status |
|---|---|---|
| Launcher → game | CLI arguments only (memory, resolution, flags, feature flags JSON, IDs) | Confirmed |
| Launcher → game, during play | Game settings are **not** synchronized over game IPC. The gameipc services carry account, launch, location, store, radio and promotion data only. | Confirmed by schema |
| In-game UI ↔ game | Settings flow through the WebOSR bridge, and are persisted by Java to `settings/game/<Profile>/*.json` | Confirmed |
| Launcher ↔ game settings files | The launcher has a game-settings path helper (Codex). No concurrent-write coordination with the running game was found. | Unknown |
