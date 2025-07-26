from fastapi import FastAPI
from routers import analyze
import uvicorn

app = FastAPI(
    title="Site Güvenilirlik Analizi API",
    description="Gemini destekli bir uygulama ile girilen sitelerin güvenilirliğini değerlendirir.",
    version="1.0.0"
)

app.include_router(analyze.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

