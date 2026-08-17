import nltk
import re


try:

    nltk.data.find(
        "tokenizers/punkt"
    )

except LookupError:

    nltk.download("punkt")


def split_into_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def calculate_clarity_score(
    student_answer
):

    if not student_answer.strip():

        return 0


    try:

        sentences = nltk.sent_tokenize(
            student_answer
        )

    except LookupError:

        sentences = split_into_sentences(
            student_answer
        )


    if not sentences:

        return 0


    words = student_answer.split()


    if not words:

        return 0


    average_sentence_length = (
        len(words)
        / len(sentences)
    )


    score = 100


    if average_sentence_length > 30:

        score -= 30

    elif average_sentence_length > 25:

        score -= 20

    elif average_sentence_length > 20:

        score -= 10


    if len(words) < 5:

        score -= 30


    return max(
        0,
        min(100, score)
    )