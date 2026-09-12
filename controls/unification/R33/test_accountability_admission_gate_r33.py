#!/usr/bin/env python3
import copy
import unittest

from accountability_admission_gate_r33 import evaluate


def base_record():
    return {
        "subject": "node://braink/example",
        "action": "MODIFY",
        "requested_claim": "IMPLEMENTED",
        "claim_scope": "runtime://braink",
        "estate_search": {
            "scopes": ["repo://BRAINK", "repo://KEDDEH_SOFTWARE_NODES"],
            "queries": ["subject identity", "capability lineage", "adapters descendants predecessors"],
            "completeness": "EXHAUSTIVE_FOR_SCOPE",
            "candidates": [
                {
                    "ref": "repo://BRAINK/runtime/example.py",
                    "role": "IMPLEMENTATION",
                    "working_observed": True,
                }
            ],
        },
        "braink_resolution_ref": "braink://resolution/example",
        "illlm_lineage_ref": "illlm://braink/lineage/example",
        "authority": {
            "current_authority_root": "braink://authority/example",
            "mutation_authority": "braink://authority/example",
        },
        "preservation": {
            "source_preserved": True,
            "source_ref": "repo://BRAINK/runtime/example.py",
        },
        "proposed_mutation": {
            "authority_role": "IMPLEMENTATION",
            "synthesized": False,
            "source_domain": "BRAINK_RUNTIME",
            "target_domain": "BRAINK_RUNTIME",
        },
        "evidence": {
            "scope": "runtime://braink",
            "predicates": ["implementation_present"],
        },
        "facts": {},
    }


