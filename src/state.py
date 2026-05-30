from typing import TypedDict, List, Optional

class AgentState(TypedDict):
  user_query : str
  target_product : str
  approx_quantity: Optional[int]
  eligible_records: List[dict]
  ranked_results: List[dict]
  final_output: str
  weight_price: float
  weight_delivery: float
  weight_quality: float