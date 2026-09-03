# RUNTIME REGIME R1

## Purpose

Define how runtime authority is established and how work crosses process, host, sector, and persistence boundaries.

## Runtime authority order

1. Executable local workspace/runtime state.
2. Resident process state and direct readback.
3. Mounted/persistent state volumes.
4. Repository source synchronization and CI evidence.
5. Google Drive / Library continuity and archival readback.
6. External/provider state only when the owning actuator is actually invoked and read back.

GitHub and Google Drive are boundaries around the workspace, not the primary development environment.

## Execution loop

ENTER LOCAL WORKSPACE
→ VERIFY ACTUAL STATE
→ LOCATE EXISTING MECHANIC
→ EXECUTE
→ OBSERVE
→ PATCH THE SMALLEST REAL DEFICIENCY
→ TEST
→ FAILURE-INJECT
→ PERSIST / READ BACK
→ FOLLOW DESCENDANTS
→ BENCHMARK
→ SYNC SOURCE
→ CI READBACK
→ PERSIST CONTINUITY EVIDENCE

## Runtime identity law

logical service identity ≠ current process
logical computer identity ≠ current host
work identity ≠ current agent
persistent state ≠ current carrier
authority ≠ network location

## Runtime lifecycle

PROCESS_DEFINED
→ PROCESS_BOUND
→ PROCESS_EXECUTED
→ PROCESS_SIGNALED
→ PROCESS_OBSERVED
→ PUBLIC_PROJECTION_OBSERVED
→ PROMOTED

## Successor/continuation regime

Every durable work unit SHOULD carry:
- work_id
- actor_id / holder
- lease_epoch
- definition/class identity
- input_state_root
- continuation pointer
- evidence pointer
- checkpoint root
- descendant references

Worker/process replacement is valid only when successor readback proves continuity and stale authority is fenced.
