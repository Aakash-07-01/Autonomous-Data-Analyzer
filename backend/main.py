import os
import uuid
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage

# Load environment variables
load_dotenv(override=True)

from agent.graph import build_graph
from agent.prompts import SYSTEM_PROMPT
from report.generator import generate_html

app = FastAPI(title="Autonomous Data Analyst Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store for jobs
jobs_store = {}

# Compile LangGraph once
graph = build_graph()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
        
    jobs_store[job_id] = {
        "file_path": file_path,
        "filename": file.filename,
        "status": "idle",
        "findings": "",
        "charts": [],
        "report_markdown": ""
    }
    
    return {"job_id": job_id, "filename": file.filename}

@app.get("/analyse/{job_id}")
async def analyse(job_id: str):
    if job_id not in jobs_store:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_info = jobs_store[job_id]
    csv_path = job_info["file_path"]
    
    initial_state = {
        "messages": [SystemMessage(content=SYSTEM_PROMPT)],
        "csv_path": csv_path,
        "charts": [],
        "findings": "",
        "thoughts": [],
        "iteration": 0
    }
    
    async def event_generator():
        last_thoughts_len = 0
        final_state = None
        
        try:
            async for s in graph.astream(initial_state, stream_mode="values"):
                final_state = s
                
                # Check for new thoughts
                thoughts = s.get("thoughts", [])
                
                # Yield new thoughts
                if len(thoughts) > last_thoughts_len:
                    for thought in thoughts[last_thoughts_len:]:
                        yield {
                            "event": "message",
                            "data": json.dumps({"type": "thought", "thought": thought})
                        }
                    last_thoughts_len = len(thoughts)
            
            # Graph execution finished
            if final_state:
                findings = final_state.get("findings", "")
                charts = final_state.get("charts", [])
                
                job_info["status"] = "done"
                job_info["findings"] = findings
                job_info["charts"] = charts
                job_info["report_markdown"] = findings
                
                yield {
                    "event": "message",
                    "data": json.dumps({
                        "type": "done", 
                        "findings": findings,
                        "charts": charts,
                        "report_markdown": findings
                    })
                }
        except Exception as e:
            yield {
                "event": "message",
                "data": json.dumps({"type": "error", "message": str(e)})
            }
            
    return EventSourceResponse(event_generator())

@app.get("/report/{job_id}/html")
async def download_html(job_id: str):
    if job_id not in jobs_store:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_info = jobs_store[job_id]
    
    if job_info["status"] != "done":
        raise HTTPException(status_code=400, detail="Report not ready yet")
        
    try:
        html_content = generate_html(
            job_info["report_markdown"], 
            job_info["charts"],
            filename=job_info.get("filename", "dataset.csv"),
            job_id=job_id
        )
        
        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": f"inline; filename=eda_report_{job_id}.html"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating HTML: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
