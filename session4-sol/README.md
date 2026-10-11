# Lunar Client static RE — session 4 (SOL)

Date: 2026-10-11. This directory contains new work only. Reports and evidence outside this directory are inputs and must not be overwritten.

## Boundaries

- Do not execute or load Lunar JARs, natives, JavaScript or other target code.
- Installation files are read-only. Do not access credentials, accounts.json, installation-id, tokens, or personal settings values.
- No anti-cheat/integrity investigation, protection bypass, reimplementation, runtime attach, or tooling installation/configuration.
- Use static javap/disassembly, archive parsing and available REA static operations.
- Label findings Confirmed / Strong inference / Tentative / Unknown, with actual artifact, class, method and method-relative bytecode offset (or native RVA/file offset). Bounded negative searches are not universal proofs.

## Investigation checklist

1. Event-bus thread checks, locking, nested dispatch, deferred mutations and cancellation.
2. RpcChannel tracking, timeouts, error paths and cleanup.
3. Server/support/restriction/intercept transitions and propagation to children/subscriptions.
4. Six additional modules: ARMORSTATUS, POTION_EFFECTS, TOGGLE_SNEAK, REACH_DISPLAY, COMBO and PACK_DISPLAY.
5. New WebOSR/JNI/native rendering evidence beyond the session-3 metadata and mismatch inventory.
6. Contradiction checks, an evidence ledger, preservation checks and remaining questions.

## Starting evidence

The parent directory's session-3 ledger closes registration filtering, HUD global math/snapping, migration-list/load algorithm and UI throttle identity. It structurally catalogs events and traces FPS/CPS/ZOOM/Coordinates/Keystrokes/Waypoints. Those investigations will not be repeated.

Retained static dumps and extracted class files are in:
`C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad`.

Progress and final findings will be indexed here as work completes.
