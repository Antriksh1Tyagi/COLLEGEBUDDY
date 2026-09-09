import pandas as pd

from utils import (
    clean_text,
    tokenize_text,
    remove_stopwords,
    lemmatize_words,
    preprocess_text,
    load_faq_data,
    create_faq_vectors,
    find_best_match
)


# =========================================================
# PREPROCESSING TEST
# =========================================================

faq_data = pd.read_csv("data/faq.csv")


if "Question" not in faq_data.columns:
    raise ValueError(
        "Column 'Question' was not found in faq.csv"
    )


print("=" * 70)
print("COLLEGEBUDDY - NLP PREPROCESSING TEST")
print("=" * 70)


# Test five questions from the actual dataset
number_of_tests = min(5, len(faq_data))

for index in range(number_of_tests):

    question = faq_data.loc[index, "Question"]

    print("\n" + "-" * 70)
    print(f"FAQ {index + 1}")
    print("-" * 70)

    # Cleaning
    cleaned = clean_text(question)

    # Tokenization
    tokens = tokenize_text(cleaned)

    # Stopword removal
    filtered_tokens = remove_stopwords(tokens)

    # Lemmatization
    lemmatized = lemmatize_words(filtered_tokens)

    # Complete preprocessing
    processed = preprocess_text(question)

    print("Original Question:")
    print(question)

    print("\nAfter Cleaning:")
    print(cleaned)

    print("\nTokens:")
    print(tokens)

    print("\nAfter Stopword Removal:")
    print(filtered_tokens)

    print("\nAfter Lemmatization:")
    print(lemmatized)

    print("\nFinal Processed Text:")
    print(processed)


print("\n" + "=" * 70)
print("NLP PREPROCESSING VERIFICATION COMPLETED")
print("=" * 70)


# =========================================================
# RETRIEVAL TEST
# =========================================================

print("\n\n" + "=" * 70)
print("COLLEGEBUDDY - FAQ RETRIEVAL TEST")
print("=" * 70)


# Load FAQ data and generate TF-IDF vectors
load_faq_data("data/faq.csv")
create_faq_vectors()


print("\nTotal FAQs loaded:", len(faq_data))
print("TF-IDF FAQ vectors generated successfully.")


# Test questions
retrieval_questions = [
    "What percentage of attendance do students need?",
    "When will the odd semester theory examinations happen?",
    "How many IKS credits must I complete every year?",
    "Can I see my CGPA through Parakh?",
    "Do we have to submit our project on GitHub?"
]



for question in retrieval_questions:

    result = find_best_match(
        question,
        threshold=0.30
    )

    print("\n" + "-" * 70)
    print("User Question:", question)
    print("-" * 70)

    print("Matched Answer:", result["answer"])
    print("Category:", result["category"])
    print("Source:", result["source"])
    print(
        "Similarity Score:",
        round(result["similarity"], 4)
    )


print("\n" + "=" * 70)
print("FAQ RETRIEVAL VERIFICATION COMPLETED")
print("=" * 70)


# =========================================================
# LEMMATIZATION UNIT TEST
# =========================================================

def test_lemmatization_uses_verb_forms():

    tokens = [
        "does",
        "included",
        "running",
        "students"
    ]

    assert lemmatize_words(tokens) == [
        "do",
        "include",
        "run",
        "student"
    ]


if __name__ == "__main__":
    pass