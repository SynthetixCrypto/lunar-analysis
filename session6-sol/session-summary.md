# Session 6 — Remaining Java Internals and Native Analysis

Completed 2026-10-11. Static-only, read-only target investigation. Previous reports and evidence were preserved. Lunar binaries/classes were not executed; credentials, personal profile values, private services and protection mechanisms were not accessed.

## What was resolved

- **G-04/G-05:** actual modern attack-distance producers, entity tick units, outgoing target/timestamp writer, status/hurt producers, periodic reset timing and range-source branches. The “last attacker” bridge names refer to the last **outgoing attacked target**. Combo counts fresh correlated timestamps, so it is not universally one increment per hit. Actual Minecraft class writers were checked in retained installed caches.
- **G-18/G-19 and G-22:** direct override producer table, conditional observer-to-full-toggle lifecycle, criteria reset versus predicate removal, retained interceptor hierarchy and generic source arbitration. Generic settings use a single last-accepted slot; server refresh's category-blind generic clear can remove another source's active override. Toggle isEnabled can read an intercepted effective setting rather than raw intent. Broader remote deletion/live source ordering remain open.
- **G-13:** the specified 16 non-auth call-containing methods show no demonstrated pre-send request-pending spinner/lock. Radio refresh/reset and checkout screen boundaries were traced. A separate checkout close-push dependency remains a conditional cleanup concern.
- **G-11:** one locked diagnostic reader of the exposed map, repeatable batch wrapper producers, and screen/hotbar paired callers were classified in the 8,095-class direct-call scope. **G-10:** escaping active-dispatch failures and failed replay now have concrete static chains; runtime failure occurrence remains unknown.
- **G-01/G-02:** remaining armor geometry/protection/custom-point formulas and potion layout/order/blink/inventory cancellation were recovered with explicit sub-branch limits. Armor's protection term literally uses integer XOR, not an assumed square.
- **G-14/G-16/G-17/G-21/G-32/G-33:** narrowed null-message/error precursor, serialized normal receive path, old-transport retention, successful dependency callback order, PromiseJS codec continuation and FunctionBus caller/queue recovery boundaries. These do not establish live failure frequency, prompt GC or native promise semantics.

## Native preparation and results

Fresh REA diagnostics already select the intended Microsoft **JDK 21.0.10**. No Java configuration repair or system-wide change was necessary. A usable Ghidra installation was not found in the bounded search, and REA reports it unconfigured. It was **not installed**, respecting the explicit approval requirement. Deep native analysis could not begin; no native database, new native decompilation or native REA Evidence ID is claimed.

The DLL's fresh SHA-256 matches prior native evidence. The JNI mismatch is now exact: **55 shared bindings, Java-only Session.name, and DLL-only Session_getName, Browser_swapBuffers and WebEngine_setTimers**. A four-JAR constant-pool scan covered 27,075 class occurrences and found no symbolic Session method references; alternate registration/native/reflection/external callers remain unresolved.

Java implementation evidence now fixes byte-stride units, source/destination rectangles, version-gated BGRA→RGBA conversion, reusable staging memory, reverse framebuffer→native image transfer and Java shutdown/failure boundaries. **Native paint callbacks, allocation/ownership/lifetime, copying/borrowing, worker threads, synchronization, affinity and native failure unwind remain unknown.** Java declarations were not used to invent those answers.

[native-rendering-analysis.md](native-rendering-analysis.md) records every N-0..N-8 stage, all 16 questions, the five exact native seeds and concrete provider setup/analysis steps after installation approval.

## Deliverables and validation

The seven requested reports are:

1. [java-gap-resolution.md](java-gap-resolution.md)
2. [native-rendering-analysis.md](native-rendering-analysis.md)
3. [jni-and-webosr.md](jni-and-webosr.md)
4. [additional-findings.md](additional-findings.md)
5. [evidence-index.md](evidence-index.md)
6. [remaining-unknowns.md](remaining-unknowns.md)
7. This [session-summary.md](session-summary.md)

Detailed supplements: [reach/combo](reach-combo-findings.md), [support](support-findings.md), [RPC](rpc-findings.md), [event bus](bus-findings.md), [armor](armor-followup.md), [potion](potion-followup.md) and [FunctionBus](functionbus-followup.md). Every discovery points to artifact/class/method/offset or a native coordinate with confidence/limits. Original identifiers and output/raw hashes are distinguished in the evidence index.

[evidence-validation.json](evidence-validation.json) records successful checks of 85 class-manifest entries, all seven required reports and 190 local Markdown links; [evidence-integrity.json](evidence-integrity.json) hashes 395 saved report/helper/evidence files. Validation confirms saved evidence consistency, not target runtime behavior.

## Session 7 recommendation

Prioritize **further native static analysis after Ghidra installation approval**, using the prepared five seeds and 16-question checklist. The JDK prerequisite is already satisfied. If Ghidra remains unavailable, the strongest alternative is **implementation-ready technical specifications** for settings/support, events, RPC state and the recovered HUD algorithms. Additional feature algorithms should then follow the independent client's chosen scope; another inventory pass has low value.

All G-01..G-33 dispositions and unchanged B-01..B-05 boundaries are preserved in [remaining-unknowns.md](remaining-unknowns.md).
