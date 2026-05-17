# server.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# 4. Create the API Endpoint
@api_server.post("/api/procure/rank")
async def process_procurement_query(payload: QueryRequest):
    """
    Accepts a user request string, routes it through the LangGraph engine,
    and returns full analytics and markdown responses.
    """
    if not payload.user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty string.")
        
    try:
        # Packages the parameter into our known graph state dictionary
        inputs = {"user_query": payload.user_query}
        
        # Invoke the compiled graph synchronously 
        graph_output = app.invoke(inputs)
        
        # Return a clean production JSON response containing both structural arrays and markdown content
        return {
            "status": "success",
            "extracted_target": graph_output.get("target_product"),
            "requested_quantity": graph_output.get("approx_quantity"),
            "ranked_leaderboard": graph_output.get("ranked_results", []),
            "markdown_report": graph_output.get("final_output", "")
        }
        
    except Exception as e:
        # Ensure errors are safely reported back to the client interface
        raise HTTPException(status_code=500, detail=f"Graph Engine Error: {str(e)}")

# Fallback basic status path
@api_server.get("/health")
def health_check():
    return {"status": "healthy", "service": "procurement_agent_backend"}