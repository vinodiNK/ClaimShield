# fraud_engine.py

def calculate_fraud_score(amount: float, description: str) -> float:
    score = 0

    # Rule 1: High claim amount
    if amount > 50000:
        score += 40
    elif amount > 20000:
        score += 20

    # Rule 2: Suspicious keywords
    suspicious_keywords = [
        "urgent payout",
        "immediately",
        "cash settlement",
        "lost documents"
    ]

    description_lower = description.lower()

    for keyword in suspicious_keywords:
        if keyword in description_lower:
            score += 15

    # Cap score at 100
    return min(score, 100)


def determine_status(score: float) -> str:
    if score >= 60:
        return "REJECTED"
    elif score >= 30:
        return "UNDER_REVIEW"
    else:
        return "APPROVED"