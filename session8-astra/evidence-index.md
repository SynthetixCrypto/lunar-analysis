# Session 8 — sanitized evidence index

Date: 2026-10-12. This public index contains identities, addresses and hashes, not decompiled target code. Complete raw MCP envelopes, bytecode and the exported bundle remain under ignored `session8-astra/.local/`; those files are intentionally not public hyperlinks. [Machine-readable metadata](evidence-records.json) maps every alias to its exact Evidence ID and envelope digest, and Java aliases to JAR member identity/class-byte hash/disassembly hash.

## Target and provider

- Native target: **WebOSR-Binding.dll**, SHA-256 `4368a692fec3fa44f34fc3a356d676966f0b7191dd91fb5fc5b89064b01faebf`, image base `0x180000000`, PE x64.
- REA **6.4.0**, Ghidra **12.1.4**, JDK **21.0.10**. Active built-in `binary_session` first showed a stale install path; the workspace-only MCP helper's `provider-status` showed Ghidra available. `binding-open` returned the expected target digest. No global configuration was changed.
- The Session 7 binding snapshot was used as a compatible analysis seed; fresh calls and assembly results are listed below. Reused results are not presented as independent runtime observations.
- `evidence-export` reported **209 records**, **63,078,134 bytes**, zero ledger unknown records. This bundle includes inherited records; 209 is not the number of new discoveries. Ledger unknown counts do not measure unresolved research questions.
- `binding-close` succeeded; `closed-status` has `open: false`; the helper exited normally. No target binary was executed.

## Native records

Each alias is the local envelope filename without `.json`. Addresses are provider virtual addresses. A record may be a search or table observation rather than a behavioral conclusion. Confidence and limitations remain in the full envelope; reports state their narrower interpretations.

