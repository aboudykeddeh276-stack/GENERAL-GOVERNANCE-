# KEDDEH Systems Estate Repository Registry R1

Authority: estate repository classification and migration control.

## Governance law

A repository name is not proof of sector authority. Existing carriers are classified by observed mechanics, then migrated by COPY -> HASH -> TEST -> READBACK -> AUTHORITY SWITCH -> optional retirement. No destructive move is permitted before readback.

## Canonical / candidate sector roots

| Sector | Canonical or candidate repository | State |
|---|---|---|
| BRAINK | `aboudykeddeh276-stack/BRAINK` | ACTIVE CANONICAL |
| SERVER-RUNTIME | `aboudykeddeh276-stack/SERVERS-KEDDEHSYSTEMS` | ACTIVE CANONICAL |
| BTC-MINING | `aboudykeddeh276-stack/MINING` | ACTIVE, MIXED CONTENT REQUIRES EXTRACTION |
| CLOUD-INFRASTRUCTURE | `aboudykeddeh276-stack/kcloud-substrate` | CANONICAL CANDIDATE |
| K-DRIVE / STORAGE | `aboudykeddeh276-stack/virtualized-storage` | CANONICAL CANDIDATE |
| QUANTUM-COMPUTE | `aboudykeddeh276-stack/quantum-computer-by-keddeh-systems` | CANONICAL CANDIDATE |
| ESTATE-GOVERNANCE | `aboudykeddeh276-stack/GENERAL-GOVERNANCE-` | ACTIVE GOVERNANCE ROOT |
| KEX | `aboudykeddeh276-stack/kex-braink-substrate` | CANDIDATE; BRAINK/KEX CONTENT MUST BE SEPARATED |

## Existing carrier classification

| Repository | Observed / inferred role | Migration disposition |
|---|---|---|
| BRAINK | BRAINK core, Observer², governance, runtime lineage | KEEP; extract non-BRAINK sector code over time |
| emrg-attempt-ui | UI/projection prototype | WEB-FABRIC candidate; inspect before promotion |
| Quantum-Dashboard | quantum UI/dashboard | QUANTUM-COMPUTE projection candidate |
| ai-shell | agent shell / Expo-parent runtime bridge | AGENTS-ORCHESTRATION candidate |
| MINING | Bitcoin mining plus BRAINK/KEX/mesh/runtime material | KEEP mining; extract cross-sector mechanics |
| backend | ambiguous backend carrier | QUARANTINE/DISCOVERY |
| BRAINK_DESKTOP_ORGANISED | BRAINK desktop legacy carrier | BRAINK supporting/legacy; compare then migrate |
| KERA_SERVER | KERA server/mesh descendant | SERVER-RUNTIME supporting carrier |
| btc-mining-edu | Bitcoin mining education/projection | BTC-MINING supporting documentation/projection |
| KEX_HYPERDRIVE_DASHBOARD_UI | KEX dashboard projection | KEX projection / WEB-FABRIC relation |
| quantum-computer-by-keddeh-systems | quantum compute carrier | QUANTUM-COMPUTE canonical candidate |
| KEDDEH-SYSTEMS-QUANTUM-RUNTIME-MATRIX- | quantum runtime matrix | QUANTUM-COMPUTE supporting evidence/model |
| app | generic application carrier with KEDDEH/BRAINK/KEX material | QUARANTINE/DISCOVERY; likely WEB-FABRIC projection |
| GENERAL-GOVERNANCE- | governance carrier | ESTATE-GOVERNANCE root |
| K-SYSTEM_UPDATE_LANE_PROCESS_x-x | update/process lane | AGENTS-ORCHESTRATION / GOVERNANCE supporting process |
| KSYSTEMS_LEARNING- | learning carrier | IL-LLM / AGENTS candidate; inspect before authority |
| VIRTUALISED_MEMORY | virtual memory/storage mechanics | K-DRIVE supporting carrier |
| KEDDEH_SOFTWARE_NODES | software-node mechanics | EDGE-IOT / NETWORK-FABRIC candidate |
| K-SYSTEMS-CODE-SPACE- | development/code-space carrier | DEVELOPMENT/QUARANTINE; no production authority |
| 1AXIS-MATRIX-OS | matrix/OS carrier | WORKBOOK-OS/KEX candidate |
| UNIVERSAL-CALIBRATION-MATRIX | calibration/matrix carrier | KEX mathematical/core supporting carrier |
| random.k.test- | experimental test carrier | QUARANTINE/EXPERIMENT |
| KEDDEH-CLOUD-SERVERS-ID-1 | cloud/server logical runtime bindings | CLOUD-INFRASTRUCTURE + SERVER-RUNTIME supporting carrier |
| SERVERS-KEDDEHSYSTEMS | server runtimes / host binding / DA execution | SERVER-RUNTIME canonical |
| KEDDEH-ALGEBRA-CORES | algebra/core mechanics | KEX mathematical core candidate |
| Google-studio-Keddeh-OSxOS | OS prototype carrier | WORKBOOK-OS/BRAINK prototype; inspect |
| virtualized-storage | storage implementation carrier | K-DRIVE canonical candidate |
| repository-based-to | KEDDEH research engine/integration carrier | RESEARCH/QUARANTINE; extract proven mechanics |
| untitled | Zeroless Matrix algorithm/spec/tests | KEX mathematical implementation supporting carrier; rename/migrate, do not discard |
| untitled-good | KEDDEH optimizer, core wiring, healing UI | KEX/BRAINK research implementation supporting carrier |
| gogo | empty/near-empty carrier | QUARANTINE; no authority |
| kcloud-substrate | cloud substrate carrier | CLOUD-INFRASTRUCTURE canonical candidate |
| Braink-Beta | BRAINK beta carrier | BRAINK legacy/beta supporting carrier |
| BRAINK-CONSOLE-PLUS | BRAINK console projection | BRAINK HCI supporting carrier |
| kex-braink-substrate | combined KEX/BRAINK substrate | KEX candidate; split shared-vs-owned mechanics |

## Mandatory repository status classes

- `ACTIVE_CANONICAL`: sector authority is established here.
- `CANONICAL_CANDIDATE`: strongest current carrier, pending comparison/readback.
- `SUPPORTING`: valid descendant or implementation surface, not sector root.
- `QUARANTINE_DISCOVERY`: contains material but authority is unresolved.
- `LEGACY`: retained for provenance while canonical mechanics move elsewhere.
- `EXPERIMENT`: no production authority.

## Immediate extraction priority

1. Extract BRAINK/KEX/mesh code from `MINING` without disturbing the Bitcoin path.
2. Consolidate Zeroless Matrix / algebra / calibration mechanics from `untitled`, `untitled-good`, `KEDDEH-ALGEBRA-CORES`, and `UNIVERSAL-CALIBRATION-MATRIX` into the eventual KEX canonical root.
3. Compare `virtualized-storage` and `VIRTUALISED_MEMORY`; establish K-DRIVE authority from executed mechanics, not repository size.
4. Compare `kcloud-substrate`, `KEDDEH-CLOUD-SERVERS-ID-1`, `KERA_SERVER`, and `SERVERS-KEDDEHSYSTEMS`; keep cloud allocation separate from generic server execution.
5. Inventory `app`, `backend`, `repository-based-to`, `untitled-good`, and `emrg-attempt-ui` as projection/research carriers before moving code.
6. Preserve every original carrier until hashes, tests and target readback are complete.
