# User-facing feature inventory

Study date: 2026-10-11. Continuation of the six existing reports. **No implementation or runtime observation.** This inventory is comprehensive within the inspected static UI/API/settings/class/localization scope; it is not a claim to list every active Lunar feature or its complete behavior.

## Reading the evidence

**C** = confirmed shipped declaration, source operation or classfile observation. **I** = inferred responsibility/independent design. **U** = unknown. No item is runtime-observed. A route, identifier, method or option proves an affordance/contract more strongly than successful end-to-end functionality.

Readiness **A** means a bounded independent implementation can be specified using the evidence plus explicit new design choices. **B** means partial UI/interface/framework evidence; host requirements remain. **C** means remote service/content/authorization dependence. **D** means name/catalog evidence only. These are planning ratings, not recovered-source completeness.

## Catalog scope and sources

| Inventory | Confirmed quantity / boundary | Evidence |
|---|---|---|
| Launcher preload | 353 distinct literal channel names; 356 matched literal call sites in supplemental scan; REA reports 365 IPC operations including dynamic cases | reconstruction-preload-channels.json; reconstruction-preload-rea-summary.json |
| Launcher routes | 70 literal declarations, 36 distinct literals including relative children/redirects; not 70 unique screens | LRF-ROUTES, reconstruction-launcher-features.json |
| Launcher settings | 113 registered IDs with store paths/default expressions; 12 groups traced more deeply | LRF-DEFAULTS and controls/settings arrays in launcher JSON |
| Game UI routes/overlays | 21 flat routes including blank root; nine overlay IDs | RG-01/02, reconstruction-game-ui-evidence.json |
| Game UI provider/model wrappers | 60 namespace providers plus one direct model wrapper in bounded examined block | providerWrappers and coverage in game UI JSON |
| Candidate game feature catalog | 379 IDs; 348 correlate by exact strings with 353 feature-base descendants; 31 unmatched by that scan | reconstruction-minecraft-features.json |
| Feature/HUD framework | 460 feature-base descendants; 128 HUD-base/descendant classes; 159 setting-class records | confirmedFramework and counts in Minecraft feature JSON |
| Localization metadata | 5,780 leaf key names, without translation values | localizationKeyNames in Minecraft feature JSON |

Counts are overlapping inventories, not additive feature totals. Child, legacy, debug, specialized and service-backed entries occur. The appendix preserves every candidate ID and its individual readiness. Proprietary images, models, fonts, translated text and application files are not delivered for reuse.

## Launcher features

Every action below is **C at the declaration/interface level**. User-facing interpretation and readiness are I. “A” applies to new local behavior, not exact private file/network compatibility.

