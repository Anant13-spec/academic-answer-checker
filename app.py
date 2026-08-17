from flask import Flask, render_template, request

from evaluator.similarity import calculate_similarity
from evaluator.coverage import calculate_coverage
from evaluator.grammar import calculate_grammar_score
from evaluator.clarity import calculate_clarity_score
from evaluator.scoring import calculate_final_score
from evaluator.feedback import generate_feedback


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    coverage = None
    grammar_score = None
    clarity_score = None
    final_score = None

    covered_points = []
    missing_points = []

    feedback = []


    if request.method == "POST":

        model_answer = request.form.get(
            "model_answer",
            ""
        ).strip()

        student_answer = request.form.get(
            "student_answer",
            ""
        ).strip()


        if model_answer and student_answer:

            score = calculate_similarity(
                model_answer,
                student_answer
            )


            (
                coverage,
                covered_points,
                missing_points
            ) = calculate_coverage(
                model_answer,
                student_answer
            )


            grammar_score = (
                calculate_grammar_score(
                    student_answer
                )
            )


            clarity_score = (
                calculate_clarity_score(
                    student_answer
                )
            )


            final_score = (
                calculate_final_score(
                    score,
                    coverage,
                    grammar_score,
                    clarity_score
                )
            )


            feedback = generate_feedback(
                score,
                coverage,
                grammar_score,
                clarity_score,
                missing_points
            )


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


if __name__ == "__main__":

    app.run(
        debug=True
    )