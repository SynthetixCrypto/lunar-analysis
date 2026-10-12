# Session 5 evidence index (verification addendum)

Date: 2026-10-11. Session 5 (Deepseek). This index covers **only** the new evidence produced by Session 5 (independent verification). It complements, and does not replace, the session-2/3/4 indexes.

## Scope and integrity of this index

- Static, read-only. No Lunar JAR/native/JS executed or loaded; installation untouched; no credentials/personal data read.
- **No new REA Evidence IDs were created.** All REA identifiers cited in Session 5 are session-2/3/4 identifiers read from retained exports. Fabricating new IDs would misrepresent provenance.
- The new evidence consists of **fresh `javap -p -c` disassembly** of Lunar classes (the same obfuscated bytes sessions 3–4 used), a **PE export-table read** of the session-4 retained JSON, and **reader notes**.
- Artifact identity is anchored to session-4's recorded digests (unchanged this session):

| Artifact | SHA-256 (as recorded by session 4) |
|---|---|
| `lunar.jar` | `bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9` |
| `modern-0.1.0-SNAPSHOT-all-nomappings.jar` | `99df64c5913e9a32111135bfde140343d4baa954fe5ba08069962670566db02e` |
| `WebOSR-Binding.dll` | `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf` |

Obfuscated classes were disassembled from the session-4 scratchpad extraction (`…\Temp\claude\…\eeca5643-\scratchpad\{lunar,modern}\…`), **not** from a new extraction. The scratchpad is a temp path and is not a durable dependency; the class identities and offsets below are what matter and are reproducible from any faithful extraction of the same `lunar.jar` digest.

## Session-5 evidence files (this directory)

| File | Produced by | What it shows | Authoritative? |
|---|---|---|---|
| `evidence/bus-base.javap-c.txt` | JDK 21 `javap -p -c` | Full base event-bus class `RORCICOHRIOIIIOIOHIIIICRCIHRII`: thread-check `RHCCHHHHIHHRIICRIHRRIHRORIIOHO`, pending helper `COOCHIRORIICRCIIRIROHIIRIRICCH(Class,T,Supplier)`, constructor, exposure getters | Full dump (authoritative) |
| `evidence/pe_rva.py` | Python 3.11 (stdlib `json`) | Extracts and prints the five named export records from the retained session-4 PE JSON | Reader; source JSON is authoritative |
| `evidence/` (console outputs referenced inline) | `javap`, Python, PowerShell | Method-header line indexes, bytecode greps | Reading aids |

`bus-base.javap-c.txt` was generated with:
`javap -p -c -classpath <scratchpad>\lunar com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII`

## Class identity map used in Session 5

| Alias (session 4) | JVM class | Source |
|---|---|---|
| `L._d4ca6c._590f69` (bus base) | `com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RORCICOHRIOIIIOIOHIIIICRCIHRII` | `session4-sol/evidence-bus/class-mapping.json` |
| `L._d4ca6c._cfe983` (bus debug subclass) | `…RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.COOCHIRORIICRCIIRIROHIIRIRICCH` | same |
| `L._cb9292._21aca6` (RpcChannel) | `com.moonsworth.lunar.client.COOIOIRCCICRCCIHCCRHRCIHROHCCI.RROHOCRCCHCIORHICIHCOHRIRCIHCI` | `session4-sol/evidence-rpc/class-map.tsv` |
| `L._cb9292._21aca6$_cfe983` (pending entry) | `…RROHOCRCCHCIORHICIHCOHRIRCIHCI$COOCHIRORIICRCIIRIROHIIRIRICCH` | same |
| `L._88f3cf._cfe983` (feature base) | `com.moonsworth.lunar.client.RIHHCHHHROOHOOIOIIRIOOCRHHOOOR.COOCHIRORIICRCIIRIROHIIRIRICCH` | `session4-sol/evidence-support/mapping.json` |
| `L._c8175c._cfe983._21aca6` (override category enum) | `com.moonsworth.lunar.client.IROCROOIOIORORHHCCOOCCHRRRIOIC.COOCHIRORIICRCIIRIROHIIRIRICCH.RROHOCRCCHCIORHICIHCOHRIRCIHCI` | same |
| `WebEngine` | `com.moonsworth.webosr.wrappers.WebEngine` | `session4-sol/evidence-native/class-map.json` |
| `FunctionBus` | `com.moonsworth.webosr.javascript.FunctionBus` | same |
| `NativeHandle` | `com.moonsworth.webosr.NativeHandle` | same |

