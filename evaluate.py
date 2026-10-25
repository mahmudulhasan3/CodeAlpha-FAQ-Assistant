from src.chatbot import FAQChatbot

# (question, expected FAQ id). None means the bot should refuse to answer.
TEST_SET = [
    ("how do i send my finished task", 22),
    ("what name should the repo have", 23),
    ("do i have to tag codealpha on linkedin", 24),
    ("must i record a video of my project", 25),
    ("how many tasks should i finish", 15),
    ("will i get a certificate if i only do 1 task", 16),
    ("which technologies can i use for the faq bot", 19),
    ("is a gui needed for the chatbot task", 20),
    ("is this an unpaid internship", 4),
    ("how do i reach support", 31),
    ("my certificate has not arrived", 30),
    ("is there job placement help", 14),
    ("can i get an lor", 13),
    ("what are the available fields", 8),
    ("how long does the internship run", 7),
    ("what is the deadline for submission", 26),
    ("what is codealpha", 1),
    ("i will be late with my submission", 28),
    ("what is the weather today", None),
    ("who won the football match", None),
]


def main() -> None:
    bot = FAQChatbot()
    top1 = top3 = fallback_ok = answerable = unanswerable = 0

    for question, expected in TEST_SET:
        results = bot.matcher.match(question, top_k=3)
        reply = bot.reply(question)
        ids = [faq["id"] for faq, _ in results]

        if expected is None:
            unanswerable += 1
            if reply["fallback"]:
                fallback_ok += 1
            else:
                print(f"[WRONG ANSWER on out-of-scope] {question}")
        else:
            answerable += 1
            if not reply["fallback"] and ids[0] == expected:
                top1 += 1
            else:
                print(
                    f"[MISS] {question} -> got {ids[0]} "
                    f"(score {results[0][1]:.2f}), expected {expected}"
                )
            if expected in ids:
                top3 += 1

    print(f"\nTop-1 accuracy : {top1}/{answerable} = {top1 / answerable:.0%}")
    print(f"Top-3 accuracy : {top3}/{answerable} = {top3 / answerable:.0%}")
    print(f"Correct refusal: {fallback_ok}/{unanswerable}")


if __name__ == "__main__":
    main()