| Alias | Address / selector | Exact Evidence ID |
|---|---|---|
| `actor-consume-assembly` | `0x180035ec0` | `ev_628e1564c595ff25a61103f129395b8d1009dea5a31ae983b30749e6b69d923f` |
| `actor-send-assembly` | `0x180036380` | `ev_9d8ecd2f436e58fd1a2d7fca46768ac190401ad4667396cfccfc307b598c9dce` |
| `attach-incoming` | `0x180001f60` | `ev_0007a7f922632cfac229567367f7c9f4ddfa22b2fac8c5a40456c7a475d40fd0` |
| `bitmap-premultiply` | `0x18004cdd0` | `ev_e2d80d455696d387ce582d2e90b02be3934c78f58862e5aba77ffd4cdbb1c579` |
| `bitmap-vtable-correct` | `0x1800621a0` | `ev_d53b0c2c6fa38fa381da2d0d5964b8718478dff38e2bd3b580b6fa2e9c3beb1d` |
| `deferred-bitmap-methods` | `0x1800620c0` | `ev_169bd700fd8893a04c312a8986e6d8e3601e145105b142f019ff136567feb7c3` |
| `delete-incoming` | `0x18002d630` | `ev_29d48e1f5d7e00b873a88296c627f93aa45b54edfcf393f2b478a2191d2564a0` |
| `delete-texture-references` | `0x18002d630` | `ev_3b95c39da7d67051ff68122c896facfcc733b12446f2202e11df37b10afb67a1` |
| `engine-constructor-assembly` | `0x180038ac0` | `ev_9f4ed16e8e06db4919ef840a24b6a32551d6ad99a4f0db57f709ea897ff983d9` |
| `env-attach-assembly` | `0x180001f60` | `ev_05c79d2c28ab99fc0507c8e9c3129848dc1f640932973c63ed62389b5c0072d5` |
| `env-construction-refs` | `0x1800014c0` | `ev_e75da204b65e284745ce47ea4e10843892cdae1b6e6e3d2b7d8f3b14fe513a86` |
| `environment-actual-ctor` | `0x1800014c0` | `ev_d5c097b009e5ae077f35b3d5f57dd823ca5fe161834791127f221b29bedb2482` |
| `environment-functions` | `search_strings` | `ev_b24603c8ed1f5c247f9470fea72ea2c952ec67b85d4006bcd7ce5b794e8fad96` |
| `global-delete-helper` | `0x180001a60` | `ev_416fa33cbff2bebfdc66b9ee41ec91456783a842f5a8e5d4bd3c68d6bff20fe3` |
| `handler-delete-table` | `0x180060c30` | `ev_6a27009e5f8647d2e1dcb3e7ddd9da9b78ad006bae1646b90b2b6c3123d42cab` |
| `handler-vtable-correct` | `0x1800602d0` | `ev_3c59eebe42e860131a219542a90055e84b36a4e7c765a90c8c4f4ed1da788ae3` |
| `image-destroy-jni` | `0x1800278f0` | `ev_97e5587ef362f5c800c832505a7f1c5c122e008e21bf6176ae5fff9398f8dbf6` |
| `image-dtor-adjusted` | `0x18004a0b0` | `ev_f2ca6f3a4e877eb5e86e3959684a91919c166a0fa27c267e668dd39924d48b7b` |
| `image-dtor-table` | `0x180061f28` | `ev_f030280d0cfd731c7ca10cdee6894975478c353ae8554f289cc1b105e5449417` |
| `image-dtor-thunk` | `0x18004a0a4` | `ev_55b613a7cfab1fada6f5b06f5bb7ddf7a0050e7f975e694c93e0d8a367b68355` |
| `image-exports` | `search_procedures` | `ev_99149efd480a60101ae83eeffb97310691d08e0972db39059c7915fab991b980` |
| `image-primary-delete` | `0x18004a084` | `ev_7ff9601826b51a570ce3902a521911be165103b51c961069b5412fbad5bbe265` |
| `image-unbind-jni` | `0x180027ca0` | `ev_7e763c5eabbe32ddfed1e0f3ab47f8c846e7f6678d06e3007db4aac6b61b9dd6` |
| `jni-attach-xrefs` | `0x180001f60` | `ev_6e52f4bfcdb3cbe9ff91ea3e13fdcb28b93a8ba86268a1e3fa3faddb3d427046` |
| `jni-create-asm` | `0x18002d580` | `ev_1baa136bb14a6f07092d5c97d783fbb2885d9435ffc783435a270c4f04034e81` |
| `jni-delete-asm` | `0x18002d630` | `ev_45386fc9be9b83e48e66198f9a6da1e760b2af49f51032b0eb9d794e27db5a32` |
| `jni-env-access` | `0x1800021d0` | `ev_d50a931b9ae688e2bfcb754b7e5b08a28fedc0df9abca6bb1c450c39ca87552d` |
| `js-argument-text` | `0x1800475f0` | `ev_298d86b7e4688053c9adf130e1c6abf994842c5826362cb77c6a11c2a5c66bca` |
| `premultiply-references` | `0x180062430` | `ev_44ef1e4560a0d107041239c16eea2cdbbd6484a5368ea36bcd523750fd50a769` |
| `promise-create-assembly` | `0x180047920` | `ev_245f6e7b3174ef26fb619076b1d43f035d649934dd66a1a3eebb752658ec2150` |
| `promise-create-body` | `0x180047920` | `ev_2a3b227b2a169210de494debe067248b09e570e01caa1400b930636bb245f41f` |
| `promise-create-containing` | `0x180047920` | `ev_aad073f1cbc4f5ecac776644431a9658d416ee5dd5a40b9135652de8714d7236` |
| `promise-create-refs` | `find_xrefs_to_name` | `ev_84d9ff6b9f2a32fb33136276bc2f22ceaa5ffecf6c74483331bb4a456f8499ad` |
| `promise-create-xrefs-correct` | `0x18005e748` | `ev_935ed6440e87923dc32a2ebaf7cf77667485726c1203ffbada3f20a9fe85bb62` |
| `promise-dtor` | `0x180043930` | `ev_8e824010c9f08ee09af84ad0086b917f1db940f7433c6f993943f3cf708ecfc7` |
| `promise-empty-worker` | `0x1800464b0` | `ev_378f0635dd0cf775ff1bf9f3acdf018fa71ead73ef788fc64c3bc23c04847469` |
| `promise-json-complete` | `0x1800436b0` | `ev_cc6d4c19c18857bf8f81b876ccb45c095968775f5c25ea9dfc3844ada5d74f62` |
| `promise-reject-native` | `0x180048460` | `ev_40a2ac42f4699972f37a6911d0992ba4c281483b962ec1306cf612b2f5274ba5` |
| `promise-resolve-jni` | `0x1800268d0` | `ev_f9465efab975ca3d774db4291dc213d44a12c8faafbd6a38acb435d633792ab0` |
| `promise-resolve-native` | `0x180048800` | `ev_736ae549392a3e00fd51a56119f309d02fdc40dc28c20432703d1db61c8c667b` |
| `promise-string-assembly` | `0x1800436b0` | `ev_dbb95ded32104355d303df3e9540af6ec3c1e8e6e0adb0b41190e635488682db` |
| `promise-table` | `0x180061790` | `ev_68b5dfd36ab3be099d7537af161a591fca2722a5251069823c2e268037042670` |
| `promise-task-tables` | `0x180061cb0` | `ev_615c676969bcf8cdf38bc9ad96cf2c2c5b73335a6b73bb5ca8cef0c7893177e2` |
| `promise-value-resolve` | `0x180048570` | `ev_90d95f051f36bf0d79d8138e60e092ecfc156fd35a30563a9d87d0f8f420e4a3` |
| `promise-value-worker` | `0x1800464a0` | `ev_b3b7acfa6c966cc388e139c56a5383c6570474a2784980e664b0a8af4a925ece` |
| `shutdown-assembly` | `0x18003a160` | `ev_24d3270b6eaa1e4af12c35ab3c28b5f709b86a85011a28d7790da863614be7f0` |
| `source-base-unbind` | `0x18004cc50` | `ev_7f437a0d9f5556b7aba9129e0899a2eeb9f5d42404c7b5a32f74edfa1ece69b0` |
| `source-base-vtable` | `0x180061e38` | `ev_b62427850f3f02967fcb250db8cecb16bfbba190502ec9af37994736c1844b00` |
| `source-bitmap` | `0x18004ccc0` | `ev_8754b7384171505bca803e4b54cd548648bc6f7cd6b8be07cd2f717c5fad3589` |
| `source-cleanup-string` | `search_strings` | `ev_d7b093b6f257aca7e1c835f7dc39debc4711da43389a2cb86a8272eadca6ef6a` |
| `source-close-table` | `0x180061e28` | `ev_584a326f29b82dc3e8309fbf0f3445930b5a8d37feeea6612ff05ac872cf16cd` |
| `source-dtor-asm` | `0x180049400` | `ev_85868f05338f89b9f2498442fd4331c1de0ef5241bed58c7d3f77851a7b8f55e` |
| `source-dtor-body` | `0x180049400` | `ev_3bf8e42a702154658ac0f3645bcd7a128ee9a48d8ce3bedff2f76f227c23d777` |
| `source-dtor-task-asm` | `0x1800499e0` | `ev_3afd5db5dde72e82281320b9e33405a9977e6430bb7c60d7146c26fd156ed31f` |
| `source-dtor-task` | `0x1800499e0` | `ev_0171602dd62b968574c336c6c6dc7042747e1a95b2f7b3f4ce70a12dae27d258` |
| `source-handle-cleanup` | `0x180027610` | `ev_f2210ac048cd0ea6e190abefa687198c2d522f8829bb8568fbe7e95d303bc2b9` |
| `source-refcount-destroy` | `0x18003a130` | `ev_d169c104ae67490e3c1d7e4ae95ef1cfd738d12d9adbc642e326b0cd56a86ba3` |
| `source-refcount-table` | `0x180061010` | `ev_02dff5476789f3247973fc77ee65cb99f6c65e3e817b5f8aaa787bb49b2cd8c2` |
| `source-reset` | `0x180049c90` | `ev_c1491201714ca1790d28088d5b626d27ea2ea75b3c17ede8d80f82a3c26bb7c2` |
| `source-unbind-adjust` | `0x18004a094` | `ev_97eed2f5a7529882b36dd45a1af7fe3f10e4a3f00185a1dfc0e671a311ec3970` |
| `source-update-asm` | `0x18004a530` | `ev_491b63f9e820f0fde852ed50f5fc53053de357b96b24556e33029d989f50b5f1` |
| `swapchain-publish-asm` | `0x18004c360` | `ev_d3ac5ce0a5f777f0ba93ec6df67b8f33983d8d6fd879f8157ba064104600765f` |
| `vm-actual-ctor` | `0x180001560` | `ev_d1296a16304e9899712872083dc0368b468a6240db5ffbaf118d5c4427453011` |
| `vm-ctor` | `0x180001440` | `ev_b3ce52abae85a8bac04042dce0d2fac69ed893e1467af77bcf5167dc8a2abecd` |
| `vm-environment-map-release` | `0x180001910` | `ev_30b7689f34361c7c398e043d36f2d706d3dfb6f96b94e7f362a90686032d550e` |
| `vm-refcount-release` | `0x180001c60` | `ev_a6cafcc7e9aa436127bae3349ff5b79cd2b7043ae9775941e6ff7d9373764b65` |
| `vm-release` | `0x180001870` | `ev_bddc66e5af97a699d719dfd2fdb2e645a962a1bbe4458854a73c2eedd7c4a401` |
| `vm-vtable` | `0x18005ec18` | `ev_dda532ceef96d959292140f092082ce51115c7f2093ab63d3122230a501d2b45` |
| `worker-entry` | `0x180039990` | `ev_826dc7f6b08bc05444a81aae9d4a067f526338e59de6c3bc807b631c74f7bd61` |

