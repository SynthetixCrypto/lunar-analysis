# Session 7 — Research onboarding

Date: 2026-10-12. Scope: static investigation of the installed WebOSR native binding and its Java contracts, supporting an original independent client architecture.

## Read first

1. [Session summary](session-summary.md): results and corrected assumptions.
2. [Rendering](webosr-rendering.md): worker → CPU surface → Java upload, and the reverse image-source path.
3. [Threading and lifecycle](native-threading-lifecycle.md): actor queues, initialization, shutdown and ownership gaps.
4. [JNI mapping](native-jni-mapping.md) and [cross-language contracts](cross-language-contracts.md).
5. [Ghidra verification](ghidra-verification.md), [evidence index](evidence-index.md), [remaining gaps](remaining-gaps.md).

## Starting point and independent checks

The investigation began with the latest Session 4 corrections, Session 5 native plan, and Session 6 summary, contracts and gap ledger. Earlier Java investigations were reused as leads. Native seeds were independently resolved in Ghidra; the export reconciliation was independently rebuilt from PE bytes and Java class files. The selected Java implementations and lifecycle classes were freshly disassembled with JDK `javap`, with matching class hashes.

Historical references:

- [Session 6 native acceptance checklist](../session6-sol/native-rendering-analysis.md).
- [Session 6 Java/native contracts](../session6-sol/jni-and-webosr.md).
- [Original G-01–G-33 definitions and Session 6 status](../session6-sol/remaining-unknowns.md).
- [Session 4 PE addresses](../session4-sol/evidence-native/binding-pe-addresses.json).

The principal advance is removal of the native-provider blocker. A usable Ghidra installation was present at `C:\tools\ghidra_12.1.4_PUBLIC`; the connected server pointed to a nonexistent nested/versioned directory. A second, workspace-scoped REA process used the correct environment. This supersedes the earlier environment diagnosis for this session; it does not establish when the installation appeared.

## Targets and coordinates

Installed artifact root: `C:\Users\Admin\.lunarclient\offline\multiver`.

| Artifact | This session's treatment | SHA-256 |
|---|---|---|
| `natives/WebOSR-Binding.dll` | Ghidra function, vtable and instruction analysis; PE exports | `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf` |
| `natives/Ultralight.dll` | Ghidra renderer creation/vtables/update/render bodies | `718f0f1cfdb2832afcd6c32b59516b08ddc131586f6230ce85962cdf6e9ebd47` |
| `natives/UltralightCore.dll` | PE identity/exports and bounded ASCII search only | `84b64678a61c1acbffc1820cd72176b453e4b66ada783450c02caba318e553c0` |
| `natives/WebCore.dll` | PE identity/exports and bounded ASCII search only | `c6630afde603edd5323c59d4e690de142c72d5fb60e3f34e174244a5ee5e07cb` |
| `lunar.jar` | WebOSR class declarations; selected `javap` bodies | `bf36e10e21154263ac16363f8c83bb08cff3a077cb788120954d3625b94a02e9` |

[Fresh PE inventory](evidence/pe-identities.json), [fresh JNI reconciliation](evidence/jni-reconciliation-fresh.json), [texture class hashes](evidence/java-hash-verification.json), [lifecycle class hashes](evidence/lifecycle-fresh-hashes.json).

Native addresses in these reports are **virtual addresses**, with the binary named whenever a dependency address is used. Both analyzed DLLs have image base `0x180000000`; the same numeric address in different DLLs is not the same function. Object offsets are relative to the identified object/subobject. In particular the swapchain's supplier interface is at surface `+0x18`; its method bodies use that adjusted pointer.

## Evidence discipline

- **Verified / high confidence:** observed static instruction, decompilation, class bytecode, PE table or vtable fact, corroborated where indirect calls/prototypes require it. This does not mean observed runtime execution.
- **Inferred / medium confidence:** architectural meaning derived from those facts; proposed source-level names are not recovered debug symbols.
- **Unknown:** unresolved indirect edge, caller coverage, failure path, real thread identity, runtime behavior or outside-scope behavior.

Full MCP responses in `evidence/` are authoritative; `views/` contains readable projections. A filename is an analyst label, not proof of a function's identity. Corrected exploratory labels are listed in [Ghidra verification](ghidra-verification.md). Each Evidence record retains its provider, target digest, analysis profile and limitations. [The index](evidence-index.md) supplies full Evidence IDs and locations.

## Workspace and reproducibility

- `rea-local.mjs`: existing REA 6.4.0 launcher and MCP SDK, corrected environment limited to the child process.
- `initial-requests.json`, `seeds.json`, `trace*.json`, `ultralight*.json`, `final-native.json`: exact requests.
- `queue/`: completed request/response receipts.
- `verify_artifacts.py`: independent PE and class-file parsing; selected `javap` extraction.
- `verify_contracts.py`: JNI header offsets, bounded registration search, fresh lifecycle bytecode.
- `project_evidence.py`: derived pseudocode/table views.
- `finalize_research.py`: evidence index, link/JSON checks, content manifest and final target digest comparison.

The opened targets have been closed with snapshots and the workspace helper has exited normally. The snapshots are REA analysis snapshots, not a claim that a persistent Ghidra GUI project exists. Resume with the exact matching target and an advertised snapshot parameter; inspect `tools-catalog.json` before composing new calls.

All new work is under `session7-astra`. Previous research and installed target artifacts were preserved. No Lunar code was executed, no private services were contacted, and no personal profiles or credentials were inspected. The output is research and architecture guidance; it does not implement the proprietary client.
