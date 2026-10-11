# Launcher reconstruction feature study

## Scope and evidence status

This supplement records observable shipped declarations and inferred independent implementation options. It is not an implementation, a working replacement, or evidence of feature parity. All inspected JavaScript was inert text. No application code, native addon, Java runtime or helper was executed; no service requests or runtime observations were made. Personal configs, databases, credentials and logs were not read. No proprietary UI assets are proposed for reuse.

Source: installed `C:/Users/Admin/AppData/Local/Programs/Lunar Client/resources/app.asar`, ASAR SHA-256 `506574f17a6b7aeb5a13fe5f53fc83329fa705141505dde30ec88e00aa03a9f4`; REA extraction `ev_31648b1ec89765d65a3cd9a6929cd7461fb4a5a4ab47e7da16d3ed9fbd42c71a`. The extraction used record-and-continue for the previously documented unrelated archive integrity mismatch. Source hashes below bind this report to the exact observed bytes; they do not certify package authenticity.

REA availability was checked. Focused inert preload analysis supports the IPC boundary; root summary `reconstruction-preload-rea-summary.json`, parent `ev_c9fb45d714c1de792be65a5e6a40457bc136b02c550fdbe741e5742e2d163a8e`, reports 365 IPC operations, 353 literal channels and 36 exposed API members. Relationships in this supplement use supplemental source inspection where dynamic names/minification prevent automatic pairing. No full application graph was reloaded.

| Source ASAR logical member | Bytes | SHA-256 |
|---|---|---|
| `dist-electron/electron/main.js` | 5739762 | `9781715efe843f763240bf27874f9604da9cb4a5b2959f5d6c1768a5e20540db` |
| `dist-electron/preload/launcher/index.js` | 36886 | `d487d51504aa5ea42e3dde9cf92b08bc7baf511bcd163f43aa73e28587b3631b` |
| `dist/assets/main.js` | 2118203 | `3b4f707b3ff598d84659410e40f04a5833b42459604b6f190aa8148e8e92fa46` |
| `dist/assets/use-toast-notifications.js` | 582966 | `95199dfc92324242b7f26057f3183ce3cc30aa0006dd5434b8cd5334de3dc77a` |

LRF-* references resolve to exact file hashes, excerpts, UTF-16 offsets, UTF-8 byte offsets and line/column anchors in `reconstruction-launcher-features.json`. “Confirmed” means a static declaration/control-flow observation; execution and remote selection remain unobserved.

## User-facing feature contracts

| Feature | Static evidence | Independent implementation assessment (inference) |
|---|---|---|
| Launchpad and current launch status | confirmed-static-code; LRF-ROUTES, LRF-PRELOAD-LAUNCH, LRF-STATUS-PROGRESS | Independent UI/state machine feasible using documented phase, progress and cancel semantics. Real Lunar launch metadata and proprietary game artifact compatibility remain unresolved. |
| Version/subversion/module selection for Lunar and vanilla | confirmed-static-code; LRF-ROUTES, LRF-VERSION-SELECT, LRF-LAUNCH-GATES | Independent selector/profile persistence feasible. Current supported catalog, recommended/default modules and exact launch parameters depend on metadata services. |
| User/modpack profiles, create/clone/rename and per-profile overrides | confirmed-static-code; LRF-PRELOAD-PROFILES, LRF-PROFILE-CREATE, LRF-PROFILE-CLONE, LRF-PROFILE-NAME, LRF-PROFILE-FIELDS | Local profile manager can be specified independently. Need additional migration/database schema and provider pack edge cases for exact data compatibility. |
| Global settings categories, search, advanced mode, reset, shortcuts | confirmed-static-code; LRF-SEARCH, LRF-UI-CATEGORIES, LRF-DEFAULTS, LRF-SET-VALIDATION, LRF-KEYBINDS | Independent settings UX and storage feasible using 113 declared keys and selected control contracts. Full localization/theme/validation and all control mappings remain partial. |
| RAM warning for large modpacks | confirmed-static-code; LRF-MEMORY-WARNING, LRF-MEMORY-THRESHOLD, LRF-MEMORY-RECOMMEND, LRF-MEMORY-DECISIONS | Decision/state contract and thresholds can be independently modeled without private services. |
| Mod/resource-pack/shader management and import/export | confirmed-preload-and-selected-main-code; LRF-PRELOAD-PROFILES, LRF-PROFILE-EXPORT-SCHEMA | Local file management feasible; compatibility judgments, pack merge/rollback and provider project schemas are not yet sufficient for exact reconstruction. |
| Modrinth/CurseForge explore and modpack install/update | confirmed-declarations; LRF-ROUTES, LRF-PRELOAD-PROFILES, LRF-LAUNCH-GATES, LRF-INSTALL-CANCEL | Interface and cancel/settle skeleton feasible. Requires independently documented provider APIs/licensing and pack transaction/error semantics. |
| Featured/community servers and quick join | confirmed-static-code; LRF-ROUTES, LRF-LAUNCH-GATES | Server selection and version-required prompts feasible; live catalog and game-side push fulfillment depend on separate components/services. |
| Account actions, skin changer and screenshots | confirmed-renderer/preload-declarations; LRF-ROUTES, LRF-SEARCH | UI shell independently feasible. Account/authentication protocols and screenshot editor/storage details intentionally not traced in this pass. |
| Mission Control, Satellite, resolution preview and diagnostics UI | confirmed-static-declarations; LRF-SEARCH, LRF-WINDOW-DEFAULTS, LRF-AFTERLAUNCH-UI | Independent auxiliary windows feasible. Full renderer content/ownership and live telemetry contracts remain partial. |

