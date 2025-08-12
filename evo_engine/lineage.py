
import uuid

def new_lineage(generation:int=0, parent_id:str|None=None) -> dict:
    return {"parent_id": parent_id, "generation": generation, "id": str(uuid.uuid4())}
