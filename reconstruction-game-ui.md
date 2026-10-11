# Game UI reconstruction feasibility

## What this evidence supports

**Analyst inference:** an independently written UI shell, data-driven settings interface, waypoint manager and timeline-editor front end are feasible from the documented affordances and contracts. An equivalent Minecraft client is not specified by the web UI: game hooks, rendering, replay decoding, service behavior and authoritative feature schemas remain separate obligations. The report identifies those obligations per feature below. It does not implement a reconstruction or propose copying bundled assets/code.

**Confirmed static evidence:** the exact artifact is C:/Users/Admin/.lunarclient/ui/2545e7fc28d10de3b6f9e5b8b66a4fc8931aece9/static/index.js, 8,681,743 bytes, SHA-256 e4a51091585d654dfc80f49bf9557c89712eafffb93abd5fe3894593e6b5688d. The companion HTML SHA-256 is adbbf2b1101030dd10b14ae5b4bad5b2ccd987299d7759f2326323d115a9da81. Existing inventory, launcher, Minecraft, component, startup and findings reports were reviewed and reused. This supplement concerns the game web UI.

All RG-* anchors in reconstruction-game-ui-evidence.json identify original source text spans, decoded UTF-16 character offsets and original UTF-8 byte offsets. Ranges are contextual spans rather than AST-node boundaries. The evidence file inventories 42 anchors, 61 bounded provider/model wrapper classes and 22 feature areas. Locally assigned RG/RUI IDs are supplemental, **not REA Evidence IDs**.

REA binary_session confirmed analyze_javascript_application, inspect_analysis_view and trace_javascript_semantics available before any dependent use. No new whole-bundle graph was produced: these operations do not accept a small source-span seed without first creating an application graph, and a broad 8.68 MB UI graph would add little to the focused questions. This pass used inert text inspection; an installed Acorn import was unavailable. It did not execute target JavaScript, create a browser context, retrieve URLs, inspect personal files or copy proprietary assets. **Runtime-observed behavior: none.**

## Navigation and presentation hierarchy

**Confirmed:** Qx0 (character 8,648,325; RG-01) declares a flat set of 21 URL routes, including an empty root. No nested URL hierarchy is declared in this table. eu0 wraps the routed content in shared window state, sort state, texture-ready, model-batching and overlay contexts. Panels within feature screens commonly use local React state or host events rather than nested URL paths.

| Path | Component / user-facing role | Evidence and boundary |
|---|---|---|
| / | Empty fragment | RG-01; host selects a populated screen |
| /home; /home_wrapped | vH home menu, wrapped flag | RG-38; buttons/themes/content are host supplied |
| /server_discovery | zv0 server browser | RG-27; server directory and ping/join services external to UI |
| /multiplayer_wrapped | ou0 multiplayer wrapper/announcement/discovery affordance | RG-39; host's Minecraft screen remains separate |
| /hud | rc0 FPS-only map in this route | RG-13/14; does not establish full native HUD implementation |
| /language | sc0 language search/select/reset/Unicode | RG-40; language content and font reload host supplied |
| /locker | Ad0 equipment/cosmetics catalog | RG-26; eight tabs described below |
| /emote_wheel; /spray_wheel | ua0 / gc0 radial selectors | RG-35/36; equipped/owned items and use actions host supplied |
| /marker_wheel | tu0 flags/marker selector | RG-37; marker behavior host supplied |
| /rewind | Lf0 timeline/media/property editor | RG-22/23/34; replay/render engine separate |
| /rewind_effects | bv0 text/image effect overlay | RG-24; coordinates/properties forwarded to host |
| /rewinds_list | Av0 library/projects/quick view | RG-25; recording/project formats unknown |
| /spirit_leap | hx0 dungeon-player/map interface | RG-32; live dungeon state and action implementation separate |
| /shader_cloak_editor | Nv0 shader controls and preview | RG-28; compilation/render/export implementation separate |
| /screenshot_upload | lu0 title/privacy/upload form | RG-29/41; actual image/upload flow host supplied |
| /navigator | Xx0 waypoint browser/map/groups | RG-19; map availability queried from host |
| /configure_waypoint | Ex0 / I91 edit/create waypoint/group flows | RG-20/21; route state selects existing waypoint |
| /profile_viewer | $v0 external stats iframe | RG-31; embedded SkyCrypt service supplies content |
| /profile_import | du0 Badlion/Feather import wizard | RG-30; discovery/conversion host supplied |

