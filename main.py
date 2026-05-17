import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END, START

from src.state import AgentState
from src.nodes.extractor import extraction_node
from src.nodes.analyzer import analyzer_node
from src.nodes.formatter import formatter_node
    
graph_builder = StateGraph(AgentState)
graph_builder.add_node("extraction_node", extraction_node)
graph_builder.add_node("analyzer_node", analyzer_node)
graph_builder.add_node("formatter_node", formatter_node)

graph_builder.set_entry_point("extraction_node")
graph_builder.add_edge("extraction_node","analyzer_node")
graph_builder.add_edge("analyzer_node", "formatter_node")
graph_builder.add_edge("formatter_node", END)

app = graph_builder.compile()

if __name__ == "__main__":
    inputs = {
        "user_query": "The EEE power systems lab needs to replace some old burned out light blocks. Let's get around 60 new LED tube lights. Check the ranks."
    }
    
    print("🚀 Starting LangGraph Agentic Pipeline Execution...\n")
    
    for output in app.stream(inputs):
        for node_name, state_updates in output.items():
            print(f"✔️ Completed execution step: [{node_name}]")
            
            # Print localized insights to see exactly what changed inside the state dictionary
            if "target_product" in state_updates:
                print(f"   -> Extracted Target: '{state_updates['target_product']}'")
            if "ranked_results" in state_updates:
                print(f"   -> Ranked Leaderboard Size: {len(state_updates['ranked_results'])} vendors calculated.")

    print("\n=======================================================")
    print("               FINAL GRAPH GENERATED REPORT            ")
    print("=======================================================\n")
    
    # Fetch the final complete state dump after reaching the END node
    final_output = app.invoke(inputs)
    
    # If using basic state invocation check or direct retrieval fallback
    # The simplest way to grab the end state from a standard stream is tracking it or pulling directly:
    print(final_output["final_output"])