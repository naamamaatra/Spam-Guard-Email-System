def classify_email(subject, body):
    text = f"{subject.lower()} {body.lower()}"

    spam_keywords = [
        
        "win", "prize", "lottery", "bitcoin", "claim now", "free offer",
        "click here", "buy now", "cheap deals", "investment opportunity",
        "limited offer", "miracle", "guaranteed income", "easy money",
        "free cash","free","gift"
    ]

    support_keywords = [
        "order", "refund", "payment", "billing", "support", "complaint",
        "delivery", "delay", "return", "cancel", "service issue",
        "damaged product", "warranty", "account problem", "subscription"
    ]

    sales_keywords = [
        "pricing", "quotation", "purchase", "buy", "discount", "sale",
        "offer", "deal", "product inquiry", "wholesale", "bulk order",
        "promotion", "inquiry", "sell", "bundle", "pricing details"
    ]

    tech_keywords = [
        "technical issue", "bug", "crash", "glitch", "error", "server down",
        "troubleshooting", "network issue", "login failed", "software issue",
        "system failure", "api error", "timeout error", "connectivity",
        "application issue", "unable to login"
    ]

    priority_keywords = {
        "high": ["urgent", "immediate", "asap", "critical", "important"],
        "medium": ["reminder", "follow up", "pending", "waiting for response"],
        "low": ["suggestion", "feedback", "query", "information"]
    }

    # Check for spam first
    for word in spam_keywords:
        if word in text:
            return "spam", "low"

    # Check Tech keywords
    for word in tech_keywords:
        if word in text:
            for level, key_list in priority_keywords.items():
                if any(k in text for k in key_list):
                    return "tech", level
            return "tech", "low"

    # Check Sales keywords
    for word in sales_keywords:
        if word in text:
            for level, key_list in priority_keywords.items():
                if any(k in text for k in key_list):
                    return "sales", level
            return "sales", "low"

    # Check Support keywords
    for word in support_keywords:
        if word in text:
            for level, key_list in priority_keywords.items():
                if any(k in text for k in key_list):
                    return "support", level
            return "support", "low"

    # Default fallback
    return "support", "low"
