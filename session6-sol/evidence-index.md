# Session 6 — Evidence index

Date: 2026-10-11. This index maps discoveries to implementation evidence rather than creating another feature inventory. All target access was read-only/static. JVM offsets are decimal method-local instruction offsets; native coordinates are explicitly RVA or file offset. No new deep-native decompilation, runtime observation or native REA Evidence ID is claimed.

## Identity, provenance and confidence

`L=com.moonsworth.lunar.client`; `ML=com.moonsworth.lunar`. Each obfuscated 30-character token is replaced by `_` plus its first six MD5 hexadecimal digits. A short name is only a reading aid: authoritative original JVM names are in the linked manifests/full disassembly. Hashes are SHA-256. Fresh JDK 21 javap does not initialize or execute target classes. Retained 8,095-class disassembly was used to discover references; selected defining and caller classes were freshly checked against installed JARs. That discovery cache is not a whole-installation completeness claim.

**Confirmed** refers to bytes/bytecode/annotations. **Derived / Strong inference** refers to the stated conditional consequence. **Unknown** is retained where bytes or authorized observation do not decide the question. Reports state each discovery's confidence and limits separately.

Artifact directory: `C:\Users\Admin\.lunarclient\offline\multiver`.

| Artifact | SHA-256 | Role |
|---|---|---|
| lunar.jar | bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9 | Client, bridges, RPC/library and WebOSR wrappers |
| modern-0.1.0-SNAPSHOT-all-nomappings.jar | 99df64c5913e9a32111135bfde140343d4baa954fe5ba08069962670566db02e | Actual modern Minecraft mixins and GPU bridge |
| common-0.1.0-SNAPSHOT-all-nomappings.jar | 440e1e6fbf2f22b1ed74e2a14c1a27fe6ffcbf45bd6aeff595f19732ad4aeee3 | Bounded Session method-reference scan |
| genesis-0.1.0-SNAPSHOT-all.jar | c188afc0d9efd61eb994c23883b70e942dbd2d88777550edae24649849a1f046 | Bounded Session method-reference scan |
| natives/WebOSR-Binding.dll | 4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf | Fresh identity check; prior exact export/native-byte table reused |

The exact four-JAR hashes and class counts are also in [session-methodrefs.json](evidence-native/session-methodrefs.json). Installed Minecraft cache archives and copied class hashes are in [vanilla/manifest.json](evidence-reach/vanilla/manifest.json); no selected-launch cache identity is asserted.

## Discovery-to-evidence map

