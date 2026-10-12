# Session 5 — Independent verification audit of Session 4 (SOL)

Date: 2026-10-11. Author: Session 5 (Deepseek). Static-only. **No Lunar JAR, native library, JavaScript or other target code was executed, loaded, attached to, or modified.** Installation files remained read-only. No credentials, accounts, tokens, installation identifiers or personal settings values were read. No anti-cheat/integrity investigation, protection bypass or reimplementation was performed.

This file independently re-checks the seven Session-4 (SOL) headline findings against the shipped bytes and bytecode. It does not re-run the event catalog or completed inventories.

## 0. Method and tool reality

**Tooling actually used in this session:**

| Tool | Identity | Used for |
|---|---|---|
| REA MCP | `rea.binary_session` (reachable; session closed) | Provider/availability probe only. **No deep native provider is configured** (see below). |
| JDK `javap` | Microsoft **JDK 21.0.10** (`C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe`) | Fresh `-p -c` disassembly of extracted classes (new evidence in this folder) |
| Analyst Python | Python 3.11.9 | Reading retained JSON evidence (PE export RVAs) |
| Retained evidence | `session4-sol/evidence-*/` | Cross-checks against SOL's own dumps |
| Extracted class tree | Session-4 scratchpad `...\Temp\claude\...\scratchpad\{lunar,modern,genesis}` | Independent disassembly source (NOT a new extraction of Lunar; the same bytes SOL used) |

**Provider reality (independently re-observed, not copied).** `rea.binary_session` reports Ghidra **unavailable / `not_configured`**: `GHIDRA_INSTALL_DIR` is not set, `analyzeHeadless` missing, matching native decompiler missing. Hopper is `unsupported_host` (win32). IDA is `not_configured`. This matches `provider-availability.json` and `session4-sol/status-and-corrections.md`; **no native decompilation was possible in Session 5 either.** A separate live-observation anomaly is recorded in [contradictions.md](contradictions.md) (REA now resolves a different `java_home` than Session 3 recorded).

**What this means for the audit.** Findings that live entirely in Java bytecode are independently re-verifiable and were re-verified from fresh `javap`. Findings that depend on native decompilation cannot be upgraded and are assessed only for the correctness of the *static* claims made. No finding is marked VERIFIED on a claim that cannot be checked with the available tools.

**No new REA Evidence IDs were created in this session.** Where this audit cites REA identifiers, they are Session-2/3/4 identifiers read from retained exports. Console/`javap` citations are given with artifact, class, method and method-local bytecode offset.

**Alias convention.** `L._d4ca6c._590f69` etc. are SOL's analyst shorthand for obfuscated `com.moonsworth.*` classes; the exact JVM identity of each alias used here is given inline on first use and in `session4-sol/evidence-*/class-mapping` files.

## 1. Verdict table

| # | SOL finding | Verdict | Basis |
|---|---|---|---|
| 1 | Wrong-thread event checks log rather than reject dispatch | **VERIFIED** | Fresh `javap`; method returns unconditionally, no throw/queue/skip |
| 2 | Deferred listener additions can receive the current event | **VERIFIED (scoped)** | Fresh `javap`; true on the pending-add path only |
| 3 | RpcChannel requests expire after ten minutes without notifying failure callbacks | **VERIFIED** | Fresh reading of retained channel dump + constant pool |
| 4 | Disconnect cleanup does not notify pending callbacks | **VERIFIED** | `invalidateAll` + EXPLICIT-ignoring removal listener |
| 5 | Saved toggle intent, effective enablement, and event subscriptions are separate states | **VERIFIED** | Fresh bytecode: `updateEnabled` precedence, distinct fields |
| 6 | The six additional feature traces accurately represent their implementations | **PARTIALLY VERIFIED** | 6/6 spot-checked claims reproduced; every trace is explicitly self-labelled partial |
| 7 | WebOSR JNI mappings and Java-side queue/lifetime behavior are correctly documented | **VERIFIED (Java) / native architecture INSUFFICIENT EVIDENCE** | Java contracts + PE export RVAs reproduced exactly; native internals unverifiable without a provider |

