from __future__ import annotations

from typing import Dict


REGISTRY_BLOCKS: Dict[str, Dict[str, str]] = {
    "MATERIAL_WHOLE_BINDER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::MATERIAL::WHOLE1::BIND::v01",
        "specific_call_name": "CALL_MATERIAL_WHOLE_BIND",
    },
    "ACTIVE_STRESS_CROSSING": {
        "importance": "Highest",
        "naming_convention": "BRAINK::MATERIAL::STRESS2::CROSS::v01",
        "specific_call_name": "CALL_ACTIVE_STRESS_CROSSING",
    },
    "BOUNDARY_PAIR_DETECTOR": {
        "importance": "Highest",
        "naming_convention": "BRAINK::BOUNDARY::PAIR2::DETECT::v01",
        "specific_call_name": "CALL_BOUNDARY_PAIR_DETECT",
    },
    "NEAR_FAILURE_297_BAND": {
        "importance": "Highest",
        "naming_convention": "BRAINK::FAILURE::BAND297::DETECT::v01",
        "specific_call_name": "CALL_NEAR_FAILURE_297_BAND",
    },
    "BOUNDARY_3_ACHIEVEMENT": {
        "importance": "Highest",
        "naming_convention": "BRAINK::BOUNDARY::ACHIEVEMENT3::COMMIT::v01",
        "specific_call_name": "CALL_BOUNDARY_3_ACHIEVEMENT",
    },
    "FAILURE_CALIBRATION_LEDGER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::LEDGER::FAILURE_CALIBRATION::COMMIT::v01",
        "specific_call_name": "CALL_FAILURE_CALIBRATION_LEDGER",
    },
    "SPIKE_EVENT_CLASSIFIER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::SPIKE::EVENT::CLASSIFY::v01",
        "specific_call_name": "CALL_SPIKE_EVENT_CLASSIFY",
    },
    "TEMPERATURE_SPIKE_BOUNDARY": {
        "importance": "Highest",
        "naming_convention": "BRAINK::THERMAL::SPIKE::BOUNDARY::v01",
        "specific_call_name": "CALL_TEMPERATURE_SPIKE_BOUNDARY",
    },
    "VOLTAGE_SPIKE_BOUNDARY": {
        "importance": "Highest",
        "naming_convention": "BRAINK::ELECTRIC::SPIKE::BOUNDARY::v01",
        "specific_call_name": "CALL_VOLTAGE_SPIKE_BOUNDARY",
    },
    "RUNTIME_EXISTENCE_TRACE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::RUNTIME::EXISTENCE::TRACE::v01",
        "specific_call_name": "CALL_RUNTIME_EXISTENCE_TRACE",
    },
    "DETRIMENTAL_FAILURE_SPIKE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::FAILURE::SPIKE::DETRIMENTAL::v01",
        "specific_call_name": "CALL_DETRIMENTAL_FAILURE_SPIKE",
    },
    "BOUNDARY_REALIGNMENT_ENGINE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::BOUNDARY::REALIGN::ENGINE::v01",
        "specific_call_name": "CALL_BOUNDARY_REALIGNMENT_ENGINE",
    },
    "HEARTBEAT_TICK": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::HEARTBEAT::TICK::v01",
        "specific_call_name": "CALL_HEARTBEAT_TICK",
    },
    "INGESTION_INPUT": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::INGESTION::INPUT::v01",
        "specific_call_name": "CALL_INGESTION_INPUT",
    },
    "WHOLE_ONE_BIND": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::WHOLE1::BIND::v01",
        "specific_call_name": "CALL_WHOLE_ONE_BIND",
    },
    "ACTIVE_VALUE_PRESERVE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::ACTIVE2::PRESERVE::v01",
        "specific_call_name": "CALL_ACTIVE_VALUE_PRESERVE",
    },
    "PROOF_LEDGER_COMMIT": {
        "importance": "Highest",
        "naming_convention": "BRAINK::LEDGER::PROOF::COMMIT::v01",
        "specific_call_name": "CALL_PROOF_LEDGER_COMMIT",
    },
    "SIGNAL_OUTPUT": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::SIGNAL3::OUTPUT::v01",
        "specific_call_name": "CALL_SIGNAL_OUTPUT",
    },
    # -----------------------------------------------------------------------
    # v1.5 — Organism core, zero doctrine, calibration, thinking, learning
    # -----------------------------------------------------------------------
    "POWER_CORE_1": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CORE::POWER1::FEED::v01",
        "specific_call_name": "CALL_POWER_CORE_READ",
    },
    "ACTIVE_STATE_2": {
        "importance": "Highest",
        "naming_convention": "BRAINK::STATE::ACTIVE2::CROSS::v01",
        "specific_call_name": "CALL_ACTIVE_STATE_2_CROSS",
    },
    "BOUNDARY_SIGNAL_3": {
        "importance": "Highest",
        "naming_convention": "BRAINK::BOUNDARY::SIGNAL3::ACHIEVE::v01",
        "specific_call_name": "CALL_BOUNDARY_SIGNAL_3",
    },
    "ZERO_PARSER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::PARSER::ZERO::CLASSIFY::v01",
        "specific_call_name": "CALL_ZERO_CLASSIFY",
    },
    "ZERO_RELATION_RESOLVER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::ZERO::RELATION::RESOLVE::v01",
        "specific_call_name": "CALL_ZERO_RELATION_RESOLVE",
    },
    "SYMBOLIC_ZERO_GATE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::ZERO::SYMBOLIC::GATE::v01",
        "specific_call_name": "CALL_SYMBOLIC_ZERO_GATE",
    },
    "ENVIRONMENT_WEIGHT_BINDER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::WEIGHT::ENVIRONMENT::BIND::v01",
        "specific_call_name": "CALL_ENVIRONMENT_WEIGHT_BIND",
    },
    "SCALE_TYPE_CLASSIFIER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::SCALE::TYPE::CLASSIFY::v01",
        "specific_call_name": "CALL_SCALE_CLASSIFY",
    },
    "CALIBRATION_ENGINE": {
        "importance": "Highest",
        "naming_convention": "BRAINK::CALIBRATION::ENGINE::RUN::v01",
        "specific_call_name": "CALL_CALIBRATION_RUN",
    },
    "CELSIUS_KELVIN_COMPARATOR": {
        "importance": "Highest",
        "naming_convention": "BRAINK::THERMAL::CELSIUS_KELVIN::COMPARE::v01",
        "specific_call_name": "CALL_CELSIUS_KELVIN_COMPARE",
    },
    "RESONANCE_297_CLASSIFIER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::RESONANCE::297::CLASSIFY::v01",
        "specific_call_name": "CALL_RESONANCE_297_CLASSIFY",
    },
    "TENSOR_ZERO_TYPED_ENTRY": {
        "importance": "High",
        "naming_convention": "BRAINK::TENSOR::ZERO::TYPE_ENTRY::v01",
        "specific_call_name": "CALL_TENSOR_ZERO_TYPE_ENTRY",
    },
    "SWIRL_VORTEX_CALIBRATOR": {
        "importance": "High",
        "naming_convention": "BRAINK::SWIRL::VORTEX::CALIBRATE::v01",
        "specific_call_name": "CALL_SWIRL_VORTEX_CALIBRATE",
    },
    "SIMULATION_ROUTE_ACCELERATOR": {
        "importance": "High",
        "naming_convention": "BRAINK::SIMULATION::ROUTE::ACCELERATE::v01",
        "specific_call_name": "CALL_SIMULATION_ROUTE_ACCELERATOR",
    },
    "THINKING": {
        "importance": "Critical",
        "naming_convention": "BRAINK::MIND::THINKING::PROCESS::v01",
        "specific_call_name": "CALL_THINKING_PROCESS",
    },
    "MIRROR_UPDATE_LANE": {
        "importance": "Critical",
        "naming_convention": "BRAINK::LANE::MIRROR::UPDATE::v01",
        "specific_call_name": "CALL_MIRROR_UPDATE_LANE",
    },
    "LEARNING": {
        "importance": "Critical",
        "naming_convention": "BRAINK::MIND::LEARNING::MIRROR_UPDATE::v01",
        "specific_call_name": "CALL_LEARNING_MIRROR_UPDATE",
    },
    "MEMORY_MATRIX": {
        "importance": "Critical",
        "naming_convention": "BRAINK::MEMORY::MATRIX::STORE::v01",
        "specific_call_name": "CALL_MEMORY_MATRIX",
    },
    "KEDDEH_THEOREM_LEDGER": {
        "importance": "Highest",
        "naming_convention": "BRAINK::LEDGER::KEDDEH_THEOREM::COMMIT::v01",
        "specific_call_name": "CALL_KEDDEH_THEOREM_LEDGER",
    },
    # -----------------------------------------------------------------------
    # v1.6 — Birth boundary anchor and author resonance key
    # -----------------------------------------------------------------------
    "BIRTH_BOUNDARY_ANCHOR": {
        "importance": "High",
        "naming_convention": "BRAINK::AUTHOR::BIRTH_BOUNDARY::ANCHOR::v01",
        "specific_call_name": "CALL_BIRTH_BOUNDARY_ANCHOR",
    },
    "AUTHOR_RESONANCE_KEY": {
        "importance": "High",
        "naming_convention": "BRAINK::AUTHOR::RESONANCE_KEY::MAP::v01",
        "specific_call_name": "CALL_AUTHOR_RESONANCE_KEY",
    },
}
