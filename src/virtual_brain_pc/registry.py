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
}