No finding was CONTRADICTED. One scope over-statement risk is flagged in finding 2 (headline vs. branch scope). Detail follows.

---

## 2. Finding-by-finding

### Finding 1 — Wrong-thread check logs, does not reject dispatch — **VERIFIED**

- **Artifact:** `lunar.jar` (`bf36e10e…`, unchanged per `session4-sol/evidence-native/class-map.json` → `lunar.sha256 = bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9`).
- **Class/method:** base bus `L._d4ca6c._590f69` = `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII`; private method `RHCCHHHHIHHRIICRIHRRIHRORIIOHO(Class)` (SOL alias `_a140a8`).
- **Fresh evidence:** `evidence/bus-base.javap-c.txt` lines 987–1006. Method begins `0: getstatic ORCHIOIHCIRHOROOOIHCRCOCCHIIOI:Z / 3: ifne 7 / 6: return`; then `7: ldc …external-thread-marker class / 10: isAssignableFrom / 13: ifeq 17 / 16: return`; then `17: invokestatic …ICRORIHOHOIHCCROIHOORIHHROORHI()` render-thread predicate, `20: invokeinterface …OHIHOICHOROCHRRHROHIIIRRROCOOO:()Z / 25: ifne 47`; failure branch `28–44` calls a logger then `44: invokestatic java/lang/Thread.dumpStack:()V`; `47: return`.
- **Verdict:** the method has exactly three return sites (early flag-off, external-thread marker, end) and **contains no `throw`, no queue write, no cancellation of dispatch**. The name clue in the feature flags (`THROW_ON_WRONG_THREAD_*`) does not describe this method's action.
- **Call sites (fresh):** `bus-base.javap-c.txt` shows this private method invoked at bytecode `2:` of the two public registration paths (lines 328, 441) and the paired posting path (521, 524). It is a **diagnostic executed on the public posting/registration entry**, consistent with SOL.
- **Corroboration of the bridge predicate:** SOL cites modern bridge `ML._d4ca6c._d4ca6c._21aca6._21aca6._21aca6._3d8570 @0–17` using `RenderSystem.isOnRenderThread()`. Retained `session4-sol/evidence-bus/ML-…-21aca6.aliases.txt` exists; I did not need to re-derive it to confirm finding 1. **Confidence:** Confirmed (implementation). Runtime flag state and real thread identities remain Unknown (as SOL states).

### Finding 2 — Deferred additions can receive the current event — **VERIFIED (with scope)**

- **Class/method:** same base bus; protected helper `COOCHIRORIICRCIIRIROHIIRIRICCH(Class,T,Supplier)` (SOL alias `_cfe983(Class,event,Supplier)`).
- **Fresh evidence:** `evidence/bus-base.javap-c.txt` lines 187–266. Guard at `0–20` (`aload_2 ifnonnull 8 … List.isEmpty ifeq 21 … return`). The deferred/addition walk begins at bytecode **21** and runs to the end:
  - `44: if_icmpge 138` loop bound = captured list size;
  - `65: getfield HICIHROOOORRCRRCCHOIHHORORCCHH:Z` (an add/remove discriminator) and `75/78: getfield HHHIOIHHRRHROOICCHRCRRRIRROHRR:Class` compared to the posted class `if_acmpne 132`;
  - `109/111: getfield CCIHCOCRHICCRIICRRCCOOHCOORROH:Consumer` then `115: Consumer.accept(aload_2)` — **the current event object is passed to the pending consumer**;
  - `138/142 List.size` then `149/153 if_icmpne 27` **re-runs the scan while the tail list keeps growing** (self-registration re-entry);
  - `156/158 ifeq 165` then `162: OHRCRIICRROCCIORHCCICIOOCOCHHI()` (post-replay hook).
  - Exception table covers `82–120` → handler `123`, calling `COOCHIRORIICRCIIRIROHIIRIRICCH(Throwable,Class)` (the distinct pending policy helper).
