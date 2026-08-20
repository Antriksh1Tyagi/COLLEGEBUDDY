import pandas as pd

from utils import (
    clean_text,
    tokenize_text,
    remove_stopwords,
    lemmatize_words,
    preprocess_text
)


# Load the actual CollegeBuddy FAQ dataset

faq_data = pd.read_csv("data/faq.csv")


# Check that the required column exists

if "Question" not in faq_data.columns:
    raise ValueError("Column 'Question' was not found in faq.csv")


print("=" * 70)
print("COLLEGEBUDDY - NLP PREPROCESSING TEST")
print("=" * 70)


# Test a few questions from the actual dataset

number_of_tests = min(5, len(faq_data))

for index in range(number_of_tests):

    question = faq_data.loc[index, "Question"]

    print("\n" + "-" * 70)
    print(f"FAQ {index + 1}")
    print("-" * 70)

    # Step 1: Cleaning

    cleaned = clean_text(question)

    # Step 2: Tokenization

    tokens = tokenize_text(cleaned)

    # Step 3: Stopword removal

    filtered_tokens = remove_stopwords(tokens)

    # Step 4: Lemmatization

    lemmatized = lemmatize_words(filtered_tokens)

    # Step 5: Final processed text
    
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