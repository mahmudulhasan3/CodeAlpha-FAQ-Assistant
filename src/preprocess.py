import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def _ensure_nltk_data() -> None:
    """Download the NLTK resources we need, only if they are missing."""
    resources = {
        "punkt_tab": "tokenizers/punkt_tab",
        "stopwords": "corpora/stopwords",
        "wordnet": "corpora/wordnet",
    }
    for name, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


_ensure_nltk_data()

# "not" and "no" flip the meaning, so we always keep them.
NEGATION_WORDS = {"not", "no"}

# Question words help separate FAQs, so we keep them for ranking,
# but they must NOT count as evidence that a question is on-topic.
QUESTION_WORDS = {"how", "what", "when", "where", "who", "which"}

STOP_WORDS = set(stopwords.words("english")) - NEGATION_WORDS - QUESTION_WORDS
lemmatizer = WordNetLemmatizer()


def preprocess(text: str) -> list[str]:
    """Convert a raw question into a list of clean tokens."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # remove punctuation
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOP_WORDS]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens


def preprocess_text(text: str) -> str:
    """Same as preprocess() but returns one string (needed by TF-IDF)."""
    return " ".join(preprocess(text))


if __name__ == "__main__":
    print(preprocess("How can I Submit my TASK?"))
    print(preprocess("I did not receive my certificates!"))
    print(preprocess("What is Task 2?"))
