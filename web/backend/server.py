import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load .env file from root or local dir
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Add core and backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from openrouter_client import call_openrouter_agent

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

app = FastAPI(
    title="Universal Job & Internship Talent Scout API",
    description="Universal AI Talent Scout for ANY engineering domain (Embedded, PCB, Hardware, AI, Software) via OpenRouter stealth/ox-alpha"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UniversalSearchRequest(BaseModel):
    role: str = "Embedded Systems Engineer Intern"
    location: str = "Hyderabad"
    job_type: str = "Internship"
    paid_only: bool = True

@app.get("/api/health")
async def health_check():
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    model_id = os.getenv("OPENROUTER_MODEL_ID", "stealth/ox-alpha").strip()
    return {
        "status": "healthy",
        "model_id": model_id,
        "api_key_configured": bool(api_key and api_key != "your_openrouter_api_key_here"),
        "supported_domains": ["Embedded Systems", "PCB Design", "VLSI / Semiconductor", "AI / ML / Agentic", "Full-Stack Software", "Aerospace & Robotics"]
    }

@app.post("/api/search")
async def search_jobs(req: UniversalSearchRequest):
    try:
        role = req.role.strip() or "AI Engineer Intern"
        loc = req.location.strip() or "Hyderabad"
        jtype = req.job_type.strip() or "Internship"

        print(f"[SEARCH REQUEST] Domain/Role: '{role}' | Location: '{loc}' | Type: '{jtype}' | Paid: {req.paid_only}")
        
        leads, model_used, is_live = call_openrouter_agent(
            role=role,
            location=loc,
            job_type=jtype
        )

        return {
            "success": True,
            "leads": leads,
            "count": len(leads),
            "model_used": model_used,
            "is_live_agent": is_live,
            "query": {
                "role": role,
                "location": loc,
                "job_type": jtype
            }
        }
    except Exception as e:
        print(f"[SEARCH ERROR]: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Serve canonical root index.html
root_index = Path(__file__).resolve().parent.parent.parent / "index.html"

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if root_index.exists():
        return FileResponse(str(root_index))
    return HTMLResponse("<h1>Universal Job Scout</h1><p>Frontend is building...</p>")

def start():
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on http://localhost:{port} ...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    start()
