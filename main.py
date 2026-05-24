import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from agent.pipeline import run_agent
from agent.config import config


app = FastAPI(title=" AI Safety Voice Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "active"}

@app.websocket("/ws")
async def google_agent(websocket: WebSocket):
    await websocket.accept()
    try:
        await run_agent(websocket)
    except Exception as exc:
        logger.exception(f"[/ws] Session error: {exc}")
    finally:
        logger.info("[/ws] Connection closed.")

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    uvicorn.run("main:app", host=config.host, port=port, reload=False)