Confirmed renderer route declarations include launchpad `/`, `/guest`, `/servers` and `/servers/:tab`; version areas for Lunar, vanilla, modpacks, Badlion and featured versions; version detail children for mods/gallery/resource packs/shaders and explore views; global explore; skins and screenshots. The complete 70 literal route declarations (including relative child paths and redirects) are indexed in JSON. The count includes repeated/relative declarations and is not a count of 70 unique screens. LRF-ROUTES.

Confirmed command search offers settings categories game/general/notifications/storage/discord/privacy, create-profile, stations, add-account, update check, restart, about, licenses and log-related actions. Account actions depend on loaded authentication state; stream/deeplink/app-folder actions depend on advanced mode; Badlion entries depend on enablement. This is a declared action surface, not proof that every action succeeds. LRF-SEARCH.

## Settings and validation

Confirmed: 113 entries occur in both the ZA default table and ZM setting registry. The complete key, class, store-path, declared default expression and anchor index appears below and in JSON. These are code-declared defaults, not effective settings. Allocated memory, window sizes and some view/retention classes have custom default methods; migration, stored values, profile overrides and runtime metadata can change effective behavior. LRF-DEFAULTS, LRF-WINDOW-DEFAULTS.

The base setter applies a per-class transform, catches a thrown transform failure and returns without saving, checks keybind conflicts, then persists and updates Redux. Most inspected transforms simply return the supplied value. The registry does not supply a universal strict schema for all 113 settings. Renderer options/types indicate intended input shapes; they must not be described as comprehensive main-process validation. LRF-SET-VALIDATION, LRF-RESTART.

Selected controls were followed deeply:

| Key / group | Shape and control | Declared default / validation | Evidence |
|---|---|---|---|
| `allocated-memory` | Stored number in MiB; setter request {memory?: number, recommended?: boolean}; Global RAM drag/slider; profile override switch and reset | ZA table says 1024, but cwe.getDefaultValue overrides it via hj(gj(true)). Global transformGet replaces values above rounded physical memory with current recommendation. Global transformSet picks recommended, else truthy memory, else recommendation; no numeric/minimum validator is present in this method. Slider maps 0..100 to 500..metadata.totalSystemMemory decimal display units and converts through ceil(x*1.024); the global writer is debounced 300ms. | LRF-RAM, LRF-RAM-UI, LRF-PROFILE-MEMORY, LRF-RAM-CONVERSION |
| `game-resolution` | {width:number,height:number,fullscreen:boolean,lockedAspectRatio?:{lockedWidth:number,lockedHeight:number}}; Width/height text inputs; drag; arrows +/-10 or Shift +/-100; fullscreen and ratio switches; preset and visualizer | {width:1280,height:720,fullscreen:false}. Global setter throws if width<=0 or height<=0; getter parseInt converts string dimensions. UI parseInt ignores NaN, caps by current monitor and recalculates ratio. DB resolution schema checks number/number/boolean; profile setter does not use global transform. | LRF-RESOLUTION, LRF-RESOLUTION-UI, LRF-PROFILE-FIELDS, LRF-PROFILE-RESOLUTION |
| `after-launch-action` | enum HIDE / SHOW; Select | HIDE. swe transformSet is pass-through; UI offers SHOW/HIDE. | LRF-DEFAULTS, LRF-AFTERLAUNCH-UI, LRF-STATUS-PROGRESS |
| `mission-control-after-launch-action` | SHOW_ON_AVAILABLE_MONITOR / OPEN_IN_BACKGROUND / DONT_SHOW; Select | SHOW_ON_AVAILABLE_MONITOR. Options are UI declarations; pass-through setter. | LRF-AFTERLAUNCH-UI, LRF-LAUNCH-GATES |
| `game-update-preference` | NEUTRAL / OPT_IN / OPT_OUT; Select | NEUTRAL. Options are UI declarations; pass-through setter. | LRF-DEFAULTS, LRF-ADVANCED-UI |
| `include-snapshots` | boolean by control/default; Toggle | false. Pass-through setter; changing to false triggers metadata fetch in Xwe.afterSet. | LRF-ADVANCED-UI, LRF-RESOLUTION |
| `jvm-args` | string; Textarea with Enter/save; profile override switch | empty string. Pass-through main setter; launcher builds custom arguments by split on space/filter(Boolean), not a shell-quote parser in the inspected build path. | LRF-ADVANCED-UI, LRF-PROFILE-OVERRIDE-UI, LRF-LUNAR-PIPELINE |
| `environment-variables` | Array<{key:string,value:string}>; profile override stored as JSON text; Key/value list with add/remove/save/reset and profile override | []. UI filters entries whose key.trim() is empty. Main global setter is pass-through; profile setter stringifies array. Full key syntax/duplicate validation unresolved. | LRF-ENV-UI, LRF-LAUNCH-GATES, LRF-PROFILE-FIELDS, LRF-ENV-PROFILE |
| `pre-launch-command / wrapper-command / post-exit-command` | strings; optional per-profile overrides; Textarea Enter/save, variables helper, override switch/reset | empty strings. No semantic command validation established; these are authorized app capabilities, never run by study. | LRF-PROFILE-OVERRIDE-UI, LRF-SPAWN-HOOKS |
| `search-keybind / settings-keybind / navigate-back-keybind / navigate-forward-keybind / station-selector-keybind` | string keybind expressions; Shortcut recording/swap/conflict workflow | mod+k / mod+, / alt+arrowleft / alt+arrowright / mod+shift+m. writeSetting refuses conflict; swap verifies IDs, stale previous bindings, allowed target binds and existing conflict state. Stored invalid/conflicting values can be discarded and cascade reset. | LRF-SET-VALIDATION, LRF-KEYBINDS |
| `hardware-acceleration / ads-optimization / dev-services` | booleans by defaults; Toggle; restart pending/modal behavior | true / true / false. Main setting constructors declare requiresRestart; persistence dispatches pending restart differences. | LRF-DEFAULTS, LRF-SET-VALIDATION, LRF-RESTART |
| `launcher-resolution-*` | {width:number,height:number,...}; Window sizing and persistence | Custom wj.getDefaultValue uses tTe window configuration; global ZA literals are not effective defaults. transformGet replaces widths/heights below per-window minimum with configured default dimensions. Source declares main 1400x800 min1120x760; embedded-browser1400x800 min460x500; updater fixed300x400; mission-control1300x800 min1000x800. | LRF-WINDOW-DEFAULTS |