**Confirmed:** Jd0 listens to an overlay event independently of pathname (RG-02, near 8,127,710). Nine overlay IDs map to components: browser, friends, lockerSettings, hostedWorldsConfirmation, sbStorageOverlaySettings, accountSettings, accountSwitcher, themeSelector and socialLink. Overlay state selects/dismisses the mounted overlay. The declaration of the browser overlay alone does not establish usable browsing: its examined Od0 component initializes an iframe URL to an undefined state.

**Confirmed:** the top-level route-state fallback contains isMainMenu=true, streaming=false and creative=false. This is a frontend fallback, not observed game state. Current pathname is reported to setActiveRoute; host route events carry route/state. Host screen requests use NULL, SINGLEPLAYER, MULTIPLAYER, SETTINGS, REALMS, LANGUAGE and HOSTED_WORLD_SETTINGS declarations. Mapping these declarations onto Minecraft screens requires host implementation.

**Confirmed:** uiState supplies window records containing width, height, x, y, fullscreen and shown, plus sorts and quickNavigation order/pinned fields. eu0 maintains a local window stack and delegates window/sort changes to host callbacks (RG-33). **Inference:** this is enough to design independent persistent windows; exact persistence encoding and transaction behavior remain unknown.

## Settings schema recovered from consumers

**Confirmed:** the settings Redux initial state has empty general, performance, controls and rewind arrays and an empty features object. initSettings replaces these with host payloads. This bundle is a schema consumer; it is not a complete list of every supported mod or setting. The settings wrapper rejects a payload with missing features. option:update recursively replaces option records by ID; a missing option ID or unknown scope raises an error (RG-08/12).

Scopes are GENERAL, PERFORMANCE, CONTROLS, FEATURE and REWIND. Feature-scoped calls also carry a feature ID. The UI recursively walks children; a category may contain controls and subcategories. It supports scoped whitelists, category navigation and search over name, description, ID and badge text. ADVANCED-tagged settings are hidden unless advancedMode is enabled. Hidden options are omitted unless the renderer's showHidden flag is true (RG-03/09).

| Consumer-observed field | Meaning established by UI code | Limits |
|---|---|---|
| id, name, type | Identity, label and renderer choice | Host uniqueness and ID stability unknown |
| value, default | Current value and reset comparison; JSON.stringify equality enables/disables reset | Product defaults come from payload, not inferred from UI fallbacks |
| children | Recursive hierarchy and nested settings affordance | Complete population unknown |
| description, icon | Explanatory text and presentation | Translation/source catalog separate |
| isHidden, badges | Visibility, ADVANCED and DUPLICATE_KEY status | Host rules for setting these flags unknown |
| actionButton.text/icon | Optional action calls invokeAction with option ID | Action semantics external to UI |
| choices[].id/name/description | Dropdown/radio alternatives and labels | Complete choices and authoritative validation host supplied |
| min/max/roundTo/forceMin/forceMax | Slider bounds/step and manual-input clamping | Values are dynamic; no universal range established |
| clashesWith, ignoreClashing | Keybind conflict presentation/policy hint | Real conflict detection and game capture remain host-side |
| hue/saturation/brightness/alpha/chroma | Color editor and favorites | Host rendering/color space/chroma timing still require specification |

**Confirmed:** the S0 enum declares 20 types: button, range, slider, checkbox, toggle, date, password, radio, text, textarea, color_picker, dropdown, keybind, players, multi_number, packs, modifiable_list, inventory_slots, unknown and category. Declaration alone does not prove a renderer is implemented.

