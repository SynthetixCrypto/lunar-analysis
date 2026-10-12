# Session 6 — G-04 / G-05 reach and combo

Date: 2026-10-11. Static inspection only; Lunar, Minecraft and native libraries were not executed. The investigation used the exact definitions in Session 5 remaining-gaps.md. **Confirmed** means directly established by class bytes / bytecode / annotations; **Strong inference** means a consequence of those branches; **Unknown** means not established. Offsets below are decimal, method-local JVM bytecode offsets.

## Artifact identity and evidence conventions

Primary artifacts are C:/Users/Admin/.lunarclient/offline/multiver/lunar.jar (SHA-256 bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9) and modern-0.1.0-SNAPSHOT-all-nomappings.jar (99df64c5913e9a32111135bfde140343d4baa954fe5ba08069962670566db02e). Each exact original JVM class identity and class SHA-256 is in the matching [evidence-reach](evidence-reach/) *.json manifest. Fresh full javap -p -c -v evidence is *.javap.txt; shortened but losslessly traceable identifiers are in *.aliases.txt. L expands com.moonsworth.lunar.client; ML expands com.moonsworth.lunar; each 30-character obfuscated token becomes underscore + first six MD5 hex digits, as in Sessions 3–5. [focused-excerpts.json](evidence-reach/focused-excerpts.json) retains the decisive methods including annotations.

The installed cache archives provide real Minecraft implementation bodies in addition to Lunar's mixins. [vanilla/manifest.json](evidence-reach/vanilla/manifest.json) records five cache roots and exact extracted class SHA-256 values. These are retained installed artifacts, not proof that a particular launch selects a cache. The report identifies a representative cache explicitly and corroborates the setter across all five; concrete cache→Minecraft-version assignment remains outside this gap closure.

## S6-RC-01 — counter identity resolved

**Confirmed.** lunar.jar interface ML._590f69._2ce426._1e73d7._0be1fc() has a runtime-visible bridge-mapping annotation: version=0 field ticksExisted; version=6 field tickCount. See [interface aliases](evidence-reach/ML._590f69._2ce426._1e73d7.aliases.txt), exact method annotation. It is the entity's integer age/tick counter, not a millisecond clock or attack count. The reach module stores it in a long named sentTime by i2l; that field name does not change its units.

## S6-RC-02 — misleading last-attacker names mean outgoing target and tick

**Confirmed.** modern mixin ML._d4ca6c._1e73d7._02d7ad._590f69._a140a8 extends Entity, targets LivingEntity, and exposes Shadow fields lastHurtMob and lastHurtMobTimestamp. bridge$getLastAttacker() @0–10 reads lastHurtMob and Optional.ofNullable; bridge$getLastAttackerTime() @0–4 reads lastHurtMobTimestamp. Its lunar$setLastAttackerTime hook injects at setLastHurtMob HEAD; this separate hook records a Lunar millisecond value in the auxiliary entity state, but the combo timestamp getter directly reads the vanilla integer field, not that millisecond value.

Backing behavior is verified from cache/876f0fb/51b21bae/bake.zip entry net.minecraft.world.entity.LivingEntity (class SHA-256 73100ba5d579c8904b6dd8db16a5166f336abc5ba2d8f49aea35074f20b24029): setLastHurtMob(Entity) @0–22 stores the argument if it is LivingEntity, else null; @25–30 copies THIS.tickCount into lastHurtMobTimestamp. Cached Player.attack(Entity) @237–249 calls target.hurtOrSimulate(source,damage) and branches around the success body if false; @313–315 calls THIS.setLastHurtMob(target). Player.stabAttack @246–248 also updates the outgoing target. These are instructions, not interpretations based solely on names. Four other retained caches show the same setter semantics (@0–31 or @0–33); the 9dcd110f Player.attack setter call is @308–310.

Therefore the Optional is the last attacked living target; its timestamp is the attacking entity's own tickCount when that state was set. It does not identify the mob that last damaged the player. Cached LivingEntity.baseTick @538–557 clears lastHurtMob when that target is no longer alive; it does not clear its timestamp there. Distinct lastHurtByMob state follows after @560, corroborating the directional distinction.

## S6-RC-03 — actual attack-distance event producer resolved

**Confirmed.** modern MultiPlayerGameMode mixin ML._d4ca6c._590f69._21aca6._1e73d7._bb4487._590f69.lunar$clickMouse$eventPreAttackEntityClient(Player,Entity,CallbackInfo) @0–38 injects at attack HEAD. It requires non-null Minecraft camera entity and hitResult, then posts L._d4ca6c._cfe983._2ce426._cfe983._02d7ad through the event bus @21–34. It does not itself cancel attack.

The lambda producer @46–82 constructs the event with the target Entity argument, distance from camera.getEyePosition(partialTick) to Minecraft.hitResult.getLocation(), and the hit location itself. It measures the current ray-hit position rather than target center or player feet. Partial tick comes from deltaTracker$v1_21_2.deltaTicks at MC_VERSION>=26, timer$v1_21_0.deltaTicks at >=24, else timer$v1_16_1.partialTick (@0–45). The event getDistance() directly returns its constructor-stored double; no hidden distance recomputation occurs there.