Confirmed RAM recommendation literal branches are: physical memory below 4096 MiB ->1024; strictly greater than4096 and below6144 ->2048; strictly greater than6144 and below8192 ->3072; otherwise4096. Exact boundary values4096 and6144 therefore fall through to4096 in this build. This preserves the shipped branch behavior without assuming a corrected formula. gj(true) floors physical MiB to a multiple of100. LRF-RAM.

Confirmed modpack RAM warning selects8192 MiB for >=200 enabled .jar files, or6144 for>=100. It reserves4096 physical MiB, rounds remaining capacity down to a1024 multiple, caps the recommendation and warns only if recommendation>=4096 and current allocation is lower. Accepted decisions are recommended, continue and cancel. Recommended is saved to the profile; cancel stops launch; another outstanding warning causes requestMemoryWarning to resolve cancel. LRF-MEMORY-THRESHOLD, LRF-MEMORY-RECOMMEND, LRF-MEMORY-WARNING, LRF-MEMORY-DECISIONS.

Confirmed profile overrides differ from global settings. Main setters can write resolution/memory overrides directly; the global resolution positive-dimension transform is not called by the inspected profile resolution setter. An independent implementation should define a deliberate common validation policy; treating global and profile validation as identical would not match the observed source. LRF-PROFILE-RESOLUTION, LRF-PROFILE-MEMORY, LRF-RESOLUTION.

Confirmed profile rename trims input, requires a nonempty name of at most32 characters, and refuses another profile with the same trimmed lowercase name. DB conversion declares fields for ID/name/path/type, major/game version, loaders, provider metadata, Lunar module, overrides and config_version. Export/import metadata uses required name/majorGameVersion/gameVersion strings and optional typed fields; overrides/provider fields are any in that declaration. A complete strict profile schema is not established. LRF-PROFILE-NAME, LRF-PROFILE-FIELDS, LRF-PROFILE-EXPORT-SCHEMA.

## Version, profile and install workflows

Confirmed Lunar version selection filters profiles using requested major/subversion, chooses a sorted candidate, resolves selected module/loaders from metadata, saves a saved profile when changed and updates active selection. At launch, missing subversion can fall back to declared default/first metadata subversion; missing module can select the metadata default; invalid resulting version/module produces errors. These are conditional code paths, not a live catalog snapshot. LRF-VERSION-SELECT, LRF-LAUNCH-GATES.

Confirmed profile create normalizes an optional recommended Fabric loader and saves/selects a virtual profile; launch can materialize a virtual profile to saved state. Clone refuses base Lunar/vanilla profiles, handles sensitive override selection through a prompt, generates a new ID/name and removes provider affiliation. Watcher pauses and profile claims guard some mutation flows. Full transaction/rollback semantics remain partial. LRF-PROFILE-CREATE, LRF-PROFILE-CLONE, LRF-LAUNCH-GATES.

