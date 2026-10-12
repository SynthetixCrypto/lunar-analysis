# Session 6 — Priority Java gap resolution

Date: 2026-10-11. Static analysis only. The exact gap definitions came from [Session 5 remaining-gaps.md](../session5-deepseek/remaining-gaps.md), with [verification-audit.md](../session5-deepseek/verification-audit.md) and [contradictions.md](../session5-deepseek/contradictions.md) used to avoid repeating closed findings. Native work follows [native-investigation-plan.md](../session5-deepseek/native-investigation-plan.md).

**Confirmed** means an artifact directly implements the cited branch or data flow. **Strong inference / Derived** means a conditional consequence, not an observed run. **Unknown** means the available evidence does not establish it. “Resolved” below always retains its stated artifact/version/static scope. No target execution, credentials, personal profile values, private services or protection bypass was used.

Offsets are decimal JVM instruction offsets within the named method. `L` expands to `com.moonsworth.lunar.client`; `ML` to `com.moonsworth.lunar`. Obfuscated tokens use the established `_` plus MD5-first-six alias. Original class names, class hashes, artifact identities and full disassembly are linked through the manifests in [evidence-index.md](evidence-index.md).

## Priority disposition

| Gap | Result | Evidence report |
|---|---|---|
| G-04 | Resolved for retained modern implementation: attack-distance producer, entity age counter, periodic reset producer and range source | [Reach/combo](reach-combo-findings.md), S6-RC-01/03/05/06 |
| G-05 | Resolved for retained modern implementation and inspected Minecraft caches: outgoing attacked target, timestamp writer and correlated counting | [Reach/combo](reach-combo-findings.md), S6-RC-02/04 |
| G-18 | Direct override producers enumerated; conditional lifecycle chain resolved. Reflection/plugins and live order remain open | [Support](support-findings.md), S6-SUPPORT-01/02/08 and producer table |
| G-19 | Reset/predicate and interceptor implementations resolved; absent metadata does not demonstrate remote removal in inspected paths | [Support](support-findings.md), S6-SUPPORT-03..06 |
| G-13 | Resolved within the specified 16 non-auth call-containing methods and traced callback/UI state | [RPC](rpc-findings.md), S6-RPC-01 |
| G-10 | Concrete exceptional paths established; actual positive-depth/stale-replay workload remains unobserved | [Bus](bus-findings.md), G-10 |
| G-11 | Resolved for direct calls in 8,095 retained classes: one locked diagnostic map reader, five wrapper producer bodies, eight paired call instructions | [Bus](bus-findings.md), G-11 |

## Reach and combo: actual Minecraft state, not bridge-name interpretation

**Confirmed.** `ML._590f69._2ce426._1e73d7._0be1fc()` is annotated as `ticksExisted` at version 0 and `tickCount` at version 6. The module's saved “time” is an entity tick count. Modern LivingEntity mixin `ML._d4ca6c._1e73d7._02d7ad._590f69._a140a8.bridge$getLastAttacker @0–10` reads `lastHurtMob`; its timestamp getter @0–4 reads `lastHurtMobTimestamp`.

The retained Minecraft `cache/876f0fb/51b21bae/bake.zip` LivingEntity class, SHA-256 `73100ba5d579c8904b6dd8db16a5166f336abc5ba2d8f49aea35074f20b24029`, supplies the missing field writer: `setLastHurtMob(Entity) @0–22` stores the outgoing living target and @25–30 copies THIS.tickCount. Cached `Player.attack @237–249` gates the success body on target damage acceptance and @313–315 calls THIS.setLastHurtMob(target). Four other retained caches corroborate the setter. This establishes direction: the misleading “last attacker” bridge returns the player's last attacked target. Exact cache/class identities: [vanilla manifest](evidence-reach/vanilla/manifest.json).

**Confirmed.** Modern MultiPlayerGameMode mixin `ML._d4ca6c._590f69._21aca6._1e73d7._bb4487._590f69.lunar$clickMouse$eventPreAttackEntityClient @0–38` posts at attack HEAD when camera and hitResult exist. Its lambda @46–82 computes camera interpolated eye position to current ray-hit position, carrying the target argument and hit location. A min=35 piercingAttack producer shares the event. The distance is not target-center distance. Exact annotations and methods: [focused excerpts](evidence-reach/focused-excerpts.json).

**Confirmed.** COMBO `L._88f3cf._bb4487._429bf0._cfe983` accepts a player-bridge status entity, matches it by reference to the outgoing target, consumes a changed timestamp, then increments only if `abs(timestamp-player.tickCount)<=4 @17–55`. It has no status-byte-2 check. **Derived:** same-tick attacks may collapse; duplicate status/hurt callbacks with the same timestamp cannot increment again, and a stale first callback consumes the timestamp without incrementing. It is not a universal per-hit counter. Reach instead requires byte 2, matching target ID and `currentTick-sentTick<=4`, then clamps to current range.

**Confirmed.** `ML._d4ca6c._1e73d7._590f69._a140a8.lunar$preRunTick @14–48` posts `_1eb51c` when its global pre-increment counter is nonzero and divisible by 20. Therefore the modules' 80-tick stale checks are periodically sampled, with their existing alternating reset flag; an exact four-second expiry is not established. Modern attack-range branches use active item ATTACK_RANGE/default at ordinal >=35, entityInteractionRange at >=22, otherwise far-pick 6 or 3. Full offsets and limits: [reach-combo-findings.md](reach-combo-findings.md).

## Overrides: conditional observers connect to the full lifecycle

