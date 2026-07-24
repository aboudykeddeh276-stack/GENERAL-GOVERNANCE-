# KEX-BRAINK Sector Evolution Compiler V5

This package evolves the verified V4 BRAINK seed compiler into a whole-system
sector compiler.

## Completed scope

- Parent V4 seed package preserved.
- 15 operational sectors plus one master coordinator compiled.
- All 25 current GitHub repositories assigned exactly once to an accountable repository-bound sector.
- Workbook OS, Web4/KCPU, research/publication, linguistic/bioethics, and Codex fleet systems compiled as conceptual sectors.
- Every sector includes a profile, KEX sector seed, repository bindings, task schema, evolution policy, generation state, runtime wrapper, compiled agent instruction, sector bundle, and compile receipt.
- Receipt-driven evolution uses exact rational arithmetic and preserves the parent generation whenever a promotion gate fails.

## Compile every sector

```bash
python3 compiler/kex_sector_compiler.py --root . compile-all
```

## Compile one sector

```bash
python3 compiler/kex_sector_compiler.py --root . compile-sector S01_BRAINK_CORE_ORCHESTRATION
```

## Run one sector package

```bash
python3 sectors/S01_BRAINK_CORE_ORCHESTRATION/runtime.py status
python3 sectors/S01_BRAINK_CORE_ORCHESTRATION/runtime.py task "Repair and verify the active runtime route"
```

## Apply an execution receipt

```bash
python3 compiler/kex_sector_compiler.py --root . evolve-sector \
  S01_BRAINK_CORE_ORCHESTRATION \
  --receipt /path/to/execution_receipt.json
```

## Promotion theorem

```text
PROMOTE =
  [anchor=1] * [validation=1] * [continuity=1]
  * [mean(anchor,factor,translation,action,validation,continuity)>=49/60]
  * [bilateral_residual=0] * [proof_product=1]
```

Bias update:

```text
b_next = clip((19/20)b_current + (1/5)(axis - 49/60), -3/20, 3/20)
```

Uniform polygons apply zero directional bias.

## Verification

The package test suite validates repository coverage, deterministic compilation,
required runtime files, successful promotion, parent preservation on failure,
neutral-input behavior, and bounded bias.
