# Reconstruction feasibility

Study date: 2026-10-11. Assessment of an **independent launcher and Minecraft extension with comparable user outcomes**, not an exact rebuild. No implementation or dynamic analysis has begun.

**Assessment:** the local launcher/profile/launch/settings infrastructure and a selected HUD/utility suite are the strongest starting points. Broad feature parity is substantially less certain. Native browser composition, replay, complex game assistance and remote services carry the largest gaps. No defensible whole-product reconstruction percentage can be derived from artifact/class/setting counts.

## Evidence and rating definitions

- **C:** confirmed filesystem, packaged metadata, static source or classfile declaration/reference.
- **I:** inferred responsibility or proposed independent design.
- **U:** unresolved. No live user behavior, screen geometry, network traffic or performance was observed.
- **A — sufficient for bounded independent implementation:** the stated functional subset is clear enough to design new code, with explicit new schemas/UX choices. Does not imply exact Lunar compatibility.
- **B — partial:** useful UI/API/framework evidence exists, but end-to-end requirements or host semantics remain missing.
- **C — service/contract dependent:** local artifacts cannot supply required remote data, identities, entitlements or backend behavior.
- **D — catalog/name only:** feature identity/affordance is known; implementation requirements/algorithm are not established.

Feasibility High/Medium/Low concerns the stated **independent outcome**, subject to scope and integration verification. Relative effort Small/Medium/Large/Very large is engineering judgment, not a measured schedule. Exactness remains unverified even for High rows.

## Launcher subsystems

| Subsystem / target outcome | Readiness; feasibility; relative effort | Evidence sufficient now | Missing detail / reconstruction ceiling |
|---|---|---|---|
| Original shell/navigation/windows/tray | A; High; Medium | Electron main/renderer/preload split; window lifecycle, routes and controls | Exact rendered appearance, interaction timing/responsive behavior unobserved; design original UI |
| Launcher settings store/editor | A; High; Medium | Store paths/migrations; setting registrations, defaults/validators; set/reset/swap bridge | Code-declared defaults may be overridden; exact current values excluded; new schema/migrations recommended |
| Profile CRUD/selection | A; High; Medium | create/clone/select/delete, profile metadata, version/memory/resolution/content APIs | Clone/deletion/recovery edge cases and exact persisted format partial |
| Profile advanced launch settings | A; High; Medium | JVM/GC/environment/command/gameDir setters and argument construction | New policy/validation needed; configured personal commands/environment deliberately unread |
| Game/runtime/artifact launch | A for own verified launch path; Medium–High; Large | Metadata-to-runtime/artifacts/mainClass pipeline, stage concurrency, argument/process/status boundary | Effective Lunar response/mainClass unknown; own authorized metadata/loader contract required |
| Cancel/exit/progress/errors | A; High; Medium | AbortController/process-kill path, phase/progress/status markers and exit classification | Runtime race behavior/retry UX untested; independent tests and policy needed |
| Java selection/memory/resolution | A; High; Small–Medium | JRE metadata paths, three verified x64 runtimes, code RAM/dimension validators | Version-to-runtime decision from remote metadata; recommendations are not measured hardware suitability |
| Loader/version expansion | B; Medium; Large/continuing | Fabric/Quilt/Forge/NeoForge/OptiFine APIs and versioned integration artifacts | Every supported combination, processor behavior, compatibility validation and active version set unknown |
| Local mods/resource packs/shaders | A for basic lifecycle; Medium–High; Medium | List/add/toggle/remove/import/folder APIs and profile boundaries | Dependency resolution/version conflicts/provider semantics remain B |
| Provider search/modpacks/update | B/C; Medium; Large | Modrinth/CurseForge install/update/dependency/search families, profile link/pack reset/divergence surfaces | Exact service/API/format rules and rollback/conflict semantics must be separately verified |
| World/datapack management | A for new local CRUD/import subset; High; Medium | World list/import/datapack/folder operations | Cross-version world compatibility and import overwrite/collision policy require specification |
| Profile import/export/pack migration | B; Medium; Large | Export/import/content-list/verification-resume interfaces and profile migration hooks | Complete pack formats, trust rules, extension compatibility and lossless migrations unresolved |
| Local server lists/ping/favorites | A; High; Medium | CRUD/reorder/import/ping/list API contracts | Discovery catalog/ranking is C; independent ping/error/data-format implementation required |
| Screenshots | A; High; Small–Medium | List/read/save/rename/delete/favorite/copy/reveal methods | Exact indexing/thumbnail/search/upload semantics partial; no image assets copied |
| Notes/backups/search | A; High; Medium | CRUD/move/lock/backup restore/export/search methods | Lock semantics, backup retention/search indexing and format details partial; define independently |
| Diagnostics/log UI/cache/storage cleanup | A for own product; High; Medium | Archive/list/search/upload, reclaim/cache/fix interfaces | Fix algorithms/remote upload policy partial; future logs must be redacted; original logs not read |
| Accounts/device login/skins/capes | B/C; Medium; Large | Account/device-login/skin-history/preset/cape affordances, auth boundary | Authorized public integration must be verified; no credential flow tested or secrets collected; Lunar entitlements unavailable |
| Friends/chat/conversations/notifications | C; Medium for own service, Low for Lunar parity; Large | Extensive local method names and protocol/UI boundaries | Backend delivery, persistence, moderation, identity, membership and access rules missing |
| Self-update/distribution | A/B; High for own feed; Medium–Large | Updater channel/feed/event/interval and cleanup boundaries | Own packaging, signing, recovery/feed/update validation required; no Lunar update service dependency |
| Promotions/music/social linking/Overwolf/other-client integration | C/B; Low–Medium; Large | Named modules and playlist/promotion/link/permission interfaces | External contracts/content/entitlements and actual runtime use unknown; low priority |

