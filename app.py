from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
import nltk
import re

app = Flask(__name__)

# LanguageTool setup

tool = language_tool_python.LanguageTool("en-US")


# Download/check NLTK tokenizer

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


# Semantic Similarity

def calculate_similarity(model_answer, student_answer):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        model_answer,
        student_answer
    ])

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(similarity * 100, 2)


# Split text into sentences

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
# Key Point Coverage

def calculate_coverage(model_answer, student_answer):

    model_points = split_into_sentences(model_answer)

    covered_points = []
    missing_points = []

    for point in model_points:

        vectorizer = TfidfVectorizer()

        try:

            vectors = vectorizer.fit_transform([
                point,
                student_answer
            ])

            similarity = cosine_similarity(
                vectors[0],
                vectors[1]
            )[0][0]

        except ValueError:

            similarity = 0

        if similarity >= 0.25:

            covered_points.append(point)

        else:

            missing_points.append(point)

    if len(model_points) == 0:

        coverage = 0

    else:

        coverage = (
            len(covered_points)
            / len(model_points)
        ) * 100

    return (
        round(coverage, 2),
        covered_points,
        missing_points
    )


# Grammar Score

def calculate_grammar_score(student_answer):

    if not student_answer.strip():
        return 0

    matches = tool.check(student_answer)

    words = len(student_answer.split())

    if words == 0:
        return 0

    errors = len(matches)

    # Grammar errors per 100 words
    error_rate = (errors / words) * 100

    # Convert error rate to score
    score = 100 - (error_rate * 5)

    # Keep score between 0 and 100
    score = max(
        0,
        min(100, score)
    )

    return round(score, 2)


# Clarity Score

def calculate_clarity_score(student_answer):

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
        len(words) / len(sentences)
    )

    score = 100

    # Penalize very long sentences

    if average_sentence_length > 30:

        score -= 30

    elif average_sentence_length > 25:

        score -= 20

    elif average_sentence_length > 20:

        score -= 10

    # Penalize extremely short answers

    if len(words) < 5:

        score -= 30

    return max(
        0,
        min(100, score)
    )


# Final Score

def calculate_final_score(
    similarity,
    coverage,
    grammar,
    clarity
):

    final_score = (

        similarity * 0.40

        + coverage * 0.30

        + grammar * 0.15

        + clarity * 0.15

    )

    return round(
        final_score,
        2
    )


# Feedback Generation

def generate_feedback(
    similarity,
    coverage,
    grammar,
    clarity,
    missing_points
):

    feedback = []


    # Similarity feedback

    if similarity >= 80:

        feedback.append(
            "Your answer is highly similar "
            "to the model answer."
        )

    elif similarity >= 60:

        feedback.append(
            "Your answer is reasonably similar "
            "to the model answer."
        )

    else:

        feedback.append(
            "Your answer differs significantly "
            "from the model answer."
        )


    # Coverage feedback

    if coverage >= 80:

        feedback.append(
            "You covered most of the "
            "important points."
        )

    elif coverage >= 50:

        feedback.append(
            "You covered some important points, "
            "but some concepts are missing."
        )

    else:

        feedback.append(
            "Several important points from "
            "the model answer are missing."
        )


    # Grammar feedback

    if grammar >= 80:

        feedback.append(
            "Your grammar is generally good."
        )

    elif grammar >= 60:

        feedback.append(
            "There are some grammar issues "
            "that should be corrected."
        )

    else:

        feedback.append(
            "Your answer contains significant "
            "grammar issues."
        )


    # Clarity feedback

    if clarity >= 80:

        feedback.append(
            "Your answer is clear and "
            "easy to understand."
        )

    elif clarity >= 60:

        feedback.append(
            "Your answer is understandable "
            "but could be clearer."
        )

    else:

        feedback.append(
            "Try using shorter and clearer "
            "sentences."
        )


    # Missing points

    if missing_points:

        feedback.append(
            "Important missing concepts: "
            + " ".join(missing_points)
        )


    return feedback


# Home Route

@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    score = None
    coverage = None
    grammar_score = None
    clarity_score = None
    final_score = None

    covered_points = []
    missing_points = []

    feedback = []


    # Handle form submission

    if request.method == "POST":

        model_answer = request.form.get(
            "model_answer",
            ""
        ).strip()

        student_answer = request.form.get(
            "student_answer",
            ""
        ).strip()

        # Calculate Similarity

        if model_answer and student_answer:

            score = calculate_similarity(
                model_answer,
                student_answer
            )


            # Calculate Coverage

            (
                coverage,
                covered_points,
                missing_points
            ) = calculate_coverage(
                model_answer,
                student_answer
            )


            # Calculate Grammar

            grammar_score = calculate_grammar_score(
                student_answer
            )


            # Calculate Clarity

            clarity_score = calculate_clarity_score(
                student_answer
            )


            # Calculate Final Score

            final_score = calculate_final_score(
                score,
                coverage,
                grammar_score,
                clarity_score
            )


            # Generate Feedback

            feedback = generate_feedback(
                score,
                coverage,
                grammar_score,
                clarity_score,
                missing_points
            )



    # Send results to HTML
    return render_template(

        "index.html",

        score=score,

        coverage=coverage,

        grammar_score=grammar_score,

        clarity_score=clarity_score,

        final_score=final_score,

        covered_points=covered_points,

        missing_points=missing_points,

        feedback=feedback

    )

# Run Flask
if __name__ == "__main__":

    app.run(
        debug=True
    )