Confirmed installs use separate `installs:cancel(id)` and `installs:settle(id)` preload contracts. Cancel looks up or creates an AbortController and aborts it; settle awaits an existing tracked promise while swallowing rejection, then deletes controller/promise/progress maps. Install progress is clamped0..100 and ordinarily throttled by300ms/minimum1 percentage point, with completion bypass. This does not prove rollback, deletion of every partial file or a bounded cancellation latency. LRF-PRELOAD-INSTALLS, LRF-INSTALL-CANCEL, LRF-INSTALL-MODULE.

## Launch sequence: ordered code path versus enum

Confirmed phase enum values are loading, ready, error, authenticating, updating, launching, building-cache and launched. Initial Redux phase is loading. A new ordinary launch is permitted only from ready/error; the enum itself is not a legal-transition table. LRF-PHASES, LRF-LAUNCH-INITIAL.

The inspected Lunar-specific path orders the following operations, with conditional branches:

1. Resolve selected/default profile and verify metadata/migration/launch state. LRF-LAUNCH-GATES.
2. Resolve quick-join recommended pack/version and claim profile; validate/fallback subversion/module; optional memory and update prompts. LRF-LAUNCH-GATES.
3. Authenticating / contacting-lc-servers request stage. LRF-LAUNCH-REQUEST.
4. If uninstalled provider modpack, install then possibly repeat launch request; require JRE and launchTypeData. LRF-LUNAR-PIPELINE.
5. Updating / downloading-lc-assets: licenses/textures/Minecraft assets/artifacts+natives/JRE/UI in parallel; artifact and native substage sequential. LRF-STAGE-EXECUTION.
6. Validate profile JARs; optional Fabric check; abort checks; Launching / preparing-game-launch. LRF-LUNAR-PIPELINE.
7. Build arguments and hooks; Launching / starting-jvm; await optional prelaunch command; spawn JVM; register process handlers. LRF-SPAWN-HOOKS.
8. stdout marker STATUS_INIT => Launching / starting-game; optional STATUS_BUILD_CACHE => BuildingCache / building-cache; STATUS_STARTED => Launched / game-launched. LRF-STATUS-PROGRESS.

Confirmed f$ runs supplied stages using Promise.all; p$ checks abort and awaits each stage sequentially. LUe groups licenses/textures/assets/artifacts+natives/JRE/UI under the parallel container, while artifacts precede natives within their subcontainer. Progress events from parallel substages can interleave. LRF-STAGE-EXECUTION, LRF-LUNAR-PIPELINE.

Confirmed progress dispatches Redux phase/subtext and sends `launch:onProgress` a display/value object or undefined. Percentage display uses one decimal place; numeric events are throttled350ms. Progress ignores updates after abort, endedAt or launchProgressComplete; reaching launched marks progress complete. Game stdout status-marker parsing drives starting-game, optional cache-building and launched decisions. Marker availability/order and UI rendering were not observed. LRF-STATUS-PROGRESS.

Confirmed after-launch hide occurs at STATUS_INIT when configured HIDE and no promotion play lock; it may keep Mission Control visible. It is not unconditionally triggered at spawn or STATUS_STARTED. LRF-STATUS-PROGRESS.

## Cancel, failure and exit contracts

| Condition | Confirmed declared behavior | Evidence |
|---|---|---|
| Memory warning outstanding and no active session | resolve warning cancel and close modal; no session.cancel call required | LRF-MEMORY-WARNING |
| Session exists | notify closing when phase launched, otherwise cancelling; abortController.abort(); set endedAt and stop timer | LRF-SESSION |
| Spawned process handler already registered | abort listener destroys stdout/stderr and calls process.kill() without explicit signal; exit callback handles cleanup/classification | LRF-PROCESS-WIRING |
| Stage/request cancellation | stage signal checks and request cancellation mapper produce xb / ABORTED. Not every awaited operation was established cancellable, and atomic cancellation guarantee is unresolved. | LRF-ABORT-ERROR |

| Trigger | Confirmed result | Evidence |
|---|---|---|
| No profile / missing metadata / running migration / wrong launch phase | No profile => NO_PROFILE_SELECTED; missing metadata/migration => early return; wrong phase => already-open notification rather than new session | LRF-LAUNCH-GATES |
| Missing invalid version/module or quick-join unsupported version / required pack resolution failure | INVALID_VERSION, INVALID_MODULE, UNSUPPORTED_VERSION, MODPACK_REQUIRED/RESOLVE_FAILED error paths | LRF-LAUNCH-GATES |
| Missing asset lookup / launch fetch failure / JRE / launch type data | INVALID_ASSETS_URL, FAILED_TO_FETCH, MISSING_JRE, MISSING_LAUNCH_TYPE_DATA | LRF-LAUNCH-REQUEST, LRF-LUNAR-PIPELINE |
| Prelaunch command nonzero / Java spawn error | PRE_LAUNCH_COMMAND_FAILED / JAVA_INVOKE_ERROR | LRF-SPAWN-HOOKS |
| Session start catches disk full / structured LauncherError / other | NO_SPACE_LEFT / code-short-description-classification / UNEXPECTED_ERROR; YQ resets session first | LRF-SESSION |
| JVM exit callback | reset() runs before classification; exit0/SIGTERM/143 and stageSTARTED => Ready; same clean statuses before STARTED => ABORTED => Ready; other exit => crash classification or UNKNOWN_ERROR/CLASSIFICATION_FAILED | LRF-EXIT |
| YQ dispatcher | ABORTED => Ready and cancellation toast; GAME_ALREADY_OPEN => notification; classification.openPrompt false => Ready; otherwise Error state with code/short/description/classification context | LRF-ERROR-DISPATCH |