**Confirmed.** `L._02d7ad._cfe983._55938e(feature) @67–105` installs the enabled-setting observer; its bound callback `_cfe983(toggle,feature,Boolean) @6` calls the full toggle API. Feature interceptor `L._88f3cf._1e73d7._a140a8._cfe983(feature,category,Boolean) @316–348` forwards selected override changes to that setting's interceptor. Generic setting interceptor `L._ec7e36._1e73d7._2ce426._cfe983 @89–147` invokes observers only when the effective value changes by Objects.equals. Thus an override can synchronously enter the full toggle lifecycle before trailing recursive feature recomputation; equality, a decorator, absent observer or absent enabled setting can stop that chain.

The [producer table](support-findings.md) classifies all 46 retained direct override/criteria/removal instructions and separately records 32 ordinary setter instructions. Sources include server refresh, Apollo feature/option updates, option loading, remote metadata, initialization, internal feature callbacks, saved-state restoration and action contexts. Predicate installation is distinguished from immediate application. Enumeration is bounded to direct references in the retained cache, not all possible reflection/plugin/native callers.

**Confirmed refinement.** `L._88f3cf._1e73d7._2ce426.isEnabled @0–15` calls enabledSetting.get(), which can return an interceptor value; it is not universally a raw stored-intent read. `setEnabled @0–13` writes the underlying option, and observers may be suppressed while an override masks it. The raw setting accessor is `_1f5b06`. Keep raw option, effective option, selected feature override, dynamic allowance and cached feature activation separate.

**Confirmed.** Feature booleans use category selection, but generic settings hold one active category/value. `L._ec7e36._1e73d7._2ce426._cfe983 @79–86` replaces it on accepted non-null write; null @56–76 clears it without checking the supplied category. Server refresh `L._dd3308._1e73d7._f636dc @18–32` visits setting interceptors and helper `_21aca6 @0–12` requests SERVER/null without a category guard. **Derived:** that request can erase a generic CLIENT_REMOTE/CLIENT_OVERRIDE value, while feature Boolean clearing remains category-specific. This resolves G-22 as well as sharpening G-19.

Criteria reset preserves definitions: holder `_0ee36d @0–22` clears active category/value but retains predicate and criteria value. Generic `_000018 @0–30` clears active CLIENT_CRITERIA only; a failed subsequent predicate match does not itself clear active state. Metadata loader `L._02d7ad._d4ca6c._cfe983.load @71–126` skips absent/already-processed categories; refresh `_02d7ad(Map) @9–17` clears the processing record, not all remote interceptors. No broader remote-deletion contract is inferred. Specialized interceptor hierarchy, decorator behavior and exact resets: [support-findings.md](support-findings.md).

## RPC callers: no demonstrated request-pending latch, with separate screen/state limits

**Confirmed in the 16-method scope.** All specified calls pass a null RpcController. Most acknowledgements are no-ops; capability/promotion/fetch/checkout callbacks update state or display a screen. No request-specific pending spinner/lock is set before sending and released only by those completion lambdas. Missing callbacks can still leave old radio/capability data or omit notifications. [caller-audit.json](evidence-rpc/caller-audit.json) records exact signatures and offsets rather than treating 16 methods as 16 individual RPC instructions.

Radio `L._88f3cf._bb4487._6247d7._cfe983._88f3cf @0–31` polls on an event-age gate strictly greater than 2000 ms, without an in-flight guard. `_1253fc(transport) @0–26` clears track/controls/progress when a present transport is not OPEN; absent Optional transport skips that reset. An open lost fetch can leave stale state until another update.

Checkout callbacks `L.util._252625 @21–47` can install screen `L._2f4182._2f4182._cfe983`; its own key/update/close/render bodies are empty. Transport's TebexJsCheckoutClosed handler @0–4 clears the screen, but onClose has no screen cleanup. **Derived:** after successful callback installation, losing that separate push lacks cleanup in these traced methods. Permanent lock is not established because all adapter/dismissal paths were not traced. This is separate from abandonment before callback. [rpc-findings.md](rpc-findings.md) contains the exact caller table and UI bounds.

## Event bus: static failure facts versus runtime reachability

**Confirmed.** Exact owner/descriptor search found one exposed-map caller, diagnostic `L._88f3cf._bb4487._a1dd3a._21aca6._21aca6._21aca6._f54c89 @26`; it locks @17–18, snapshots @21–35 and unlocks both success and catch paths @247–262. It does not mutate the map. Wrapper producers are repeatable chunk-unload/player-info batch loops. The wrapper can invoke the producer again for pending listeners; fresh batch construction does not mean every captured listener is called twice. Eight paired calls wrap screen/hotbar rendering. [focused-callers.json](evidence-bus/focused-callers.json) and [bus-findings.md](bus-findings.md) enumerate each exact class/method.

**Confirmed control flow; Derived consequences.** Base wrapper `_1253fc @16–18` increments depth. Policy throws before end @76–77, and second outer Consumer @59–67 is outside the first catch. Reporting calls virtual getMessage and external logging/capture without guaranteeing return. An escaping active-dispatch failure can therefore leave positive depth. Separately, `_57e17e @0–14` decrements first; replay `_455ac7 @13–80` can throw before List.clear @83–87, leaving depth zero with stale deferred records. Hook marker checks and class initialization supply actual throwing operations, not an observed invalid shipped event. Public finally blocks unlock but do not repair these fields. No live stuck-bus claim is made. G-12's pending-only PRE cancellation workload remains open.

The remaining runtime/version/native limits are consolidated in [remaining-unknowns.md](remaining-unknowns.md). Further feature and Java/native boundary work is in [additional-findings.md](additional-findings.md) and [jni-and-webosr.md](jni-and-webosr.md).