The generic settings path has seven base control mappings (checkbox, toggle, slider, dropdown, text, radio, multi_number), with game-specific keybind/color_picker mappings and recursive category handling. Unmapped generic types fall back to logging and null rendering. The separate Rewind zh0 property renderer additionally handles players, packs, date and button. This is a specialized path with keyframe/reset/visibility behavior, not proof these types work in ordinary settings (RG-03/34).

### Defaults, value encoding and validation

These are **confirmed frontend observations**, not authoritative game validation:

- Checkbox/toggle updates serialize booleans to the strings true/false. Generic displays consume option.value. Rewind checkbox controls explicitly JSON.parse their value, showing that value encoding varies by consumer.
- Dropdown/radio updates send selected choice IDs. Radio receives option.default and hideRecommended. Text updates forward strings; the generic control has no recovered domain-specific validator.
- Generic multi_number parses a JSON array, parses changed entries as floats, substitutes zero for NaN and sends JSON. Rewind uses specialized scalar/vector/pose controls and optional names/integer metadata.
- Slider pointer input clamps to min/max and rounds by step; manual input converts commas to periods, strips non-digit/non-period characters, parses on blur, rounds, and clamps when forceMin/forceMax apply. The generic wrapper passes roundTo as step and defaults both force flags to true. Display formatting is two decimals. Do not mistake those display/interaction rules for every host setting's range or precision (RG-07).
- Reset availability compares serialized value and default; reset delegates to host rather than locally replacing value. Action buttons similarly delegate. A newly written independent store can choose its own persistence and validation while honoring these UX concepts.
- Keybind editor displays modifiers/key labels and clash hints. Editing begins/stops via host capture calls. The UI does not establish the native key-code enumeration or capture arbitration.
- Color changes send JSON describing HSB/opacity/chroma. Favorites are host-supplied; pickedColor events supply sampled color. Copy/paste uses base64-encoded JSON; paste failures are caught/logged. This is an interchange affordance, not a complete authoritative color schema.
- Referenced general IDs include streamerMode, streamerModeBehaviour, playJams, advancedMode, ingameUiTransparency and showNewBubbles. Controls reference emoteWheelKeybind and sprayWheelKeybind. WAYPOINTS references waypointBeams, waypointShowDistance, highlightWaypointBlock and confirmDelete. This bounded literal-reference list is not a comprehensive settings catalog.
- The language selector synthesizes a forceUnicode toggle whose default is false. UI fallbacks such as true for waypoint beams/distance or streamer mode are fallback choices, not proof of configured or product defaults.

**Confirmed via Java metadata:** the settings CallbackJS methods are setAdvancedMode(Boolean), update(Scope,String,String,String), reset/invokeAction/setEditingKeybind(Scope,String,String), and stopEditingKeybind(). This corroborates scope/option/value/feature forwarding and string-oriented values. Exact namespace bindings and typed declarations are further documented in minecraft-ui-bridge-metadata.json and the Minecraft reconstruction supplement. They do not reveal every payload option/default.

## Host API and rendering contracts

**Confirmed Java + JS corroboration:** lunar.jar SHA-256 bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9 contains a Browser.bindFunction call binding the literal lunarInternalInvoke (recorded bytecode offsets 58 and 64 in the provider class method). Its browser listener onDocumentReady contains a bridge injection literal at bytecode offset 13. That literal defines lunarInternalAccept, lunarReady and a Proxy-backed window.lunar; subscribe/unsubscribe use a DOM event bus, and accept dispatches CustomEvent with detail payloads. Its comment explicitly references Ultralight. These findings resolve the general bridge association that was unresolved during the first UI-only pass. The exact local HTML URL/root selection remains separate.

**Confirmed:** c0.invoke(namespaceMethod,...args) calls window.lunarInternalInvoke with provider namespace, method and arguments, then attempts JSON.parse of the response and otherwise returns the raw value. Provider event names are data:<namespace> or data:<namespace>-<argument>. S2 subscribes, requests an initial payload, caches by namespace|argument, and unregisters after 250ms without subscribers. Those declarations support a host adapter design; complete error/exception, concurrency and scheduling contracts were not observed.