Confirmed prelaunch command nonzero exit prevents JVM spawn through PRE_LAUNCH_COMMAND_FAILED. The optional postexit hook has a once guard and is registered for both process exit and error; its nonzero result is warned, not routed through the same prelaunch failure path. None of these commands was run or their configured values inspected. LRF-SPAWN-HOOKS.

Confirmed exit handling calls session reset before clean/aborted/crash classification. Reset releases profile claim, removes session, sets endedAt, ends timer, clears progress and may focus main. Clean statuses0/SIGTERM/143 with status stageSTARTED return to Ready; clean statuses beforeSTARTED are classified ABORTED and also returnReady. Other exits enter classifier handling; no actual stdout, crashes or Windows event logs were collected. LRF-EXIT, LRF-STATUS-PROGRESS, LRF-ERROR-DISPATCH.

## Declared setting inventory

Expressions are retained as source declarations. !0=true, !1=false and void0=undefined. Enum references are deliberately retained where their exact numeric/string decoding was not followed. Dynamic paths have been instantiated from constructor arguments. CustomDefault indicates a class overrides getDefaultValue; it does not imply a changed value in every case. Detailed control/validation remains untraced for rows outside the selected contracts above.

| Key | Store path | ZA declared default expression | CustomDefault |
|---|---|---|---|
| `allocated-memory` | `settings.allocatedMemory` | `1024` | yes |
| `use-osr-overlay` | `settings.useOsrOverlay` | `!0` | no |
| `update-notifications` | `settings.updateNotifications` | `!0` | no |
| `start-playing-notifications` | `settings.startPlayingNotifications` | `KA.Always` | no |
| `show-tooltips` | `settings.showTooltips` | `!0` | no |
| `show-new-indicators` | `settings.showNewIndicators` | `!0` | no |
| `os-notifications` | `settings.osNotifications` | `!0` | no |
| `navigate-home-on-launch` | `settings.navigateHomeOnLaunch` | `!0` | no |
| `auto-upload-logs` | `settings.autoUploadLogs` | `!1` | no |
| `copy-upload-id-to-clipboard` | `settings.copyUploadIdToClipboard` | `!0` | no |
| `enable-animations` | `settings.enableAnimations` | `!0` | no |
| `exit-to-dock` | `settings.exitToDock` | `!0` | no |
| `allow-analytics-collection` | `settings.allowAnalyticsCollection` | `!0` | no |
| `hardware-acceleration` | `settings.hardwareAcceleration` | `!0` | no |
| `computer-startup` | `settings.computerStartup` | `VA.Docked` | no |
| `closing-notifications` | `settings.closingNotifications` | `BA.JustOnce` | no |
| `friend-sort` | `settings.friendSort` | `HA.ByNameAlpha` | no |
| `ignore-forge-processor-hash-check` | `settings.ignoreForgeProcessorHashCheck` | `!1` | no |
| `ads-optimization` | `settings.adsOptimization` | `!0` | no |
| `game-branch` | `settings.gameBranch` | ``master`` | no |
| `after-launch-action` | `settings.afterLaunchAction` | `zA.Hide` | no |
| `game-update-preference` | `settings.gameUpdatePreference` | `ICe.NEUTRAL` | no |
| `discord-rich-presence` | `settings.discordRichPresence.enabled` | `!0` | no |
| `discord-rich-presence-hide-when-idle` | `settings.discordRichPresence.hideWhenIdle` | `!0` | no |
| `advanced-mode` | `settings.advancedMode` | `!1` | no |
| `search-keybind` | `settings.searchKeybind` | ``mod+k`` | no |
| `settings-keybind` | `settings.settingsKeybind` | ``mod+,`` | no |
| `navigate-back-keybind` | `settings.navigateBackKeybind` | ``alt+arrowleft`` | no |
| `navigate-forward-keybind` | `settings.navigateForwardKeybind` | ``alt+arrowright`` | no |
| `station-selector-keybind` | `settings.stationSelectorKeybind` | ``mod+shift+m`` | no |
| `game-resolution` | `settings.gameResolution` | `{width:1280,height:720,fullscreen:!1}` | no |
| `radio-muted` | `settings.radio.muted` | `!1` | no |
| `radio-should-loop` | `settings.radio.shouldLoop` | `!0` | no |
| `radio-volume` | `settings.radio.volume` | `.8` | no |
| `mission-control-after-launch-action` | `settings.missionControl.afterLaunchAction` | `WA.ShowOnAvailableMonitor` | no |
| `mission-control-position` | `settings.missionControl.position` | `{x:0,y:0}` | no |
| `mission-control-screen` | `settings.missionControl.screen` | `void 0` | no |
| `mission-control-console-font-size` | `settings.missionControl.consoleFontSize` | `ACe.Medium` | no |
| `mission-control-console-log-density` | `settings.missionControl.consoleLogDensity` | `jCe.Cozy` | no |
| `mission-control-console-search-mode` | `settings.missionControl.consoleSearchMode` | `MCe.Find` | no |
| `mission-control-console-dividers` | `settings.missionControl.consoleDividers` | `!0` | no |
| `mission-control-console-sensitive-mode` | `settings.missionControl.consoleSensitiveMode` | `!0` | no |
| `mission-control-console-hidden-log-types` | `settings.missionControl.consoleHiddenLogTypes` | `[]` | no |
| `mission-control-skyblock-wiki-display` | `settings.missionControl.skyblockWikiDisplay` | `NCe.OnSkyblock` | no |
| `mission-control-minecraft-wiki-display` | `settings.missionControl.minecraftWikiDisplay` | `PCe.Always` | no |
| `servers-favorites` | `servers.favorites` | `[]` | no |
| `profile-groups` | `profiles.groups` | `[]` | no |
| `game-profile` | `settings.gameProfile` | `void 0` | no |
| `language` | `settings.language` | ``en_US`` | no |
| `discord-rich-presence-language` | `settings.discordRichPresence.language` | `void 0` | no |
| `dev-services` | `settings.devServices` | `!1` | no |
| `dangerously-bypass-trusted-domains-filter` | `settings.dangerouslyBypassTrustedDomainsFilter` | `!1` | no |
| `force-country` | `settings.forceCountry` | `void 0` | no |
| `bypass-lunar-plus-ad-exemption` | `settings.bypassLunarPlusAdExemption` | `!1` | no |
| `core-dump` | `settings.coreDump` | `!1` | no |
| `launcher-resolution-main` | `settings.launcherResolution.main` | `{width:1300,height:750}` | yes |
| `launcher-resolution-mission-control` | `settings.launcherResolution.mission-control` | `{width:1300,height:750}` | yes |
| `launcher-resolution-embedded-browser` | `settings.launcherResolution.embedded-browser` | `{width:565,height:445}` | yes |
| `launcher-resolution-updater` | `settings.launcherResolution.updater` | `{width:300,height:400}` | yes |
| `launcher-resolution-visualise-resolution` | `settings.launcherResolution.visualise-resolution` | `{width:854,height:480}` | yes |
| `launcher-resolution-satellite` | `settings.launcherResolution.satellite` | `{width:1200,height:700}` | yes |
| `views-servers-sort` | `views.servers.sort` | ``recommended`` | yes |
| `views-servers-tab` | `views.servers.tab` | ``featured`` | yes |
| `views-servers-display-type` | `views.servers.displayType` | `YA.GRID` | yes |
| `views-versions-sort` | `views.versions.sort` | ``popular`` | yes |
| `explore-provider` | `settings.explore.provider` | `XA.CurseForge` | yes |
| `explore-type` | `settings.explore.type` | ``mod`` | yes |
| `show-hidden-settings` | `settings.showHiddenSettings` | `!1` | no |
| `country-flag-visibility` | `settings.countryFlagVisibility` | `LA.CountryFlagVisibility.COUNTRY_FLAG_VISIBILITY_FRIENDS` | no |
| `allow-friend-requests` | `settings.allowFriendRequests` | `!0` | no |
| `last-seen-visibility` | `settings.lastSeenVisibility` | `LA.LastSeenVisibility.LAST_SEEN_VISIBILITY_FRIENDS` | no |
| `radio-playing-visibility` | `settings.radio.playingVisibility` | `RA.RadioPlayingVisibility.RADIO_PLAYING_VISIBILITY_FRIENDS` | no |
| `socials-visibility` | `settings.socialsVisibility` | `DCe.SocialsVisibility.SOCIALS_VISIBILITY_FRIENDS` | no |
| `log-retention` | `settings.logRetention` | `GA.Forever` | yes |
| `default-screenshot-upload-privacy` | `settings.defaultScreenshotUploadPrivacy` | `ECe.ScreenshotPrivacy.SCREENSHOT_PRIVACY_UNLISTED` | no |
| `incoming-gift-privacy` | `settings.incomingGiftPrivacy` | `OCe.IncomingGiftPrivacy.INCOMING_GIFT_PRIVACY_EVERYONE` | no |
| `wrapped-leaderboard-visibility` | `settings.wrappedLeaderboardVisibility` | `kCe.WrappedLeaderboardVisibility.WRAPPED_LEADERBOARD_VISIBILITY_EVERYONE` | no |
| `cosmetic-ownership-visibility` | `settings.cosmeticOwnershipVisibility` | `IA.CosmeticOwnershipVisibility.COSMETIC_OWNERSHIP_VISIBILITY_UNSPECIFIED` | no |
| `confirm-critical-actions` | `settings.confirmCriticalActions` | `!0` | no |
| `badlion-services` | `settings.badlion.enabled` | `!1` | no |
| `badlion-insider-mode` | `settings.badlion.insiderMode` | `!1` | no |
| `badlion-test-mode` | `settings.badlion.testMode` | `!1` | no |
| `badlion-debug-mode` | `settings.badlion.debugMode` | `!1` | no |
| `badlion-garbage-collector` | `settings.badlion.garbageCollector` | `!0` | no |
| `badlion-java-path` | `settings.badlion.javaPath` | ```` | no |
| `badlion-backup-java-installation` | `settings.badlion.backupJavaInstallation` | `!1` | no |
| `badlion-custom-jar` | `settings.badlion.customJar` | ```` | no |
| `badlion-discord-rich-presence` | `settings.badlion.discordRichPresence` | `!0` | no |
| `badlion-discord-show-servers` | `settings.badlion.discordShowServers` | `!0` | no |
| `ui-retention` | `settings.uiRetention` | `GA.OneWeek` | yes |
| `use-arm64-runtime` | `settings.useArm64Runtime` | `!0` | no |
| `jvm-args` | `settings.jvmArgs` | ```` | no |
| `garbage-collector` | `settings.garbageCollector` | `UA.Automatic` | no |
| `pre-launch-command` | `settings.preLaunchCommand` | ```` | no |
| `wrapper-command` | `settings.wrapperCommand` | ```` | no |
| `post-exit-command` | `settings.postExitCommand` | ```` | no |
| `environment-variables` | `settings.environmentVariables` | `[]` | no |
| `detach-game-process` | `settings.detachGameProcess` | `!0` | no |
| `compress-pack-folders` | `settings.compressPackFolders` | `!0` | no |
| `satellite-pinned-friend-sort` | `settings.satellitePinnedFriendSort` | `HA.ByNameAlpha` | no |
| `satellite-in-game-friend-sort` | `settings.satelliteInGameFriendSort` | `HA.ByNameAlpha` | no |
| `satellite-online-friend-sort` | `settings.satelliteOnlineFriendSort` | `HA.ByNameAlpha` | no |
| `satellite-offline-friend-sort` | `settings.satelliteOfflineFriendSort` | `HA.ByNameAlpha` | no |
| `notification-position` | `settings.notificationPosition` | `FCe.BottomRight` | no |
| `notify-game-launching` | `settings.notifyGameLaunching` | `!1` | no |
| `notify-experimental-branch` | `settings.notifyExperimentalBranch` | `!0` | no |
| `notify-content-installed` | `settings.notifyContentInstalled` | `!0` | no |
| `notify-modpack-installed` | `settings.notifyModpackInstalled` | `!1` | no |
| `notify-opening-folder` | `settings.notifyOpeningFolder` | `!0` | no |
| `notify-branch-change` | `settings.notifyBranchChange` | `!0` | no |
| `notify-game-closed` | `settings.notifyGameClosed` | `!1` | no |
| `include-snapshots` | `settings.includeSnapshots` | `!1` | no |
| `enable-attach` | `settings.enableAttach` | `!1` | no |

