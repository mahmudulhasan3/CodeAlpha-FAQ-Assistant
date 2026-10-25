# CodeAlpha FAQ Assistant

A simple FAQ chatbot that answers questions about the **CodeAlpha internship** (tasks, submission, certificates and more). It uses NLP preprocessing and TF-IDF with cosine similarity to find the best matching FAQ.

🔗 **Live demo:** [codealpha-faq-assistant.streamlit.app](https://codealpha-faq-assistant.streamlit.app/)

## Features

- Matches a user's question to the closest FAQ using TF-IDF (unigrams + bigrams) and cosine similarity
- Each FAQ has multiple paraphrased questions, and the best-matching paraphrase decides the score
- Confidence threshold: if the match is weak, the bot says it is unsure and suggests related questions
- Out-of-scope guard: questions with no known content words are not forced into a wrong answer
- Handles greetings and thanks
- Chat UI built with Streamlit

## How it works

```
User question
      │
      ▼
 Preprocessing  (src/preprocess.py)
      │
      ▼
 TF-IDF vector  ──►  Cosine similarity with all FAQ paraphrases  (src/matcher.py)
      │
      ▼
 Best score ≥ threshold?
   ├── Yes → return the FAQ answer
   └── No  → fallback message + top 3 suggested questions  (src/chatbot.py)
```

## Project structure

```
CodeAlpha_FAQ_Assistant/
├── app.py              # Streamlit chat UI
├── evaluate.py         # Evaluation script, used to tune the confidence threshold
├── requirements.txt
├── .gitignore
├── data/
│   └── faqs.json       # FAQ questions, answers and categories
└── src/
    ├── __init__.py
    ├── chatbot.py      # Reply logic, greetings, fallback
    ├── matcher.py      # TF-IDF + cosine similarity matching
    └── preprocess.py   # Text cleaning and tokenization
```

## Run locally

```bash
# 1. Clone the repo
git clone https://github.com/mahmudul-hasan3/codealpha-faq-assistant.git
cd codealpha-faq-assistant

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py
```

To try the bot in the terminal instead:

```bash
python -m src.chatbot
```

## Customize

- **Add or edit FAQs:** change `data/faqs.json`. Add more paraphrases under `questions` to improve matching.
- **Tune strictness:** change `CONFIDENCE_THRESHOLD` in `src/chatbot.py` (default `0.35`). Higher means stricter matching, lower means more answers but more wrong matches.

## Tech stack

Python, Streamlit, scikit-learn, NLTK

## Author

**Mahmudul Hasan**: CSE student at NITER, Aspiring AI Engineer
- GitHub: [@mahmudul-hasan3](https://github.com/mahmudul-hasan3)
- LinkedIn: [mahmudulhasan03](https://www.linkedin.com/in/mahmudulhasan03/)

Built as part of the CodeAlpha internship (Task 2: FAQ Chatbot).