**Confirmed:** window.lunar provides requestPayload/unregisterPayload, subscriptions, screen/route/overlay selection, openUri, clipboard, click sound, color picking and keybind gating. UI focus/blur handlers suppress/release host keybinds; the facade tracks an authority counter and debounces updates by 16ms. Static declarations do not establish an OS process boundary here.

**Confirmed texture/model contracts (RG-15/16/17):**

1. gameTexture events carry ID/readiness. oa0 caches readiness; $f renders an img element with the source ID.imgsrc when ready. The default display flips Y and uses contain/pixelated rendering.
2. ca0 batches addModel/updateModel/removeModel JSON arrays/ID lists after 16ms, suppresses identical updates and removes stale IDs.
3. z31 sends model props, DOM width/height and zoom default 1. ResizeObserver updates geometry. Optional interactions include cosmetic hover, dragging, horizontal/vertical rotation and manual zoom. Hover reports model ID and DOM x/y; cleanup removes the model.
4. Independent Java metadata exposes TextureHandler create/resize/upload(ByteBuffer)/read/delete signatures, FileSystem.onRequest(String) returning Payload(buffer,length,mimeType,statusCode), doesResourceExist, and WebEngine.createImageSourceTextured(String). These corroborate native texture/resource extension points. The specific ID.imgsrc resolver, pixel format, thread ownership, lifetime and upload-to-frame path were not traced. Owner Thread/queue fields alone do not prove scheduling behavior.

**Inference:** a standalone reconstruction needs its own browser-to-renderer adapter and original models/textures or an independent preview system. Reproducing the DOM alone will not display the game's model/map/preview pixels.

### Focused namespace command inventory

The JSON evidence retains every recovered bounded wrapper, parameter-name signatures, literal command calls and source offsets. Minified parameter names do not establish semantic types. Conditional serialization and dynamic calls can exceed this lexical inventory; the following is a useful contract index, not a normative service specification.

| Namespace / bundle-local symbol | Confirmed literal commands | Character offset |
|---|---|---|
| hudModMetadata (ll0) | Payload/provider only in this wrapper | 7,808,810 |
| hudModProperty (al0) | Payload/provider only in this wrapper | 7,808,873 |
| mods (cl0) | Payload/provider only in this wrapper | 7,808,936 |
| rewindCreateProject (ml0) | init, updateValue, validate, rename | 7,811,313 |
| rewindDev (vl0) | goToTick | 7,811,586 |
| rewindEffects (xl0) | updateBoundingBoxes | 7,811,691 |
| rewindExport (Fl0) | updatePropertyValue, resetPropertyValue, export, setRenderRegion, addToRenderQueue, startRenderQueue, renderTimeline, removeTimeline, exportProject, exportScreenshot, downloadFfmpeg, stopRendering | 7,811,838 |
| rewindInteraction (wl0) | setAsCameraTarget, hide, nametag, skin | 7,812,651 |
| rewindMedia (yl0) | onClick, importMedia, removeMedia, newFolder, rename, moveMedia | 7,812,902 |
| rewindPacks (Ll0) | Payload/provider only in this wrapper | 7,813,301 |
| rewindProperties (_l0) | addProperty, removeProperty, setPropertyExtended, setPropertyEnabled, startPropertyUpdate, updatePropertyValue, endPropertyUpdate, handlePropertyButton, resetPropertyValue, deletePropertyValue, previousKeyframe, keyframe, nextKeyframe, setShowKeyframesInTimeline | 7,813,358 |
| rewindTimeline (bl0) | cut, addTrack, addLayer, startLayersSelection, stopLayersSelection, selectLayer, selectLayers, unselectLayer, moveLayer, moveLayers, trimLayer, setShowKeyframes, setTrackEnabled, deleteTrack, selectKeyframe, selectKeyframes, unselectKeyframe, moveKeyframe, moveKeyframes, linkLayers | 7,814,422 |
| rewindTimelinesList (kl0) | selectTimeline, editTimelineName, duplicateTimeline, deleteTimeline, newTimeline | 7,815,750 |
| rewindsList (Sl0) | create, open, openLocation, delete, getMissingMods | 7,816,130 |
| rewind (Ml0) | updatePreviewWindow, updateEditorLayout, exit, pause, save, undo, redo, goStart, goEnd, reload, setPreviewMode, setPlayhead, startPlayheadDrag, stopPlayheadDrag, clickPreview, setZoom, setRuleOfThirdsOverlay, setQuartersOverlay, showSettings, setInputFocused | 7,816,503 |
| settings (Rl0) | setAdvancedMode, update, reset, invokeAction, setEditingKeybind, stopEditingKeybind | 7,820,365 |
| uiState (zl0) | setSortState, setQuickNavigationState, setWindowState | 7,823,192 |
| waypointGroup (Nl0) | createWaypointGroup, deleteWaypointGroup, updateWaypointGroup, setWaypointGroup | 7,823,776 |
| waypointImportExport (Vl0) | copyWaypoints, exportWaypoints, pasteWaypoint, importWaypointsFromClipboard, importWaypointsFromFile, saveImportedWaypoints | 7,824,208 |
| waypointMap (Wl0) | setMapDimensions, mapDrag, mapZoomBy, resetMapInteraction, resetMapInteractionZoom, showMap | 7,824,805 |
| waypointModImport (Zl0) | searchForWaypoints, importWaypoints | 7,825,267 |
| waypointSort (Ul0) | updateWaypointSortIndexes, setActiveSortIndex | 7,825,500 |
| waypointUtility (Kl0) | requestColor, showAddWaypoint | 7,825,728 |
| waypoints (Gl0) | setEnabled, editWaypoint, toggleVisibility, deleteWaypoint, teleportToWaypoint, addWaypoint | 7,825,906 |