- **Verdict:** additions queued during dispatch can be invoked against the **current** event, in insertion order, and the loop re-reads the growing list. Matches SOL's `S4-BUS-03`.
- **Scope correction (important).** This behavior exists only where the pending helper is reached with a non-null event, i.e. the supplier posting path and the paired PRE/POST path. **Ordinary array-only dispatch has no pending list to walk** (pending entries only exist while `depth != 0`; the private register/remove implementations append only then). SOL already states this ("Indirectly via pending path"), but the README headline "Deferred additions can receive the current event" should be read in that branch scope — see [contradictions.md](contradictions.md) (C-4).
- **Confidence:** Confirmed (implementation branch). A live self-registration loop was not executed.

### Finding 3 — RpcChannel: 10-minute expiry, no failure callback — **VERIFIED**

- **Class/method:** `L._cb9292._21aca6` = `com.moonsworth.lunar.client.COOIOIRCCICRCCIHCCRHRCIHROHCCI.RROHOCRCCHCIORHICIHCOHRIRCIHCI` (channel). Evidence: `session4-sol/evidence-rpc/rpc-channel.verbose.javap.txt` (constant pool) and `rpc-channel.javap.txt` (code).
- **Evidence:**
  - constant pool: `#52 TimeUnit.MINUTES`, `#54 CacheBuilder.expireAfterWrite:(JLjava/util/concurrent/TimeUnit;)`, `#66 CacheBuilder.removalListener:`, `#120 InvokeDynamic #3:onRemoval:`, `#46 RemovalListener` — the `expireAfterWrite(10, MINUTES)` policy is real and is a **cache** policy, not a scheduled caller timeout.
  - `callMethod @0–164`: `4: isOpen ifne 41` (closed → log + `return` at 40, no callback/controller failure); `41 UUID.randomUUID → 44/47 ByteString.copyFromUtf8`; build envelope `52–113`; `118–150` **`Cache.put(requestId, pending)` BEFORE `155–164 transport.send`**; no catch around send.
  - removal listener `COOCHIRORIICRCIIRIROHIIRIRICCH(RemovalNotification) @0–42`: `1 getCause / 4 getstatic RemovalCause.EXPLICIT / 7 if_acmpne 11 / 10 return` → EXPLICIT ignored; else logs `value.methodName + cause` at `11–39`. **No RpcCallback invocation.**
- **Verdict:** exactly SOL's `S4-RPC-01/02`. The "ten minutes" is a write-expiry policy; expiry logs and abandons; it does not complete the caller. **Confidence:** Confirmed (implementation). Physical maintenance timing / transitive caller deadlines remain Unknown.

### Finding 4 — Disconnect cleanup does not notify pending callbacks — **VERIFIED**

- **Evidence:** channel cleanup `ORIRHCHRRHRCCOCIHCOOCHHOHCCCIO() @0–9` = single call `Cache.invalidateAll()`. `session4-sol/evidence-rpc/transport-lifecycle.javap.txt` shows transport `onClose(int,String,boolean) @…` calling that cleanup at `4` then updating disconnect state (`READY` static at 173 region). Because `invalidateAll` removals are `RemovalCause.EXPLICIT`, the removal listener **returns immediately** — disconnect is silent abandonment.
- `onError(Exception)` at line 195 region: `1: invokevirtual Exception.getMessage / 6: String.startsWith` with **no null guard** before the dereference; it does not invalidate the cache.
- **Verdict:** SOL's `S4-RPC-04` reproduced. **Confidence:** Confirmed (implementation); a null-message NPE is a Strong inference, not observed.

### Finding 5 — Four distinct states (intent / effective / subscription / …) — **VERIFIED**