A second producer lunar$piercingAttack$eventPreAttackEntityClient injects at piercingAttack$v1_21_11 HEAD, version gate min=35. It requires camera and an EntityHitResult. Its lambda @0–39 uses EntityHitResult.getEntity and getLocation with camera-eye interpolation from deltaTracker.deltaTicks. This confirms an additional modern attack mechanism that shares the same event without claiming every pierced target produces its own separate event.

## S6-RC-04 — status/hurt producers and combo counting resolved

**Confirmed.** modern ClientPacketListener mixin ML._d4ca6c._590f69._21aca6._2f4182._1e73d7 produces L._d4ca6c._cfe983._2ce426._cfe983._c8175c in three paths:

| Producer | Injection site | Event byte |
|---|---|---|
| lunar$handleEntityStatus @0–16 | handleEntityEvent packet handler, before Entity.handleEntityEvent(B)V invocation | packet.getEventId(), lambda @8–12 |
| lunar$handleHurtAnimation(HurtAnimationPacket) @0–15 | min=16, handleHurtAnimation$v1_19_4 before Entity.animateHurt(F) | synthesized 2, lambda @8–9 |
| lunar$handleHurtAnimation(DamageEventPacket) @0–15 | min=16, handleDamageEvent$v1_19_4 before Entity.handleDamageEvent(DamageSource) | synthesized 2, lambda @8–9 |

COMBO's root L._88f3cf._bb4487._429bf0._cfe983 status handler accepts only entities implementing ML._590f69._2ce426._1253fc._590f69 (@0–7). The modern Player mixin implements that exact interface, so this is the **player bridge**, narrower than the generic living-entity wording in the previous partial trace. It obtains the local player's last attacked target, requires reference identity with the status entity, and compares lastHurtMobTimestamp against saved timestamp. A changed timestamp is stored before freshness is tested; increment occurs only when abs(timestamp-player.tickCount)<=4 (@17–55). There is no event-byte==2 guard in combo.

**Strong inference.** This is one increment per newly correlated outgoing target timestamp, not a per-click or universal per-hit counter. Repeated hurt/status callbacks with the same timestamp cannot increment again; multiple attacks within one player tick share a timestamp and can collapse. A stale first callback consumes the timestamp even though no increment occurs. Two modern packet routes both synthesizing byte 2 do not necessarily double count because the timestamp gate deduplicates them. Which packets arrive, their order and whether a particular attempt registers are runtime unknowns.

REACH_DISPLAY differs: L._88f3cf._bb4487._327414._cfe983._590f69(attackEvent) @0–37 stores target ID, candidate distance, and player tickCount. Status handler @0–64 requires byte==2, matching ID, and currentTick-sentTick<=4 (no explicit lower bound); then display=min(current attack range,candidate distance). This confirms the existing correlation branch in its now-resolved tick units.

## S6-RC-05 — periodic reset producer timing resolved

**Confirmed.** modern Minecraft mixin ML._d4ca6c._1e73d7._590f69._a140a8.lunar$preRunTick injects at tick()V HEAD. @0–13 posts pre-tick event _3a14e3; @14–26 checks its static _dbf1c0 count is nonzero and divisible by 20; @29–42 posts _1eb51c; @43–48 increments that count. Thus _1eb51c is periodic on the global client pre-tick counter, every 20 ticks after the initial zero, before the increment. It is not a wall-clock timer and is not indexed to a particular player's birth tick. bridge$processRewindTick @0–48 repeats this exact posting and increment sequence. No deeper Replay/Reverse investigation was performed.

**Strong inference.** The 80-tick stale thresholds in the two modules are sampled on these periodic callbacks, and their existing reset-phase boolean clears on alternating eligible stale callbacks. Consequently displayed expiry is not an exact four-second timer; it depends on player ticks, global phase, previous flag state, pauses and actual tick cadence. At a nominal 20 ticks/second, callback cadence is about one second, but no runtime wall-time guarantee was measured.

## S6-RC-06 — modern clamp range implementation resolved

**Confirmed.** Player mixin ML._d4ca6c._1e73d7._02d7ad._590f69._d4ca6c._bb4487.bridge$entityAttackRange @0–44: MC_VERSION>=35 reads active ItemStack DataComponents.ATTACK_RANGE; absent component falls back to AttackRange.defaultFor(this); returns effectiveMaxRange(this) converted float→double. Earlier versions delegate to bridge$entityInteractionRange @45–49. That helper calls entityInteractionRange$v1_20_5 for MC_VERSION>=22; earlier it asks MultiPlayerGameMode.hasFarPickRange and returns 6.0 or 3.0 (@13–37). These source branches resolve the bridge implementation; component internals and attributes' complete algorithms were not needed to establish this boundary.

## Gap disposition and limits

G-04 is **resolved for the retained modern implementation**: attack producer and distance inputs, counter backing field and units, periodic producer/timing, and current range source are concrete. G-05 is **resolved for the retained modern implementation and inspected Minecraft cache bodies**: outgoing target and timestamp writer are traced, and count is timestamp-correlated rather than universal hit increment. Actual launch/cache selection, all legacy implementations, packet arrival ordering, pause/tick-rate behavior and runtime correctness remain unknown. No credentials, personal profiles or remote services were read. The installation remained read-only; extracted class copies and report files reside only in session6-sol.