## HUD, waypoints and Rewind details

**Confirmed HUD limit:** fi0 filters mod descriptors by enabled && allowed. rc0's examined /hud renderer maps only the ID fps to tc0; tc0 consumes hudModProperty(fps) and hudModMetadata(fps), displays FPS and position/scale labels, and positions the element by anchor/x/y. ec0 has left/center/right and top/middle/bottom anchoring cases. The descriptor's scale is displayed by this component; a full generic scale/editor implementation is not demonstrated. Other Minecraft/native HUD rendering may exist outside this route. It would be incorrect to infer an exhaustive HUD/mod feature catalog from this single web route.

**Confirmed waypoint model:** reducer payloads include waypoints keyed by server and world, groups, active server, loaded world, knownDimensions and active sort index. Navigator filters across selected servers, dimensions, groups and death waypoints and aggregates counts. Editors expose name, group, coordinates/world, dimension and text/beam/highlight/distance/icon/color. Set to current obtains host player location. Waypoint name rejects zero length; group save requires trimmed nonblank name. Numeric input normalizes commas and transient negative/decimal forms; save coerces invalid/empty forms to zero. The editor requires a color object before sending addWaypoint. None of this establishes host uniqueness, valid coordinate bounds or permission rules.

Groups can override member display options and optionally delete their waypoints on group deletion. confirmDelete affects the UI confirmation path. Import/export/clipboard/mod-import and teleport exist as host calls; file encodings, mod conversion and actual game commands are unresolved. Map size/drag/zoom values are floored before host calls, and showMap returns availability. The code establishes an adapter, not map projection or tile generation.

**Confirmed Rewind decomposition:** the UI separates project creation/validation, library, editor, timeline/layers/keyframes, properties, media/folders, packs, interaction targets, text/image effects and export/render queue. Playback controls include pause, start/end, playhead drag, preview mode, zoom, composition guides, undo/redo, save and reload. Timeline commands include cut/add/trim/move/link/select, track visibility and keyframes. Properties expose keyframe navigation/reset/delete/visibility and transaction-style start/end update calls. Text/image effect bounds come from DOM rectangles and are sent to the host.

