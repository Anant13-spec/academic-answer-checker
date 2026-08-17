import re

from sklearn.metrics.pairwise import cosine_similarity

from .similarity import model


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


def calculate_coverage(
    model_answer,
    student_answer
):

    model_points = split_into_sentences(
        model_answer
    )

    covered_points = []
    missing_points = []

    if not model_points:

        return (
            0,
            covered_points,
            missing_points
        )


    model_embeddings = model.encode(
        model_points
    )

    student_embedding = model.encode(
        [student_answer]
    )


    for index, point in enumerate(
        model_points
    ):

        point_embedding = (
            model_embeddings[index]
            .reshape(1, -1)
        )

        similarity = cosine_similarity(
            point_embedding,
            student_embedding
        )[0][0]


        if similarity >= 0.45:

            covered_points.append(point)

        else:

            missing_points.append(point)


    coverage = (
        len(covered_points)
        / len(model_points)
    ) * 100


    return (
        round(coverage, 2),
        covered_points,
        missing_points
    )