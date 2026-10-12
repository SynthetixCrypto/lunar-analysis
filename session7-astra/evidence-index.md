# Session 7 — Evidence index

Date: 2026-10-12. This index maps exact retained Evidence IDs to raw MCP envelopes or exported bundle records. Addresses are provider virtual addresses, not file offsets. Read each envelope's limitations and target digest before reusing it.

## Foundational local evidence

- [PE identities, exports and sections](evidence/pe-identities.json): independently parsed installed DLL bytes.
- [JNI reconciliation](evidence/jni-reconciliation-fresh.json): class-file native declarations and full mapping.
- [JNI ABI offsets](evidence/jni-abi-offsets.json): indexed installed JDK header and its digest.
- [Registration search bounds](evidence/registration-bounded-scan.json): four DLL ASCII searches and binding .text byte candidates.
- [Texture class hash checks](evidence/java-hash-verification.json) and [lifecycle class checks](evidence/lifecycle-fresh-hashes.json): original identities reused only as leads, fresh byte reads agree.
- Fresh `*.javap.txt` files under `evidence/`: static Java bytecode, descriptors and original class names. No target class initialization was performed.
- [Content manifest](file-manifest.json) and [validation result](validation.json): SHA-256 and integrity checks for retained files. These are local validation records, not REA Evidence IDs.

## Exported bundles and snapshots

| Bundle | Records reported in file | Unknown records |
|---|---:|---:|
| [binding-evidence-bundle.json](binding-evidence-bundle.json) | 121 | 0 |
| [binding-final-evidence-bundle.json](binding-final-evidence-bundle.json) | 141 | 0 |
| [ultralight-evidence-bundle.json](ultralight-evidence-bundle.json) | 14 | 0 |

Bundle unknown-record counts are REA ledger metadata, not counts of research questions left open. See [remaining gaps](remaining-gaps.md) for substantive unknowns.

[Binding initial snapshot](binding-analysis-snapshot.json), [binding final snapshot](binding-final-analysis-snapshot.json), [Ultralight snapshot](ultralight-analysis-snapshot.json). Full request inputs and completion receipts are in the root batch files and `queue/`.

## Raw response Evidence records

154 envelopes below contain inline Evidence. Duplicate Evidence IDs may legitimately occur when the same observation was requested more than once. The complete unique set including bundle-only records has 155 IDs.

