from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
import re

app = Flask(__name__)

tool = language_tool_python.LanguageTool("en-US")


def calculate_similarity(model_answer, student_answer):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        model_answer,
        student_answer
    ])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(similarity * 100, 2)


def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def calculate_coverage(model_answer, student_answer):

    model_points = split_into_sentences(model_answer)

    covered_points = []
    missing_points = []

    for point in model_points:

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform([
            point,
            student_answer
        ])

        similarity = cosine_similarity(
            vectors[0],
            vectors[1]
        )[0][0]

        if similarity >= 0.25:
            covered_points.append(point)
        else:
            missing_points.append(point)

    if len(model_points) == 0:
        coverage = 0
    else:
        coverage = (
            len(covered_points) / len(model_points)
        ) * 100

    return (
        round(coverage, 2),
        covered_points,
        missing_points
    )


def calculate_grammar_score(student_answer):

    matches = tool.check(student_answer)

    words = len(student_answer.split())

    if words == 0:
        return 0

    errors = len(matches)

    # Error rate per 100 words
    error_rate = (errors / words) * 100

    # Convert error rate into a score
    score = 100 - (error_rate * 5)

    score = max(0, min(100, score))

    return round(score, 2)


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    coverage = None
    grammar_score = None

    covered_points = []
    missing_points = []

    if request.method == "POST":

        model_answer = request.form["model_answer"]
        student_answer = request.form["student_answer"]

        score = calculate_similarity(
            model_answer,
            student_answer
        )

        coverage, covered_points, missing_points = calculate_coverage(
            model_answer,
            student_answer
        )

        grammar_score = calculate_grammar_score(
            student_answer
        )

    return render_template(
        "index.html",
        score=score,
        coverage=coverage,
        grammar_score=grammar_score,
        covered_points=covered_points,
        missing_points=missing_points
    )


if __name__ == "__main__":
    app.run(debug=True)