## Independent reconstruction limits

- No effective runtime settings, user profiles, personal configurations or selected version were read. All defaults are declarations, not measured behavior.
- Only selected control schemas and handlers were followed deeply. Most of 113 settings have declared defaults/storage paths but incomplete validation/control mapping.
- Latest version catalog/module defaults, actual launch response/JRE/mainClass/artifact selection and service authorization remain unknown.
- No service requests were sent. Provider pack formats, update/merge/rollback, content gating and version-conditioned edge cases remain partial.
- Static cancellation does not establish a bounded cancellation latency, handling of every pre-spawn await, or an atomic no-spawn-after-cancel guarantee.
- Crash classifier tables and all solution branches were not enumerated; no actual crash/exit/log data was examined.
- Database field mapping is recorded from code, but full SQL migrations/constraints and legacy profile migration roundtrips are not yet fully specified.
- All minified symbols/offsets are build-specific; no assets, branding, images or proprietary implementation files are proposed for reuse.
- Exact authentication/account, store/social subscription and game-side feature parity are outside what this launcher-only static pass establishes.
- A reconstruction based on these behavioral contracts would be an independent design hypothesis until validated with separately authorized non-secret runtime tests.

## Evidence index

Exact excerpts are in the JSON; this table supplies build-bound anchors. All offsets are zero-based UTF-8 byte offsets in the source ASAR logical member.

