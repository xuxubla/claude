import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="claude-proxy")


class CompletionRequest(BaseModel):
    prompt: str
    system: str | None = None


class CompletionResponse(BaseModel):
    content: str


@app.post("/complete")
def complete(req: CompletionRequest) -> CompletionResponse:
    prompt = req.prompt
    if req.system:
        prompt = f"{req.system}\n\n{req.prompt}"
    cmd = ["claude", "-p", prompt, "--bare"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        raise HTTPException(503, "claude CLI не найден")
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "claude CLI превысил таймаут")
    if result.returncode != 0:
        raise HTTPException(502, f"claude CLI ошибка: {result.stderr.strip()}")
    return CompletionResponse(content=result.stdout.strip())


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