Launcher evidence: [original architecture](launcher-architecture.md), [focused launcher study](reconstruction-launcher-features.md), [literal channel inventory](reconstruction-preload-channels.json), and focused REA summary/module/trace records.

## Minecraft-side subsystems

| Subsystem / target outcome | Readiness; feasibility; relative effort | Evidence sufficient now | Missing detail / reconstruction ceiling |
|---|---|---|---|
| Lifecycle/version adapter | A for a chosen version; Medium–High; Medium | Constructor/tick/frame/input/screen/options Mixin targets and bootstrap boundaries | Actual activation and broad compatibility unobserved; new integration implementation required |
| Feature/module framework | A; High; Medium | Feature base enabled/isEnabled/updateEnabled/load/handle declarations; subclass relationships | Full registration/init order, listener cleanup and error policy partial; define own lifecycle |
| Typed settings/config framework | A; High; Medium | Typed value/default/codec/numeric-bound interfaces and UI setting controls/scopes | Per-feature defaults/validation/migrations mostly unknown; new schema/codecs required |
| Keybinds/input focus | A/B; High for own policy; Medium | Keyboard/mouse hooks; UI text-focus gating; host keybind editing/conflict affordances | Exact propagation/order/repeat/capture semantics untested; define own rules |
| Original settings/profile/routes UI | A; High; Medium–Large | Route/provider structure, host calls, reset/action/keybind control semantics | Exact visuals/assets excluded; host initial payload/defaults must be supplied independently |
| HUD layout/editor | A for new geometry/enable/layout model; Medium–High; Medium | HUD base x/y/width/height; metadata/property providers; catalog | Exact snapping/scale/anchor/preview behavior incomplete; /hud JS route cannot establish full HUD implementation |
| Simple telemetry/info widgets | A after choosing explicit requirements; High; Small–Medium each | Catalog IDs and feature/render/input bases; FPS UI special case | Names alone do not specify sampling, smoothing, formatting or precise layout |
| Per-feature behavior across catalog | D/B; varies; potentially Very large | 379 candidate identifiers; subclass/string correlation and setting-key structure | No basis to claim every algorithm, activation/version/default or expected behavior is recovered |
| Local waypoints/navigation | B; Medium–High; Large | Waypoint namespaces/edit/import/group/sort/map surfaces and feature IDs | World/dimension scoping, coordinate persistence, map/texture producer and rendering details partial |
| Core rendering/HUD composition | B; Medium; Large | GameRenderer/Gui/render-target hooks, browser textures/JNI and TextureHandler signatures | Frame/thread/graphics-state ownership, scale/color/format/context-loss behavior and benchmarks unknown |
| Embedded web browser UI replacement | B; Medium; Large | Browser lifecycle/input/focus/texture API, FileSystem payload, FunctionBus bridge | Native producer/resolver/scheduling implementations missing; choose native game UI or own renderer |
| Player/model/cosmetic previews | B; Medium; Large | Batched add/update/remove models, DOM bounds/zoom/hover, gameTexture readiness/image source contract | Renderer/texture lifetime/animation/camera semantics and content missing; original assets required |
| Cosmetics/locker/emotes/sprays | B/C; Medium for own content, Low for Lunar parity; Large | UI routes/providers and model/cosmetic callbacks | Proprietary content/entitlements/backends excluded; own assets/services needed |
| Shader cloak/editor | B/D; Low–Medium; Large | Route/provider and shader/model surface | Shader language/validation/runtime/effect semantics and assets incomplete |
| Replay/Rewind/record/export | B/D; Low–Medium; Very large | Timeline/effects/list/export UI and ReplayMod/Flashback compatibility JARs | Recording/event/world snapshot format, playback/seek sync, media/export pipeline missing |
| Server discovery/multiplayer/profile viewer | B/C; Medium for own/basic service; Large | Routes, server ping/data wrappers and profile embed declaration | Ranking/catalog/social data/privacy/backend compatibility unknown |
| Friends/social/shared profiles | C; Medium for own service, Low for Lunar parity; Large | UI providers and protobuf models/callbacks | Live identities, remote persistence, moderation and interoperable service contracts absent |
| SkyBlock/server/domain-specific assistance | D/B; varies, often Low–Medium; Very large collectively | Domain feature IDs and namespaces | Game-data sources, detection rules, versions and each feature algorithm require separate specification |
| Hosted-world UI and hosting | B/C; Medium for own bounded service; Large | Confirmation/settings/home/social affordances and host screen calls | Hosting transport, discovery, access/session/NAT behavior and server lifecycle not recovered |
| Language/theme/localization | A for own content; High; Medium | Language search/select/reset/Unicode and theme/host metadata surfaces | Original translations/themes/assets excluded; new content, font/resource reload and fallback rules required |
| Performance optimizations | D/B; Unknown until measured; Large | Performance settings and rendering/Sodium compatibility boundaries | No FPS/latency/CPU/GPU/memory baseline or optimization effectiveness measured |
| Audio/Mumble/media | B; Medium for independent narrow integration; Large | JNI init/update and file-mapping imports; audio/media package presence | Shared-memory peer/name/schema, timing and actual media pipeline incomplete |
| Broad platform/version parity | B/D; Low initially; Very large/continuing | Verified current Windows architecture and versioned adaptation metadata | Other platforms, complete supported matrices and regressions unexamined |