class AccountabilityGateR33Tests(unittest.TestCase):
    def test_valid_bounded_change_allows(self):
        self.assertEqual(evaluate(base_record()).decision, "ALLOW")

    def test_partial_no_result_is_not_absence(self):
        r = base_record()
        r["requested_claim"] = "ABSENT"
        r["estate_search"]["completeness"] = "PARTIAL"
        r["estate_search"]["candidates"] = []
        d = evaluate(r)
        self.assertEqual(d.decision, "DENY")
        self.assertIn("DENY:NOT_OBSERVED_IS_NOT_ABSENT", d.reasons)
        self.assertIn("IMPLEMENTATION_STATUS_UNRESOLVED", d.unresolved)

    def test_synthesized_replacement_of_working_runtime_denied_without_real_parity(self):
        r = base_record()
        r["action"] = "REPLACE"
        r["proposed_mutation"]["synthesized"] = True
        r["authority_transfer"] = {
            "explicitly_authorized": False,
            "behavioral_parity_against_original": True,
            "real_path_readback": False,
            "original_ref": "repo://BRAINK/runtime/example.py",
        }
        d = evaluate(r)
        self.assertIn("DENY:WORKING_SOURCE_SYNTHESIZED_REPLACEMENT_UNPROVEN", d.reasons)

    def test_derived_representation_cannot_become_source_authority(self):
        r = base_record()
        r["proposed_mutation"]["authority_role"] = "DERIVED"
        d = evaluate(r)
        self.assertIn("DENY:DERIVED_CANNOT_BECOME_SOURCE_AUTHORITY", d.reasons)

    def test_queue_cannot_become_execution_authority(self):
        r = base_record()
        r["proposed_mutation"]["authority_role"] = "QUEUE_OR_INDEX"
        d = evaluate(r)
        self.assertIn("DENY:QUEUE_OR_INDEX_CANNOT_BECOME_SOURCE_AUTHORITY", d.reasons)

    def test_carrier_cannot_become_state_authority(self):
        r = base_record()
        r["proposed_mutation"]["authority_role"] = "CARRIER"
        d = evaluate(r)
        self.assertIn("DENY:CARRIER_CANNOT_BECOME_SOURCE_AUTHORITY", d.reasons)

    def test_simulation_cannot_claim_local_execution(self):
        r = base_record()
        r["requested_claim"] = "LOCALLY_EXECUTED"
        r["evidence"]["predicates"] = ["simulation_readback"]
        d = evaluate(r)
        self.assertTrue(any(x.startswith("DENY:CLAIM_EVIDENCE_MISSING:local_execution_readback") for x in d.reasons))

    def test_local_http_cannot_claim_public_http(self):
        r = base_record()
        r["requested_claim"] = "PUBLICLY_REACHABLE"
        r["claim_scope"] = "network://public-http"
        r["evidence"] = {"scope": "http://loopback", "predicates": ["local_execution_readback"]}
        d = evaluate(r)
        self.assertIn("DENY:EVIDENCE_SCOPE_PROMOTION", d.reasons)
        self.assertTrue(any(x.startswith("DENY:CLAIM_EVIDENCE_MISSING:external_boundary_readback") for x in d.reasons))

    def test_github_runner_zero_does_not_describe_braink_runtime(self):
        r = base_record()
        r["facts"]["github_actions_runner_id"] = 0
        d = evaluate(r)
        self.assertIn("DENY:GITHUB_RUNNER_FACT_CANNOT_DESCRIBE_KEX_BRAINK_RUNTIME", d.reasons)

    def test_workbook_isp_intent_does_not_prove_public_bgp(self):
        r = base_record()
        r["requested_claim"] = "PUBLICLY_REACHABLE"
        r["claim_scope"] = "network://public-bgp"
        r["evidence"] = {"scope": "workbook://network-intent", "predicates": ["implementation_present"]}
        r["facts"]["workbook_network_intent"] = True
        d = evaluate(r)
        self.assertIn("DENY:EVIDENCE_SCOPE_PROMOTION", d.reasons)
        self.assertIn("DENY:WORKBOOK_INTENT_IS_NOT_PUBLIC_NETWORK_EXECUTION", d.reasons)

    def test_private_da_readback_does_not_prove_parent_delegation(self):
        r = base_record()
        r["requested_claim"] = "PUBLICLY_REACHABLE"
        r["claim_scope"] = "dns://parent-delegation"
        r["evidence"] = {"scope": "dns://private-authority", "predicates": ["local_execution_readback"]}
        r["facts"]["private_da_authority_readback"] = True
        d = evaluate(r)
        self.assertIn("DENY:EVIDENCE_SCOPE_PROMOTION", d.reasons)
        self.assertIn("DENY:PRIVATE_DA_READBACK_IS_NOT_PUBLIC_DELEGATION", d.reasons)

    def test_cross_domain_mutation_requires_existing_binding_and_bilateral_authority(self):
        r = base_record()
        r["action"] = "BIND"
        r["proposed_mutation"]["source_domain"] = "BRAINK_RUNTIME"
        r["proposed_mutation"]["target_domain"] = "SERVER_CARRIER"
        d = evaluate(r)
        self.assertIn("DENY:CROSS_DOMAIN_EXISTING_BINDING_REQUIRED", d.reasons)
        self.assertIn("DENY:CROSS_DOMAIN_BILATERAL_AUTHORITY_REQUIRED", d.reasons)

    def test_valid_existing_node_binding_claim_is_bounded(self):
        r = base_record()
        r["action"] = "BIND"
        r["requested_claim"] = "EDGE_BOUND"
        r["claim_scope"] = "edge://braink/software-nodes"
        r["evidence"] = {
            "scope": "edge://braink/software-nodes",
            "predicates": ["edge_binding_readback"],
        }
        r["proposed_mutation"]["source_domain"] = "BRAINK_RUNTIME"
        r["proposed_mutation"]["target_domain"] = "SOFTWARE_NODES"
        r["cross_domain_binding"] = {
            "existing_binding_ref": "binding://r33/existing",
            "source_authority_ref": "braink://authority/example",
            "target_authority_ref": "software-nodes://authority/sector",
        }
        self.assertEqual(evaluate(r).decision, "ALLOW")


if __name__ == "__main__":
    unittest.main()