## Java and inherited evidence

Fresh `javap -p -c -s` reads named classes without initializing target code. `java-10` is the concrete TextureHandler, `cleanup-0/1` are downstream graphics release bridges, `java-21` is PromiseJS and `java-22` is Session. Full class identities and hashes are in the JSON index; exact original names are preserved there to avoid ambiguous analyst aliases. The bounded string scan selected candidates from `lunar.jar` and the modern bridge JAR; symbol occurrence alone is not a call-edge proof.

Session 7 authority: [evidence index](../session7-astra/evidence-index.md), [rendering](../session7-astra/webosr-rendering.md), [threading](../session7-astra/native-threading-lifecycle.md), [JNI reconciliation](../session7-astra/native-jni-mapping.md). The Session 8 reports distinguish re-inspected earlier evidence from new calls. Prior public raw records remain subject to the [repository audit](repository-audit.md).

## Corrections to exploratory record names

- `image-dtor-thunk`, `image-dtor-adjusted` and `image-primary-delete` were exploratory guesses: the first two lead to child creation; the last guessed address must not establish a destructor. Actual destruction is `source-refcount-destroy` → `source-dtor-body` at `0x180049400`.
- `vm-ctor` (`0x180001440`) is a generic callable-transfer helper; `vm-release` (`0x180001870`) is a vector-storage helper. Use `vm-actual-ctor` and `vm-refcount-release` for VM-specific conclusions.
- `handler-delete-table` and `deferred-bitmap-methods` used wrong table seeds. The authoritative corrected tables are `handler-vtable-correct` and `bitmap-vtable-correct`.
- `promise-json-complete` actually produces a string/null; it does not parse JSON. `promise-create-body` loses indirect-call outputs in pseudocode; the corresponding assembly corrects apparent zero-valued protection arguments.
- Initial `procedure_references` calls defaulted to outgoing. `attach-incoming` and `delete-incoming` explicitly request incoming references. `promise-create-refs` returned `name_not_found`; the qualified import-slot xref and containing-procedure results supplied the working seed.
- `delete-callsite-context` reports a data-table address outside a procedure, with unsupported optional comment/bookmark facets. It is not a deletion-callsite discovery.
- One attempted unversioned Fabric setup URL returned 404; the versioned setup URL in the architecture references succeeded. No external-link liveness guarantee is inferred from local-link validation.

## Integrity and reproduction boundaries

Local-only scripts `rea.mjs`, request batches and receipts record tool parameters and preserve complete responses. The helper requires the already installed REA/Ghidra/JDK environment; do not run target code to reproduce static findings. Raw evidence is not necessary to read the design reports, but independently reviewing low-level claims requires the matching artifacts and local archive.

`validate_documentation.py` checks local documentation targets/fragments and Evidence ID index membership. `audit_repository.py` inventories tracked files and reachable Git object sizes without untracking anything. The local finalizer also parses all new JSON, compares prior tracked-file hashes (allowing only README modification), verifies indexed envelope/class hashes, and compares four native DLLs plus `lunar.jar` with the retained Session 7 identities. The sanitized result is [validation](validation.json).

SHA-256 integrity is not a semantic proof; REA's canonical Evidence ID algorithm was not independently reimplemented. No native runtime cadence, selected backend, contention or failure frequency was measured.