| ID | Feature / concrete actions | Evidence | Independent readiness / missing requirements |
|---|---|---|---|
| LF-01 | Launchpad, current profile, launch/progress/cancel and running state | launch:*; LRF-STATUS-PROGRESS/PHASES | A; state/phase contracts traced; races/runtime outcomes untested |
| LF-02 | Version/subversion/module/branch selection, vanilla/snapshot areas | profiles:selectLunarVersion/selectVanillaVersion; metadata:*; LRF-VERSION-SELECT | A selector; B/C current metadata/catalog and complete version compatibility |
| LF-03 | Profile create/clone/select/delete/rename/description/image/reset | profiles:*; LRF-PROFILE-CREATE/CLONE/NAME/FIELDS | A local manager; B precise DB/migration/image edge cases |
| LF-04 | RAM allocation/recommended warning and per-profile override | setAllocatedMemory; LRF-RAM/MEMORY-* | A; threshold/default methods traced; hardware suitability not measured |
| LF-05 | Resolution/fullscreen/aspect ratio/preset/visualizer | setGameResolution; LRF-RESOLUTION/UI/PROFILE-RESOLUTION | A; global/profile validators differ; choose independent consistent policy |
| LF-06 | JVM arguments/GC/environment/prelaunch/wrapper/postexit/detach | profile setters; LRF-ADVANCED-UI/ENV-UI/SPAWN-HOOKS | A; new validation/ownership policy required; personal configured commands unread |
| LF-07 | Profile game directory, content counts/list/import from Minecraft folders | profiles:*GameDirectory/*Content; externalImport:* | A basic local flows; B import collision/override/transaction semantics |
| LF-08 | Local mod list/add/remove/toggle/import and compatibility preview | profiles:*Mods/previewModCompatibility; LRF-PRELOAD-PROFILES | A file lifecycle; B dependency/conflict solver; REA trace proves boundary only |
| LF-09 | Resource packs/shaders: local add/toggle/import/reveal and provider install/uninstall | profiles:*ResourcePack/*Shader; provider methods | A local subset; B version/provider compatibility |
| LF-10 | Modrinth/CurseForge browse/search/project/files/dependencies/organization views | modrinth:*; curseforge:*; /explore routes | B/C; verify independent provider interfaces/data and error contracts |
| LF-11 | Provider modpack install/update/reset/skip/detach/migrate and pack divergence | provider/profile/misc interfaces; LRF-LAUNCH-GATES | B; format/solver/merge/rollback semantics incomplete |
| LF-12 | Install progress/cancel/settle | installs:*; LRF-INSTALL-CANCEL/INSTALL-MODULE | A lifecycle; rollback and cancellation latency U |
| LF-13 | Profile/content export/import and resume verification prompts | profiles:export/import/importDawnpack/resume*Import | B; complete format/trust/migration semantics incomplete |
| LF-14 | World discovery/import/folder access and datapack add/toggle/remove/import | worlds:* | A defined local subset; cross-version/import policies B |
| LF-15 | Server lists/favorites/ping/import/reorder and quick join | servers:*; LRF-LAUNCH-GATES | A local list/ping; B game-side join/version-pack resolution; C curated directory |
| LF-16 | Account add/device-login/cancel/switch/remove | auth:* | B/C; authorized account integration independently verify; secrets uncollected |
| LF-17 | Skins upload/reset/saved/history/presets, cape select/hide | auth skin/cape calls; /skin-changer | A local library; B/C account mutations/remote ownership |
| LF-18 | Screenshot library/save/rename/delete/favorite/copy/reveal | screenshots:*; /screenshots | A local subset; editor/thumbnail/upload details B |
| LF-19 | Notes create/list/search/read/write/rename/move/lock/restore/export/remove | notes:* | A with new storage/lock/backup policies; exact semantics partial |
| LF-20 | Friends requests/remove/status/pins/chat | friends:* | C end-to-end; A/B shell; own backend required for independent service |
| LF-21 | Conversations/messages/participants/owner/name/icon/pins/policies/GIF search | conversation:* | C delivery/backend; UI/API names do not specify persistence/moderation |
| LF-22 | Notification inbox/read/delete/actions/native notifications | notifications:*; notification settings | A local notifications; C remote inbox/push data |
| LF-23 | Music playlists/play/next/stop/progress/preferences and radio settings | styngr:* and radio keys | C content/service; media/rights/runtime behavior unresolved |
| LF-24 | Promotion play/complete/no-fill/shutdown and store/checkout integration | promotions:*; checkout module/HTML | B/C; flow/backend/content/entitlements not reconstructed |
| LF-25 | Settings search/categories/advanced visibility/reset and shortcuts | settings:*; LRF-SEARCH/KEYBINDS/UI-CATEGORIES | A generic editor; per-key validation/control coverage partial |
| LF-26 | Privacy/notifications/language/Discord/rich-presence preferences | 113 settings and socials:* | A local preferences; C remote enforcement/linking/presence |
| LF-27 | Mission Control/Satellite/embedded browser/wiki/window controls | windows:*; LRF-WINDOW-DEFAULTS/AFTERLAUNCH-UI | A auxiliary shells; B full content/telemetry/browser behavior |
| LF-28 | Log archive/list/search/delete/upload, debug export and diagnostic fixes | logs:*; misc:*Fix/*Debug | A own diagnostics; B repair algorithms; C upload service |
| LF-29 | Disk usage/reclaim/clear caches/unreferenced files/profile leftovers/retention | metadata:*Storage/*Cache; misc:clearCache; retention keys | A new cleanup policy; B exact reference tracking/recovery |
| LF-30 | Launcher update/restart/stream/branch/startup/tray/after-launch visibility | updater module, misc:*; LRF-STATUS-PROGRESS | A own updater; HIDE is triggered by STATUS_INIT subject to promotion/window conditions |
| LF-31 | News/post/read/guest/announcement/recent-search/explore cache | cache:* | A local state; C remote content source |
| LF-32 | License/about/terms/consent links and external/deep links | metadata:getLicenses/acceptTerms; cmp:*; misc:* | A own product UX; C external content; exact policy flow incomplete |
| LF-33 | Other-client/Overwolf integration and developer/test affordances | badlion:*; electron:isOverwolf; module/route inventory | B/C, low priority; presence does not establish normal launch use; no anti-cheat/protection behavior investigated |

Full literal operations, grouped by namespace and with offsets, are in [reconstruction-preload-channels.json](reconstruction-preload-channels.json). This preserves individual API affordances beyond the grouped rows.

## Launcher UI structure, settings and launch flow

**C:** main routes cover launchpad /, guest, servers/tab, version lists/details (Lunar/vanilla/modpacks/user-modpacks/other-client), child mods/gallery/resourcepacks/shaders/datapacks/worlds/servers, provider explore/detail description/gallery/changelog/versions, skins and screenshots. Full routes and offsets are in LRF-ROUTES. Relative literals must be interpreted in their declared parent; the distinct-literal count is not a fully resolved route count.

Settings categories in command search include game/general/notifications/storage/discord/privacy. Selected controls include memory slider/recommendation/override, resolution inputs/fullscreen/aspect/presets, enum selects, toggles, JVM/command text areas, environment key/value lists and shortcut capture/swap. All 113 IDs/default expressions/storage paths are in [launcher setting table](reconstruction-launcher-features.md) and its JSON.

Important **C static details**:
- The base setter transforms then persists/updates Redux; most traced transforms are pass-through, so no universal validation schema is recovered.
- Profile rename trims, requires nonempty <=32 characters and case-insensitive uniqueness.
- Global resolution rejects nonpositive dimensions; the inspected profile override setter writes directly.
- allocated-memory table literal1024 is overridden by a recommendation method. Runtime/user/profile values were not read.
- Keybind conflict/swap and restart-pending contracts are present. Source-declared defaults/options are not effective runtime defaults.

The Lunar launch code orders: metadata/profile gates → launch request → optional pack install/re-request → parallel licenses/textures/assets/artifacts+natives/JRE/UI preparation (artifacts then natives within one substage) → validation/Fabric checks → args/hooks → spawn → stdout INIT/optional BUILD_CACHE/STARTED statuses. Cancel aborts the session; registered process handler destroys streams and kills the child. Exact outcomes/races remain unobserved. See LRF-LUNAR-PIPELINE/STAGE-EXECUTION/PROCESS-WIRING/EXIT and [startup-flow.md](startup-flow.md).

## Minecraft-side framework and capability groups

**C:** feature base declares enabled/isEnabled/updateEnabled/load(JsonObject)/handle(Class,Consumer), with priority/Runnable overloads. HUD base declares x/y/width/height floats and scale accessors. Typed setting classes expose default values, codecs and numeric-bound builders. Exact obfuscated symbols and member descriptors are preserved in [reconstruction-minecraft-features.md](reconstruction-minecraft-features.md) and its JSON.

**I:** this supports a new feature/event/config/HUD framework. It does not establish full registration order, cleanup, event delivery, per-feature algorithms/defaults or serialization.

| Planning category | Candidate IDs | Correlation/readiness |
|---|---:|---|
| Common HUD/data display | 42 | 28 class-correlated IDs have partial contracts suitable for fresh small-feature specifications; remaining child/unmatched IDs are not complete features |
| Domain/server/service related | 212 | Algorithms/data/state/service/version requirements mostly missing |
| Rendering/input/UI related | 97 | Shared interfaces/IDs, not recovered rendering/input implementations |
| Debug/specialized scope-excluded inventory | 28 | Names preserved; behavioral investigation excluded |

Categorization is **I based on identifiers and correlations**, not authoritative product taxonomy. All 379 IDs appear below. No feature is marked behaviorally complete.

## Game UI routes, controls and feature workflows

**C:** Qx0 declares 21 flat routes including a blank root; shared wrappers manage UI windows/sorts/texture readiness/model batching/overlays. Overlay selection is separate from pathname. Host events route/set screen and receive current pathname. Host window records contain width/height/x/y/fullscreen/shown.

**C:** settings initial arrays/features are empty and are supplied by Java host payloads. Scopes GENERAL/PERFORMANCE/CONTROLS/FEATURE/REWIND; options have identity/type/value/default, recursive children, choices, visibility/badges and action metadata. Slider min/max/rounding, keybind clashes, colors and other fields are consumer-observed schema, not complete authoritative validation.

The enum declares 20 types. Generic paths implement checkbox/toggle/slider/dropdown/text/radio/multi_number, game keybind/color_picker and recursive category. Specialized Rewind additionally handles players/packs/date/button. Other enum types do not prove ordinary settings support. Reset compares payload value/default; complete per-feature defaults/options remain host-side. See RG-03/08/09/12/34.

Game UI feature-area rows below are derived from the 22 evidence-qualified assessments in reconstruction-game-ui-evidence.json. “Enough” identifies the bounded independent UI work; it does not include the missing host obligations.


| ID / area | Confirmed affordance | Enough for independent UI (I) | Missing end-to-end host behavior | Anchors |
|---|---|---|---|---|
| RUI-01 / Host shell, routes and overlays | 21 flat pathname declarations under common window/model/overlay context; nine overlay names | Independent navigation shell, readiness/error states, window state and overlay presentation | Live route/state payloads, enabled-version matrix, runtime transition order and original visual verification | RG-01; RG-02; RG-33 |
| RUI-02 / General/performance/control/feature settings | Hierarchical category/search UI with host-supplied options, reset, advanced mode and action buttons | Generic data-driven settings interface and an independent settings store | Complete feature catalog, per-version schemas, authoritative defaults/ranges/validation, setting effects and migrations | RG-03; RG-08; RG-09; RG-12 |
| RUI-03 / Checkbox/toggle/dropdown/radio/text/numeric controls | Mapped generic controls and reset comparison | Local controls and observed serialization conventions | Host-side validation and error payload contract; complete choice/default population | RG-04; RG-05; RG-06; RG-07 |
| RUI-04 / Keybind and color tools | Capture-mode/conflict UI; HSB/alpha/chroma, saved colors and picker/copy/paste | Independent keybind editor and color editor with chosen local storage | Actual game key codes/capture authority/conflict policy, sampled-color source, complete chroma behavior | RG-10; RG-11; RG-12 |
| RUI-05 / HUD and mod metadata | Enabled/allowed mod filtering; /hud contains an fps renderer using property and metadata providers | Basic independent FPS display and metadata adapter | Full mod list/behavior, generic HUD editor, actual layout/scale semantics and game frame metrics | RG-13; RG-14 |
| RUI-06 / Game textures and 3D previews | id/ready event gate, id.imgsrc image source, batched model lifecycle and geometry/hover updates | Independent renderer adapter interface and placeholder/own-model preview | Concrete image-source resolver, texture ownership/lifetime/pixel formats, animation assets, mesh/model semantics and host rendering | RG-15; RG-16; RG-17 |
| RUI-07 / Waypoint navigator and groups | Server/group/dimension/death filters, counts, sorting, visibility, add/edit/delete, group overrides | Independent waypoint CRUD/list/group/filter UI | Persistence format/versioning, authoritative identities/uniqueness, world/server matching and actual in-world rendering | RG-18; RG-19; RG-20; RG-21 |
| RUI-08 / Waypoint maps/import/export/teleport | Host map availability, size/drag/zoom/reset; file/clipboard/mod imports and teleport call | Independent map/input adapter and import dialog using a newly specified format | Map tiles/projection and renderer, supported import formats/conversion, game permission/capability enforcement and command behavior | RG-18; RG-19 |
| RUI-09 / Rewind library and project creation | Compatible/all/project/rewind filters, name/location search, missing-mod warning, validate/rename/open/delete/location | Independent media/project catalog UI with custom validation | Recording/project file formats, compatibility rules, required-mod semantics, file discovery and migration | RG-22; RG-25 |
| RUI-10 / Rewind editor, timeline and keyframes | Tracks/layers/cut/trim/move/link/select, playhead/zoom/playback, undo/redo/save, property keyframes | Independent timeline editor front end and own document model | Replay recording/decoding, simulation/camera state, interpolation, edit transaction history and clock semantics | RG-22; RG-23; RG-34 |
| RUI-11 / Rewind effects, media and export | Text/image effect bounds, media folders/import/rename/move; render region/queue/export/FFmpeg download commands | Independent effect/media controls and export UX specification | Composition/render backend, codec/container defaults, FFmpeg acquisition/invocation, queue recovery and output file schemas | RG-22; RG-24; RG-34 |
| RUI-12 / Locker cosmetics, outfits, skins and badges | Eight tabs; favorite/seen/equip/unequip, outfits and skin actions; host model previews | Independent local catalog/equipment UI using original assets | Entitlement services, ownership/availability, cosmetic formats, skins upload constraints, backend synchronization and original visual assets | RG-26; RG-17 |
| RUI-13 / Emote/spray/marker wheels and jams | Host-owned/equipped lists, radial selection and use/select/wheel callbacks; marker flags; jams controls | Independent radial menus and own animation/audio selection | Animation/spray/marker implementation, slot limits and key handling in game, audio licensing/service behavior | RG-35; RG-36; RG-37 |
| RUI-14 / Home/themes/radio/promotions | Host buttons, theme/addition lists, news, social prompts, wrapped UI and radio controls | Independent customizable menu/feed surface | Service payload schemas/content, theme availability, promotion reward rules and audio delivery | RG-38 |
| RUI-15 / Server discovery and multiplayer wrapper | Search/autocomplete/details/ping/join/save/announcement and not-interested callbacks | Independent server browser UI with its own directory provider | Recommendation/ranking service, data freshness, server protocol ping implementation, persistence and join/error behavior | RG-27; RG-39 |
| RUI-16 / Language selector | Host available/default/active languages, search, reset, forceUnicode and deferred selection call | Independent localization selector and own translations | Translation catalog, supported language metadata and game font/resource reload behavior | RG-40 |
| RUI-17 / Shader cloak editor | Resolution/uniforms/shader source/types/samplers/hot reload/FPS cap/errors/preview/export | Independent shader-editor shell and own renderer integration | Shader dialect/compile pipeline, binding convention, sampler formats, host feed actions and CDN export schema | RG-28; RG-15 |
| RUI-18 / Screenshot upload | Title field max32 and public/unlisted/private selection; default unlisted; host upload call | Independent upload form and privacy selector | Image acquisition/upload endpoint/schema, privacy enforcement, completion/error states and hosting policy | RG-29; RG-41 |
| RUI-19 / Profile import | Badlion/Feather discovery flags/lists, selection limit maxImports and host import | Independent profile-import wizard and bounded selection behavior | Third-party formats, file discovery, conversion, source/destination compatibility and rollback/errors | RG-30 |
| RUI-20 / SkyBlock profile viewer and Spirit Leap | External stats iframe; dungeon/player list and host map actions/geometry/default view | Independent stats embedding shell or own stats UI; dungeon team/menu shell | Stats service permissions/data model, dungeon map/state detection, leap implementation and game interaction constraints | RG-31; RG-32 |
| RUI-21 / Friends, chat and hosted worlds | Named overlays, friends/hostedWorlds/conversations providers and command inventory | Independent contact/chat/session UI with a separately designed service | Service protocols/authorization/state machine/moderation/delivery semantics, invitation permissions and backend session management | RG-02; RG-42 |
| RUI-22 / Account/settings/social overlays | Overlay names and high-level controls declared; no account material read | Independent account-switch/settings presentation with external legitimate auth integration | Authorized account/session backend, token lifecycle and provider policies; credential handling intentionally outside evidence collection | RG-02 |

### Game route and overlay index

| Route | Source UTF-16 offset in exact hashed game UI bundle |
|---|---:|
| `/` | 8649628 |
| `/home` | 8649678 |
| `/home_wrapped` | 8649734 |
| `/server_discovery` | 8649798 |
| `/multiplayer_wrapped` | 8649857 |
| `/hud` | 8649919 |
| `/language` | 8649965 |
| `/locker` | 8650016 |
| `/emote_wheel` | 8650065 |
| `/rewind` | 8650119 |
| `/rewind_effects` | 8650168 |
| `/rewinds_list` | 8650225 |
| `/spirit_leap` | 8650280 |
| `/marker_wheel` | 8650334 |
| `/shader_cloak_editor` | 8650389 |
| `/screenshot_upload` | 8650451 |
| `/spray_wheel` | 8650511 |
| `/navigator` | 8650565 |
| `/configure_waypoint` | 8650617 |
| `/profile_viewer` | 8650678 |
| `/profile_import` | 8650735 |

Overlays (C declarations): `browser`, `friends`, `lockerSettings`, `hostedWorldsConfirmation`, `sbStorageOverlaySettings`, `accountSettings`, `accountSwitcher`, `themeSelector`, `socialLink`. The examined browser overlay initializes an undefined iframe URL; a declared overlay does not establish working browsing.

### Provider namespace index

These are bounded static wrapper contracts, not a list of active services. Complete parameter signatures, property candidates and offsets are in the game UI JSON.

| Namespace / wrapper | Explicit host commands |
|---|---|
| accounts / zs0 | addAccount; removeAccount; selectAccount |
| analytics / Ns0 | submit |
| friends / Vs0 | addFriend; removeFriend; setFriendRequests; acceptFriendRequest; denyFriendRequest; setVisibilityStatus; setLastSeenVisibility; setIncomingGiftPrivacy; setPinnedFriend; setCosmeticOwnershipVisibility; join |
| hostedWorlds / Ws0 | inviteFriend; kick; promote; demote; onModalCallback |
| assetsClient / Zs0 |  |
| badges / Us0 | equip |
| colors / Ks0 | add; remove |
| conversations / Gs0 | refreshConversations; getConversations; unfocusConversations; sendConversationMessage; preSendAction; loadConversationAnchor; loadConversationBefore; loadConversationAfter; loadConversation; loadConversation; createConversation; deleteConversation; deleteConversationMessageHistory; deleteConversationMessage; updateConversationOwner; addConversationParticipants; removeConversationParticipant; updateConversationName; updateConversationIcon; pickGroupIconForPreview; uploadPendingGroupIcon; pickChatImagesForPreview; uploadPendingChatImages; loadPinnedMessages; addPinnedMessage; removePinnedMessage; setInvitePolicy; setNamePolicy; setIconPolicy; setMessagePinningPolicy; getUploadUrls; searchGifs |
| cosmetics / $s0 | updateCosmeticOption; requestData; getCosmeticData; sync; updateContext; markAllAsSeen; markAsSeen; unequipAll; toggleCosmetic; showCosmeticLocker; previewCosmetics; setCosmeticFavorite |
| emotes / Ys0 | emote; selectEmote; showEmoteLocker; unequipAll; remove; add |
| alerts / qs0 | dismiss |
| blogPosts / Xs0 | open |
| homeNavigation / Qs0 |  |
| homeRadio / Js0 | mute; setVolume; close |
| homeTheme / el0 | selectTheme; selectDefaultTheme; playSound; openWrapped; openAdvent; playSuccessSound; playFailSound; setBalloonHighscore; openStoreCoins |
| socialMedia / tl0 | openSocialMedia; unlinkSocial |
| homeButtons / rl0 |  |
| language / nl0 | selectLanguage; setForceUnicode; resetToDefault |
| lunarPlus / ol0 | setColor |
| markers / il0 | mark |
| metadata / sl0 |  |
| hudModMetadata / ll0 |  |
| hudModProperty / al0 |  |
| mods / cl0 |  |
| (direct host model calls) / dl0 | playEmote; stopEmote; addModel; updateModel; removeModel; setHighlightingEnabled; forceHighlightCosmetic; selectCosmetic; setToggleButtonHoveredState; setHoveredModel |
| notification / ul0 |  |
| outfits / Cl0 | add; delete; setDefault; setFavorite; rename |
| player / hl0 |  |
| profiles / fl0 |  |
| profileImport / gl0 | importProfiles; close |
| promotion / pl0 | playPromotion; claimReward; refresh; openMedalPromotion |
| rewindCreateProject / ml0 | init; updateValue; validate; rename |
| rewindDev / vl0 | goToTick |
| rewindEffects / xl0 | updateBoundingBoxes |
| rewindExport / Fl0 | updatePropertyValue; resetPropertyValue; export; setRenderRegion; addToRenderQueue; startRenderQueue; renderTimeline; removeTimeline; exportProject; exportScreenshot; downloadFfmpeg; stopRendering |
| rewindInteraction / wl0 | setAsCameraTarget; hide; nametag; skin |
| rewindMedia / yl0 | onClick; importMedia; removeMedia; newFolder; rename; moveMedia |
| rewindPacks / Ll0 |  |
| rewindProperties / _l0 | addProperty; removeProperty; setPropertyExtended; setPropertyEnabled; startPropertyUpdate; updatePropertyValue; endPropertyUpdate; handlePropertyButton; resetPropertyValue; deletePropertyValue; previousKeyframe; keyframe; nextKeyframe; setShowKeyframesInTimeline |
| rewindTimeline / bl0 | cut; addTrack; addLayer; startLayersSelection; stopLayersSelection; selectLayer; selectLayers; unselectLayer; moveLayer; moveLayers; trimLayer; setShowKeyframes; setTrackEnabled; deleteTrack; selectKeyframe; selectKeyframes; unselectKeyframe; moveKeyframe; moveKeyframes; linkLayers |
| rewindTimelinesList / kl0 | selectTimeline; editTimelineName; duplicateTimeline; deleteTimeline; newTimeline |
| rewindsList / Sl0 | create; open; openLocation; delete; getMissingMods |
| rewind / Ml0 | updatePreviewWindow; updateEditorLayout; exit; pause; save; undo; redo; goStart; goEnd; reload; setPreviewMode; setPlayhead; startPlayheadDrag; stopPlayheadDrag; clickPreview; setZoom; setRuleOfThirdsOverlay; setQuartersOverlay; showSettings; setInputFocused |
| savedSkins / El0 | updateSkinType; setFavorite; apply; delete; add; rename; save |
| screenshotUpload / Dl0 | upload |
| serverDiscovery / jl0 | discoverServers; searchServers; loadAutocompleteSuggestions; loadServerModal; joinServer; saveServer; openDiscovery; trackSectionNotInterested |
| serverPing / Ol0 | ping |
| settings / Rl0 | setAdvancedMode; update; reset; invokeAction; setEditingKeybind; stopEditingKeybind |
| shaderEditor / Pl0 | toggleUniform; toggleHiddenUniform; updateResolution; updateShaderType; updateStaticShader; requestCustomShader; updateMiscToggle; requestFeedAction; requestHotReload; createSampler; requestSamplerRename; requestSamplerFile; requestDeleteSampler |
| skyblock / Il0 |  |
| spiritLeap / Tl0 | setMap; sendButtonPress; sendMapPress; showMap; settings; close; setDefault |
| sprays / Hl0 | spray; selectSpray; showSprayLocker; unequipAll; remove; add |
| styngr / Bl0 | addJam; removeJam; previewJam; stopPreview |
| uiState / zl0 | setSortState; setQuickNavigationState; setWindowState; setWindowState |
| waypointGroup / Nl0 | createWaypointGroup; deleteWaypointGroup; updateWaypointGroup; setWaypointGroup |
| waypointImportExport / Vl0 | copyWaypoints; exportWaypoints; pasteWaypoint; importWaypointsFromClipboard; importWaypointsFromFile; saveImportedWaypoints |
| waypointMap / Wl0 | setMapDimensions; mapDrag; mapZoomBy; resetMapInteraction; resetMapInteractionZoom; showMap |
| waypointModImport / Zl0 | searchForWaypoints; importWaypoints |
| waypointSort / Ul0 | updateWaypointSortIndexes; setActiveSortIndex |
| waypointUtility / Kl0 | requestColor; showAddWaypoint |
| waypoints / Gl0 | setEnabled; editWaypoint; toggleVisibility; deleteWaypoint; teleportToWaypoint; addWaypoint |

## Rendering and component interactions

| Boundary | C interface / observation | I responsibility and U limits |
|---|---|---|
| Launcher renderer → main | Preload namespaced invoke/listen; Redux synchronization | Own typed service APIs can deliver same categories; payload schemas partially unresolved |
| Main → Java process | Metadata-driven runtime/args/spawn, progress/cancel/exit handlers | Own authorized launch adapter; exact Lunar response uncollected |
| Main ↔ game | 127.0.0.1 WebSocket/protobuf; selected --ipcPort; RPC/push types | Own protocol feasible; actual traffic/service semantics unobserved |
| Game → UI host | Browser.bindFunction lunarInternalInvoke; FunctionBus and injected lunarReady/lunarInternalAccept | UI/provider contracts corroborated; complete scheduling and payloads missing |
| Browser → rendering | Browser.getTexture/swapBuffers; native input/resize/focus; WebEngine.createImageSourceTextured | Independent renderer choice needed; native implementation/frame composition unknown |
| Texture upload lifecycle | TextureHandler create/resize/upload/read/delete; ByteBuffer signatures | Exact format/stride/context/thread ownership unresolved |
| Resource resolution | EngineConfig.fileSystem; FileSystem.onRequest→Payload(buffer,length,mimeType,statusCode), doesResourceExist | Interface known; exact URL→directory and .imgsrc resolver implementations unknown |
| UI model preview | Batched addModel/updateModel/removeModel, DOM bounds/zoom/hover; gameTexture{id,ready}, id.imgsrc | New model/texture producer and original content required |
| UI/input focus | Text-field focus disables host keybinds; keyboard/mouse/screen hooks | Version propagation/capture/repeat/scale behavior requires specification |

**C limitation:** the examined /hud web route maps only fps to its specialized component. This does not imply the whole client has only FPS, and does not prove the full native HUD/editor is implemented in that web route.

Typed rendering declarations are preserved in reconstruction-render-interfaces.json; JNI/native evidence in native-runtime-evidence.json. FunctionBus MAIN_ACTOR_QUEUE/consumeMainActorQueue and WebEngine.owner Thread are declarations, not proof of runtime scheduling. No native/protection behavior was executed.

## Per-identifier Minecraft catalog

This table preserves all 379 IDs once. Names are shipped localization keys, not copied display text. Correlations count exact-string links in feature-base descendants. Full class paths, constant-pool indexes, candidate setting keys and gaps are in [reconstruction-minecraft-features.json](reconstruction-minecraft-features.json).

Catalog readiness differs from A/B/C/D product-subsystem readiness: **S** partial contract suitable for a fresh small-feature specification; **P** partial interface, insufficient for behavioral reconstruction; **N** identifier-only in this bounded scan; **X** scope-excluded/debug/specialized inventory. None means complete. Defaults and per-feature validation remain U throughout.

| Identifier | Candidate subsystem (I) | Correlated classes (C) | Catalog readiness (I) |
|---|---|---:|---|
| `2D_ITEMS` | render_input_ui | 1 | P |
| `3D_SKINS` | render_input_ui | 1 | P |
| `ACTION_BAR` | render_input_ui | 1 | P |
| `ARMORSTATUS` | common_hud | 1 | S |
| `ARMORSTATUS_BARS_CHILD` | common_hud | 1 | S |
| `ARMORSTATUS_BOOTS_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_CHESTPLATE_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_HELD_ITEM_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_HELMET_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_LEGGINGS_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_OFF_HAND_HELD_ITEM_CHILD` | common_hud | 0 | N |
| `ARMORSTATUS_PROTECTION_CHILD` | common_hud | 1 | S |
| `ATTACK_INDICATOR` | render_input_ui | 1 | P |
| `AUDIO_SUBTITLES` | render_input_ui | 1 | P |
| `AUTO_TEXT_ACTIONS` | render_input_ui | 1 | P |
| `AUTO_TEXT_HOTKEY` | render_input_ui | 1 | P |
| `BETTERMAP_PRIMARY` | domain_or_service | 1 | P |
| `BETTERMAP_SECONDARY` | domain_or_service | 1 | P |
| `BLOCK_OUTLINE` | render_input_ui | 1 | P |
| `BOSSBAR` | render_input_ui | 1 | P |
| `CHAT` | render_input_ui | 1 | P |
| `CHAT_COMMAND_ALIASES_CHILD` | render_input_ui | 1 | P |
| `CHUNK_BORDERS` | render_input_ui | 1 | P |
| `CLOCK` | common_hud | 1 | S |
| `COLOR_SATURATION` | render_input_ui | 1 | P |
| `COMBO` | common_hud | 1 | S |
| `COMPANION_DEBUG` | excluded_inventory | 1 | X |
| `COOLDOWNS` | render_input_ui | 1 | P |
| `COORDINATES` | common_hud | 1 | S |
| `COORDINATES_BIOME_CHILD` | common_hud | 0 | N |
| `COORDINATES_C_CHILD` | common_hud | 0 | N |
| `COORDINATES_DIRECTION_CHILD` | common_hud | 0 | N |
| `COORDINATES_X_CHILD` | common_hud | 0 | N |
| `COORDINATES_Y_CHILD` | common_hud | 0 | N |
| `COORDINATES_Z_CHILD` | common_hud | 0 | N |
| `CPS` | common_hud | 1 | S |
| `CROSSHAIR` | render_input_ui | 1 | P |
| `CROSSHAIR_ELYTRA` | render_input_ui | 3 | P |
| `CROSSHAIR_ENEMY` | render_input_ui | 0 | N |
| `CROSSHAIR_FRIENDLY` | render_input_ui | 0 | N |
| `CROSSHAIR_NORMAL` | render_input_ui | 0 | N |
| `CUSTOM_DROPPED_ITEMS` | render_input_ui | 1 | P |
| `CUSTOM_HELD_ITEMS` | render_input_ui | 1 | P |
| `DAMAGE_TINT` | render_input_ui | 1 | P |
| `DAY_COUNTER` | common_hud | 1 | S |
| `DEBUG_TIMER_HUD` | excluded_inventory | 1 | X |
| `DIRECTION_HUD` | common_hud | 1 | S |
| `DUNGEON_SECRET_WAYPOINTS` | domain_or_service | 1 | P |
| `DUNGEON_WAYPOINTS` | domain_or_service | 1 | P |
| `ENCHANTMENT_SPRITE_TEXT_DECORATION` | render_input_ui | 1 | P |
| `ETHERWARP_PREVIEW` | domain_or_service | 1 | P |
| `F3_DISPLAY` | render_input_ui | 1 | P |
| `FOG` | render_input_ui | 1 | P |
| `FOV` | render_input_ui | 1 | P |
| `FPS` | common_hud | 1 | S |
| `FPS_DEBUG_MOD` | excluded_inventory | 1 | X |
| `FREELOOK` | render_input_ui | 1 | P |
| `GECKOLIB_DEBUG_MOD` | excluded_inventory | 1 | X |
| `GLINT_COLORIZER` | render_input_ui | 1 | P |
| `GRAVITY_STORM_PREVIEW` | domain_or_service | 1 | P |
| `GUI_SCALE` | render_input_ui | 1 | P |
| `HEIGHT_LIMIT` | render_input_ui | 1 | P |
| `HEIGHT_LIMIT_BEDWARS` | render_input_ui | 0 | N |
| `HEIGHT_LIMIT_BRIDGE` | render_input_ui | 0 | N |
| `HEIGHT_LIMIT_SERVER` | render_input_ui | 0 | N |
| `HEIGHT_LIMIT_VANILLA` | render_input_ui | 0 | N |
| `HELD_ITEM_ANIMATIONS` | render_input_ui | 1 | P |
| `HIT_COLOR` | render_input_ui | 1 | P |
| `HITBOX` | render_input_ui | 1 | P |
| `HORSE_STATS` | render_input_ui | 1 | P |
| `HURT_CAM` | render_input_ui | 1 | P |
| `HYPIXEL_BEDWARS` | domain_or_service | 1 | P |
| `HYPIXEL_BEDWARS_RESOURCE_COUNTER_CHILD` | domain_or_service | 2 | P |
| `HYPIXEL_BEDWARS_STATS_CHILD` | domain_or_service | 1 | P |
| `HYPIXEL_BEDWARS_TEAM_DISPLAY_CHILD` | domain_or_service | 2 | P |
| `HYPIXEL_BEDWARS_TIMERS_CHILD_HUD` | domain_or_service | 1 | P |
| `HYPIXEL_BEDWARS_UPGRADE_DISPLAY_CHILD` | domain_or_service | 2 | P |
| `HYPIXEL_MOD` | domain_or_service | 1 | P |
| `HYPIXEL_TPS` | domain_or_service | 1 | P |
| `INVENTORY_HUD` | render_input_ui | 1 | P |
| `INVENTORY_MOD` | render_input_ui | 1 | P |
| `INVENTORY_SEARCH` | render_input_ui | 2 | P |
| `ITEM_COUNTER` | common_hud | 1 | S |
| `ITEM_COUNTER_CHILD` | common_hud | 0 | N |
| `ITEM_CUSTOMIZER` | render_input_ui | 1 | P |
| `ITEM_DROP_PROTECTION` | render_input_ui | 1 | P |
| `ITEM_PHYSICS` | render_input_ui | 1 | P |
| `ITEM_TRACKER` | render_input_ui | 1 | P |
| `KEYSTROKES` | common_hud | 1 | S |
| `KILL_SOUND_BEDWARS_WIN_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUND_BOW_KILL_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUND_MELEE_KILL_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUND_PLAYER_KILL_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUND_ROD_KILL_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUND_THROWABLE_KILL_CHILD` | render_input_ui | 0 | N |
| `KILL_SOUNDS` | render_input_ui | 1 | P |
| `KNOCKBACK_GROUND_GRAPH` | domain_or_service | 1 | P |
| `KNOCKBACK_JUMP_TIMING` | domain_or_service | 1 | P |
| `KNOCKBACK_STATS` | domain_or_service | 1 | P |
| `KNOCKBACK_TRAINER` | domain_or_service | 1 | P |
| `LIGHT_OVERLAY` | render_input_ui | 1 | P |
| `LIGHTING` | render_input_ui | 1 | P |
| `MARKERS` | domain_or_service | 1 | P |
| `MEMORY` | common_hud | 1 | S |
| `MENU_BLUR` | render_input_ui | 1 | P |
| `MINIMAP` | domain_or_service | 1 | P |
| `MOB_SIZE` | render_input_ui | 1 | P |
| `MODS_ENABLED_DEBUG_MOD` | excluded_inventory | 1 | X |
| `MOMENTUM` | render_input_ui | 1 | P |
| `MOTION_BLUR` | render_input_ui | 1 | P |
| `MUMBLE_LINK` | domain_or_service | 1 | P |
| `NAMETAG` | render_input_ui | 1 | P |
| `NICK_HIDER` | render_input_ui | 1 | P |
| `ONE_SEVEN_ANIMATIONS_LEGACY` | render_input_ui | 2 | P |
| `ONE_SEVEN_ANIMATIONS_MODERN` | render_input_ui | 2 | P |
| `ONE_SEVEN_ITEMS_LEGACY` | render_input_ui | 2 | P |
| `ONE_SEVEN_ITEMS_MODERN` | render_input_ui | 2 | P |
| `ONE_SEVEN_VISUALS` | render_input_ui | 1 | P |
| `OPTIMIZATION_DEBUG_MOD` | excluded_inventory | 1 | X |
| `OVERLAY_MOD` | render_input_ui | 1 | P |
| `PACK_DISPLAY` | common_hud | 1 | S |
| `PACK_ORGANIZER` | render_input_ui | 1 | P |
| `PARTICLE_CHANGER` | render_input_ui | 1 | P |
| `PING` | common_hud | 1 | S |
| `PING_HUD` | common_hud | 1 | S |
| `PING_NAMETAG` | common_hud | 1 | S |
| `PLAYTIME` | common_hud | 1 | S |
| `POTION_COUNTER` | common_hud | 1 | S |
| `POTION_EFFECTS` | common_hud | 1 | S |
| `PROFILER_DEBUG_MOD` | excluded_inventory | 1 | X |
| `PVP_INFO` | render_input_ui | 1 | P |
| `PVP_INFO_HEALTH_CHILD` | render_input_ui | 1 | P |
| `PVP_INFO_MELEE_CHILD` | render_input_ui | 1 | P |
| `PVP_INFO_PROJECTILE_CHILD` | render_input_ui | 1 | P |
| `QUICKPLAY` | domain_or_service | 1 | P |
| `RADIO` | domain_or_service | 1 | P |
| `REACH_DISPLAY` | common_hud | 1 | S |
| `REPLAYMOD` | domain_or_service | 1 | P |
| `REPLAYMOD_RECORDING_INDICATOR_CHILD` | domain_or_service | 1 | P |
| `REWIND` | domain_or_service | 1 | P |
| `REWIND_HANDLERS` | domain_or_service | 5 | P |
| `REWIND_RECORDING_INDICATOR_CHILD` | domain_or_service | 1 | P |
| `SATURATION` | common_hud | 1 | S |
| `SATURATION_HUD_CHILD` | common_hud | 1 | S |
| `SCOREBOARD` | render_input_ui | 1 | P |
| `SCREENSHOT` | render_input_ui | 1 | P |
| `SCROLLABLE_TOOLTIPS` | render_input_ui | 1 | P |
| `SERVER_ADDRESS` | common_hud | 1 | S |
| `SERVER_COMMAND_CONFIG` | domain_or_service | 1 | P |
| `SHADER_DEBUG_MOD` | excluded_inventory | 1 | X |
| `SHADER_PACK_DISPLAY` | common_hud | 1 | S |
| `SHIELDS` | render_input_ui | 1 | P |
| `SHINY_POTS` | render_input_ui | 1 | P |
| `SHULKER_PREVIEW` | render_input_ui | 1 | P |
| `SKYBLOCK` | domain_or_service | 2 | P |
| `SKYBLOCK_ANGLE_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_ARMOR_DYE_COLOR` | domain_or_service | 1 | P |
| `SKYBLOCK_ARROW_POISON_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_AUTO_COPY_RARE_DROPS` | domain_or_service | 1 | P |
| `SKYBLOCK_AUTO_REQUEUE` | domain_or_service | 1 | P |
| `SKYBLOCK_BITS_SHOP_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_BLAZE_SLAYER` | domain_or_service | 1 | P |
| `SKYBLOCK_BOSS_TIMER` | domain_or_service | 1 | P |
| `SKYBLOCK_BURROW_LOCATING` | domain_or_service | 1 | P |
| `SKYBLOCK_BURROW_SHARING` | domain_or_service | 1 | P |
| `SKYBLOCK_CALCULATOR_IN_SIGNS` | domain_or_service | 1 | P |
| `SKYBLOCK_CAUGHT_CRITTERS_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_CHAT_COMMANDS` | domain_or_service | 1 | P |
| `SKYBLOCK_CHAT_WAYPOINTS` | domain_or_service | 1 | P |
| `SKYBLOCK_CHEST_LOOTED` | domain_or_service | 1 | P |
| `SKYBLOCK_CHEST_PROFIT` | domain_or_service | 1 | P |
| `SKYBLOCK_CHILD_ENABLED_DEBUG` | excluded_inventory | 1 | X |
| `SKYBLOCK_CHOCOLATE_FACTORY` | domain_or_service | 1 | P |
| `SKYBLOCK_CHOCOLATE_SHOP_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_CHOCOLATE_STATS` | domain_or_service | 1 | P |
| `SKYBLOCK_COLLECTED_SECRET` | domain_or_service | 1 | P |
| `SKYBLOCK_COMPLETED_COMMISSIONS` | domain_or_service | 1 | P |
| `SKYBLOCK_COMPOSTER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_CREATION_DATE` | domain_or_service | 1 | P |
| `SKYBLOCK_CRITICAL_DUNGEON_TEAMMATE` | domain_or_service | 1 | P |
| `SKYBLOCK_CROESUS_CHESTS` | domain_or_service | 1 | P |
| `SKYBLOCK_CROP_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_CRYSTAL_HOLLOWS_MAP` | domain_or_service | 1 | P |
| `SKYBLOCK_CUSTOM_MENU_CLICK` | domain_or_service | 1 | P |
| `SKYBLOCK_DAMAGE_SPLASH` | domain_or_service | 1 | P |
| `SKYBLOCK_DEATH_COUNTER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_DEBUG_DISPLAY_ALERT` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_GRAPHS` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_HIDE_HUD` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_HOTBAR_STACK_SIZE` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_HUD` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_HUD_INTERACTABLE` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_HUD_SCROLLABLE` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_MOD` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_RANDOM_LORE` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_RARITY_BACKGROUND` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEBUG_SECRET_CHIME` | excluded_inventory | 1 | X |
| `SKYBLOCK_DEF_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_DIANA_MOB_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_DIVAN_ALL_TOOLS_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_DNA_ANALYZER_SOLVER` | domain_or_service | 1 | P |
| `SKYBLOCK_DRAGON_FEATURES` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_BAT_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_BLESSING_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_BLOOD_CAMP_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_BREAKER` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_COLORS` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_FEEDBACK` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_HIGHLIGHT_DOORS` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_MILESTONE_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_NAMETAGS` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_PUZZLES` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_QUALITY` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_ROUTES` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_SCORE_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_TEAMMATE_HIGHLIGHT` | domain_or_service | 1 | P |
| `SKYBLOCK_DUNGEON_TIMER` | domain_or_service | 1 | P |
| `SKYBLOCK_ENCHANT_DISPLAY` | domain_or_service | 1 | P |
| `SKYBLOCK_ENCHANTS` | domain_or_service | 1 | P |
| `SKYBLOCK_END_NODE_HIGHLIGHT` | domain_or_service | 1 | P |
| `SKYBLOCK_ENDERMAN_SLAYER` | domain_or_service | 1 | P |
| `SKYBLOCK_ENHANCED_MINION_MENU` | domain_or_service | 1 | P |
| `SKYBLOCK_EXPERIMENT_SOLVERS` | domain_or_service | 1 | P |
| `SKYBLOCK_FAIRY_SOULS` | domain_or_service | 1 | P |
| `SKYBLOCK_FARMING_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_FARMING_TOOL_CROP_ICON` | domain_or_service | 1 | P |
| `SKYBLOCK_FIRE_FREEZE_TIMER` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_BAIT_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_CIRCLE_OVERLAY` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_HIDE_PLAYERS` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_HOTSPOT_LOCATOR` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_INFO_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_MARKER` | domain_or_service | 1 | P |
| `SKYBLOCK_FISHING_REEL_TIMER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_FLOOR_FOUR` | domain_or_service | 1 | P |
| `SKYBLOCK_FORAGING_BEACON_SOLVER` | domain_or_service | 1 | P |
| `SKYBLOCK_FOSSIL_EXCAVATION_SOLVER` | domain_or_service | 1 | P |
| `SKYBLOCK_GALATEA_MOB_HIGHLIGHT` | domain_or_service | 1 | P |
| `SKYBLOCK_GARDEN_PESTS` | domain_or_service | 1 | P |
| `SKYBLOCK_GEMSTONE_PROFIT` | domain_or_service | 1 | P |
| `SKYBLOCK_GIANT_HP_AT_FEET` | domain_or_service | 1 | P |
| `SKYBLOCK_GLACITE_COMMISSIONS` | domain_or_service | 1 | P |
| `SKYBLOCK_GLOWING_MUSHROOM_HIGHLIGHT` | domain_or_service | 1 | P |
| `SKYBLOCK_GRAVITY_WELL_WAYPOINTS` | domain_or_service | 1 | P |
| `SKYBLOCK_HARVEST_FEAST_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_HEALING_CIRCLE_OVERLAY` | domain_or_service | 1 | P |
| `SKYBLOCK_HEALTH_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_ARMOR` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_CHUM_BUCKETS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_EX_COOPS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_FALLING_BLOCKS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_FAR_ENTITIES` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_FOOD` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_LOTUSFISH_NAMETAG` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_MAGIC_SOUP_MESSAGES` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_MIDAS_BLOCKS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_OTHERS_GIFTS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIDE_PLAYERS_NEAR_NPC` | domain_or_service | 1 | P |
| `SKYBLOCK_HIGHLIGHT_FILLED_BZ_ORDERS` | domain_or_service | 1 | P |
| `SKYBLOCK_HIGHLIGHT_TRASH_DUNGEON_ITEMS` | domain_or_service | 1 | P |
| `SKYBLOCK_HOPPITY_EGG_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_INACTIVE_EFFIGY_DISPLAY` | domain_or_service | 1 | P |
| `SKYBLOCK_INVENTORY_BUTTONS` | domain_or_service | 1 | P |
| `SKYBLOCK_INVINCIBILITY_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_ITEM_ID_LORE` | domain_or_service | 1 | P |
| `SKYBLOCK_KEY_GUARDIAN_TIMER` | domain_or_service | 1 | P |
| `SKYBLOCK_KUUDRA` | domain_or_service | 1 | P |
| `SKYBLOCK_KUUDRA_ARMOR_STACKS_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_KUUDRA_HEALTH` | domain_or_service | 1 | P |
| `SKYBLOCK_LASSO_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_LILY_PAD_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_LIVID_SOLVER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_LOCK_MOUSE` | domain_or_service | 1 | P |
| `SKYBLOCK_MAGE_BEAM` | domain_or_service | 1 | P |
| `SKYBLOCK_MANA_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_METAL_DETECTOR` | domain_or_service | 1 | P |
| `SKYBLOCK_METAL_DETECTOR_DATA_GEN` | excluded_inventory | 1 | X |
| `SKYBLOCK_MIDDLE_CLICK_GUI` | domain_or_service | 1 | P |
| `SKYBLOCK_MINESHAFT_CORPSE_WAYPOINTS` | domain_or_service | 1 | P |
| `SKYBLOCK_MINI_BOSS_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_MINING_SPEED_BOOST_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_MUTE_BEEHEEMOTH_SOUNDS` | domain_or_service | 1 | P |
| `SKYBLOCK_MYTHOLOGICAL_RITUAL` | domain_or_service | 0 | N |
| `SKYBLOCK_NETHER_BOSS_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_PARTY_FINDER` | domain_or_service | 1 | P |
| `SKYBLOCK_PICKONIMBUS_DURABILITY` | domain_or_service | 1 | P |
| `SKYBLOCK_POWDER_TRACKER` | domain_or_service | 0 | N |
| `SKYBLOCK_POWDER_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_PRICE_IN_LORE` | domain_or_service | 1 | P |
| `SKYBLOCK_PROFESSOR_GUARDIAN_HP` | domain_or_service | 1 | P |
| `SKYBLOCK_PROFILE_VIEWER` | domain_or_service | 1 | P |
| `SKYBLOCK_PROTECT_ITEM` | domain_or_service | 1 | P |
| `SKYBLOCK_QUIVER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_RABBIT_COLLECTION_OVERLAY` | domain_or_service | 1 | P |
| `SKYBLOCK_RAFFLE_TASKS_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_RAINBOW_BELL_WAYPOINTS` | domain_or_service | 1 | P |
| `SKYBLOCK_RARITY_BACKGROUND` | domain_or_service | 1 | P |
| `SKYBLOCK_RENDER_DEBUG_BLOCK_COLORS` | excluded_inventory | 1 | X |
| `SKYBLOCK_RENDER_DEBUG_LAVA_WATER` | excluded_inventory | 1 | X |
| `SKYBLOCK_RENDER_DEBUG_UTILITIES` | excluded_inventory | 1 | X |
| `SKYBLOCK_REPLACE_LAVA_TEXTURE` | domain_or_service | 1 | P |
| `SKYBLOCK_REVIVE_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SCATHA_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SEA_CREATURE_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_SEA_CREATURE_MESSAGES` | domain_or_service | 1 | P |
| `SKYBLOCK_SEND_COORDS` | domain_or_service | 1 | P |
| `SKYBLOCK_SKELETON_HELMET_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SKILL_GLOBE_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SKILL_PROGRESS_BAR_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SKILL_PROGRESS_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SKILL_XP_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SKY_MALL_BUFF_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_SKYMART_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_SMOOTH_TELEPORT` | domain_or_service | 1 | P |
| `SKYBLOCK_SPARKLING_CRITTER_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_SPEED_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SPHINX_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_SPIDER_DEN_RAIN_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_SPIRIT_LEAP_ANNOUNCE` | domain_or_service | 1 | P |
| `SKYBLOCK_SPIRIT_LEAP_DEBUG` | excluded_inventory | 1 | X |
| `SKYBLOCK_STACKING_ENCHANTS` | domain_or_service | 1 | P |
| `SKYBLOCK_STORAGE_HOVER_PREVIEW` | domain_or_service | 1 | P |
| `SKYBLOCK_STORM_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_TAB_WIDGET_CHILD` | domain_or_service | 0 | N |
| `SKYBLOCK_TERMINAL_SOLVERS` | domain_or_service | 1 | P |
| `SKYBLOCK_TERMINAL_SPLITS` | domain_or_service | 1 | P |
| `SKYBLOCK_TERMINAL_STATUS` | domain_or_service | 1 | P |
| `SKYBLOCK_TERRACOTTA_TIMER` | domain_or_service | 1 | P |
| `SKYBLOCK_TICK_TIMER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_TITANIUM_SPAWN_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_TREASURE_CHEST_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_TROPHY_FISH_EXCHANGE_RATE` | domain_or_service | 1 | P |
| `SKYBLOCK_UNFINISHED_TERMINALS` | domain_or_service | 1 | P |
| `SKYBLOCK_VAMPIRE_SLAYER` | domain_or_service | 1 | P |
| `SKYBLOCK_VANILLA_ITEM_MODELS` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_ALERT` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_BAZAAR_HELPER` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_PROFIT` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_SHOPPING_LIST_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_VISITOR_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_VITALITY_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_WARDROBE_HOTKEYS` | domain_or_service | 1 | P |
| `SKYBLOCK_WEBSITE_ADBLOCK` | domain_or_service | 1 | P |
| `SKYBLOCK_WHISPER_TRACKER_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_WISHING_COMPASS` | domain_or_service | 1 | P |
| `SKYBLOCK_WITHER_HEALTH_HUD` | domain_or_service | 1 | P |
| `SKYBLOCK_WORM_SCATHA_ALERT` | domain_or_service | 1 | P |
| `SLOT_BINDING` | render_input_ui | 1 | P |
| `SLOT_LOCKING` | render_input_ui | 1 | P |
| `SNAPLOOK` | render_input_ui | 1 | P |
| `SOUND_CHANGER` | render_input_ui | 1 | P |
| `SPIRIT_LEAP_OVERLAY` | domain_or_service | 1 | P |
| `STAFF_XRAY` | excluded_inventory | 1 | X |
| `STARRED_MOB_HIGHLIGHT` | domain_or_service | 1 | P |
| `STOPWATCH` | common_hud | 1 | S |
| `STOPWATCH_HUD_CHILD` | common_hud | 0 | N |
| `STORAGE_OVERLAY` | render_input_ui | 1 | P |
| `TAB` | render_input_ui | 1 | P |
| `TEAM_CAKE_HIGHLIGHT` | domain_or_service | 1 | P |
| `TEAM_VIEW` | render_input_ui | 1 | P |
| `TICK_DEBUG` | excluded_inventory | 1 | X |
| `TIER_TAGGER` | render_input_ui | 1 | P |
| `TIERS_AS_STACK_SIZE` | domain_or_service | 1 | P |
| `TIME_CHANGER` | render_input_ui | 1 | P |
| `TITLES` | render_input_ui | 1 | P |
| `TNT_COUNTDOWN` | render_input_ui | 1 | P |
| `TOGGLE_SNEAK` | render_input_ui | 1 | P |
| `TOGGLE_SNEAK_HUD_CHILD` | render_input_ui | 1 | P |
| `TOTEM_ANIMATION_OVERLAY_CHILD` | render_input_ui | 2 | P |
| `TOTEM_COUNTER` | common_hud | 1 | S |
| `TOTEM_COUNTER_HUD_CHILD` | common_hud | 1 | S |
| `UHC_OVERLAY` | render_input_ui | 0 | N |
| `WAILA` | render_input_ui | 1 | P |
| `WATER_ROOM_SOLUTION_GENERATOR` | excluded_inventory | 1 | X |
| `WAYPOINTS` | domain_or_service | 1 | P |
| `WEATHER_CHANGER` | render_input_ui | 1 | P |
| `WORLDEDIT_CUI` | domain_or_service | 1 | P |
| `ZOOM` | render_input_ui | 1 | P |

### Strongest candidates for fresh small-feature specifications

`ARMORSTATUS_BARS_CHILD`, `ARMORSTATUS_PROTECTION_CHILD`, `ARMORSTATUS`, `CLOCK`, `COMBO`, `COORDINATES`, `CPS`, `DAY_COUNTER`, `DIRECTION_HUD`, `FPS`, `ITEM_COUNTER`, `KEYSTROKES`, `MEMORY`, `PACK_DISPLAY`, `PING_HUD`, `PING_NAMETAG`, `PING`, `PLAYTIME`, `POTION_COUNTER`, `POTION_EFFECTS`, `REACH_DISPLAY`, `SATURATION_HUD_CHILD`, `SATURATION`, `SERVER_ADDRESS`, `SHADER_PACK_DISPLAY`, `STOPWATCH`, `TOTEM_COUNTER_HUD_CHILD`, `TOTEM_COUNTER`.

These 28 IDs have useful shared/class evidence, not complete algorithms. Some are children/presentation variants. Independently specify metrics, event windows, units, visibility, reset/persistence and Minecraft data adapters before implementing.

## Evidence navigation

- [Launcher focused study and complete setting table](reconstruction-launcher-features.md), [launcher JSON](reconstruction-launcher-features.json).
- [Minecraft feature/base/setting study](reconstruction-minecraft-features.md), [complete feature catalog JSON](reconstruction-minecraft-features.json).
- [Game UI structure/controls/feature workflows](reconstruction-game-ui.md), [UI JSON](reconstruction-game-ui-evidence.json).
- [Subsystem feasibility](reconstruction-feasibility.md), [missing evidence](missing-evidence.md), [roadmap](development-roadmap.md).

Existing [inventory](inventory.md), [launcher architecture](launcher-architecture.md), [Minecraft architecture](minecraft-client-architecture.md), [component map](component-map.md), [startup flow](startup-flow.md) and [findings](findings.md) remain the artifact/provenance baseline. New focused findings refine earlier unresolved questions; they do not turn static declarations into observed execution.
