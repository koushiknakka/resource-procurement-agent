import json
import os
from src.state import AgentState

def analyzer_node(state: AgentState) -> dict:
    target = state["target_product"]
    
    # 1. FETCH DYNAMIC WEIGHTS SENT FROM FASTAPI (With fallback defaults)
    w_quality = state.get("weight_quality", 0.4)
    w_delivery = state.get("weight_delivery", 0.3)
    w_cost = state.get("weight_price", 0.3)
    
    # Line 13: Standard 3-level directory jump using clean os.path calls
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Line 14: Standard os.path.join to connect to data.json
    data_path = os.path.join(base_dir, "datasets", "data.json")
    
    with open(data_path, 'r') as file:
        all_orders = json.load(file)
        
    eligible_orders = [
        orders for orders in all_orders
        if orders["product_ordered"].lower() == target.lower()
    ]
    
    if not eligible_orders:
        return {"eligible_orders": [], "ranked_results": []}
        
    # Creating dict of retailers and their orders from prev orders
    retailer_groups = {}
    for orders in eligible_orders:
        retailer_name = orders["name_of_the_retailer"]
        if retailer_name not in retailer_groups:
            retailer_groups[retailer_name] = []
        retailer_groups[retailer_name].append(orders)
        
    ranked_retailers = []
    
    for retailer_name, orders in retailer_groups.items():
        total_order = len(orders)
        
        contact = orders[0]["retailer_contact"]
        place = orders[0]["retailer_place"]
        moq = orders[0]["minimum_order_quantity_moq"]
        
        # avg quality score
        avg_quality = sum(o["product_quality"] for o in orders) / total_order
        quality_score = avg_quality * 20  # 5 rating to 100
        
        # avg delivery score
        total_delivery_points = 0
        for o in orders:
            days_late = o["target_delv_date_vs_actual_delv_date"]["days_delayed"]
            total_delivery_points += max(0, 100 - (days_late * 20))
            
        delivery_score = total_delivery_points / total_order
        
        # avg cost score
        total_unit_cost = 0
        for o in orders:
            unit_cost = o["product_cost"] / o["product_quantity"]
            total_unit_cost += unit_cost
        avg_unit_cost = total_unit_cost / total_order
        
        # higher cost -> lower cost score
        cost_score = max(10, 100 - (avg_unit_cost / 50))
        
        # DYNAMIC SCORE CALCULATION
        final_score = (quality_score * w_quality) + (delivery_score * w_delivery) + (cost_score * w_cost)
        
        ranked_retailers.append({
            "name": retailer_name,
            "contact": contact,
            "place": place,
            "moq": moq,
            "score": round(final_score, 1),
            "avg_quality": round(avg_quality, 1),
            "avg_unit_cost": round(avg_unit_cost, 2),
            "total_past_orders": total_order
        })
        
    ranked_retailers.sort(key=lambda x: x["score"], reverse=True)
    
    # FIX B: Returning state keys that match your LangGraph schema expectations
    return {"ranked_results": ranked_retailers, "eligible_orders": eligible_orders}
