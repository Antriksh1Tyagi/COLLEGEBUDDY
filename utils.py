import re
import nltk
import pandas as pd
from pathlib import Path
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- NLTK SETUP ----------------
def setup_nltk():
    resources = [
        ("corpora/stopwords","stopwords"),
        ("corpora/wordnet","wordnet"),
        ("tokenizers/punkt","punkt"),
        ("tokenizers/punkt_tab","punkt_tab"),
        ("taggers/averaged_perceptron_tagger_eng","averaged_perceptron_tagger_eng"),
    ]
    for path,res in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try: nltk.download(res, quiet=True)
            except: pass

setup_nltk()
STOP_WORDS=set(stopwords.words("english"))
LEMMATIZER=WordNetLemmatizer()

# ---------------- PREPROCESS ----------------
def validate_input(text):
    return isinstance(text,str) and text.strip()

def clean_text(text):
    if not validate_input(text): return ""
    text=text.lower()
    text=re.sub(r"[^a-zA-Z0-9\s]"," ",text)
    return re.sub(r"\s+"," ",text).strip()

def tokenize_text(text):
    return nltk.word_tokenize(text) if text else []

def remove_stopwords(tokens):
    return [t for t in tokens if t.lower() not in STOP_WORDS]

def _wn(tag):
    if tag.startswith("J"): return wn.ADJ
    if tag.startswith("V"): return wn.VERB
    if tag.startswith("R"): return wn.ADV
    return wn.NOUN

def preprocess_text(text):
    if not validate_input(text): return ""
    tokens=tokenize_text(clean_text(text))
    tokens=remove_stopwords(tokens)
    tagged=pos_tag(tokens)
    return " ".join(LEMMATIZER.lemmatize(w.lower(),_wn(t)) for w,t in tagged)

# ---------------- FAQ RETRIEVAL ----------------
faq_data=None
tfidf_vectorizer=None
faq_vectors=None

def load_faq_data(file_path=None):
    global faq_data
    if file_path is None:
        data_dir=Path("data")
        if (data_dir/"faqs.csv").exists():
            file_path=data_dir/"faqs.csv"
        else:
            files=list(data_dir.glob("*.csv"))
            if not files:
                raise FileNotFoundError("No CSV found in data folder.")
            file_path=max(files,key=lambda p:p.stat().st_size)
    faq_data=pd.read_csv(file_path)
    for col in ["Question","Answer","Category","Source"]:
        if col not in faq_data.columns:
            raise ValueError(f"Missing column: {col}")
    faq_data["Keywords"]=faq_data.get("Keywords","").fillna("")
    return faq_data

def create_faq_vectors():
    global tfidf_vectorizer,faq_vectors,faq_data

    if faq_data is None:
        load_faq_data()

    # faq_data["Search_Text"]=faq_data["Question"].fillna("")+" "+faq_data["Keywords"]
    faq_data["Search_Text"] = (
        faq_data["Question"].fillna("") + " "
        + faq_data["Keywords"].fillna("") + " "
        + faq_data["Category"].fillna("")
        )

    faq_data["Processed_Question"]=faq_data["Search_Text"].apply(preprocess_text)
    tfidf_vectorizer=TfidfVectorizer(lowercase=False)
    faq_vectors=tfidf_vectorizer.fit_transform(faq_data["Processed_Question"])
    return faq_vectors

def find_best_match(question, threshold=0.60, top_k=3):
    global faq_data, faq_vectors, tfidf_vectorizer

    if not validate_input(question):
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": 0.0,
            "candidates": []
        }

    if faq_data is None:
        load_faq_data()

    if faq_vectors is None:
        create_faq_vectors()

    processed = preprocess_text(question)

    if not processed:
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": 0.0,
            "candidates": []
        }

    query_vector = tfidf_vectorizer.transform([processed])
    scores = cosine_similarity(query_vector, faq_vectors)[0]

    # ---------- Keyword Boost ----------
    query_words = set(processed.split())

    for i, row in faq_data.iterrows():
        keywords = preprocess_text(str(row.get("Keywords", "")))
        keyword_set = set(keywords.split())

        overlap = len(query_words & keyword_set)

        if overlap:
            scores[i] += overlap * 0.08

    # ---------- Top K ----------
    top_indices = scores.argsort()[::-1][:top_k]

    candidates = []

    for idx in top_indices:
        row = faq_data.iloc[idx]
        candidates.append({
            "question": row["Question"],
            "answer": row["Answer"],
            "category": row["Category"],
            "source": row["Source"],
            "similarity": float(scores[idx])
        })

    best = candidates[0]

    if best["similarity"] < threshold:
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": best["similarity"],
            "candidates": candidates
        }

    return {
        "answer": best["answer"],
        "category": best["category"],
        "source": best["source"],
        "similarity": best["similarity"],
        "candidates": candidates
    }

if __name__=="__main__":
    load_faq_data()
    create_faq_vectors()
    print(find_best_match("What is hostel fee?"))
