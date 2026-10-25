import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocess import QUESTION_WORDS, preprocess, preprocess_text

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "faqs.json"


class FAQMatcher:
    def __init__(self, faq_path: Path = DEFAULT_PATH):
        with open(faq_path, encoding="utf-8") as f:
            self.faqs = json.load(f)

        # Every paraphrase becomes its own document.
        # owner[i] tells us which FAQ the i-th document belongs to.
        documents, self.owner = [], []
        for idx, faq in enumerate(self.faqs):
            for question in faq["questions"]:
                documents.append(preprocess_text(question))
                self.owner.append(idx)

        # The custom token_pattern keeps one-character tokens such as "2".
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b"
        )
        self.matrix = self.vectorizer.fit_transform(documents)

    def _is_on_topic(self, query: str) -> bool:
        """True if at least one content word (not a question word) is known."""
        vocab = self.vectorizer.vocabulary_
        content = [t for t in preprocess(query) if t not in QUESTION_WORDS]
        return any(token in vocab for token in content)

    def match(self, query: str, top_k: int = 3) -> list[tuple[dict, float]]:
        """Return the top_k (faq, score) pairs, best first."""
        # Out-of-scope guard: no known content word means no real match.
        if not self._is_on_topic(query):
            return [(faq, 0.0) for faq in self.faqs[:top_k]]

        query_vec = self.vectorizer.transform([preprocess_text(query)])
        scores = cosine_similarity(query_vec, self.matrix).ravel()

        # A FAQ's score is the best score among its paraphrases.
        best = {}
        for doc_idx, score in enumerate(scores):
            faq_idx = self.owner[doc_idx]
            if score > best.get(faq_idx, 0.0):
                best[faq_idx] = float(score)

        ranked = sorted(best.items(), key=lambda x: x[1], reverse=True)
        return [(self.faqs[i], s) for i, s in ranked[:top_k]]
