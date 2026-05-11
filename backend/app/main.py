from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.rate_limiter import rate_limiter
from app.websocket.orders import router as websocket_router


app = FastAPI(
    title="Food Delivery Marketplace API",
    version="0.1.0",
    description="Backend API for food-delivery marketplace project",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def token_bucket_rate_limiter(request: Request, call_next):
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)

    if not rate_limiter.is_allowed(request):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests. Please try again later.",
            },
        )

    response = await call_next(request)
    return response


@app.get("/", tags=["health"])
def root():
    return {
        "message": "Food Delivery Marketplace API is running",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": "backend",
    }


app.include_router(api_router, prefix="/api")
app.include_router(websocket_router)
