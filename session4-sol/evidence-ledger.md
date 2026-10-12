# Session 4 local finding ledger

This ledger indexes **28 local finding groups**, not 28 new REA analyses. Each report carries detailed artifact/class/method/offset citations and confidence limits. The machine-readable [finding-locations.tsv](finding-locations.tsv) gives a representative primary location for each group; it does not replace the report's additional branches/citations. Retained file hashes are in [evidence-files.sha256.tsv](evidence-files.sha256.tsv), with document/path/preservation checks in [session4-validation.json](session4-validation.json).

JVM artifact: `lunar.jar`, using retained static disassembly and selected fresh JDK javap views. Original artifact hashes belong to the preserved [artifact index](../artifact-index.tsv); aliases resolve through each evidence area's mapping. Native artifact: `WebOSR-Binding.dll`, SHA-256 `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf`. Hashes bind files, not evidence interpretation or runtime identity.

| Local ID | Finding group | Report | Coverage / limit |
|---|---|---|---|
| S4-BUS-01 | Base thread diagnostics and debug subclass role | [Event bus](event-bus-threading.md) | Confirmed selected code; runtime flag unknown |
| S4-BUS-02 | Public lock/reentrancy and backing-map exposure | [Event bus](event-bus-threading.md) | Public wrappers, not all external map access |
| S4-BUS-03 | Exact class, priorities and current-event pending additions | [Event bus](event-bus-threading.md) | Selected helpers; stable sort consequences inferential |
| S4-BUS-04 | Different failure policies and unbalanced-depth possibilities | [Event bus](event-bus-threading.md) | Code confirmed; risks conditional, not reproduced |
| S4-BUS-05 | Paired PRE cancellation and deferred-only branch | [Event bus](event-bus-threading.md) | Selected overload, not every event producer |
| S4-RPC-01 | UUID textual IDs, pending callbacks and send ordering | [RpcChannel](rpc-channel.md) | Controller unused in channel; callers not exhaustive |
| S4-RPC-02 | Ten-minute cache expiration logs, not failure completion | [RpcChannel](rpc-channel.md) | Standard Guava maintenance interpretation, not measured timer |
| S4-RPC-03 | Invalidate-before-decode and callback scheduling | [RpcChannel](rpc-channel.md) | Transport/channel/util branches, not observed queue timing |
| S4-RPC-04 | Close invalidates silently; onError logs only | [RpcChannel](rpc-channel.md) | Library may separately close; runtime ordering unknown |
| S4-RPC-05 | New transport on reconnect and bounded backoff | [RpcChannel](rpc-channel.md) | Null-input IPC branch; no connection initiated |
| S4-SUPPORT-01 | Effective gates precede override | [Transitions](feature-support-transitions.md) | Static registration differs from effective state |
| S4-SUPPORT-02 | Flipped/remembered toggle and server recursion | [Transitions](feature-support-transitions.md) | Selected event paths; full producer ordering unknown |
| S4-SUPPORT-03 | Server category clear and descendant recompute | [Transitions](feature-support-transitions.md) | Does not clear all client categories |
| S4-SUPPORT-04 | Toggle, subscription and child propagation | [Transitions](feature-support-transitions.md) | Not a universal atomic override transaction |
| S4-SUPPORT-05 | Boolean EnumMap category priority/restoration | [Transitions](feature-support-transitions.md) | Boolean interceptor only, not all setting types |
| S4-SUPPORT-06 | Remote/criteria parser and dynamic allowance | [Transitions](feature-support-transitions.md) | Source key names/types, not payload/personal values |
| S4-MOD-01 | Armor children, equipment/preview source and durability | [Armor/potions](modules-armor-potions.md) | Full bars/protection/layout remains partial |
| S4-MOD-02 | Potion version filters, tick/mode and duration math | [Armor/potions](modules-armor-potions.md) | Blink/layout/inventory hooks remain partial |
| S4-MOD-03 | Toggle root/child, tap thresholds and key state | [Toggle/reach](modules-toggle-reach.md) | Flight formulas/special version producers partial |
| S4-MOD-04 | Reach correlation/clamp/reset/text/highlight | [Toggle/reach](modules-toggle-reach.md) | Distance geometry/counter field not mapped here |
| S4-MOD-05 | Combo timestamp deduplication/count/reset | [Combo/pack](modules-combo-pack.md) | Bridge semantics/producer timing not fully mapped |
| S4-MOD-06 | Pack update/order/texture/description/formatting | [Combo/pack](modules-combo-pack.md) | Child/dimensions/texture release incomplete |
| S4-NATIVE-01 | JNI destinations/mismatch bounded export search | [Native](native-rendering.md) | No observed lookup failure/alternate registration proof |
| S4-NATIVE-02 | Exact 27-byte iteration forwarding stub | [Native](native-rendering.md) | Manual decode; helper/pointee/slot semantics unknown |
| S4-NATIVE-03 | Owner-thread Java queue drain, unconditional native call | [Native](native-rendering.md) | Does not recover native threading |
| S4-NATIVE-04 | FunctionBus dispatch/conversion/promise boundaries | [Native](native-rendering.md) | Native marshalling and failure translation unknown |
| S4-NATIVE-05 | Handle/promise/future check-call-zero contracts | [Native](native-rendering.md) | Native arbitration and waiting implementation unknown |
| S4-NATIVE-06 | Texture logical-ID/ABI and browser creation boundary | [Native](native-rendering.md) | Java boundary/string evidence, not native paint call graph |

## Evidence provenance and negative searches

- Bus mapping: [class-mapping.json](evidence-bus/class-mapping.json); RPC mapping: [class-map.tsv](evidence-rpc/class-map.tsv); support mapping: [mapping.json](evidence-support/mapping.json).
- Modules A mapping: [class-map.tsv](evidence-modules-a/class-map.tsv); B mapping: [full-name-mappings.json](evidence-modules-b/full-name-mappings.json); C mapping: [class-manifest.jsonl](evidence-modules-c/class-manifest.jsonl).
- Native mapping: [class-map.json](evidence-native/class-map.json); PE offsets/raw bytes: [binding-pe-addresses.json](evidence-native/binding-pe-addresses.json); availability: [rea-provider-status.json](evidence-native/rea-provider-status.json).
- [Bounded future search](evidence-rpc/bounded-future-search.json): 16 non-auth IPC-call-containing bodies; excludes transitive caller bodies/generated code. No Future/timeout symbols there is **not** a whole-program absence claim.
- [Module event-producer search](evidence-modules-b/event-producers.json) is empty. This cannot establish producer absence or complete hook coverage.
- Native named-export search lacks Session.name/JNI_OnLoad/JNI_OnUnload; no claim that non-exported or other-library native registration is absent.
- [REA bundle](rea-evidence-session4.json) contains inherited records only. Python/manual/javap findings receive local S4 labels, not invented REA Evidence IDs.

## Reuse and limitations

Collectors' retained caches/fresh dumps were reused after usage-limit stops; none is described as a finished worker report. The validators do not parse every Java method into a proof and do not test Lunar execution. Library consequences and concurrency risks stay Strong inference. Existing personal-data exclusions apply even if a report mentions schema filenames, source-declared keys or command-line field names.