## Claim → evidence → verdict (Session-5 rows)

| ID | Claim (source report) | Primary Session-5 evidence | Verdict | Confidence |
|---|---|---|---|---|
| S5-V1 | Thread check logs, no rejection (S4-BUS-01) | `evidence/bus-base.javap-c.txt` lines 987–1006 (`ifne 7`/`return`; `dumpStack` @ instr 44; three returns; no throw) | VERIFIED | Confirmed |
| S5-V2 | Deferred additions see current event (S4-BUS-03) | same file, lines 187–266 (`getfield Consumer` @111; `accept` @115; size re-check @138–153) | VERIFIED (branch-scoped) | Confirmed |
| S5-V3 | RPC 10-min write-expiry, no failure callback (S4-RPC-01/02) | `evidence-rpc/rpc-channel.verbose.javap.txt` (`expireAfterWrite`, `MINUTES`, `removalListener`); `rpc-channel.javap.txt` (`put` before `send`; removal listener EXPLICIT-return) | VERIFIED | Confirmed |
| S5-V4 | Disconnect silent abandonment (S4-RPC-04) | `rpc-channel.javap.txt` `ORIRHCHRRHRCCOCIHCOOCHHOHCCCIO @0–9` (`invalidateAll`); `transport-lifecycle.javap.txt` `onClose` calls it; `onError` no null guard | VERIFIED | Confirmed |
| S5-V5 | Four-state model (S4-SUPPORT-01..06) | `evidence-support/L._88f3cf._cfe983.short.javap.txt` (`updateEnabled`, `_98d4d1`); `L._c8175c._cfe983._21aca6.short.javap.txt` (enum order SERVER→…→CLIENT_OVERRIDE) | VERIFIED | Confirmed |
| S5-V6 | Six module traces accurate (S4-MOD-01..06) | `evidence-modules-a/…` (armor 100/imul/idiv; potion 20.0f/3600/600), `evidence-modules-b/…` (200l/400l; iconst_2/iconst_4/Math.min), `evidence-modules-c/…` (iconst_4; List.size→List.get) | PARTIALLY VERIFIED (sampled claims reproduced; reports self-labelled partial) | Confirmed (sampled) |
| S5-V7a | WebOSR Java owner/queue/lifetime (S4-NATIVE-03/04/05) | `evidence-native/…WebEngine.fresh-verbose.txt` (owner, unconditional `invokeIteration0`); `…FunctionBus.fresh-verbose.txt` (`sipush 4096`, static queue, `add`); `…NativeHandle.fresh-verbose.txt` (close not synchronized) | VERIFIED (Java) | Confirmed |
| S5-V7b | JNI/PE export mapping (S4-NATIVE-01/02) | `evidence/pe_rva.py` → `0x1FC10/0x29690/0x1C400/0x1C3B0/0x10A30` + entry bytes match report | VERIFIED (PE metadata) | Confirmed |
| S5-V7c | Native paint/thread/dirty-rect architecture (S4-Java §7) | — (no deep provider) | INSUFFICIENT EVIDENCE | Unknown |

## Provider/tooling evidence (Session 5)

| Observation | Value | Source |
|---|---|---|
| `rea.binary_session` reachable | yes (session closed after probe) | live tool call this session |
| Ghidra | unavailable / `not_configured` (`GHIDRA_INSTALL_DIR` unset) | live tool call |
| Hopper | unavailable / `unsupported_host` (win32) | live tool call |
| IDA | unavailable / `not_configured` | live tool call |
| REA server `java_home` (this run) | `C:\Program Files\Java\jre1.8.0_461`, `unsupported_version` | live tool call — **differs from** `provider-availability.json` (see contradictions C-6) |
| Standalone disassembler | Microsoft JDK 21.0.10 `javap.exe` (works) | `javap -version` |
| Python | 3.11.9 | `python --version` |
| Git HEAD of research repo | `9522660 .` (working tree clean) | `git log/status` |

## What Session 5 did NOT do

- No `open_binary` native analysis, no Ghidra, no decompilation.
- No new REA Evidence records.
- No re-extraction of `lunar.jar`; the scratchpad tree (same bytes) was used.
- No execution/loading/runtime attach; no settings/credential reads.
- No modification of any existing report/ledger.
