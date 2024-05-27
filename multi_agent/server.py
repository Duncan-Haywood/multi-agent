# src/my_crewai_project/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse 
from multi_agent.crew import kickoff_crew


app = FastAPI()

# redirect to the /docs endpoint
@app.get("/")
async def redirect():
    return RedirectResponse(url='/docs')

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/start_crew/")
async def start_crew():
    result = kickoff_crew()
    return {"result": result}