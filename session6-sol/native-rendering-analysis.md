# Session 6 — Native rendering analysis and provider boundary

Date: 2026-10-11. Static-only investigation. No Lunar executable, DLL, JAR or application JavaScript was executed. Lunar installation and Minecraft-side artifacts remained read-only. Analysis programs were JDK javap, local Python readers, PowerShell/Node filesystem helpers and REA's availability probe. No Ghidra was installed or downloaded; no system Java settings were changed.

## Environment verification

The fresh REA `binary_session` result is saved as [provider-status-live.json](provider-status-live.json). Ghidra candidate resolves **Microsoft full x64 JDK 21.0.10**, at `C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\java.exe`; its Java check is accepted. The shell probe independently reports the same JAVA_HOME and executable version in [environment-probe.json](environment-probe.json). Therefore Session 5's Java 8 observation is superseded as a statement of the current environment; its historical cause remains unknown. **No repair was necessary or applied.** JDK javap was always invoked by absolute path for this session's evidence.

Ghidra still reports `unavailable / not_configured`: GHIDRA_INSTALL_DIR unset, application properties/headless launcher/native decompiler unavailable. A bounded local search of Program Files, Program Files (x86), tools, Downloads, Desktop, Local Programs and scoop/apps to depth five found no installation. `C:\Users\Admin\AppData\Local\ghidra` exists but contains only `fscache2` and `packed-db-cache`, not an executable installation. This is **not** a claim that every directory on every drive was searched. No usable configured installation was found. Hopper is unsupported on Windows; IDA is unconfigured. No replacement disassembly packages were installed.

The default shell helper failed during setup; the authorized static tools ran through successfully reviewed scoped `require_escalated` calls. This was an executor issue, separate from REA's provider prerequisite. No automatic approval rejection remains outstanding.

## N-0 through N-8 disposition

| Stage from Session 5 | Session 6 result |
|---|---|
| N-0 host decision | Windows x64 + the existing JDK 21 remains the proposed host; no host migration performed. |
| N-1 install/extract Ghidra | **Blocked on absent usable installation and the user's explicit installation-approval requirement.** No install attempted. |
| N-2 server environment | JDK already correct; no configuration edit/restart required. GHIDRA_INSTALL_DIR cannot be set meaningfully before an installation exists. |
| N-3 re-probe | Done, live diagnostics saved. Deep native provider remains unavailable. |
| N-4 open target | Not repeated: prior sessions already validated the exact PE, and no deep provider is available. Fresh SHA-256 matches the retained table. |
| N-5 engine/helper/vtable analysis | Blocked; exact seeds below preserved, no forwarding stub relabelled as Render/Update. |
| N-6 texture JNI callback analysis | Native body blocked. Java region/stride/conversion and reverse image-source transfer materially advanced in jni-and-webosr.md. |
| N-7 Session_getName/registration | Native body blocked. Complete bounded four-JAR symbolic-reference scan found no Session method references; see evidence-native/session-methodrefs.json. |
| N-8 evidence/close | Local evidence saved and hashed. REA stayed closed; no native database was opened, so there is no native analysis snapshot or new native REA Evidence ID to claim. |

## Exact binary identity and retained seeds

`C:\Users\Admin\.lunarclient\offline\multiver\natives\WebOSR-Binding.dll` freshly read SHA-256: `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf`, identical to the retained Session 4 PE export/address evidence. [jni-reconciliation.json](evidence-native/jni-reconciliation.json) records that comparison. Thus the exact prior address table can be reused without redoing the completed entry-byte investigation.

| Export suffix, full prefix `Java_com_moonsworth_webosr_wrappers_` | RVA | Original file offset | Next question |
|---|---:|---:|---|
| WebOSR_createEngine | 0x10a30 | 0xfe30 | Construction, field assignment, JNI callbacks and failure unwind |
| WebEngine_invokeIteration0 | 0x1c3b0 | 0x1b7b0 | Resolve helper RVA 0x199c0, pointee +0xe8 and vtable slot +8 |
| WebEngine_setTimers | 0x1c400 | 0x1b800 | Timer wiring and callers despite absent Java declaration |
| Browser_swapBuffers | 0x1fc10 | 0x1f010 | Surface/present action and callers despite absent Java declaration |
| Session_getName | 0x29690 | 0x28a90 | JNI object lookup/conversion, relation to Java name() |

Exact native-byte authority: [Session 4 binding-pe-addresses.json](../session4-sol/evidence-native/binding-pe-addresses.json); table entries include raw bytes and `.pdata` records. RVA and file offset are different coordinate systems. A future Ghidra query must use provider-returned virtual addresses or exported symbols, **not pass these RVAs as if they were loaded virtual addresses**.

## All 16 native questions, explicit disposition

