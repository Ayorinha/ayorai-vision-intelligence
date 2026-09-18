from fastapi import FastAPI,HTTPException
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry

mcp_app=FastAPI(title="AYORAI Tool Gateway")
registry:ToolRegistry=build_registry()

@mcp_app.get("/mcp/tools")
def tools():
    return {"transport":"HTTP tool gateway","tools":registry.names()}

@mcp_app.post("/mcp/call/{name}")
def call(name:str,arguments:dict|None=None):
    try: return {"result":registry.call(name,**(arguments or {}))}
    except KeyError as exc: raise HTTPException(404,str(exc))
