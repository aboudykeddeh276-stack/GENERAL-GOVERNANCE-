from __future__ import annotations
import hashlib,json,uuid,time

class ResearchGraph:
    def __init__(self): self.nodes={};self.edges=[]
    def add_node(self,node_type,payload):
        nid=f"{node_type.upper()}-{uuid.uuid4().hex[:10]}"
        self.nodes[nid]={"type":node_type,"payload":payload,"root":hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(),"created_ns":time.time_ns()}
        return nid
    def link(self,a,b,relation,weight=1.0):
        assert a in self.nodes and b in self.nodes
        self.edges.append({"from":a,"to":b,"relation":relation,"weight":float(weight)})
    def contradictions(self):
        return [e for e in self.edges if e["relation"]=="contradicts"]
