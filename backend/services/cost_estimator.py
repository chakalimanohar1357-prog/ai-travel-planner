"""Utility helpers for budget feasibility checks used by the trips route."""


def check_budget_feasibility(estimated_total, user_budget):
    if user_budget <= 0:
        return {"feasible": True, "message": "No budget cap set.", "difference": 0}

    difference = round(user_budget - estimated_total, 2)
    if difference >= 0:
        return {
            "feasible": True,
            "message": f"This plan fits your budget with ${difference} to spare.",
            "difference": difference,
        }
    return {
        "feasible": False,
        "message": f"This plan exceeds your budget by ${abs(difference)}. "
                    f"Consider a budget-tier hotel or shorter duration.",
        "difference": difference,
    }
