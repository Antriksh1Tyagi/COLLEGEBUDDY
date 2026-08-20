import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



# NLTK SETUP


def setup_nltk():

#Download the NLTK resources required by the project.

    resources = [
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab")
    ]

    for path, resource in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(resource)


setup_nltk()



# NLP TOOLS

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()



# INPUT VALIDATION


def validate_input(text):
#Check whether the input is a valid text string.

    if text is None:
        return False

    if not isinstance(text, str):
        return False

    if not text.strip():
        return False

    return True



# TEXT CLEANING


def clean_text(text):


    """
    Clean the input text by:
    1- converting it to lowercase
    2- removing punctuation
    3- removing numbers
    4- removing extra spaces
    """

    if not validate_input(text):
        return ""

    text = text.lower()

    # Remove numbers, punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove unnecessary spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()



# TOKENIZATION


def tokenize_text(text):

#Convert text into individual words.

    if not text:
        return []

    return nltk.word_tokenize(text)



# STOPWORD REMOVAL


def remove_stopwords(tokens):

#Remove common English stopwords.

    if not tokens:
        return []

    return [
        word for word in tokens
        if word not in STOP_WORDS
    ]



# LEMMATIZATION


def lemmatize_words(tokens):

#Convert words into their base/dictionary form.

    if not tokens:
        return []

    return [
        LEMMATIZER.lemmatize(word)
        for word in tokens
    ]



# COMPLETE PREPROCESSING PIPELINE


def preprocess_text(text):

    """
    Complete NLP preprocessing pipeline.

    Processing steps:
    1. Input validation
    2. Text cleaning
    3. Tokenization
    4. Stopword removal
    5. Lemmatization

    Returns:
        A cleaned string ready for further NLP processing.
    """

    if not validate_input(text):
        return ""

    cleaned_text = clean_text(text)

    tokens = tokenize_text(cleaned_text)

    filtered_tokens = remove_stopwords(tokens)

    lemmatized_tokens = lemmatize_words(filtered_tokens)

    return " ".join(lemmatized_tokens)



# TESTING


if __name__ == "__main__":

    print("=" * 60)
    print("COLLEGEBUDDY - NLP PREPROCESSING")
    print("=" * 60)

    sample_questions = [
        "What are the Hostel Fees?",
        "What is the minimum attendance requirement?",
        "How can I apply for admission?",
        "Does the college provide library facilities?",
        "When will the semester examinations be conducted?"
    ]

    for question in sample_questions:

        processed_question = preprocess_text(question)

        print("\nOriginal  :", question)
        print("Processed :", processed_question)

    print("\n" + "=" * 60)
    print("Preprocessing test completed successfully.")
    print("=" * 60)