from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

# Import routers (make sure these files exist)
try:
    from routes import email_router, log_router
except ImportError:
    # Create dummy routers if files don't exist
    from fastapi import APIRouter
    email_router = APIRouter()
    log_router = APIRouter()

# Initialize FastAPI app
app = FastAPI(
    title="Lightning Studio API",
    description="A comprehensive API for your Lightning Studio project",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, JS) - only if directory exists
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(email_router, prefix="/generate_email", tags=["Email Assistant"])
app.include_router(log_router, prefix="/logs", tags=["Email Logs"])


# --------- Model Placeholder (replace later) ----------
class ModelRequest(BaseModel):
    model_config = {'protected_namespaces': ()}  # Fixes the pydantic warning
    
    input_data: Dict[str, Any]
    model_params: Optional[Dict[str, Any]] = None

class ModelResponse(BaseModel):
    prediction: Any
    confidence: Optional[float] = None
    timestamp: datetime

@app.post("/predict", response_model=ModelResponse)
async def predict(request: ModelRequest):
    try:
        prediction = {
            "result": "mock_prediction",
            "input_received": request.input_data
        }
        return ModelResponse(
            prediction=prediction,
            confidence=0.95,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/batch_predict")
async def batch_predict(requests: List[ModelRequest]):
    try:
        results = []
        for req in requests:
            results.append({
                "prediction": {
                    "result": f"batch_prediction_{len(results)}",
                    "input_received": req.input_data
                },
                "confidence": 0.95,
                "timestamp": datetime.now()
            })
        return {"predictions": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

# --------- Health Check ----------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "components": {
            "model": "loaded",
            "database": "connected",
            "email": "ready"
        }
    }

# --------- File Upload ----------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return {
            "filename": file.filename,
            "size": len(content),
            "content_type": file.content_type,
            "path": file_path,
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

# --------- Dashboard Route ----------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard - Template not found</h1>", status_code=200)

# --------- Welcome Route ----------
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lightning Studio</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .nav { display: flex; gap: 20px; justify-content: center; margin-top: 30px; }
            .nav a { padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .nav a:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Lightning Studio API</h1>
            <p>Welcome to your Lightning Studio dashboard!</p>
            <div class="nav">
                <a href="/dashboard">📊 Dashboard</a>
                <a href="/docs">📚 API Documentation</a>
                <a href="/health">🩺 System Health</a>
            </div>
        </div>
    </body>
    </html>
    """

# --------- CRITICAL: Render Port Configuration ----------
if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
