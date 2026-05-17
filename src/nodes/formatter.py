from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
from src.state import AgentState

def formatter_node(state : AgentState)->dict:
  target = state["target_product"]
  rankings = state["ranked_results"]
  requested_qty = state.get("approx_quantity")

  if not rankings:
    return {
      "final_output" : f"---NO HISTORICAL ORDERS FOUND---"

    }
  
  llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash",temperature = 0.3)

  data_summary = ""
  for idx, v in enumerate(rankings, 1):
    data_summary+=(
      f"Rank {idx}: {v['name']} (Score: {v['score']}/100)\n"
            f"- Contact: {v['contact']} | Location: {v['place']}\n"
            f"- Avg Quality: {v['avg_quality']}/5 | Avg Unit Cost: Rs. {v['avg_unit_cost']}\n"
            f"- Total Past Successful Orders: {v['total_past_orders']} | Vendor MOQ: {v['moq']}\n\n"
    )
  
  system_prompt = (
    "You are an expert college procurement intelligence agent.\n"
    "Your task is to take the provided mathematical vendor rankings and generate a professional, "
    "crisp summary report in Markdown format.\n\n"
    "Guidelines for the report:\n"
    "1. Highlight the clear #1 recommended vendor and explicitly mention *why* they won based on the metrics (e.g., fast delivery, cost efficiency, or top-tier quality).\n"
    "2. Provide a brief overview comparing the other alternative vendors.\n"
    "3. Keep the tone professional, helpful, and organized with clear bullet points.\n"
    "4. Emphasize key details like contact emails or specific costs using bold text."
  )

  user_message = (
    f"Item Requested: {target}\n"
    f"Requested Quantity: {requested_qty if requested_qty else 'Not specified'}\n\n"
    f"Calculated Vendor Rankings Context Data:\n{data_summary}"
  )

  response = llm.invoke([
    ("system", system_prompt),
    ("user", user_message)
  ])

  return {"final_output" : response.content}