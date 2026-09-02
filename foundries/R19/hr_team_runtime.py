from __future__ import annotations
from dataclasses import dataclass,asdict
import uuid,time

@dataclass
class Team:
    team_id:str
    name:str
    capacity:int
    allocated:int=0

@dataclass
class Candidate:
    candidate_id:str
    role_id:str
    state:str
    score:float=0

class HRTeamRuntime:
    def __init__(self): self.teams={};self.candidates={};self.events=[]
    def create_team(self,name,capacity):
        tid="TEAM-"+uuid.uuid4().hex[:10];self.teams[tid]=Team(tid,name,int(capacity));return asdict(self.teams[tid])
    def allocate(self,team_id,units):
        t=self.teams[team_id]
        if t.allocated+units>t.capacity:return {"status":"CAPACITY_EXCEEDED","available":t.capacity-t.allocated}
        t.allocated+=units;return {"status":"ALLOCATED","team":asdict(t)}
    def recruit(self,role_id):
        cid="CAND-"+uuid.uuid4().hex[:10];self.candidates[cid]=Candidate(cid,role_id,"SOURCED");return asdict(self.candidates[cid])
    def assess(self,candidate_id,score):
        c=self.candidates[candidate_id];c.score=float(score);c.state="QUALIFIED" if score>=0.7 else "REJECTED";return asdict(c)