| Raw response | Binary | Operation / location | Evidence ID |
|---|---|---|---|
| [actor-consume](evidence/actor-consume.json) | WebOSR-Binding.dll | analyze_function `0x180035ec0` | `ev_1193db83fe857dec496ab583dec8a792c1858cc1c52c29d45ee3b980f9e2e476` |
| [actor-dispatch](evidence/actor-dispatch.json) | WebOSR-Binding.dll | analyze_function `0x180036380` | `ev_7716d57acdb11661f11c0a53fbf41524f60d571747885265c5c6d1c62ab202a2` |
| [actor-lookup](evidence/actor-lookup.json) | WebOSR-Binding.dll | analyze_function `0x180035aa0` | `ev_5cacdce6dde5acc5ea353f1a843db4115e70da427ba565308b92a48c3fe01897` |
| [actor-pump](evidence/actor-pump.json) | WebOSR-Binding.dll | analyze_function `0x180036320` | `ev_a16d2c0813afd3d3557d0f657124b8495589962095b5feb6d47e26c6bb99dc36` |
| [actor-register](evidence/actor-register.json) | WebOSR-Binding.dll | analyze_function `0x180035b40` | `ev_2fb667817483067c9fb90d62db1dc604fc769417dd76f4ae3d27aaed2fac3427` |
| [binding-config-texture](evidence/binding-config-texture.json) | WebOSR-Binding.dll | analyze_function `0x18000f790` | `ev_74841d2d0c6f223ded5e2ed82fb2135330619fd75b65dc55522b984b3cf81bd3` |
| [binding-dll-entry](evidence/binding-dll-entry.json) | WebOSR-Binding.dll | analyze_function `0x180059758` | `ev_3fb9b00eeee02b143b4ab1fc9429cc857fc7194bc9d005ed11eac36d0f6f3576` |
| [binding-entry](evidence/binding-entry.json) | WebOSR-Binding.dll | search_procedures `` | `ev_71f83979d5dd3f3eb3e8551a610be9e4659737c181509024f33c8d42783a2432` |
| [binding-names](evidence/binding-names.json) | WebOSR-Binding.dll | list_names `` | `ev_b2e828fb0509e6c47254191e9df52de6ff1ff7002457edab5b345b7bd503f964` |
| [binding-overview](evidence/binding-overview.json) | WebOSR-Binding.dll | binary_overview `` | `ev_1aad67a9cd1cb0eeb83b0aab9a7e2e6cc12974ac9dce191dc9e32f03bcaef7d6` |
| [binding-procedures](evidence/binding-procedures.json) | WebOSR-Binding.dll | list_procedures `` | `ev_ce1d1c6c66ef0ab1ba1ac6384a8bba436aea53e2491c422239280ce5a68ebdd3` |
| [binding-registration-strings](evidence/binding-registration-strings.json) | WebOSR-Binding.dll | search_strings `` | `ev_8ff9d2ba63d2bbded5721d465adc9ea53617d561c372697fd23fe4ea24179e22` |
| [binding-registry-ctor](evidence/binding-registry-ctor.json) | WebOSR-Binding.dll | analyze_function `0x18000dd30` | `ev_9f794b99f41ef2efacc0d7b3a4db658926daa9321a80e8287e9055fe3d2864f3` |
| [binding-rendering-graph](evidence/binding-rendering-graph.json) | WebOSR-Binding.dll | get_call_graph `0x18001f7b0` | `ev_fd73ea713f8bdecc46c86fa85ed207f050d991deab9dbba4814c73e78dabb474` |
| [browser-create-jni](evidence/browser-create-jni.json) | WebOSR-Binding.dll | analyze_function `0x18001bda0` | `ev_0b4b4f80bc73eca0aca91a8ce973ad34b88c37c6f0b25111225c1afb75da5541` |
| [browser-create-worker](evidence/browser-create-worker.json) | WebOSR-Binding.dll | analyze_function `0x180042c00` | `ev_2dd904963c8963a6a64854df16b8dcf02c4dc3572b81cda34aa9f75f3f488b7e` |
| [browser-ctor-correct](evidence/browser-ctor-correct.json) | WebOSR-Binding.dll | analyze_function `0x180041fe0` | `ev_ca503495163972f55f62e736563cc34b4b60ab9a66e5a35a37d9a32c6db49010` |
| [browser-ctor](evidence/browser-ctor.json) | WebOSR-Binding.dll | analyze_function `0x180047920` | `ev_1cb877019a143b5162c700a19b47ac669486b29d8e49d6ba29c8bb5ffc215ea3` |
| [browser-destroy-task](evidence/browser-destroy-task.json) | WebOSR-Binding.dll | analyze_function `0x180046090` | `ev_9af875b1eb0df0e1873b7e7c4813e79cc5c679735cb1016c4a17aedd34a7f406` |
| [browser-dtor-assembly](evidence/browser-dtor-assembly.json) | WebOSR-Binding.dll | procedure_assembly `0x180042860` | `ev_b2fcd6081f38f9604e424854c3158875892bc3a05b9aac156849b083faf0d615` |
| [browser-dtor-body](evidence/browser-dtor-body.json) | WebOSR-Binding.dll | analyze_function `0x180042860` | `ev_8fe77bec1043f2ef13bb324b82295641efa347586db0d673a21e593710306c9a` |
| [browser-dtor-lambda-table](evidence/browser-dtor-lambda-table.json) | WebOSR-Binding.dll | read_bytes `0x180061888` | `ev_91df40ae4db7d0fd84ebe9737ab1b23285252bbfdbf7379e101f9e4520c5542e` |
| [browser-dtor](evidence/browser-dtor.json) | WebOSR-Binding.dll | analyze_function `0x180039ae0` | `ev_267065e2f72ef8b88dfdd254dfb4bc8e96165a39c73a7eae74ad09802ec17441` |
| [browser-factory-native](evidence/browser-factory-native.json) | WebOSR-Binding.dll | analyze_function `0x18003a900` | `ev_ee4b1906fd7bf09d94d3b397f59ea9ddc568e7f1518927bc5d2de0f221cd2775` |
| [browser-init-lambda-table](evidence/browser-init-lambda-table.json) | WebOSR-Binding.dll | read_bytes `0x180061850` | `ev_0b71b50d3fb03efd08e99ef54da73729f11df58d3611937e423e2302c3ce46bb` |
| [browser-init-task](evidence/browser-init-task.json) | WebOSR-Binding.dll | analyze_function `0x180046080` | `ev_4147c0b6343b57270eaad9ac93544add1bf35d4de2f6d27175195bd039afa3e1` |
| [browser-supplier-bytes](evidence/browser-supplier-bytes.json) | WebOSR-Binding.dll | read_bytes `0x180047760` | `ev_11d60cd987bcb272e7186e4fc19966f5adf460fb95412b9c3aa41be827a341f5` |
| [browser-texture-supplier](evidence/browser-texture-supplier.json) | WebOSR-Binding.dll | analyze_function `0x180047760` | `ev_57a0061f1684520f1e8edaa8cd84a0e8ce064ff7698af3042c9de876c113b34f` |
| [browser-vtable](evidence/browser-vtable.json) | WebOSR-Binding.dll | read_bytes `0x180061490` | `ev_41f13338de6bb00bad314d009ebca92e6c6de8e5b20d9c67afc6e0c421079a0f` |
| [browser-wrapper-ctor](evidence/browser-wrapper-ctor.json) | WebOSR-Binding.dll | analyze_function `0x18001ddc0` | `ev_74250d3d96e1cd99be1aff3d33f31b35a791336bf6ff965421f37fe3041e024f` |
| [create-engine](evidence/create-engine.json) | WebOSR-Binding.dll | analyze_function `0x180010a30` | `ev_1fe511c015349899ecc05f3c6650c6e6c3f790f9e2f2919cf89bc22402bd04e8` |
| [destroy-browser](evidence/destroy-browser.json) | WebOSR-Binding.dll | analyze_function `0x18001f460` | `ev_8e077f88cadc235a6be53bb769cfe444e374e88f529eaa0abd16be2e2c6d1afe` |
| [destroy-engine](evidence/destroy-engine.json) | WebOSR-Binding.dll | analyze_function `0x18001c290` | `ev_8dcfa18c1f4b45dcf22568443fe9afa4c715959f7b1bd7f38271beb863866631` |
| [dirty-regions](evidence/dirty-regions.json) | WebOSR-Binding.dll | analyze_function `0x18004b740` | `ev_dbff08c73303e8781a0028212c70026cfde9f0c12e71138d2795842a86e7d35f` |
| [engine-dtor-body](evidence/engine-dtor-body.json) | WebOSR-Binding.dll | analyze_function `0x1800396e0` | `ev_ee6eef617010f429934f1e5a655827a523a578df29338b83d76ac4a1177c9bc9` |
| [engine-dtor](evidence/engine-dtor.json) | WebOSR-Binding.dll | analyze_function `0x180037900` | `ev_8564ab25a953e140f5c8b4dbf970a7a16cfce34eabe087fca6d599788a20b0b3` |
| [engine-factory](evidence/engine-factory.json) | WebOSR-Binding.dll | analyze_function `0x180037950` | `ev_798af3247c946abfdd929f6bf4b1682520f4a77b6611d4653667427bff28d3a1` |
| [engine-fps](evidence/engine-fps.json) | WebOSR-Binding.dll | analyze_function `0x18003aa60` | `ev_cfb22dab6ac84cabfe281f5bfc4e3bae964e6469f54abcc517080d05bfcd7f28` |
| [engine-handle](evidence/engine-handle.json) | WebOSR-Binding.dll | analyze_function `0x1800199c0` | `ev_76e6eef383a420b1e93561d5eafaac1f19b850df5312fc343fbd85bb1542fc31` |
| [engine-impl-ctor](evidence/engine-impl-ctor.json) | WebOSR-Binding.dll | analyze_function `0x180038ac0` | `ev_4324fb7ba619dfccfa40a5e231ca14906bc9222bb68a216fa11d402c539c042c` |
| [engine-iteration](evidence/engine-iteration.json) | WebOSR-Binding.dll | analyze_function `0x18003aeb0` | `ev_9818a347b88c0f1d2d2c1c4f58cf635bbbbbd1df854ea3f20b578caa74b4f402` |
| [engine-secondary-tables](evidence/engine-secondary-tables.json) | WebOSR-Binding.dll | read_bytes `0x180060dd8` | `ev_424968ab86509ac38eb1e8f982c0e546eabcf50d6bcb7cbda8773369e6d38eee` |
| [engine-timers](evidence/engine-timers.json) | WebOSR-Binding.dll | analyze_function `0x18003afd0` | `ev_e0f2f13d26d86156f899ce913b40b0438b05b08f90a4db499941c71842eb0640` |
| [engine-vtable-bytes](evidence/engine-vtable-bytes.json) | WebOSR-Binding.dll | read_bytes `0x180060d88` | `ev_21c5f7af23034956187c4aa8b65f672bcf46f271b56993ba2a515d0853a8fb04` |
| [engine-vtable](evidence/engine-vtable.json) | WebOSR-Binding.dll | inspect_native_data_type `0x180060d88` | `ev_8c481ba076722f148012f9faef5548749c8fe1e46ab23c1432db8526a4d2bec6` |
| [engine-worker](evidence/engine-worker.json) | WebOSR-Binding.dll | analyze_function `0x1800383f0` | `ev_f9086ae951437158452af23c60deac7d46e3e64e1f84aa4943d5ee4510e0ecc0` |
| [engine-wrapper-ctor](evidence/engine-wrapper-ctor.json) | WebOSR-Binding.dll | analyze_function `0x180018be0` | `ev_71ea826385848a020a4f45a0e234b9c6095cc1f39c717a0f7bfa8e567624e91d` |
| [fps-body](evidence/fps-body.json) | WebOSR-Binding.dll | analyze_function `0x18003af30` | `ev_55c777ae974a4250cfc0675f3ea4ea1b390c84a867ff935f99f09d8667cdfa68` |
| [fps-jni](evidence/fps-jni.json) | WebOSR-Binding.dll | analyze_function `0x18001c3d0` | `ev_d62200e72967eef82706c92c2474ec5adab23904a9d790882a0da6805d774802` |
| [get-texture-callsite](evidence/get-texture-callsite.json) | WebOSR-Binding.dll | resolve_native_call_targets `0x18001f7d4` | `ev_c5399389b13acc5fbea0ee3a3628328a374ec970fb67ca4a35a5725e62105ddf` |
| [get-texture](evidence/get-texture.json) | WebOSR-Binding.dll | analyze_function `0x18001f7b0` | `ev_0ba0b287b24bf25f0030ce143a63b150caa298a4b76a02cd82a37b184de80fa2` |
| [image-all-tables](evidence/image-all-tables.json) | WebOSR-Binding.dll | read_bytes `0x180061e28` | `ev_8e397225f56328ab5d907ffc635524c7da9a4cd2d52388bca2e87481889dcda2` |
| [image-ctor](evidence/image-ctor.json) | WebOSR-Binding.dll | analyze_function `0x180049180` | `ev_8f67b0610263e50dc1204aa3d3cc331498009a72f135200cd185003248306510` |
| [image-error-xrefs](evidence/image-error-xrefs.json) | WebOSR-Binding.dll | xrefs `0x180061ea0` | `ev_ae27727a693c99545195880eb94e8ee161b9fc12a9288c63c545fa3a5837d1b0` |
| [image-handle](evidence/image-handle.json) | WebOSR-Binding.dll | analyze_function `0x1800277f0` | `ev_f88eb81cee05f35211c49d41d7f9ead2a857126d05215ff764dc799029db5e31` |
| [image-update-copy](evidence/image-update-copy.json) | WebOSR-Binding.dll | analyze_function `0x18004a530` | `ev_d09c55c10422aa429e29ff761a6a7e9b29d988fea912a255e64c45bc5e6d0031` |
| [image-update-jni](evidence/image-update-jni.json) | WebOSR-Binding.dll | analyze_function `0x180027cd0` | `ev_6a04dd211570c00b92cd459839056953c86131a4ca7564555d6c50850682c5e7` |
| [image-update-lambda-table](evidence/image-update-lambda-table.json) | WebOSR-Binding.dll | read_bytes `0x180061f98` | `ev_ee9b75ad0c18dfc9467cc59aada5c216ca9a4b040c4635606a72cf9e85bcf115` |
| [image-update-native](evidence/image-update-native.json) | WebOSR-Binding.dll | analyze_function `0x18004a50c` | `ev_da24d2736a04c66d997c30accd860a4f1e59c5c636e999585d1d58dd04c2ea02` |
| [image-update-task-invoke](evidence/image-update-task-invoke.json) | WebOSR-Binding.dll | analyze_function `0x180049a80` | `ev_c7189fcc3e6af1702da8fccd486ca914aa9a706b4243dd04c70334ca2c8b6f81` |
| [image-update-task-release](evidence/image-update-task-release.json) | WebOSR-Binding.dll | analyze_function `0x180049940` | `ev_448c06f25eff8189f54db3b60ca60edfb651b913d593ec6501a57b8fd76d2392` |
| [image-upload-work](evidence/image-upload-work.json) | WebOSR-Binding.dll | analyze_function `0x180049510` | `ev_0ea09cd33af356281ef4b774dcbba424b49600d030bb7a50d5a93f687812b0f5` |
| [image-vtable](evidence/image-vtable.json) | WebOSR-Binding.dll | read_bytes `0x180061e38` | `ev_b62427850f3f02967fcb250db8cecb16bfbba190502ec9af37994736c1844b00` |
| [iterate](evidence/iterate.json) | WebOSR-Binding.dll | analyze_function `0x18001c3b0` | `ev_8464ecd5d86a7ce7c48eb2a0beea6286df0f437210b5051f7f8093d8afe83e62` |
| [iteration-call-asm](evidence/iteration-call-asm.json) | WebOSR-Binding.dll | procedure_assembly `0x18003aeb0` | `ev_6fbdc5fd6ae184bddf59fae58ea14958598266ad04f7e6f77c576049fa2e06a4` |
| [java-vm](evidence/java-vm.json) | WebOSR-Binding.dll | analyze_function `0x180001e60` | `ev_1e922dce73eccf588773887631eb50a37dfcf2fb87b1958eb09af2514326ff55` |
| [jni-attach-lambda-names](evidence/jni-attach-lambda-names.json) | WebOSR-Binding.dll | search_strings `` | `ev_e336287a8d859c649059d5b7c69a230c92fded925107aa3fdaa6307bb270db35` |
| [jni-create-texture](evidence/jni-create-texture.json) | WebOSR-Binding.dll | analyze_function `0x18002d580` | `ev_0d06d835253abec2ad9ed336ee457302658b10548e84b21cbbd6a2fb07fd51d4` |
| [jni-delete-global-body](evidence/jni-delete-global-body.json) | WebOSR-Binding.dll | analyze_function `0x180001a60` | `ev_933b60e63935ac527933d8dac4a47b2ba6450a8f382bec6183366f65db188f67` |
| [jni-delete-global-task](evidence/jni-delete-global-task.json) | WebOSR-Binding.dll | analyze_function `0x180001d10` | `ev_cfa154dd74c19a7f450964ec6405dc346c64278b3b66c3c3718c19447216eaa1` |
| [jni-delete-texture](evidence/jni-delete-texture.json) | WebOSR-Binding.dll | analyze_function `0x18002d630` | `ev_279bb344224d54581eb1200e29039670791d45fc34664bf04ce15fe2d4c931ee` |
| [jni-detach-task](evidence/jni-detach-task.json) | WebOSR-Binding.dll | analyze_function `0x180001cf0` | `ev_29e8fe7522de9dc167f8f3620fbbba6e551a32476cd59fea6e66d68fabdbf62d` |
| [jni-environment](evidence/jni-environment.json) | WebOSR-Binding.dll | analyze_function `0x1800021d0` | `ev_276d72f33f27f36ad3fc536d5fee4e4fcc29ba89cc0c489dcc67c464b426730b` |
| [jni-field-idle](evidence/jni-field-idle.json) | WebOSR-Binding.dll | analyze_function `0x180009e80` | `ev_eebe8d694af83aac92dae9451077000fe1dd663f762d7892d1a175f8d02bc708` |
| [jni-field-render-target](evidence/jni-field-render-target.json) | WebOSR-Binding.dll | analyze_function `0x1800100b0` | `ev_cb081711356c06c596b0c58000cc28f32f7c7e14b75a4b2749c1d5cdcdcac63f` |
| [jni-field-render](evidence/jni-field-render.json) | WebOSR-Binding.dll | analyze_function `0x18000a010` | `ev_9ec170aa534fbc6e2b3f121c3c105da7042e8de46e2c3afa4b9ceaf88931345a` |
| [jni-field-update](evidence/jni-field-update.json) | WebOSR-Binding.dll | analyze_function `0x180008c80` | `ev_ba44c04991680be5d7edc7552ca4c812b5990d9db2de274744b6227c52f9310c` |
| [jni-getmethod-upload-instruction](evidence/jni-getmethod-upload-instruction.json) | WebOSR-Binding.dll | inspect_native_instruction `0x18002d0cd` | `ev_9a1f077f431cbe1b61f7953aa06fae19cfdee029893444b2b6911ed47be2b531` |
| [jni-invoke-check](evidence/jni-invoke-check.json) | WebOSR-Binding.dll | analyze_function `0x1800020e0` | `ev_50ec0f800870edd8a0fb4cebc3030fb04d9db005401c5ca19d3311a20be03497` |
| [jni-ref-lambda-tables](evidence/jni-ref-lambda-tables.json) | WebOSR-Binding.dll | read_bytes `0x18005ed20` | `ev_0240451a288a4e3485362621694b560ddff1f90c3436e4c9cb7965a17ec4e5e3` |
| [jni-refs-global](evidence/jni-refs-global.json) | WebOSR-Binding.dll | analyze_function `0x1800022a0` | `ev_8d02bb9ce94ad1c9ba4c2fbf46188b0bcba938f3876c5f696a53e1c5a8add0bb` |
| [jni-resize-texture](evidence/jni-resize-texture.json) | WebOSR-Binding.dll | analyze_function `0x18002d840` | `ev_12a1dd254ccc46c231d988c4c81a99b00afc29850ae5436b329882d975751bdd` |
| [jni-texture-ctor](evidence/jni-texture-ctor.json) | WebOSR-Binding.dll | analyze_function `0x18002d360` | `ev_7716878cf3fb4ee5f11eb4a6ce304255f62d89d91b7c3b40143ab15c02d4fd1a` |
| [jni-thread-state](evidence/jni-thread-state.json) | WebOSR-Binding.dll | analyze_function `0x180001f60` | `ev_a0fe8443623f3fad30834f18e2c55d5f80bfd0253dccab215b92f87ded3b24c6` |
| [jni-upload-method-assembly](evidence/jni-upload-method-assembly.json) | WebOSR-Binding.dll | procedure_assembly `0x18002d050` | `ev_129475cfc701a9c7a3f2dd19edfb8be15b5f017b62336f119c7471d08afd076d` |
| [jni-upload-method](evidence/jni-upload-method.json) | WebOSR-Binding.dll | analyze_function `0x18002d050` | `ev_091e7767710958c23bce3e977b5ee5ffb26f2c25a0c682ef37f8836dbcd07b67` |
| [jni-upload-retain](evidence/jni-upload-retain.json) | WebOSR-Binding.dll | analyze_function `0x18002d210` | `ev_1f1a6f0225d0785b51b3a35d69d755b217e1eee630eeb85cd83a8adaa5581cf9` |
| [jni-upload](evidence/jni-upload.json) | WebOSR-Binding.dll | analyze_function `0x18002d910` | `ev_6f6f161ae96d92f5a9d8b9eb9dade54cddb8a59e1d48b43b9da244242fc199ff` |
| [join-xrefs](evidence/join-xrefs.json) | WebOSR-Binding.dll | xrefs `0x18005882b` | `ev_c3477a6c3d32f20cfdb2254bb4548302f994d40973103e46db4389e6a87af82d` |
| [method-jni-signature-helper](evidence/method-jni-signature-helper.json) | WebOSR-Binding.dll | analyze_function `0x180020280` | `ev_5a77aee4c45654e07c03b3e8c73fb24228d937f1c113c98d9887632a6fe2fd12` |
| [named-rendering](evidence/named-rendering.json) | WebOSR-Binding.dll | search_procedures `` | `ev_5f0ead89cfce3d68d2425deb62eb86c6dfaa3af2a3305a1a0784decbd9d1aab4` |
| [pixel-buffer-free](evidence/pixel-buffer-free.json) | WebOSR-Binding.dll | analyze_function `0x180049c20` | `ev_585baf1309a70763ffd3f3f2a5c95c138a4a4868b8fd75a646d9fec2c46e4bfc` |
| [pixel-buffer-grow](evidence/pixel-buffer-grow.json) | WebOSR-Binding.dll | analyze_function `0x18004c1c0` | `ev_c5abdc32bfa2330fd692796e4382054319e053edc57b797d8af40b4d5f5fbfcb` |
| [pixel-buffer-init](evidence/pixel-buffer-init.json) | WebOSR-Binding.dll | analyze_function `0x18004bc00` | `ev_672897d6b91097243208305ed8c09c34cb9c0174aee2b12b0d6590444503ca97` |
| [pixel-buffer-release](evidence/pixel-buffer-release.json) | WebOSR-Binding.dll | analyze_function `0x18004b310` | `ev_e443c3b52fcc1620130058b2a59198bd6271bfd031b3bcdf1aac1c680a841a02` |
| [registration-candidate-1-correct](evidence/registration-candidate-1-correct.json) | WebOSR-Binding.dll | inspect_native_instruction `0x18002fd08` | `ev_959152b3101af3b02cc9a3ab1674a6bf296596f83060041fa2785fdc1e275ce7` |
| [registration-candidate-1](evidence/registration-candidate-1.json) | WebOSR-Binding.dll | inspect_native_instruction `0x18002fd07` | `ev_f2d4215946765fc52659b675085efc4133e2925438acbd8ef33b24ecb33639cb` |
| [registration-candidate-2](evidence/registration-candidate-2.json) | WebOSR-Binding.dll | inspect_native_instruction `0x1800405c0` | `ev_d4cd898ba56c65b2203541432ea67a81799804f751fe22d6cccec08f72bea494` |
| [registration-candidate-3](evidence/registration-candidate-3.json) | WebOSR-Binding.dll | inspect_native_instruction `0x180043a74` | `ev_aa02eb644cf9259d52f0ca5229e5eacab3b17854223241e8ac2d0ae365adeca8` |
| [registration-candidate-4](evidence/registration-candidate-4.json) | WebOSR-Binding.dll | inspect_native_instruction `0x180043ae2` | `ev_41701a628810c5dfb4f002ec144b3656203373c9ffca1e52fa5664c8ba8ad417` |
| [registration-first-function](evidence/registration-first-function.json) | WebOSR-Binding.dll | analyze_function `0x18002f900` | `ev_e9af2c65b1d56c1c7df49dd6d367a4a3593aaf52dd73c68e02c3d1c50b1460a2` |
| [render-submit-assembly](evidence/render-submit-assembly.json) | WebOSR-Binding.dll | procedure_assembly `0x18003b490` | `ev_487e241295e61ab25b401e768682b4e5c67d040595cd02ab8de55974db96651b` |
| [renderer-ctor-type](evidence/renderer-ctor-type.json) | Ultralight.dll | inspect_native_data_type `0x18006c7e8` | `ev_ef3216f24d2df2633b17ce3622d2c31e46505ed76579d363ecc45df4c9230532` |
| [renderer-ctor](evidence/renderer-ctor.json) | Ultralight.dll | analyze_function `0x180051020` | `ev_17deac82472857e7ea4182439a755eeb6bdfb859526f1a570c565f4f1926d8ce` |
| [renderer-render-assembly](evidence/renderer-render-assembly.json) | Ultralight.dll | procedure_assembly `0x1800535d0` | `ev_3423c130dfb8b2b997029025afd7383fc194db6fcf510b273eab59b192b40560` |
| [renderer-render](evidence/renderer-render.json) | Ultralight.dll | analyze_function `0x1800535d0` | `ev_3adbbd2d7120d48acf8837865655a115fa883169240098b80a34dd81b39f65d0` |
| [renderer-select](evidence/renderer-select.json) | Ultralight.dll | analyze_function `0x180053550` | `ev_db43161cbd42bb4823cc1d572185faf9a96e7a52f33727c7ef98c9c49e62a6d5` |
| [renderer-update](evidence/renderer-update.json) | Ultralight.dll | analyze_function `0x1800532c0` | `ev_6d13508dafaed3f329a749d98825ee104f3b3170933744b3d1cbca23be80f177` |
| [renderer-vtable](evidence/renderer-vtable.json) | Ultralight.dll | read_bytes `0x18006c7e8` | `ev_7ea5ab314426c1f46f75580a631a97f9e8c0baca0b129e2938c956ddb5449243` |
| [seed-file-map](evidence/seed-file-map.json) | WebOSR-Binding.dll | address_to_file_offset `0x180010a30` | `ev_02346b0321086012e253ada14f5207a30c5d5a6a7fb0b51a100f2990ad1f7c9c` |
| [session-name](evidence/session-name.json) | WebOSR-Binding.dll | analyze_function `0x180029690` | `ev_33ec9eadff9a112b20635e57811a048c7415b3202c22c0211a35799cdb0d8e25` |
| [shutdown-lambda-table](evidence/shutdown-lambda-table.json) | WebOSR-Binding.dll | read_bytes `0x180061038` | `ev_4c8757f2d9caf4c19e7e04ca99c2c7e459a6bc4dbb77d91e7e0733f315506c21` |
| [shutdown-task](evidence/shutdown-task.json) | WebOSR-Binding.dll | analyze_function `0x18003a160` | `ev_dcabe5d409d0d576112b606c466ccd6c80682463bfea796796f4a2d38c169476` |
| [surface-create](evidence/surface-create.json) | WebOSR-Binding.dll | analyze_function `0x180039c10` | `ev_81f61a4d198cfc659e2b1f4778c4a8404da86b22d25427f00913f83b9b0c6343` |
| [surface-delete-callback-refs](evidence/surface-delete-callback-refs.json) | WebOSR-Binding.dll | procedure_references `0x18002d630` | `ev_3b95c39da7d67051ff68122c896facfcc733b12446f2202e11df37b10afb67a1` |
| [surface-destroy](evidence/surface-destroy.json) | WebOSR-Binding.dll | analyze_function `0x180039d00` | `ev_46480cab1eca3909ec87ef001b97a15759de32af4ed54a84122d30d684514e66` |
| [surface-resize-correct](evidence/surface-resize-correct.json) | WebOSR-Binding.dll | analyze_function `0x18004b550` | `ev_80b1fc0b9208dde6f0175469c86a6a162ae454289394f2802486f3d18e6fb37f` |
| [swap](evidence/swap.json) | WebOSR-Binding.dll | analyze_function `0x18001fc10` | `ev_ccab3b30a5552fdb48cc4594f2a7b0c489a8b81a89648c677118d3a8618562ad` |
| [swapchain-ctor](evidence/swapchain-ctor.json) | WebOSR-Binding.dll | analyze_function `0x18004b130` | `ev_4d711a16ddc9957ac9f73142dd7e6c9cb6757508956c70d3f469bec70558cca4` |
| [swapchain-dtor](evidence/swapchain-dtor.json) | WebOSR-Binding.dll | analyze_function `0x18004b480` | `ev_cca85a837e11ec34a9448b02c29324bff1f60959f91185101d43b9e7f458c960` |
| [swapchain-get-texture](evidence/swapchain-get-texture.json) | WebOSR-Binding.dll | analyze_function `0x18004bd60` | `ev_6ebef923932659330d31e3035017765a1a8a0de62e49ce519fc6a73bc895516e` |
| [swapchain-pixels](evidence/swapchain-pixels.json) | WebOSR-Binding.dll | analyze_function `0x18004b540` | `ev_9d4f5eca9c01d95aae3b8a516ebf3928d4b412463204a06d0b4b19cd69751f71` |
| [swapchain-present](evidence/swapchain-present.json) | WebOSR-Binding.dll | analyze_function `0x18004c360` | `ev_6cb4439aba513c61e2eeb0396c8cbefe917c88513da0f98fda5d2569c2c17320` |
| [swapchain-ready](evidence/swapchain-ready.json) | WebOSR-Binding.dll | analyze_function `0x18004bfa0` | `ev_906b2d4a7bc5738e0ed2fd2dc9b56261bd3497a565bb2344fde4ba43ee79e087` |
| [swapchain-resize](evidence/swapchain-resize.json) | WebOSR-Binding.dll | analyze_function `0x18004bd50` | `ev_5390568fe5b2ed97b7c94368801cce442d89f6cd6969f8e4f01d61c36baa5f71` |
| [swapchain-stride](evidence/swapchain-stride.json) | WebOSR-Binding.dll | analyze_function `0x18004c310` | `ev_258551f2e8b8129fda83e836f5a518c9a457f4c057c64ebd9667819829901bb2` |
| [swapchain-tables](evidence/swapchain-tables.json) | WebOSR-Binding.dll | read_bytes `0x180062020` | `ev_ef4b134983907ed784333bfc5f3bcaa725f5bd3cfd2cd6eb2ff2a88da608ee8f` |
| [swapchain-upload-assembly](evidence/swapchain-upload-assembly.json) | WebOSR-Binding.dll | procedure_assembly `0x18004bd60` | `ev_e524a70199b9f868f03e0a6048ba30dc2de169cab11257f4b49340419a03cfb2` |
| [texture-class-xrefs](evidence/texture-class-xrefs.json) | WebOSR-Binding.dll | xrefs `0x18005eee0` | `ev_acd184791d72f3d3f89e3e24f89f02aa2c4ef5c9512820aea7bf99a92dfb924c` |
| [texture-handler-dtor](evidence/texture-handler-dtor.json) | WebOSR-Binding.dll | analyze_function `0x18002d470` | `ev_02515dd352bcdc0e8ff856b0a225706328cad7f437c51bca6e7d27e33b216d8b` |
| [texture-handler-input](evidence/texture-handler-input.json) | WebOSR-Binding.dll | analyze_function `0x1800100b0` | `ev_c91a9f66ce79a3eb2dd0e0b70066213a338cd1108605d8dacde8224a4206a40e` |
| [texture-handler-vtable](evidence/texture-handler-vtable.json) | WebOSR-Binding.dll | read_bytes `0x1800602d0` | `ev_3c59eebe42e860131a219542a90055e84b36a4e7c765a90c8c4f4ed1da788ae3` |
| [texture-source-size](evidence/texture-source-size.json) | WebOSR-Binding.dll | analyze_function `0x18004a230` | `ev_f15e75e22c97f6d08862ac1e8007295ed5f77915e15264468b8310e30d6f513d` |
| [texture-source-update-thunk](evidence/texture-source-update-thunk.json) | WebOSR-Binding.dll | analyze_function `0x18004a51c` | `ev_227f83e98e2d1e6b2e26aec3894bb8c60f2b293bf0d3fe2a6bf4b9f300cc666e` |
| [texture-strings](evidence/texture-strings.json) | WebOSR-Binding.dll | search_strings `` | `ev_6a99c9a86a2ad6ab7d967bc8cd3aeb8dfb652f99736305b90ff61a3f9e5656ee` |
| [texture-update-body](evidence/texture-update-body.json) | WebOSR-Binding.dll | analyze_function `0x18004ccb0` | `ev_e99fcfe32970588bac044427776779536d7536d4885631fd3ddf8f3e0e19929b` |
| [thread-attach-cleanup](evidence/thread-attach-cleanup.json) | WebOSR-Binding.dll | analyze_function `0x1800014c0` | `ev_c9555a6b8f3bad352011fd0d2d41a3b0e29707dae912c9a86e51e18611d4d8e5` |
| [thread-join](evidence/thread-join.json) | WebOSR-Binding.dll | analyze_function `0x18003aec0` | `ev_7342ca210635c2efb9b6b5e7324dff4947e73aa6d9c851d821d5974a6c201513` |
| [threadconfig-fields](evidence/threadconfig-fields.json) | WebOSR-Binding.dll | search_strings `` | `ev_aaeddd40b480fb226b4528e8e494917e054183581e2b157ca561c4981be25820` |
| [threadconfig](evidence/threadconfig.json) | WebOSR-Binding.dll | analyze_function `0x180010810` | `ev_8824f7d0a71d8859144d13ed58477c55bdaf88c4204ea126f24cc150902d9089` |
| [timers](evidence/timers.json) | WebOSR-Binding.dll | analyze_function `0x18001c400` | `ev_81e0fd6ee657314bc856e72238fa3bd9207219f9c59f4b0fac4cb82afe599a12` |
| [ultralight-create](evidence/ultralight-create.json) | Ultralight.dll | analyze_function `0x180050190` | `ev_1706f4f60f666d115a31146f5bc38ef1e845a390019154b3e7e674dcf78e7fd9` |
| [ultralight-overview](evidence/ultralight-overview.json) | Ultralight.dll | binary_overview `` | `ev_2bcad9f9adf8dc9ed91cff298007be39a59d4c0715c6707342f649f3f5878840` |
| [ultralight-renderer-methods](evidence/ultralight-renderer-methods.json) | Ultralight.dll | search_procedures `` | `ev_4d359f1867ff934456376e505e07cbd50d489bb5434430314100e7382c5ec780` |
| [upload-call-assembly](evidence/upload-call-assembly.json) | WebOSR-Binding.dll | procedure_assembly `0x18002d910` | `ev_6f25daf435695775994fb32072eb7e339be9bd38ed8fb2c869975a6d93816eb5` |
| [upload-callback](evidence/upload-callback.json) | WebOSR-Binding.dll | analyze_function `0x18002ce90` | `ev_9ab33d77f698fa3b9f824acc05692ef8ff6d35157678750194c9a8aea44a2a4a` |
| [upload-descriptor](evidence/upload-descriptor.json) | WebOSR-Binding.dll | analyze_function `0x18002bea0` | `ev_26846980227b8e1cde9c45154f50494ea5b01ce485d8644ba22bc7b0148bac5f` |
| [upload-name-xrefs](evidence/upload-name-xrefs.json) | WebOSR-Binding.dll | xrefs `0x180060298` | `ev_f27fa8d54567038afc182404600a3907171086c3d23d9a9f8c0682f1fe218393` |
| [view-close](evidence/view-close.json) | Ultralight.dll | analyze_function `0x180057b20` | `ev_354677e7f6ef407fc55a9a8dd736be84c97dbd4b1356a8ca72979aac916b79bf` |
| [view-release](evidence/view-release.json) | Ultralight.dll | analyze_function `0x180056aa0` | `ev_8cfed108ee5ab36ca5f228d78f1f0a3f9188414e661b27704c838e0c18ec429b` |
| [view-vtable](evidence/view-vtable.json) | Ultralight.dll | read_bytes `0x18006d568` | `ev_26e19078f2d9f020303e66461fd36066ef2c52e9aa299fec699cf4b34f4e3051` |
| [worker-init](evidence/worker-init.json) | WebOSR-Binding.dll | analyze_function `0x18003b020` | `ev_6ddda76fbe0c3dff6d546814c0f88dcd049a36b41a009ec9184458c55bc9c435` |
| [worker-loop](evidence/worker-loop.json) | WebOSR-Binding.dll | analyze_function `0x180039990` | `ev_888b51beb76a8c038bf1efa67608603270d6fcfc76815e912235b8806948294b` |
| [worker-run](evidence/worker-run.json) | WebOSR-Binding.dll | analyze_function `0x18003b490` | `ev_7677cc52b19c1b0b0bfb6cbda416093ab83b24215bb18866b7433065390d8f2c` |

