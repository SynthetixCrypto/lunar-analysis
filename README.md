# Lunar Client — static analysis notes

An independent, evidence-backed study of Lunar Client's shipped launcher, Java client, feature framework and WebOSR boundary. This repository contains research reports, inventories and supporting static-analysis records—not a client implementation, executable distribution or complete behavioral specification. It is not affiliated with or endorsed by Lunar Client.

## Start here

| Topic | Reading |
|---|---|
| Overall findings and coverage | [Findings](findings.md), [component map](component-map.md), [missing evidence](missing-evidence.md) |
| Latest investigation | [Session 4 index](session4-sol/README.md), [corrections and remaining questions](session4-sol/status-and-corrections.md) |
| Historical evidence and unresolved questions | [Evidence index](evidence-index.md), [unresolved implementation](unresolved-implementation.md) |
| Launcher and startup | [Launcher architecture](launcher-architecture.md), [launcher internals](launcher-internals.md), [startup flow](startup-flow.md) |
| Java client and features | [Java internals](java-internals.md), [feature registration](feature-registration-deep-dive.md), [module lifecycle](module-lifecycle.md) |
| Events, settings and rendering | [Event payloads](event-payloads.md), [settings persistence](settings-persistence.md), [HUD math](hud-math.md), [rendering](rendering-and-hud.md) |
| IPC | [IPC deep dive](ipc-deep-dive.md), [session-4 RpcChannel policy](session4-sol/rpc-channel.md) |
| Native boundary | [Native preparation](native-analysis-preparation.md), [session-4 wrapper/native findings](session4-sol/native-rendering.md) |

Historical reports are intentionally preserved. Read later session corrections before relying on an older inference. Session 4 corrects the event-bus thread-check interpretation and resolves RpcChannel cache-expiration policy, while leaving native paint/thread internals open.

## Layout

```text
*.md                  Research reports and historical ledgers
*.tsv / *.json        Artifact inventories, mappings and evidence records
session2-tools/       Earlier analysis helpers
session3-tools/       Earlier analysis and validation helpers
session4-sol/         Latest reports, local finding ledger and retained evidence
```

Obfuscated Java aliases are analyst shorthand, not original names. The linked per-session mappings preserve original JVM identities. JVM `@` ranges are decimal bytecode offsets within a named method; native RVAs/file offsets are hexadecimal. Native/abstract declarations have no Code offset.

## Evidence and confidence

- **Confirmed:** directly supported by shipped bytes, declarations or disassembly. Does not mean runtime-observed.
- **Strong inference:** a supported interpretation or conditional consequence, with assumptions stated.
- **Tentative:** incomplete attribution or weak corroboration.
- **Unknown:** not established by the collected evidence.

`S4-*` identifiers are local findings, not REA Evidence IDs. REA exports retain their own identifiers and limitations; `session4-sol/rea-evidence-session4.json` contains inherited session-3 PE-resource records rather than new deep native analyses. Bounded searches and structural inventories do not prove whole-program behavior.

## Verification

Reading the reports needs no Lunar installation. Validate session-4 links and retained-evidence hashes with Python 3:

```powershell
python .\session4-sol\validate-session4.py
```

This validator reads research files and Git metadata; it does not run Lunar code. Its output is written only inside `session4-sol`. It cannot prove the semantic accuracy of every conclusion or reproduce native internals. See the [session-4 guide](session4-sol/README.md#verification-and-reproduction) for optional static disassembly requirements and machine-specific path limitations.

## Research boundaries

- Installation artifacts remain read-only; no Lunar JAR, native library or JavaScript is executed or loaded as target code.
- No credentials, account files, tokens, installation identifiers or personal settings values are inspected.
- No anti-cheat/integrity investigation, protection bypass or reimplementation is part of this investigation.
- Runtime observation and installation/configuration of a native analysis engine require separate explicit approval.

Native deep analysis remains partial because Ghidra was not configured. Java-wrapper behavior and PE metadata must not be presented as a recovered Ultralight architecture.

## Before publishing to GitHub

**A local Git repository is not automatically a publication-safe dataset.** Review the exact staged files and the existing history before making any remote public:

1. Exclude installation binaries, extracted class/package trees, caches, proprietary images/fonts/models, personal profiles and logs.
2. Review disassembly/evidence records for distribution rights and sensitive fields. Local evidence retention does not grant redistribution rights.
3. Redact machine-specific absolute paths and usernames in a separate publication copy where appropriate, preserving the private original evidence.
4. Use an explicit file allowlist when staging; avoid blindly staging the entire analysis folder. Ignore rules do not remove files already tracked or present in history.
5. Select a license only for research material you have the right to license. No license for Lunar software/assets or copied third-party code is granted here.

No repository initialization, staging, commit, push, history rewrite or remote publication is performed by this documentation update.
