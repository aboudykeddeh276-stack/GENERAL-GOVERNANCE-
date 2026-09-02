from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class MarketVector:
    module_id:str
    capability:str
    measurable_output:str
    buyer:str
    operational_metric:str
    deployment_dependency:str
    value_hypothesis:str
    evidence_state:str

class MarketValidator:
    def assess(self,module_id,capability,measurable_output,buyer,operational_metric,deployment_dependency,value_hypothesis,evidence_state="LOCAL_VALIDATED"):
        return asdict(MarketVector(module_id,capability,measurable_output,buyer,operational_metric,deployment_dependency,value_hypothesis,evidence_state))
    def feasibility(self,*,executable,dependency_ready,external_authority_bound,local_tests_pass):
        score=sum([25 if executable else 0,25 if dependency_ready else 0,25 if external_authority_bound else 0,25 if local_tests_pass else 0])
        return {"score":score,"classification":"MARKET_READY" if score==100 else "PARTIAL","external_authority_bound":external_authority_bound}
