# server.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import the compiled LangGraph app from your main.py file
from main import app

# 1. Initialize FastAPI application
api_server = FastAPI(
    title="College Procurement Agentic Service",
    description="Production-grade backend endpoint wrapping our LangGraph analytics workflow."
)

# 2. Configure CORS (Critical for Antigravity Frontend Hookup)
# This allows your frontend web application to make requests to localhost without being blocked
api_server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, swap with your specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the Incoming Request Body Structure
class QueryRequest(BaseModel):
    user_query: str
    weight_price: float = Field(default=0.33, description="Weight factor for price priority (0.0 to 1.0)")
    weight_delivery: float = Field(default=0.33, description="Weight factor for speed priority (0.0 to 1.0)")
    weight_quality: float = Field(default=0.34, description="Weight factor for vendor score priority (0.0 to 1.0)")

# 4. Create the API Endpoint
# server.py
@api_server.post("/api/procure/rank")
async def process_procurement_query(payload: QueryRequest):
    if not payload.user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty string.")
        
    try:
        # Initialize the state payload with complete base keys
        # This prevents any KeyError down the line inside Node 2 or Node 3
        inputs = {
            "user_query": payload.user_query,
            "weight_price": payload.weight_price,
            "weight_delivery": payload.weight_delivery,
            "weight_quality": payload.weight_quality,
            "target_product": "Unknown",
            "approx_quantity": None,
            "eligible_records": [],
            "ranked_results": [],
            "final_output": ""
        }
        
        print(f"\n📥 [API RECEIVE] Processing query: '{payload.user_query}'")
        
        # Invoke the graph engine directly
        graph_output = app.invoke(inputs)
        
        print(f"📤 [API SUCCESS] Graph executed successfully for: '{graph_output.get('target_product')}'")
        
        return {
            "status": "success",
            "extracted_target": graph_output.get("target_product"),
            "requested_quantity": graph_output.get("approx_quantity"),
            "ranked_leaderboard": graph_output.get("ranked_results", []),
            "markdown_report": graph_output.get("final_output", "")
        }
        
    except Exception as e:
        # CRITICAL: This line forces the inner trace log to show up in your uvicorn console window!
        import traceback
        print("\n❌ !!! [GRAPH EXECUTION CRASH DETECTED] !!! ❌")
        traceback.print_exc() 
        print("===============================================\n")
        
        raise HTTPException(status_code=500, detail=f"Internal Graph Engine Error: {str(e)}")

# Fallback basic status path
@api_server.get("/health")
def health_check():
    return {"status": "healthy", "service": "procurement_agent_backend"}