Library entries are host-supplied and filtered by compatibility/type/name/location; the UI can warn about missing mods before opening. Export calls include render region, queue add/start/remove, timeline render, project/screenshot export, downloadFfmpeg and stopRendering. A command name does not reveal invocation arguments, codec policy, output file encoding or recovery behavior. An independent implementation needs a separately specified replay/document/render backend; the front end alone is insufficient for recording or equivalent replay.

## Feature-by-feature sufficiency and missing details

Every affordance column below is **confirmed static**. Every sufficiency/missing judgment is **analyst inference** about an independently written implementation. No row was runtime verified, and no row authorizes using existing proprietary services/assets.

| Feature area | UI affordance found | Sufficient for independent work | Still missing for equivalent behavior | Anchors |
|---|---|---|---|---|
| RUI-01: Host shell, routes and overlays | 21 flat pathname declarations under common window/model/overlay context; nine overlay names | Independent navigation shell, readiness/error states, window state and overlay presentation | Live route/state payloads, enabled-version matrix, runtime transition order and original visual verification | RG-01, RG-02, RG-33 |
| RUI-02: General/performance/control/feature settings | Hierarchical category/search UI with host-supplied options, reset, advanced mode and action buttons | Generic data-driven settings interface and an independent settings store | Complete feature catalog, per-version schemas, authoritative defaults/ranges/validation, setting effects and migrations | RG-03, RG-08, RG-09, RG-12 |
| RUI-03: Checkbox/toggle/dropdown/radio/text/numeric controls | Mapped generic controls and reset comparison | Local controls and observed serialization conventions | Host-side validation and error payload contract; complete choice/default population | RG-04, RG-05, RG-06, RG-07 |
| RUI-04: Keybind and color tools | Capture-mode/conflict UI; HSB/alpha/chroma, saved colors and picker/copy/paste | Independent keybind editor and color editor with chosen local storage | Actual game key codes/capture authority/conflict policy, sampled-color source, complete chroma behavior | RG-10, RG-11, RG-12 |
| RUI-05: HUD and mod metadata | Enabled/allowed mod filtering; /hud contains an fps renderer using property and metadata providers | Basic independent FPS display and metadata adapter | Full mod list/behavior, generic HUD editor, actual layout/scale semantics and game frame metrics | RG-13, RG-14 |
| RUI-06: Game textures and 3D previews | id/ready event gate, id.imgsrc image source, batched model lifecycle and geometry/hover updates | Independent renderer adapter interface and placeholder/own-model preview | Concrete image-source resolver, texture ownership/lifetime/pixel formats, animation assets, mesh/model semantics and host rendering | RG-15, RG-16, RG-17 |
| RUI-07: Waypoint navigator and groups | Server/group/dimension/death filters, counts, sorting, visibility, add/edit/delete, group overrides | Independent waypoint CRUD/list/group/filter UI | Persistence format/versioning, authoritative identities/uniqueness, world/server matching and actual in-world rendering | RG-18, RG-19, RG-20, RG-21 |
| RUI-08: Waypoint maps/import/export/teleport | Host map availability, size/drag/zoom/reset; file/clipboard/mod imports and teleport call | Independent map/input adapter and import dialog using a newly specified format | Map tiles/projection and renderer, supported import formats/conversion, game permission/capability enforcement and command behavior | RG-18, RG-19 |
| RUI-09: Rewind library and project creation | Compatible/all/project/rewind filters, name/location search, missing-mod warning, validate/rename/open/delete/location | Independent media/project catalog UI with custom validation | Recording/project file formats, compatibility rules, required-mod semantics, file discovery and migration | RG-22, RG-25 |
| RUI-10: Rewind editor, timeline and keyframes | Tracks/layers/cut/trim/move/link/select, playhead/zoom/playback, undo/redo/save, property keyframes | Independent timeline editor front end and own document model | Replay recording/decoding, simulation/camera state, interpolation, edit transaction history and clock semantics | RG-22, RG-23, RG-34 |
| RUI-11: Rewind effects, media and export | Text/image effect bounds, media folders/import/rename/move; render region/queue/export/FFmpeg download commands | Independent effect/media controls and export UX specification | Composition/render backend, codec/container defaults, FFmpeg acquisition/invocation, queue recovery and output file schemas | RG-22, RG-24, RG-34 |
| RUI-12: Locker cosmetics, outfits, skins and badges | Eight tabs; favorite/seen/equip/unequip, outfits and skin actions; host model previews | Independent local catalog/equipment UI using original assets | Entitlement services, ownership/availability, cosmetic formats, skins upload constraints, backend synchronization and original visual assets | RG-26, RG-17 |
| RUI-13: Emote/spray/marker wheels and jams | Host-owned/equipped lists, radial selection and use/select/wheel callbacks; marker flags; jams controls | Independent radial menus and own animation/audio selection | Animation/spray/marker implementation, slot limits and key handling in game, audio licensing/service behavior | RG-35, RG-36, RG-37 |
| RUI-14: Home/themes/radio/promotions | Host buttons, theme/addition lists, news, social prompts, wrapped UI and radio controls | Independent customizable menu/feed surface | Service payload schemas/content, theme availability, promotion reward rules and audio delivery | RG-38 |
| RUI-15: Server discovery and multiplayer wrapper | Search/autocomplete/details/ping/join/save/announcement and not-interested callbacks | Independent server browser UI with its own directory provider | Recommendation/ranking service, data freshness, server protocol ping implementation, persistence and join/error behavior | RG-27, RG-39 |
| RUI-16: Language selector | Host available/default/active languages, search, reset, forceUnicode and deferred selection call | Independent localization selector and own translations | Translation catalog, supported language metadata and game font/resource reload behavior | RG-40 |
| RUI-17: Shader cloak editor | Resolution/uniforms/shader source/types/samplers/hot reload/FPS cap/errors/preview/export | Independent shader-editor shell and own renderer integration | Shader dialect/compile pipeline, binding convention, sampler formats, host feed actions and CDN export schema | RG-28, RG-15 |
| RUI-18: Screenshot upload | Title field max32 and public/unlisted/private selection; default unlisted; host upload call | Independent upload form and privacy selector | Image acquisition/upload endpoint/schema, privacy enforcement, completion/error states and hosting policy | RG-29, RG-41 |
| RUI-19: Profile import | Badlion/Feather discovery flags/lists, selection limit maxImports and host import | Independent profile-import wizard and bounded selection behavior | Third-party formats, file discovery, conversion, source/destination compatibility and rollback/errors | RG-30 |
| RUI-20: SkyBlock profile viewer and Spirit Leap | External stats iframe; dungeon/player list and host map actions/geometry/default view | Independent stats embedding shell or own stats UI; dungeon team/menu shell | Stats service permissions/data model, dungeon map/state detection, leap implementation and game interaction constraints | RG-31, RG-32 |
| RUI-21: Friends, chat and hosted worlds | Named overlays, friends/hostedWorlds/conversations providers and command inventory | Independent contact/chat/session UI with a separately designed service | Service protocols/authorization/state machine/moderation/delivery semantics, invitation permissions and backend session management | RG-02, RG-42 |
| RUI-22: Account/settings/social overlays | Overlay names and high-level controls declared; no account material read | Independent account-switch/settings presentation with external legitimate auth integration | Authorized account/session backend, token lifecycle and provider policies; credential handling intentionally outside evidence collection | RG-02 |

## Remaining obligations

The original source map is absent at the referenced sibling location, and names are minified; offsets and bundle-local symbols are tied to this exact digest. Text searches are bounded lexical evidence, not proof of unreachable/absent functionality. Host-supplied records mean current UI code cannot alone establish all feature names, options, defaults, constraints or enabled states.

A practical independent implementation can begin with original visuals/assets and a new local state model for navigation, settings, waypoints and timeline documents. Equivalent behavior still requires explicit specifications for game integration/version coverage, native resource/texture handling, authoritative setting effects, replay formats/clock/rendering, and legitimate service interfaces. Existing Minecraft and native reports narrow interface signatures but do not fully implement those obligations. Dynamic observation could answer some UX/state questions, but none was requested or performed in this pass.
