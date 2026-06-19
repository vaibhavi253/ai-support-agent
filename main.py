def detect_persona(message):
    msg = message.lower()

    if any(word in msg for word in ["api", "logs", "server", "token", "error", "config"]):
        return "Technical Expert"

    if any(word in msg for word in ["angry", "nothing works", "tried everything", "urgent", "not working"]):
        return "Frustrated User"

    if any(word in msg for word in ["impact", "business", "operations", "sla", "revenue", "timeline"]):
        return "Business Executive"

    return "Frustrated User"


def retrieve_knowledge(message):
    knowledge_base = {
        "password": "Password reset links expire after 15 minutes. Users should request a new reset link and check spam folder.",
        "api": "API authentication errors happen because of invalid tokens, expired API keys, or missing Authorization headers.",
        "billing": "Billing and refund issues must be escalated to the billing support team for manual verification.",
        "server": "Server downtime issues should be checked against the status page and escalated if service is unavailable.",
        "account": "Account lock issues require identity verification before manual unlock."
    }

    results = []
    for key, value in knowledge_base.items():
        if key in message.lower():
            results.append((key, value))

    return results


def generate_response(persona, message, docs):
    if not docs:
        return "I could not find enough information in the knowledge base. This should be escalated to a human support agent."

    content = docs[0][1]

    if persona == "Technical Expert":
        return f"Technical analysis: {content} Please verify logs, request headers, and configuration step by step."

    if persona == "Business Executive":
        return f"Business impact summary: {content} The issue should be reviewed based on operational impact and resolution priority."

    return f"I understand this is frustrating. {content} Please try this step first, and I will escalate if the issue continues."


def should_escalate(message, docs):
    msg = message.lower()

    if not docs:
        return True, "No relevant knowledge base content found"

    if any(word in msg for word in ["billing", "refund", "legal", "payment", "still not working"]):
        return True, "Sensitive or unresolved issue"

    return False, "No escalation required"


def create_handoff(persona, message, sources, reason):
    return {
        "persona": persona,
        "issue": message,
        "documents_used": sources,
        "actions_attempted": ["Persona detection", "Knowledge retrieval", "Response generation"],
        "recommendation": reason
    }


print("Persona-Adaptive Customer Support Agent")
print("Type 'exit' to stop\n")

while True:
    user_message = input("Customer: ")

    if user_message.lower() == "exit":
        break

    persona = detect_persona(user_message)
    docs = retrieve_knowledge(user_message)
    response = generate_response(persona, user_message, docs)
    escalate, reason = should_escalate(user_message, docs)

    print("\nDetected Persona:", persona)
    print("Retrieved Sources:", [doc[0] for doc in docs])
    print("Generated Response:", response)
    print("Escalation Status:", "Escalated" if escalate else "Not Escalated")

    if escalate:
        print("Human Handoff Summary:")
        print(create_handoff(persona, user_message, [doc[0] for doc in docs], reason))

    print("-" * 60)
