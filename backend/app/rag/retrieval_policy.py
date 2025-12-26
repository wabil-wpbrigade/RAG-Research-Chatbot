def determine_top_k(intent: str, complexity: str) -> int:
    """
    Decide retrieval depth based on query characteristics.
    """

    if intent == "factual":
        return 3 if complexity == "low" else 4

    if intent == "procedural":
        return 5

    if intent == "conceptual":
        if complexity == "high":
            return 8
        return 6

    # exploratory or fallback
    return 8