| # | Question | What this session establishes | Remaining native requirement |
|---|---|---|---|
| 1 | Helper 0x199c0 return and +0xe8 object | Prior forwarding bytes retained | Unknown: disassemble helper and identify object layout |
| 2 | Vtable +8 callee/action | Slot location known, semantics unassigned | Unknown: recover vtable and callee body |
| 3 | Frame produced by callbacks or Java pull | Java installs TextureHandler and exposes texture lookup; Java contract does not choose native behavior | Unknown: native callback/pull call graph |
| 4 | Distinct paint callback | Browser.Listener has no paint declaration (prior scope) | Unknown: internal native paint path/callbacks |
| 5 | Bitmap/surface allocator/owner | Java allocates GPU destinations and a reusable upload staging buffer; neither proves native surface owner | Unknown: Bitmap/Surface constructor and destruction references |
| 6 | Surface versus engine/texture lifetime | Java shutdown order recovered below | Unknown: native references, retained pointer lifetime and destruction order |
| 7 | Format and stride | **Java side resolved:** incoming bytes are interpreted BGRA, stride is bytes, x/y are pixel offsets | Unknown: native callback arguments and actual native buffer layout |
| 8 | Iteration thread/workers | Java rendering opportunity gate and owner queue behavior known | Unknown: native workers, callback threads, actual runtime identities |
| 9 | Native synchronization | Java upload staging buffer is static and unsynchronized | Unknown: native mutexes/atomics, external serialization |
| 10 | Native thread affinity | Java does not reject foreign-thread native iteration (prior finding) | Unknown: native checks/affinity requirements |
| 11 | JNI TextureHandler path | Exact Java consumer and shipped callback strings retained | Unknown: GetMethodID descriptors and Call*Method sites |
| 12 | Native create/resize/upload/delete calls | Java implements all four | Unknown: native call sites and order; string presence is insufficient |
| 13 | Dirty-region uploads | Java supports region x/y/w/h and byte stride | Unknown: native selection/cadence/region generation |
| 14 | Engine destruction | Java image sources → Browser.close → WebEngine.close, with unprotected exception boundaries | Unknown: native surface cleanup, callback unregistration, worker joins |
| 15 | Session.name registration | No ordinary symbol match; no symbolic callers in four scanned JARs | Unknown: RegisterNatives/JNI-table calls/other libraries |
| 16 | swapBuffers/setTimers dead/legacy/registered | Exact DLL-only symbols established | Unknown: native and external callers; absence of Java declaration does not prove dead code |

None of these native unknowns is inferred from Java declarations alone. Questions 5–7, 13–14 now have stronger **Java-side** bounds, not native implementation closure.

## Java-side lifecycle additions

Fresh originals/aliases/hashes in [lifecycle-manifest.json](evidence-native/lifecycle-manifest.json). Artifact lunar.jar except modern texture bridge identified separately.

- **Confirmed:** `L._81676d._21aca6._21aca6._d82ff1 @130–186` calls the library loader, allocates configuration, sets `ThreadConfig.idleTimer=0.001 @156–160`, then native `WebOSR.createEngine @183`; engine global is assigned only after successful return @186. No exception table provides Java rollback in this method. Timer units and native use are unknown.
- **Confirmed:** `L._81676d._21aca6._590f69._02d7ad @7–38` checks a non-null engine and wall-clock elapsed >=5 ms before calling invokeIteration; updates the timestamp only after return. This is a render-call opportunity throttle, not a scheduled 200 Hz guarantee. An exception propagates and skips that timestamp update and remaining method work. Native paint cadence remains unknown.
- **Confirmed:** `L._81676d._21aca6._21aca6._ba2ddc @0–76` sets `_7bd6aa=true`, snapshots the registered image-source set, calls each delete, closes the primary Browser @53, clears its field @63, closes engine @69 and clears global @73. There is no catch/finally or null guard for the main Browser/engine here. **Strong inference:** an escaping delete/browser-close failure prevents later cleanup on this pass; an engine-close failure prevents global nulling. No live failure was observed.
- **Confirmed:** `L._81676d._21aca6._13ea87._cfe983.delete @0–140` deletes owned framebuffer objects, clears/removes Java registrations, then calls TexturedImageSource.unbind @78 and close @85 before nulling @90. This is a separate Java-to-browser image path, not proof of Ultralight surface ownership. JNI reference counts, native copy/borrow behavior and shutdown joins remain unknown.

## Exact next steps after installation approval

1. Obtain approval to extract a Ghidra 12.1.x distribution into a concrete user-selected path, for example `<research>\tools\ghidra_12.1_PUBLIC`. Verify that path contains `Ghidra\application.properties`, `support\analyzeHeadless.bat`, and the matching Windows x64 native decompiler. No download command has been executed.
2. Prepare the existing REA server entry's environment delta, preserving other fields: `JAVA_HOME=C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot` and `GHIDRA_INSTALL_DIR=<verified extracted root>`. Back up only the configuration being edited; avoid system environment/registry edits. Reconnect REA, then require `binary_session` to report accepted Java and an available deep provider.
3. `open_binary({path:"C:\\Users\\Admin\\.lunarclient\\offline\\multiver\\natives\\WebOSR-Binding.dll",provider_id:"ghidra"})`. Check returned SHA-256 against the value above. This imports bytes for static analysis; never run the target.
4. `analyze_function({procedure:"Java_com_moonsworth_webosr_wrappers_WebOSR_createEngine"})`; then the other four symbols. Resolve helper 0x199c0 and vtable slots using the provider's observed image base/address mappings. Keep unresolved indirect calls explicit.
5. Follow TextureHandler strings/descriptors to JNI calls, callback lifetime and source/destination buffers. Inspect both directions: browser BGRA→GPU and Java framebuffer→TexturedImageSource. Trace error unwinding and destroy paths, then Session_getName/registration.
6. Export a complete REA Evidence bundle into session7, answer the 16-question table with addresses or Unknown, and `close_binary` with a new snapshot if eligible. Static analysis still cannot measure paint cadence, live contention or real race frequency.