## Records retained through exported bundles

Some large tool responses hit transport limits; the analysis record is retained in the exported bundle rather than reconstructed from a truncated preview. The bundle record with the exact ID below is the evidence authority.

| Bundle | Binary | Operation / location | Evidence ID |
|---|---|---|---|
| [ultralight-evidence-bundle.json](ultralight-evidence-bundle.json) | Ultralight.dll | list_names `` | `ev_bd4e5e78ea7df9d54e28677ece148c7abb425ee86b7acdf8c30ff818903637c6` |

## Lifecycle receipts, local data and unsuccessful tool boundaries

An MCP envelope can have `isError: false` while its structured payload reports an operation error. These files are not automatically positive evidence of the requested operation.

| File | Classification |
|---|---|
| [binding-close.json](evidence/binding-close.json) | Receipt or local derived data |
| [binding-final-close.json](evidence/binding-final-close.json) | Receipt or local derived data |
| [binding-final-evidence.json](evidence/binding-final-evidence.json) | Receipt or local derived data |
| [binding-final-export.json](evidence/binding-final-export.json) | Receipt or local derived data |
| [binding-open.json](evidence/binding-open.json) | Receipt or local derived data |
| [binding-reopen.json](evidence/binding-reopen.json) | Receipt or local derived data |
| [binding-session-open.json](evidence/binding-session-open.json) | Receipt or local derived data |
| [jni-abi-offsets.json](evidence/jni-abi-offsets.json) | Receipt or local derived data |
| [jni-reconciliation-fresh.json](evidence/jni-reconciliation-fresh.json) | Receipt or local derived data |
| [local-session-before.json](evidence/local-session-before.json) | Receipt or local derived data |
| [registration-bounded-scan.json](evidence/registration-bounded-scan.json) | Receipt or local derived data |
| [ultralight-close.json](evidence/ultralight-close.json) | Receipt or local derived data |
| [ultralight-export.json](evidence/ultralight-export.json) | Receipt or local derived data |
| [ultralight-final-export.json](evidence/ultralight-final-export.json) | Receipt or local derived data |
| [ultralight-names.json](evidence/ultralight-names.json) | Tool error/coverage boundary (not a successful finding) |
| [ultralight-open.json](evidence/ultralight-open.json) | Receipt or local derived data |

## Interpretation and coverage rules

- **Verified** means static artifact evidence, not observed runtime execution. **Inferred** conclusions and **Unknown** questions are labeled in the reports.
- Analyst filenames can be exploratory guesses. [Corrections](ghidra-verification.md) identify misleading names and their authoritative replacements.
- `views/` files project pseudocode/table values for readability. Full raw/normalized results, profile metadata and limitations stay in the JSON envelope or bundle.
- No claim of universal absence follows from a bounded negative string, byte or direct-reference search.
- JSON syntax and file hashes are validated locally; this script does not independently recompute REA canonical Evidence IDs or certify a decompiler result.
- Snapshots contain retained analysis products; they are not original executable modifications or a persistent GUI database.
