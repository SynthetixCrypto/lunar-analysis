# Minecraft-side web UI architecture

## Scope and evidence

This is a supplemental **read-only static** study of the installed HTML/JavaScript UI. No Lunar process, script, JVM, browser page, or native library was executed. Findings below are confirmed properties of shipped text unless explicitly marked inference. GUI-* identifiers refer to game-ui-evidence.json, not REA Evidence IDs. Native and JAR findings are documented separately.

Target root: C:/Users/Admin/.lunarclient/ui/2545e7fc28d10de3b6f9e5b8b66a4fc8931aece9.

- index.html SHA-256: adbbf2b1101030dd10b14ae5b4bad5b2ccd987299d7759f2326323d115a9da81.
- static/index.js: 8,681,743 bytes; SHA-256 e4a51091585d654dfc80f49bf9557c89712eafffb93abd5fe3894593e6b5688d.
- assets/index.css: 19,319 bytes. assets contains 48 files; static contains index.js only. Assets include PNG images, TTF fonts, and transition.ogg.
- .sha1 contains the same identifier as the directory name. The launcher-cache directory contains ui-2545e7fc28d10de3b6f9e5b8b66a4fc8931aece9.zip and uiIndex-2545e7fc28d10de3b6f9e5b8b66a4fc8931aece9.txt. The latter has 48 rows of filename, 40-hex field, length, and integer field. **Inference:** these fields are an asset integrity/version manifest; the bundle-to-launcher selection logic requires independent launcher evidence. The row count matches assets, but per-file hash verification was not performed.

Offsets below are zero-based UTF-16 character offsets into UTF-8-decoded static/index.js. The evidence JSON also records original UTF-8 byte offsets; do not confuse the two.

## Entry and initialization

**Confirmed:** index.html declares a root div, a module script /static/index.js, and /assets/index.css. It also declares Google Fonts preconnects and a Roboto stylesheet URL. The bundle contains React and react-dom production license headers and version 18.3.1 markers (GUI-01). Redux/react-redux fingerprints and a reducer-composed Z2 store are present; store construction disables Redux devTools and serializable/immutable middleware checks (GUI-04, near 7,797,833).

**Confirmed:** the final T91 function tests window.lunar && window.lunarReady before rendering. It retries after 500ms while the host is unavailable. On success, the React root renders a store provider, router wrapper, error boundary and Qx0 application (GUI-10, near 8,654,260). These are static branches and timing values, not an observed startup or measured delay.

**Inference:** the HTML app expects a hosting component to inject the Lunar bridge; it is not a self-sufficient ordinary browser page. The hosting Java/native implementation is not identified by this JavaScript alone.

## Component boundary and payload lifecycle

**Confirmed:** c0 (7,766,998) stores name, argument and event; event is data:<name> or data:<name>-<argument>. Its invoke(method,...args) calls window.lunarInternalInvoke(this.name,method,...args), then attempts JSON.parse on the returned value and falls back to the value. a4 extends c0 and is used by Redux-backed providers (GUI-02).

**Confirmed:** S2 uses a React layout effect to subscribe through R.subscribe, request an initial payload through R.requestPayload, and pass payloads to a callback. A Map caches the last payload by name|argument; subscriber counts permit reuse. Cleanup removes the listener and schedules unregisterPayload after 250ms when no subscribers remain (GUI-03). _o0 installs a4 providers and directs payloads to handleAction.

**Confirmed:** $l0 composes provider objects and delegates requestPayload, unregisterPayload, subscribe/unsubscribe, setScreen, onClick, setActiveRoute, setActiveOverlay, hideOverlay, openUri, clipboard, click sound, color-picking and setAllowKeybinds to window.lunar. invoke delegates to window.lunarInternalInvoke (GUI-08, near 7,826,655). The static code does not establish a socket, named pipe, or cross-process transport for these methods. **Inference:** this is an embedded browser host API boundary; calling it operating-system IPC would require additional evidence.

## Feature and state map

The following are **confirmed namespaces and wrappers**, not proof that all features are enabled or used by the selected Minecraft version:

