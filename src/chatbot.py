from src.matcher import FAQMatcher

GREETINGS = {"hi", "hello", "hey", "salam", "assalamualaikum"}
THANKS = {"thanks", "thank you", "thx"}

CONFIDENCE_THRESHOLD = 0.35  # tune this with evaluate.py
FALLBACK_MESSAGE = (
    "Sorry, I am not sure about that. " "Here are some questions I can answer:"
)


class FAQChatbot:
    def __init__(self, threshold: float = CONFIDENCE_THRESHOLD):
        self.matcher = FAQMatcher()
        self.threshold = threshold

    def reply(self, user_input: str) -> dict:
        text = user_input.strip().lower()

        if not text:
            return {
                "answer": "Please type a question.",
                "fallback": True,
                "score": 0.0,
                "suggestions": [],
            }
        if text in GREETINGS:
            return {
                "answer": "Hello! Ask me anything about the CodeAlpha internship.",
                "fallback": False,
                "score": 1.0,
                "suggestions": [],
            }
        if text in THANKS:
            return {
                "answer": "You're welcome!",
                "fallback": False,
                "score": 1.0,
                "suggestions": [],
            }

        results = self.matcher.match(user_input, top_k=3)
        best_faq, best_score = results[0]

        if best_score < self.threshold:
            return {
                "answer": FALLBACK_MESSAGE,
                "fallback": True,
                "score": best_score,
                "suggestions": [faq["questions"][0] for faq, _ in results],
            }

        return {
            "answer": best_faq["answer"],
            "fallback": False,
            "score": best_score,
            "matched_question": best_faq["questions"][0],
            "category": best_faq["category"],
            "verified": best_faq.get("verified", False),
            "suggestions": [],
        }


if __name__ == "__main__":
    bot = FAQChatbot()
    print("CodeAlpha FAQ Bot (type 'quit' to exit)")
    while True:
        q = input("You: ")
        if q.lower() in {"quit", "exit"}:
            break
        r = bot.reply(q)
        print(f"Bot: {r['answer']}  (score={r['score']:.2f})")
        for s in r["suggestions"]:
            print(f"   - {s}")
