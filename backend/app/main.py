from fastapi import FastAPI

app = FastAPI(
    title="LogFlow AI",
    description="API para automação e reconciliação logística.",
    version="0.1.0",
     
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "aplication": "LogFlow AI"
    }