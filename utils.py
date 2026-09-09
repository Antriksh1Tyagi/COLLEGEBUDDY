import re
import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# NLTK SETUP
# =========================================================

def setup_nltk():
    """Download the NLTK resources required by the project."""

    resources = [
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("taggers/averaged_perceptron_tagger_eng",
         "averaged_perceptron_tagger_eng")
    ]

    for path, resource in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass


setup_nltk()


# =========================================================
# NLP TOOLS
# =========================================================

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def _as_token_list(tokens):
    """Convert input into a token list."""

    if tokens is None:
        return []

    if isinstance(tokens, str):
        return tokenize_text(tokens)

    if isinstance(tokens, (list, tuple)):
        return list(tokens)

    return []


# =========================================================
# INPUT VALIDATION
# =========================================================

def validate_input(text):
    """Check whether the input is a valid text string."""

    if text is None:
        return False

    if not isinstance(text, str):
        return False

    if not text.strip():
        return False

    return True


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    """
    Clean the input text by:
    1. Converting it to lowercase
    2. Removing punctuation
    3. Keeping numbers
    4. Removing extra spaces
    """

    if not validate_input(text):
        return ""

    text = text.lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove unnecessary spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# TOKENIZATION
# =========================================================

def tokenize_text(text):
    """Convert text into individual words."""

    if not text:
        return []

    if not isinstance(text, str):
        return []

    return nltk.word_tokenize(text)


# =========================================================
# STOPWORD REMOVAL
# =========================================================

def remove_stopwords(tokens):
    """Remove common English stopwords."""

    tokens = _as_token_list(tokens)

    if not tokens:
        return []

    return [
        word for word in tokens
        if word.lower() not in STOP_WORDS
    ]


# =========================================================
# LEMMATIZATION
# =========================================================

def _wordnet_pos(tag):
    """Convert NLTK POS tags to WordNet POS tags."""

    if tag is None:
        return wn.NOUN

    if tag.startswith("J"):
        return wn.ADJ

    if tag.startswith("V"):
        return wn.VERB

    if tag.startswith("R"):
        return wn.ADV

    return wn.NOUN


def lemmatize_words(tokens):
    """Convert words into their base/dictionary form."""

    tokens = _as_token_list(tokens)

    if not tokens:
        return []

    tagged_tokens = pos_tag(tokens)

    lemmatized = []

    for word, tag in tagged_tokens:
        word_lower = word.lower()
        pos = _wordnet_pos(tag)

        lemmatized.append(
            LEMMATIZER.lemmatize(word_lower, pos=pos)
        )

    return lemmatized


# =========================================================
# COMPLETE PREPROCESSING PIPELINE
# =========================================================

def preprocess_text(text):
    """
    Complete NLP preprocessing pipeline.

    Processing steps:
    1. Input validation
    2. Text cleaning
    3. Tokenization
    4. Stopword removal
    5. POS-based lemmatization
    """

    if not validate_input(text):
        return ""

    cleaned_text = clean_text(text)

    tokens = tokenize_text(cleaned_text)

    filtered_tokens = remove_stopwords(tokens)

    lemmatized_tokens = lemmatize_words(filtered_tokens)

    return " ".join(lemmatized_tokens)


# =========================================================
# FAQ RETRIEVAL SETUP
# =========================================================

faq_data = None
tfidf_vectorizer = None
faq_vectors = None


def load_faq_data(file_path="data/faq.csv"):
    """
    Load the CollegeBuddy FAQ dataset.
    """

    global faq_data

    faq_data = pd.read_csv(file_path)

    required_columns = [
        "Question",
        "Answer",
        "Category",
        "Source"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in faq_data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    faq_data = faq_data.dropna(
        subset=["Question", "Answer"]
    ).reset_index(drop=True)

    return faq_data


# =========================================================
# TF-IDF VECTOR GENERATION
# =========================================================

def create_faq_vectors():
    """
    Preprocess FAQ questions and generate TF-IDF vectors.
    """

    global tfidf_vectorizer
    global faq_vectors

    if faq_data is None:
        load_faq_data()

    # Preprocess every FAQ question
    faq_data["Processed_Question"] = faq_data[
        "Question"
    ].apply(preprocess_text)

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(
        lowercase=False
    )

    # Generate vectors for FAQ questions
    faq_vectors = tfidf_vectorizer.fit_transform(
        faq_data["Processed_Question"]
    )

    return faq_vectors


# =========================================================
# BEST FAQ MATCH
# =========================================================

def find_best_match(question, threshold=0.30):
    """
    Find the most similar FAQ using TF-IDF and cosine similarity.

    Returns:
        answer
        category
        source
        similarity score
    """

    global faq_data
    global faq_vectors

    if not validate_input(question):
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": 0.0
        }

    # Load dataset if required
    if faq_data is None:
        load_faq_data()

    # Generate FAQ vectors if required
    if faq_vectors is None:
        create_faq_vectors()

    # Preprocess user question
    processed_question = preprocess_text(question)

    if not processed_question:
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": 0.0
        }

    # Convert user question into TF-IDF vector
    question_vector = tfidf_vectorizer.transform(
        [processed_question]
    )

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        question_vector,
        faq_vectors
    )[0]

    # Find highest similarity score
    best_index = similarity_scores.argmax()
    best_score = float(similarity_scores[best_index])

    # Check threshold
    if best_score < threshold:
        return {
            "answer": None,
            "category": None,
            "source": None,
            "similarity": best_score
        }

    best_faq = faq_data.iloc[best_index]

    return {
        "answer": best_faq["Answer"],
        "category": best_faq["Category"],
        "source": best_faq["Source"],
        "similarity": best_score
    }


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("COLLEGEBUDDY - NLP AND FAQ RETRIEVAL")
    print("=" * 60)

    sample_questions = [
        "What are the Hostel Fees?",
        "What is the minimum attendance requirement?",
        "How can I apply for admission?",
        "Does the college provide library facilities?",
        "When will the semester examinations be conducted?"
    ]

    print("\nPREPROCESSING TEST")
    print("-" * 60)

    for question in sample_questions:

        processed_question = preprocess_text(question)

        print("\nOriginal  :", question)
        print("Processed :", processed_question)

    print("\n" + "=" * 60)
    print("LOADING FAQ DATA")
    print("=" * 60)

    load_faq_data()
    create_faq_vectors()

    print("Total FAQs:", len(faq_data))
    print("FAQ vectors created successfully.")

    print("\n" + "=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    test_question = "What is the hostel fee?"

    result = find_best_match(test_question)

    print("\nQuestion:", test_question)
    print("Answer:", result["answer"])
    print("Category:", result["category"])
    print("Source:", result["source"])
    print("Similarity:", round(result["similarity"], 4))

    print("\n" + "=" * 60)
    print("NLP AND RETRIEVAL TEST COMPLETED")
    print("=" * 60)