| Area | Namespace / local symbols | Supporting observation |
|---|---|---|
| HUD/mod metadata | mods, hudModMetadata, hudModProperty; cl0, ll0, al0 | Factories accept per-mod arguments; mods payload dispatches a Redux action (GUI-05). |
| Settings | settings; Rl0 | Validates features payload, dispatches Fo0; wrappers update/reset/invokeAction, advanced mode and keybind editing (GUI-07). |
| Model UI | dl0 | Delegates addModel/updateModel/removeModel, cosmetic highlighting, model hover and emote commands to the host (GUI-06). |
| General UI | metadata, language, uiState, notification | Provider payloads feed store actions; uiState includes window/sort/navigation fields. |
| Social/cosmetics | friends, hostedWorlds, conversations, cosmetics, emotes, sprays, badges, outfits, savedSkins | Explicit provider construction and method wrappers. No live social/account payloads inspected. |
| Waypoints | waypoints, waypointMap, waypointGroup, waypointImportExport, waypointModImport, waypointSort, waypointUtility | Namespace-separated host calls for mapping, grouping, import/export and management. |
| Rewind | rewind plus timeline, properties, media, export, effects, dev and list providers | Explicit provider composition; timeline/edit/export wrappers. |
| Other | skyblock, spiritLeap, shaderEditor, serverDiscovery, serverPing, screenshotUpload, promotion, styngr | Explicit host namespaces. Native functionality behind these calls remains unobserved. |

**Confirmed:** Qx0 subscribes to route and option:update. The route handler navigates using event.detail.route/state; a React effect sends the current pathname to setActiveRoute. Focus on an HTMLInputElement disables host keybinds, and blur re-enables them; $l0 maintains an authority counter and debounces the host keybind state update by 16ms. A Backspace handler prevents the default outside HTMLInputElement (GUI-09, 8,648,325).

**Confirmed:** the top-level route table includes /home, /home_wrapped, /server_discovery, /multiplayer_wrapped, /hud, /language, /locker, /emote_wheel, /rewind, /rewind_effects, /rewinds_list, /spirit_leap, /marker_wheel, /shader_cloak_editor, /screenshot_upload, /spray_wheel, /navigator, /configure_waypoint, /profile_viewer and /profile_import. These strings identify UI surfaces. **Inference:** wrapped screens are integration variants; their runtime purpose was not tested.

## Rendering and native relationship

**Confirmed:** this artifact renders a DOM/React UI and defines model/overlay/route host calls. The JavaScript does not itself explain Minecraft's core OpenGL rendering or frame composition. The native supplement independently records WebOSR-Binding.dll JNI browser APIs, Ultralight dependencies and texture/input methods. **Inference:** the artifacts support an embedded browser architecture with host-rendered model capabilities. Subsequent Java classfile inspection independently confirms Browser.bindFunction with lunarInternalInvoke and document-ready injection of lunar/lunarReady/lunarInternalAccept (see minecraft-ui-bridge-metadata.json and minecraft-client-architecture.md). The exact URL-to-UI-directory selection and native rendering caller chain remain unresolved.

## Observable network dependencies

These are **static declarations**, not live requests:

- index.html declares fonts.googleapis.com and fonts.gstatic.com font resources.
- DX2/AX2/OX2 construct servermappings.lunarclientcdn.com logo/background URLs (GUI-11, 6,987,408).
- Ce1 contains img-proxy.lunarclient.com as an image proxy base (GUI-12, 7,109,384).
- A profile-viewer iframe declares skycrypt-embed.lunarclient.com/stats and sandbox permissions allow-scripts allow-forms allow-same-origin (GUI-13, 8,563,324).
- Sentry initialization contains an ingest.sentry.io endpoint, traces/replay sampling values of zero, and a production condition in beforeSend (GUI-14). Exact DSN and account-related schema are intentionally omitted. Zero tracing/replay sampling does not establish that error event sending is disabled.
- support.lunarclient.com and store.lunarclient.com occur as link destinations; occurrence alone does not prove an automatic dependency.

## Limits and unresolved questions

The bundle is minified. The referenced sibling index.js.map is absent; original source modules, stable source class names and build metadata are not recovered. Text offsets and bundle-local minified symbols are reproducible anchors for this exact SHA-256 only. No deobfuscation/protection bypass was attempted.

Subsequent Java evidence identifies the host FunctionBus binding, injected namespace and selected CallbackJS provider classes; see minecraft-ui-bridge-metadata.json. The complete callback implementation, UI URL hosting scheme, texture lifetime, render thread behavior, security boundaries and actual event payloads remain unresolved. Core Minecraft rendering/input initialization is outside the coverage of this UI bundle. No credentials, tokens, databases, logs, or account files were inspected; no remote resources were fetched.
