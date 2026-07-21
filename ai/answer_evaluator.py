def evaluate_answer(question, answer):

    score = 0
    feedback = []

    if len(answer) > 30:
        score += 3
        feedback.append("✔ Answer has good length.")
    else:
        feedback.append("✘ Answer is too short.")

    keywords = [
        "python",
        "sql",
        "flask",
        "java",
        "database",
        "object",
        "class",
        "function"
    ]

    answer_lower = answer.lower()

    keyword_score = 0

    for word in keywords:
        if word in answer_lower:
            keyword_score += 1

    score += min(keyword_score, 7)

    if keyword_score >= 3:
        feedback.append("✔ Good technical keywords.")
    else:
        feedback.append("✘ Add more technical details.")

    return {
        "score": score,
        "feedback": feedback
    }