| Discovery | Exact implementation anchor | Evidence / interpretation |
|---|---|---|
| S6-RC-01, G-04 tick units | ML._590f69._2ce426._1e73d7._0be1fc mapping annotations | [Class identity](evidence-reach/ML._590f69._2ce426._1e73d7.json), [verbose aliases](evidence-reach/ML._590f69._2ce426._1e73d7.aliases.txt), [report](reach-combo-findings.md) |
| S6-RC-02, G-05 outgoing-target writer | modern LivingEntity mixin getter @0–10; cached LivingEntity.setLastHurtMob @0–30; Player.attack @313–315 | [Mixin identity](evidence-reach/ML._d4ca6c._1e73d7._02d7ad._590f69._a140a8.json), [cache manifest](evidence-reach/vanilla/manifest.json), [report](reach-combo-findings.md) |
| S6-RC-03 attack ray-distance producer | MultiPlayerGameMode.lunar$clickMouse$eventPreAttackEntityClient @0–38, lambda @46–82; min35 piercing producer | [Original class identity](evidence-reach/ML._d4ca6c._590f69._21aca6._1e73d7._bb4487._590f69.json), [focused methods](evidence-reach/focused-excerpts.json) |
| S6-RC-04 combo correlation/status routes | L._88f3cf._bb4487._429bf0._cfe983 @17–55; ClientPacketListener status/hurt producers | [Root identity](evidence-reach/L._88f3cf._bb4487._429bf0._cfe983.json), [producer identity](evidence-reach/ML._d4ca6c._590f69._21aca6._2f4182._1e73d7.json), [report](reach-combo-findings.md) |
| S6-RC-05 periodic reset sampling | modern Minecraft.lunar$preRunTick @14–48 | [Identity](evidence-reach/ML._d4ca6c._1e73d7._590f69._a140a8.json), [focused methods](evidence-reach/focused-excerpts.json) |
| S6-RC-06 modern range source | Player.bridge$entityAttackRange @0–49 | [Identity](evidence-reach/ML._d4ca6c._1e73d7._02d7ad._590f69._d4ca6c._bb4487.json), [report](reach-combo-findings.md) |
| S6-SUPPORT-01/02/08, G-18 lifecycle and stored/effective terminology | observer _55938e @67–105; interceptor setter @89–147; toggle isEnabled @0–15 | [29-class fresh manifest](evidence-support/session6-manifest.json), [exact call scan](evidence-support/xref-ddda795f2e.json), [setter scan](evidence-support/xref-5d1f08a4fd.json), [producer table/report](support-findings.md) |
| S6-SUPPORT-03/04, G-19/G-22 single-slot/decorator | L._ec7e36._1e73d7._2ce426._cfe983 @56–86; Boolean decorator _f34034 @0–39 | [Manifest](evidence-support/session6-manifest.json), [interceptor hierarchy](evidence-support/interceptor-hierarchy.json), [report](support-findings.md) |
| S6-SUPPORT-05/06 reset/removal | holder _0ee36d @0–22; metadata load @71–126; server refresh _f636dc @18–32 | [Reset/dependency scan](evidence-support/xref-1107f11423.json), [manifest](evidence-support/session6-manifest.json), [report](support-findings.md) |
| S6-SUPPORT-07, G-21 dependency order | collector _4cf8c3 @0–150; allowance _91843f @0–101 | [Read/listener registration scan](evidence-support/xref-9c3224f2c1.json), [manifest](evidence-support/session6-manifest.json), [report](support-findings.md) |
| S6-RPC-01, G-13 all 16 callers and response bindings | exact enclosing signatures, offsets and callbacks in audit; radio _1253fc @0–46; checkout callbacks @21–47 | [Caller audit](evidence-rpc/caller-audit.json), [original classes](evidence-rpc/caller-manifest.json), [report](rpc-findings.md) |
| S6-RPC-02, G-14 null-message precursor | Draft_6455.processFrameContinuousAndNonFin @69–104; decodeFrames @106–132; Lunar onError @0–6 | [Draft](evidence-rpc/Draft_6455.javap.txt), [Exception constructor](evidence-rpc/InvalidDataException.javap.txt), [decode](evidence-rpc/WebSocketImpl.javap.txt), [report](rpc-findings.md) |
| S6-RPC-03, G-16 receive serialization | WebSocketClient.run @377–415; onMessage→accept @35–43 | [Client library](evidence-rpc/WebSocketClient.javap.txt), [accept callers](evidence-rpc/response-accept-callers.txt), [report](rpc-findings.md) |
| S6-RPC-04/05, G-17 old references/capability overwrite | main worker _a61e7a @0–21; transport constructor @40–49; capability callbacks @55 | [Transport](evidence-rpc/transport-full.aliases.txt), [manifest](evidence-rpc/caller-manifest.json), [report](rpc-findings.md) |
| G-11 exact map/wrapper/paired calls | diagnostic map read @26; six wrapper and eight paired invocation instructions | [Focused exact-owner call scan](evidence-bus/focused-callers.json), [fresh caller manifest](evidence-bus/focused-manifest.json), [report](bus-findings.md) |
| G-10 escaping policy/report/replay paths | base _1253fc @16–77; _57e17e @0–14; _455ac7 @13–87; reporting getMessage/capture | [Base identity](evidence-bus/L._ba7d98._1e73d7.json), [fresh reporting/caller manifest](evidence-bus/focused-manifest.json), [report](bus-findings.md) |
| S6-PE-01..04, G-02 potion formulas/hooks | shared alpha @29–118; vanilla comparator @0–164; three renderer dimensions; cancellable inventory HEAD hooks | [Focused methods](evidence-potion/focused-excerpts.json), per-class JSON identities beside them, [report](potion-followup.md) |
| S6-AR-01..05, G-01 armor formulas | group/individual geometry; protection _cc7511 ixor @286; custom 20-point allocation; alternate 20-unit tiles | [Focused methods](evidence-armor/focused-excerpts.json), eight per-class original-name/hash JSON manifests beside them, [report](armor-followup.md) |
| S6-WEB-01, G-31 JNI mismatch and no symbolic Session callers | 56 declarations versus 58 named exports; 27,075 class occurrences scanned | [Declarations](evidence-native/jni-declarations.json), [reconciliation](evidence-native/jni-reconciliation.json), [constant-pool scan](evidence-native/session-methodrefs.json), [report](jni-and-webosr.md) |
| S6-WEB-02, G-30 byte stride/region/conversion/staging | bridge$uploadBgra @0–190; OpenGL @12–184; static staging _8cc4be @0–41 | [Fresh class manifest](evidence-native/class-manifest.json), [staging/lifecycle manifest](evidence-native/lifecycle-manifest.json), [report](jni-and-webosr.md) |
| S6-WEB-03 reverse transfer/lifetime boundaries | image wrapper update @8–65; delete @0–140 | [Lifecycle manifest](evidence-native/lifecycle-manifest.json), [focused callers](evidence-native/native-boundary-focused.json), [report](jni-and-webosr.md) |
| S6-WEB-04, G-32 codec continuation | FunctionBus.buildInvocationParameters @257–273; PromiseJS.resolve @19–100; Lunar objectToString @0–15 | [Wrapper manifest](evidence-native/class-manifest.json), [codec subclass manifest](evidence-native/lifecycle-manifest.json), [report](jni-and-webosr.md) |
| Native environment and Java lifecycle | live provider Java accepted21.0.10; manager _d82ff1 @130–186/_ba2ddc @0–76; renderer _02d7ad @7–38 | [Live provider](provider-status-live.json), [shell probe](environment-probe.json), [lifecycle manifest](evidence-native/lifecycle-manifest.json), [native report](native-rendering-analysis.md) |
| S6-FBUS-01..04, G-33 invoke and recovery boundaries | annotated invoke router @22; FunctionBus enqueue @172–189, unknown return @98, drain @0–23; three iteration callers | [Fresh original-name manifest](evidence-functionbus/manifest.json), [caller/guard/recovery report](functionbus-followup.md) |
| Five native seeds, reused exact byte authority | RVAs 10a30,1c3b0,1c400,1fc10,29690; helper199c0 | [Session 4 PE address/byte table](../session4-sol/evidence-native/binding-pe-addresses.json), fresh identity [reconciliation](evidence-native/jni-reconciliation.json), [native disposition](native-rendering-analysis.md) |

