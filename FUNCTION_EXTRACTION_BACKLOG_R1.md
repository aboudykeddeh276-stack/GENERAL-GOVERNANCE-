# KEDDEH Systems Function Extraction Backlog R1

This backlog is derived from observed code/search evidence across the current 35-repository estate. It is intentionally non-destructive.

## Migration protocol

For every mechanic:

`SOURCE DISCOVERY -> CLASSIFY OWNER -> COPY -> CONTENT HASH -> SOURCE TEST -> TARGET TEST -> TARGET READBACK -> AUTHORITY SWITCH -> OPTIONAL SOURCE RETIREMENT`

No source deletion is permitted before target readback.

## P0 — Mixed canonical carriers

### MINING -> BRAINK
Observed candidates:
- `backend/braink_core.py` — BRAINK registration/state/directive services.
- `backend/routes/braink_instance.py` — BRAINK route surface.
- `backend/services/braink_chat_service.py` — BRAINK chat integration surface.
- `scripts/braink_cli.py` — BRAINK CLI.
- `scripts/braink_os_agent.py` — BRAINK OS agent/receipt logic.
- `scripts/braink_os_build.py` and `scripts/braink_os_manifest.py` — BRAINK OS build/manifest mechanics.
- `scripts/braink_native_runtime.py` — BRAINK native runtime compiler/launcher.

Action: compare against current BRAINK implementations; migrate only missing/superior mechanics. Keep compatibility wrappers in MINING until mining tests pass against canonical imports.

### MINING -> KEX / NETWORK-FABRIC / SERVER-RUNTIME
Observed candidates:
- `scripts/check_kex_runtime_model.py` — KEX runtime model checks.
- `backend/keddeh_mesh_os_runtime.py` — mesh/OS runtime mechanics.
- `kex_btc_full_system/scripts/btc_full_system/mesh_runtime.py` — logical KERA mesh endpoint mechanics.

Action: split KEX invariants from generic mesh/network/server mechanics; mining-specific adapters remain in MINING.

### MINING stays BTC-MINING
Observed canonical mining candidates:
- `kex_btc_full_system/scripts/btc_full_system/rpc_runtime.py` — Bitcoin Core RPC authority runtime.
- `workload_runtime.py` — workload/candidate generation path.
- `solver_runtime.py` — candidate reconstruction/freshness/submission path.
- `core_service_runtime.py` — mining/core-service coordination.
- `common_runtime.py` — compatibility/common mining runtime functions.

Action: keep in MINING; remove cross-sector ownership assumptions only after imports are rewired.

## P0 — KEX mathematical consolidation

### untitled -> KEX
Observed:
- Zeroless Matrix formal specification.
- matrix implementation and correctness tests (`src/lib/keddehTests.ts` and related implementation files).

### untitled-good -> KEX/BRAINK + projection split
Observed:
- `src/lib/keddeh-systems.ts` — system/problem-layer mechanics.
- `src/lib/keddeh-core-wiring.ts` — optimizer/deep-learning/system wiring.
- healing/resource-limit logic.
- UI dashboards such as `CoreWiringDashboard.tsx`, `KEDDEHSystemsInterface.tsx`, `AutoHealingDashboard.tsx`.

Action: extract pure core logic separately from UI. Core mechanics route to KEX/BRAINK according to state/execution ownership; dashboards route to HCI/WEB-FABRIC.

### KEDDEH-ALGEBRA-CORES + UNIVERSAL-CALIBRATION-MATRIX -> KEX
Action: inventory executable algebra/calibration contracts and compare them against the Zeroless Matrix implementation before creating a single KEX mathematical-core package.

## P1 — K-DRIVE / storage authority comparison

### virtualized-storage
Observed:
- `src/lib/storage-utils.ts` and storage-block model.
- `StorageMap.tsx` and management/projection surfaces.
- virtualized storage manager PRD, validation and R&D material.

### VIRTUALISED_MEMORY
Observed:
- `.kex/ledger/ENTER_WORKBOOK_STORAGE.md`.
- `.kex/ledger/STORAGE_SUBSTRATE_MANIFEST.json`.
- workbook storage artifact lineage and KEX pipeline evidence.

Action: benchmark actual persistence/readback mechanics. Do not equate visualization/control UI with storage authority. Preserve workbook/ledger provenance independently.

## P1 — Cloud/server split

### SERVERS-KEDDEHSYSTEMS
Keep generic server execution, host binding, listener and DA execution mechanics.

### kcloud-substrate
Candidate home for cloud substrate/public compute allocation mechanics.

### KEDDEH-CLOUD-SERVERS-ID-1
Observed mixed storage, KEX router, folder substrate, workload-governance and cloud/server material.

### KERA_SERVER
Supporting KERA server/mesh descendant.

Action: distinguish `cloud allocation` from `server execution` from `network/mesh` from `storage`. Public-IP allocation requires external readback and must not be inferred from logical cloud bindings.

## P1 — Quantum consolidation

- `quantum-computer-by-keddeh-systems`: candidate canonical runtime.
- `KEDDEH-SYSTEMS-QUANTUM-RUNTIME-MATRIX-`: runtime matrix/evidence.
- `Quantum-Dashboard`: HCI/projection.

Action: runtime first, evidence second, dashboard third. No dashboard state may establish quantum execution capability.

## P2 — Agent / learning split

- `ai-shell`: agent/HCI runtime bridge candidate.
- `KSYSTEMS_LEARNING-`: unresolved IL-LLM/agent-learning carrier.
- `K-SYSTEM_UPDATE_LANE_PROCESS_x-x`: update/process orchestration carrier.

Action: separate language/ontology data, agent decision/orchestration, process governance and HCI transport.

## P2 — OS / workbook discovery

- `1AXIS-MATRIX-OS`.
- `Google-studio-Keddeh-OSxOS`.

Action: locate executable entrypoints and distinguish workbook-native runtime, generic OS substrate, KEX mathematics and projection UI before authority assignment.

## P2 — Generic / misnamed carrier discovery

- `backend`.
- `app`.
- `repository-based-to`.
- `emrg-attempt-ui`.
- `K-SYSTEMS-CODE-SPACE-`.

Action: enumerate files, entrypoints, tests, persistence, network interfaces and deployment paths. Route each mechanic to a sector owner. Keep carrier in quarantine until all executable material is accounted for.

## P3 — Legacy / experiments

- `BRAINK_DESKTOP_ORGANISED`.
- `Braink-Beta`.
- `BRAINK-CONSOLE-PLUS`.
- `random.k.test-`.
- `gogo`.

Action: compare against canonical implementations, retain useful delta, preserve provenance, then archive only after migration proof.

## Completion condition

Repository organization is complete only when:
1. every executable mechanic has exactly one canonical sector owner;
2. every duplicate has a declared compatibility/legacy reason or is retired after proof;
3. every projection identifies the runtime it projects;
4. every runtime identifies persistence/network/authority dependencies explicitly;
5. every migration has source hash, target hash, tests and readback evidence.
