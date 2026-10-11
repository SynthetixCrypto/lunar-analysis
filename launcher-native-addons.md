# Launcher native addon inventory

## Provenance and method

Confirmed source: `C:\Users\Admin\AppData\Local\Programs\Lunar Client\resources\app.asar`, SHA-256 `506574f17a6b7aeb5a13fe5f53fc83329fa705141505dde30ec88e00aa03a9f4`. Logical member paths below are within this installed ASAR. Bytes were read from REA extraction root `C:/Users/Admin/AppData/Local/Temp/rea-extracted-23b87573-be87-479d-b524-da81ec5fc204` produced by extraction evidence `ev_31648b1ec89765d65a3cd9a6929cd7461fb4a5a4ab47e7da16d3ed9fbd42c71a`. Extraction used `record-and-continue` integrity policy; see the extraction evidence and main findings for the separately recorded ASAR integrity mismatch. This report identifies the bytes inspected and does not independently certify package integrity.

Supplemental static parsing inspected PE COFF/optional headers, section mappings, normal and delay import tables, and named export tables. None of these addons was loaded or executed. No Lunar files were modified. Ghidra and IDA were not configured, so native implementation disassembly is unavailable. Full hashes, imports with name offsets, export names/RVAs, and sections are retained in `launcher-native-addons.json`.

## Confirmed binary inventory

| Logical ASAR member | Bytes | Architecture | Registration exports |
|---|---|---|---|
| `node_modules/@lunarclient/bsdiff-node/build/Release/bsdiff.node` | 276480 | x86_64 / 0x8664 / PE32+ | `node_register_module_v146` |
| `node_modules/better-sqlite3/build/Release/better_sqlite3.node` | 1920512 | x86_64 / 0x8664 / PE32+ | `node_register_module_v146` |
| `node_modules/diskusage/build/Release/diskusage.node` | 179712 | x86_64 / 0x8664 / PE32+ | No named exports; export directory RVA/size are zero |
| `node_modules/native-is-elevated/build/Release/iselevated.node` | 110080 | x86_64 / 0x8664 / PE32+ | `napi_register_module_v1`, `node_api_module_get_api_version_v1` |

All four native addons independently have x86_64 PE machine fields (`0x8664`) and PE32+ optional headers. This determines the architecture of these installed addon bytes, not every architecture variant carried elsewhere in the launcher package.

## Declared host dependency and ABI evidence

Confirmed: each addon has one delay-import descriptor naming `node.exe`. Static delay-import declarations are:

| Addon | Delay-import symbols | Selected evidence |
|---|---|---|
| `bsdiff.node` | 36 | `node_module_register` |
| `better_sqlite3.node` | 74 | `node_module_register` |
| `diskusage.node` | 32 | `node_module_register` |
| `iselevated.node` | 3 | `napi_set_named_property`, `napi_get_boolean`, `napi_create_function` |

Confirmed: bsdiff and better-sqlite3 export `node_register_module_v146`; the symbol spelling directly declares registration entry points containing ABI number 146. Their delay imports include `node_module_register` and C++ Node/V8 symbols. Inference: these are host-ABI-specific Node addons built for ABI 146. Actual host compatibility was not tested, and no mapping from 146 to a specific Electron or Node version is asserted here.

Confirmed: iselevated exports `napi_register_module_v1` and `node_api_module_get_api_version_v1`; its three delay imports are `napi_set_named_property`, `napi_get_boolean`, and `napi_create_function`. Inference: this uses the Node-API registration surface. The `_v1` export suffix identifies the registration/export convention; it is not sufficient to claim the addon requests Node-API level 1, because the get-api-version function body was not read.

Confirmed: diskusage has no PE export directory and declares delay-imported `node_module_register` plus C++ V8 symbols. Inference: a legacy registration path is plausible, but no explicit ABI-number registration export was present and initialization was not traced. Missing exports alone do not establish a broken addon.

The declared delay-import DLL name `node.exe` does not prove a separate node.exe process is launched or a disk file of that name is loaded. Electron embedding and delay-load hooks can affect resolution; resolution/runtime loading remains unobserved.

## Boundaries and candidate responsibilities

Confirmed: the bsdiff, better-sqlite3 and diskusage normal import tables name `KERNEL32.dll`. iselevated additionally names `ADVAPI32.dll`. Useful static API declarations:

- diskusage: `GetDiskFreeSpaceExW` in KERNEL32; supports an inferred disk-capacity query responsibility.
- iselevated: `AllocateAndInitializeSid`, `CheckTokenMembership`, `FreeSid` in ADVAPI32; supports an inferred Windows membership/elevation-status check responsibility. It does not demonstrate requesting elevation.
- better-sqlite3: filesystem and locking APIs (`CreateFileW`, `LockFileEx`, `UnlockFileEx`, `FlushFileBuffers`) and mapped-file APIs (`CreateFileMappingW`, `MapViewOfFile`); consistent with its inferred SQLite storage responsibility. Import names do not establish a particular database file or actual data access.
- bsdiff: package/member identity suggests binary-delta support. Headers and import declarations alone do not establish its algorithm, patch application flow or callers; those require the launcher JavaScript evidence.

No database, credential, token, account store or anti-cheat state was opened. These native addons establish a launcher/Node-to-Windows boundary; they are distinct from Minecraft-side JNI DLLs covered in `native-runtime-inventory.md`.

## Coverage limits

Exactly these four supplied native addons were inspected. The optional `native-modules/launcher.node` bridge and all other native modules were excluded from this pass. No registration function, patching implementation, database implementation or privilege decision was executed or decompiled. Dynamic load paths, dependency search behavior and call timing remain unresolved.