| ID | Member | Byte start | Byte end |
|---|---|---|---|
| LRF-DEFAULTS | `dist-electron/electron/main.js` | 1475339 | 1479423 |
| LRF-SET-VALIDATION | `dist-electron/electron/main.js` | 1670177 | 1671907 |
| LRF-PRELOAD-LAUNCH | `dist-electron/preload/launcher/index.js` | 9509 | 10209 |
| LRF-PRELOAD-PROFILES | `dist-electron/preload/launcher/index.js` | 18062 | 23162 |
| LRF-PRELOAD-INSTALLS | `dist-electron/preload/launcher/index.js` | 9360 | 9540 |
| LRF-ROUTES | `dist/assets/main.js` | 2112874 | 2118203 |
| LRF-SEARCH | `dist/assets/main.js` | 168244 | 173844 |
| LRF-UI-CATEGORIES | `dist/assets/use-toast-notifications.js` | 489361 | 491461 |
| LRF-RAM | `dist-electron/electron/main.js` | 1489170 | 1490190 |
| LRF-RAM-UI | `dist/assets/use-toast-notifications.js` | 410769 | 413369 |
| LRF-RESOLUTION | `dist-electron/electron/main.js` | 1602854 | 1603364 |
| LRF-RESOLUTION-UI | `dist/assets/use-toast-notifications.js` | 419462 | 422882 |
| LRF-AFTERLAUNCH-UI | `dist/assets/use-toast-notifications.js` | 425295 | 426655 |
| LRF-ADVANCED-UI | `dist/assets/use-toast-notifications.js` | 422887 | 425167 |
| LRF-ENV-UI | `dist/assets/use-toast-notifications.js` | 417770 | 418870 |
| LRF-PROFILE-OVERRIDE-UI | `dist/assets/use-toast-notifications.js` | 154067 | 158567 |
| LRF-PROFILE-NAME | `dist-electron/electron/main.js` | 5067447 | 5068287 |
| LRF-PROFILE-FIELDS | `dist-electron/electron/main.js` | 4897149 | 4900549 |
| LRF-PROFILE-EXPORT-SCHEMA | `dist-electron/electron/main.js` | 5009600 | 5010750 |
| LRF-PROFILE-CLONE | `dist-electron/electron/main.js` | 4989944 | 4991394 |
| LRF-PROFILE-CREATE | `dist-electron/electron/main.js` | 4993738 | 4994438 |
| LRF-VERSION-SELECT | `dist-electron/electron/main.js` | 5045367 | 5047217 |
| LRF-PHASES | `dist-electron/electron/main.js` | 2310021 | 2310346 |
| LRF-LAUNCH-INITIAL | `dist-electron/electron/main.js` | 2330525 | 2332225 |
| LRF-LAUNCH-GATES | `dist-electron/electron/main.js` | 4839796 | 4850696 |
| LRF-MEMORY-WARNING | `dist-electron/electron/main.js` | 4836759 | 4840499 |
| LRF-MEMORY-THRESHOLD | `dist-electron/electron/main.js` | 2230438 | 2230578 |
| LRF-MEMORY-RECOMMEND | `dist-electron/electron/main.js` | 4444540 | 4444790 |
| LRF-LAUNCH-REQUEST | `dist-electron/electron/main.js` | 4494298 | 4495708 |
| LRF-STAGE-EXECUTION | `dist-electron/electron/main.js` | 4475558 | 4476748 |
| LRF-LUNAR-PIPELINE | `dist-electron/electron/main.js` | 4776323 | 4781923 |
| LRF-SPAWN-HOOKS | `dist-electron/electron/main.js` | 4783207 | 4785557 |
| LRF-SESSION | `dist-electron/electron/main.js` | 4830699 | 4835449 |
| LRF-PROCESS-WIRING | `dist-electron/electron/main.js` | 4506103 | 4508903 |
| LRF-EXIT | `dist-electron/electron/main.js` | 4821213 | 4822763 |
| LRF-STATUS-PROGRESS | `dist-electron/electron/main.js` | 4823644 | 4826494 |
| LRF-ERROR-DISPATCH | `dist-electron/electron/main.js` | 4442638 | 4444838 |
| LRF-ABORT-ERROR | `dist-electron/electron/main.js` | 807664 | 807989 |
| LRF-INSTALL-CANCEL | `dist-electron/electron/main.js` | 2270813 | 2271413 |
| LRF-INSTALL-MODULE | `dist-electron/electron/main.js` | 4438144 | 4438454 |
| LRF-KEYBINDS | `dist-electron/electron/main.js` | 1672209 | 1674339 |
| LRF-WINDOW-DEFAULTS | `dist-electron/electron/main.js` | 1610242 | 1611622 |
| LRF-MEMORY-DECISIONS | `dist-electron/electron/main.js` | 2230538 | 2230581 |
| LRF-PROFILE-RESOLUTION | `dist-electron/electron/main.js` | 5064175 | 5064705 |
| LRF-PROFILE-MEMORY | `dist-electron/electron/main.js` | 4441704 | 4442834 |
| LRF-ENV-PROFILE | `dist-electron/electron/main.js` | 5056933 | 5057503 |
| LRF-RESTART | `dist-electron/electron/main.js` | 1486678 | 1487968 |
| LRF-RAM-CONVERSION | `dist/assets/use-toast-notifications.js` | 409524 | 410544 |