- **Effective precedence** — class `L._88f3cf._cfe983` = `com.moonsworth.lunar.client.RIHHCHHHROOHOOIOIIRIOOCRHHOOOR.COOCHIRORIICRCIIRIROHIIRIRICCH`, `updateEnabled()`: `session4-sol/evidence-support/L._88f3cf._cfe983.short.javap.txt` shows `134: public final void updateEnabled()`, `145: invokeinterface L/_88f3cf/_21aca6.isEnabled` (parent), `185: invokeinterface L/_88f3cf/_a1dd3a._98d4d1` (dynamic allowance), and a `Boolean.booleanValue` read at `209/210`. This matches SOL's ordered gates: **parent → server → dynamic allowance → Boolean override → interface default**.
- **Override category order** — enum class `L._c8175c._cfe983._21aca6`: `…short.javap.txt` lists `SERVER`, `CLIENT_INTERNAL`, `CLIENT_REMOTE`, `CLIENT_CRITERIA`, `CLIENT_OVERRIDE` in exactly that declared order (`$values` at 54–70, names at 78–110). Under `EnumMap` iteration, earlier non-null wins — so **`CLIENT_OVERRIDE` is not highest priority**, as SOL states (`S4-SUPPORT-05`).
- **Field separation** — `enabled` (private effective flag) is declared separately; the ordinary stored toggle lives on `L._88f3cf._2ce426` (`isEnabled`); handler-subscription state lives on `L._88f3cf._1e73d7._429bf0`; server flip intent on `L._88f3cf._1e73d7._ba7d98._83eb1a`/`setFlipped`. SOL's four-way distinction is implemented as separate fields/branches.
- **Verdict:** `S4-SUPPORT-01..06` reproduced at the branch level. **Confidence:** Confirmed (implementation). Actual override producers / personal payloads remain unknown by design.

### Finding 6 — The six module traces accurately represent their implementations — **PARTIALLY VERIFIED**

Every headline algorithmic claim I sampled reproduced, but each SOL module report is explicitly self-labelled "Partial" and several sub-branches remain open, so this is not "fully verified".

| Module | SOL headline | Independent check | Result |
|---|---|---|---|
| ARMORSTATUS | integer `remaining=(max-dmg); pct=(remaining*100)/max` | `evidence-modules-a/L__88f3cf__bb4487__21aca6__1e73d7__21aca6.short.txt`: `100: bipush 100`, `129: isub`, `134: bipush 100`, `136: imul`, `138: idiv` | Reproduced (integer, not float) |
| POTION_EFFECTS | VANILLA duration: `sec=floor(dur/20)`, then ≥3600→h, ≥600→m | `…52e8ee__bb4487.short.txt`: `ldc float 20.0f` at 191; `sipush 3600` (196/199); `sipush 600` (204) | Reproduced (thresholds/20-division present) |
| TOGGLE_SNEAK | sneak toggle ≤200 ms, sprint ≤400 ms (wall clock) | `…91398c__590f69.short.txt`: `570: ldc2_w long 200l / 571 lcmp / 572 ifgt`; `617: ldc2_w long 400l / 618 lcmp` | Reproduced (200/400 distinct) |
| REACH_DISPLAY | status byte 2, counter delta ≤4, `min(attackRange, dist)` | `…327414__cfe983.short.txt`: `iconst_2 / if_icmpne`; `bridge$entityAttackRange`; `Math.min` at 149; `getDistance` at 15 | Reproduced |
| COMBO | reference identity attacker; |Δ|≤4; store timestamp before freshness test | `…429bf0__cfe983.alias.txt`: `bridge$getLastAttacker` Optional; `5: if_acmpeq`; `getLastAttackerTime`/`_0be1fc`; `223: iconst_4 / if_icmpgt` | Reproduced |
| PACK_DISPLAY | packOrder==FIRST selects the **last** list element | `…59b0c6__cfe983.alias.txt`: `getstatic …$cfe983.FIRST` at 135/467; `bridge$getAllSelectedPacks` at 475; `List.size` at 489 then `List.get(I)` at 495 | Reproduced (size used as index → last element) |

- **Verdict:** **PARTIALLY VERIFIED.** The six headline mechanisms are accurate; the module reports' own "Partial" caveats are honest and I did not find an overstatement in the sampled claims. The still-open sub-branches are carried forward in [remaining-gaps.md](remaining-gaps.md). **Confidence:** Confirmed for the sampled claims; the reports are not complete specifications and do not claim to be.

### Finding 7 — WebOSR JNI mappings + Java queue/lifetime — **VERIFIED (Java) / native architecture INSUFFICIENT EVIDENCE**