## Evidence validation and reproducibility

[verify_evidence.py](verify_evidence.py) checks referenced installed ZIP class bytes against supplied class hashes, supplies additional raw class hashes for manifests that only had output hashes, checks local Markdown links and required reports, and hashes Session 6 deliverables. It never loads target classes. Results: [evidence-validation.json](evidence-validation.json); complete report/helper/evidence integrity list: [evidence-integrity.json](evidence-integrity.json). These are validation artifacts, not native analysis results.

Important schema distinction: `evidence-support/session6-manifest.json` and `evidence-functionbus/manifest.json` rows' `sha256` hashes fresh verbose **disassembly text**, whereas native/reach/potion/armor `class_sha256` fields hash raw class bytes. `evidence-rpc.sha256.json` hashes saved evidence files. Do not compare those different objects. Supplemental `evidence-validation.json` explicitly names both raw-class and evidence-output hashes.

Helper scripts preserve discovery/reproduction details: [analysis_helper.py](analysis_helper.py), [bus_collect.py](bus_collect.py), [native_java_collect.py](native_java_collect.py), [reconcile_native.py](reconcile_native.py), [reach_helper.py](reach_helper.py), [support_static.py](support_static.py), [rpc_collect.py](rpc_collect.py). Several discovery helpers depend on the earlier scratchpad cache path recorded in their source; fresh evidence and raw identities remain readable without that cache. The preliminary broad bus alias scan is preserved but explicitly superseded by exact owner/descriptor `focused-callers.json`. Older `provider-status.json` is retained; current provider conclusions use `provider-status-live.json`.

No prior session report/evidence was overwritten, and no target executable was launched. Full native answers, runtime frequencies and selected-launch identities are intentionally not implied by a successful local validation.