Game evidence: [original Minecraft architecture](minecraft-client-architecture.md), [feature/settings study](reconstruction-minecraft-features.md), [UI study](reconstruction-game-ui.md), [typed rendering interfaces](reconstruction-render-interfaces.json), and [native inventory](native-runtime-inventory.md).

## How close is realistic?

| Goal | Evidence-based assessment |
|---|---|
| Similar launcher capability categories | High feasibility for local profiles/settings/launch/content/utilities, with independently chosen persistence/UX and verified external integrations |
| Useful Lunar-style local game extension | High feasibility for a selected module/settings/HUD utility subset; exact feature behavior must be specified |
| Similar breadth across all candidate feature IDs | Not established. Catalog presence is stronger than behavioral evidence; detailed work scales per feature and version |
| Same browser/native internals and performance | Not established; signatures expose interfaces, not complete implementations or performance characteristics |
| Same connected social/store/entitlement ecosystem | Not achievable from local evidence alone; own services can provide similar categories but different users/content/data |
| Exact visual/asset/source/binary reproduction | Outside this independent scope and unsupported by available evidence |

Do not convert 379 identifiers, 113 settings or 365 IPC operations into a “percent reconstructed.” They measure different inventories, include inactive/compatibility/auxiliary surfaces, and say little about algorithmic complexity.

## Architecture choices that remove unnecessary gaps

**Proposed design, not recovered Lunar behavior:** own versioned config/store, own typed IPC, own game module/event interfaces, original native screens or independently permitted web renderer, independent game/loader metadata adapter and optional owned services. These choices can deliver comparable outcomes without matching Lunar private storage/protocol/native implementation.

**Gaps that remain real even with new design:** reliable game integration; behavior specifications for selected complex features; rendering/input/resource lifecycle; account/provider integrations; data availability; multi-version maintenance; recording/playback; performance validation.

Provider/obfuscation limitations remain those in [findings.md](findings.md), supplemented by [reconstruction-provider-availability.json](reconstruction-provider-availability.json). See [missing-evidence.md](missing-evidence.md) for investigation results and [development-roadmap.md](development-roadmap.md) for sequence and gates.