- **Java queue/lifetime — reproduced:**
  - `WebEngine` (`evidence-native/com.moonsworth.webosr.wrappers.WebEngine.fresh-verbose.txt`): field `private final java.lang.Thread owner;`; `<init>` `6: Thread.currentThread / 9: putfield owner`; `invokeIteration @82…`: `1: getfield owner / 4: currentThread` compare, `13: FunctionBus.consumeMainActorQueue()`, then **`17: invokevirtual invokeIteration0()` unconditionally**.
  - `FunctionBus` static init: `evidence-native/com.moonsworth.webosr.javascript.FunctionBus.fresh-verbose.txt` line 1896 `static {}`: `new ArrayBlockingQueue / sipush 4096 / <init>(I) / putstatic MAIN_ACTOR_QUEUE`. Queue is `ACC_PROTECTED, ACC_STATIC, ACC_FINAL`; `add` at instruction 186. → shared static 4096-capacity queue, `add` (not `put`/`offer`), consistent with `S4-NATIVE-03/04`.
  - `NativeHandle.close @0–18`: `getfield handle / lconst_0 / lcmp / ifeq 18 / destroy() / putfield 0L` — not synchronized/CAS. Consistent with `S4-NATIVE-05`.
- **PE export mappings — reproduced exactly.** Independent Python read of `session4-sol/evidence-native/binding-pe-addresses.json` (`evidence/pe_rva.py`) returns, among 58 records:

| Export | RVA | File offset | Entry bytes (hex, prefix) |
|---|---:|---:|---|
| `Browser_swapBuffers` | 0x1FC10 | 0x1F010 | `4883ec28e827f1ffff488b4820488b01ff90b8…` |
| `Session_getName` | 0x29690 | 0x28A90 | `48895c24184889742420574881ec50010000…` |
| `WebEngine_setTimers` | 0x1C400 | 0x1B800 | `48895c2408488974241048897c2418415648…` |
| `WebEngine_invokeIteration0` | 0x1C3B0 | 0x1B7B0 | `4883ec28e807d6ffff488b88e8000000488b01…` |
| `WebOSR_createEngine` | 0x10A30 | 0x0FE30 | `4053565741544155415641574881ecb00200…` |

These match SOL's table (`0x1fc10 / 0x29690 / 0x1c400 / 0x1c3b0 / 0x10a30`) and the `invokeIteration0` 27-byte stub decode (`48 83 ec 28 / e8 07 d6 ff ff / 48 8b 88 e8 00 00 00 / 48 8b 01 / 48 83 c4 28 / 48 ff 60 08`), reproduced byte-for-byte.
- **Native architecture — cannot be verified.** SOL's own conclusion is that native paint/threading/dirty-rect/texture-callback internals are unavailable without a deep provider. That remains true; nothing in Session 5 upgrades or contradicts it. The **static** claims made (export destinations are real code, not forwarders; the wrapper is a forwarding stub) are reproducible; the **architectural** claims are explicitly labelled inference and stay inference.
- **Verdict:** Java-side = **VERIFIED**; native implementation architecture = **INSUFFICIENT EVIDENCE** (unchanged from SOL). **Confidence:** Confirmed (Java + PE metadata); Unknown (native).

---

## 3. Cross-cutting observations

1. **SOL's evidence is internally reproducible.** For every sampled finding I obtained the same structure from the same bytes. No sampled claim was contradicted.
2. **SOL's confidence labels are calibrated.** It over-labels rather than under-labels: every item I re-checked was either exactly reproduced or, where branch-scoped, already flagged by SOL. The one place a *headline summary* is broader than the *report body* is finding 2 (README one-liner vs. branch scope); this is a documentation nuance, not a technical error.
3. **Offsets are consistent.** Method-local decimal offsets in SOL's reports reproduce in fresh `javap` (e.g. bus pending helper "21–165" = guard 0–20 then walk 21…).
4. **Nothing here required creating new REA Evidence.** The bytecode and PE metadata are self-verifying; inventing REA IDs would have been fabrication.
5. **The biggest real gap is unchanged: no native provider.** Session 4's native section is the weakest area and it is weakest for tool-infrastructure reasons SOL documented, not because SOL over-claimed.
