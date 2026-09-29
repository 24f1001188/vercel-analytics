# api/index.py
from typing import Any, Dict, List

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS config similar to the person who got it right
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Expose-Headers": "Access-Control-Allow-Origin",
}

# Add FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Access-Control-Allow-Origin"],
)

TELEMETRY_DATA: List[Dict[str, Any]] = [
    {"region": "apac", "service": "recommendations", "latency_ms": 138.72, "uptime_pct": 97.117, "timestamp": 20250301},
    {"region": "apac", "service": "support", "latency_ms": 131.92, "uptime_pct": 97.452, "timestamp": 20250302},
    {"region": "apac", "service": "payments", "latency_ms": 119.96, "uptime_pct": 97.311, "timestamp": 20250303},
    {"region": "apac", "service": "catalog", "latency_ms": 170.2, "uptime_pct": 99.279, "timestamp": 20250304},
    {"region": "apac", "service": "support", "latency_ms": 211.74, "uptime_pct": 97.687, "timestamp": 20250305},
    {"region": "apac", "service": "support", "latency_ms": 186.43, "uptime_pct": 99.347, "timestamp": 20250306},
    {"region": "apac", "service": "recommendations", "latency_ms": 211.92, "uptime_pct": 99.147, "timestamp": 20250307},
    {"region": "apac", "service": "analytics", "latency_ms": 172.2, "uptime_pct": 97.547, "timestamp": 20250308},
    {"region": "apac", "service": "recommendations", "latency_ms": 209.78, "uptime_pct": 97.939, "timestamp": 20250309},
    {"region": "apac", "service": "analytics", "latency_ms": 189.79, "uptime_pct": 98.126, "timestamp": 20250310},
    {"region": "apac", "service": "recommendations", "latency_ms": 185.08, "uptime_pct": 98.545, "timestamp": 20250311},
    {"region": "apac", "service": "payments", "latency_ms": 164.59, "uptime_pct": 97.898, "timestamp": 20250312},
    {"region": "emea", "service": "recommendations", "latency_ms": 222.77, "uptime_pct": 99.105, "timestamp": 20250301},
    {"region": "emea", "service": "checkout", "latency_ms": 187.87, "uptime_pct": 99.499, "timestamp": 20250302},
    {"region": "emea", "service": "checkout", "latency_ms": 214.47, "uptime_pct": 99.372, "timestamp": 20250303},
    {"region": "emea", "service": "payments", "latency_ms": 108.57, "uptime_pct": 97.94, "timestamp": 20250304},
    {"region": "emea", "service": "support", "latency_ms": 139.85, "uptime_pct": 99.243, "timestamp": 20250305},
    {"region": "emea", "service": "payments", "latency_ms": 130.9, "uptime_pct": 97.302, "timestamp": 20250306},
    {"region": "emea", "service": "support", "latency_ms": 137.22, "uptime_pct": 98.665, "timestamp": 20250307},
    {"region": "emea", "service": "support", "latency_ms": 126.4, "uptime_pct": 97.45, "timestamp": 20250308},
    {"region": "emea", "service": "analytics", "latency_ms": 211.69, "uptime_pct": 98.323, "timestamp": 20250309},
    {"region": "emea", "service": "payments", "latency_ms": 220.66, "uptime_pct": 99.232, "timestamp": 20250310},
    {"region": "emea", "service": "catalog", "latency_ms": 224.1, "uptime_pct": 99.055, "timestamp": 20250311},
    {"region": "emea", "service": "recommendations", "latency_ms": 192.2, "uptime_pct": 98.139, "timestamp": 20250312},
    {"region": "amer", "service": "payments", "latency_ms": 182.59, "uptime_pct": 98.377, "timestamp": 20250301},
    {"region": "amer", "service": "payments", "latency_ms": 202.07, "uptime_pct": 98.763, "timestamp": 20250302},
    {"region": "amer", "service": "checkout", "latency_ms": 164.67, "uptime_pct": 97.648, "timestamp": 20250303},
    {"region": "amer", "service": "catalog", "latency_ms": 180.43, "uptime_pct": 98.4, "timestamp": 20250304},
    {"region": "amer", "service": "payments", "latency_ms": 169.15, "uptime_pct": 98.194, "timestamp": 20250305},
    {"region": "amer", "service": "payments", "latency_ms": 116.16, "uptime_pct": 97.76, "timestamp": 20250306},
    {"region": "amer", "service": "recommendations", "latency_ms": 135.45, "uptime_pct": 97.39, "timestamp": 20250307},
    {"region": "amer", "service": "payments", "latency_ms": 210.18, "uptime_pct": 98.924, "timestamp": 20250308},
    {"region": "amer", "service": "checkout", "latency_ms": 125.32, "uptime_pct": 97.349, "timestamp": 20250309},
    {"region": "amer", "service": "payments", "latency_ms": 192.58, "uptime_pct": 98.109, "timestamp": 20250310},
    {"region": "amer", "service": "catalog", "latency_ms": 141.01, "uptime_pct": 97.172, "timestamp": 20250311},
    {"region": "amer", "service": "support", "latency_ms": 215.4, "uptime_pct": 98.978, "timestamp": 20250312},
]

def compute_p95(values):
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    rank = 0.95 * (n - 1)
    lower = int(rank)
    upper = lower + 1
    if upper >= n:
        return sorted_vals[-1]
    fraction = rank - lower
    return sorted_vals[lower] + fraction * (sorted_vals[upper] - sorted_vals[lower])

@app.options("/api/analytics")
async def options_analytics() -> Response:
    return Response(
        status_code=204,
        headers=CORS_HEADERS,
    )

@app.post("/api/analytics")
async def analytics_endpoint(request: Request) -> JSONResponse:
    body = await request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180.0)

    result: Dict[str, Dict[str, Any]] = {}

    for region in regions:
        records = [r for r in TELEMETRY_DATA if r.get("region") == region]
        if not records:
            result[region] = {
                "avg_latency": 0.0,
                "p95_latency": 0.0,
                "avg_uptime": 0.0,
                "breaches": 0,
            }
            continue

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]

        avg_latency = sum(latencies) / len(latencies)
        p95_latency = compute_p95(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)
        breaches = sum(1 for lat in latencies if lat > threshold_ms)

        result[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    response = JSONResponse(content=result, headers=CORS_HEADERS)
    return response
