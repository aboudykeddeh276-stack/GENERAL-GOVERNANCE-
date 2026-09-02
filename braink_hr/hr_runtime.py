from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Iterable, Mapping, Any
import hashlib, json

def root(v:Any)->str:
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True)
class HRAssignment:
    assignment_id:str
    agent_id:str
    team_id:str
    sector:str
    roles:tuple[str,...]
    capabilities:tuple[str,...]
    authority_scope:tuple[str,...]
    verifier:bool=False
    promoter:bool=False
    revoked:bool=False
    @property
    def assignment_root(self): return root(asdict(self))

class HRRuntime:
    def __init__(self): self.assignments:Dict[str,HRAssignment]={}
    def assign(self,record:HRAssignment):
        if record.agent_id in self.assignments and self.assignments[record.agent_id].revoked:
            raise RuntimeError("REVOKED_AGENT_REQUIRES_FORMAL_REINSTATEMENT")
        self.assignments[record.agent_id]=record; return record
    def revoke(self,agent_id:str):
        r=self.assignments[agent_id]
        self.assignments[agent_id]=HRAssignment(r.assignment_id,r.agent_id,r.team_id,r.sector,r.roles,r.capabilities,r.authority_scope,r.verifier,r.promoter,True)
    def authorize(self,agent_id:str,sector:str,capability:str,target:str)->Mapping[str,Any]:
        r=self.assignments.get(agent_id)
        if r is None:return {"authorized":False,"reason":"AGENT_UNASSIGNED"}
        if r.revoked:return {"authorized":False,"reason":"AGENT_REVOKED"}
        if r.sector!=sector:return {"authorized":False,"reason":"SECTOR_MISMATCH"}
        if capability not in r.capabilities:return {"authorized":False,"reason":"CAPABILITY_UNASSIGNED"}
        if not any(target.startswith(prefix) for prefix in r.authority_scope):return {"authorized":False,"reason":"TARGET_OUT_OF_SCOPE"}
        return {"authorized":True,"assignment_root":r.assignment_root,"team_id":r.team_id,"roles":r.roles}
    @property
    def state_root(self): return root({k:asdict(v) for k,v in sorted(self.assignments.items())})
