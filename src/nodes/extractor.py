import os
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from src.state import AgentState

def extraction_node(state : AgentState)->dict:
  llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
  system_prompt = (
        "You are a college procurement assistant. Look at the user's query and extract two details:\n"
        "1. The product category. It must match exactly one of these items: "
        "['Ceiling Fan', 'Digital Oscilloscope', 'LED Tube Light', 'Split AC']. If it's something else, write 'Unknown'.\n"
        "2. The quantity requested as an integer number. If no number is mentioned, write 'None'.\n\n"
        "Your output must strictly follow this text format:\n"
        "PRODUCT: <product name>\n"
        "QUANTITY: <number or None>"
    )
  
  user_message = f"user request : '{state["user_query"]}'"

  response=llm.invoke([
    ('system', system_prompt),
    ('user', user_message)
  ])

  response_text = response.content.strip()

  extracted_product = "unknown"
  extracted_quantity = None

  for line in response_text.split('\n'):
    if line.startswith("PRODUCT:"):
      extracted_product = line.replace("PRODUCT:", "").strip()
    elif line.startswith("QUANTITY:"):
      qty_str = line.replace("QUANTITY:", "").strip()
      if qty_str != "None" and qty_str.isdigit():
        extracted_qty = int(qty_str)

  return {
    "target_product": extracted_product,
    "approx_quantity": extracted_qty
  }