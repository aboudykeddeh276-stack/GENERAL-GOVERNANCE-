from __future__ import annotations
import hashlib,json,time,uuid

class PublishingRuntime:
    def __init__(self): self.channels={};self.publications={}
    def register_channel(self,channel_id,handler=None): self.channels[channel_id]=handler
    def publish(self,content,channels,version="1"):
        pid="PUB-"+uuid.uuid4().hex[:10]
        root=hashlib.sha256(content.encode()).hexdigest()
        results={}
        for c in channels:
            h=self.channels.get(c)
            results[c]={"status":"AUTHORITY_UNBOUND"} if h is None else h(content,version)
        self.publications[pid]={"content_root":root,"version":version,"channels":results,"created_ns":time.time_ns()}
        return {"publication_id":pid,"content_root":root,"channels":results}
