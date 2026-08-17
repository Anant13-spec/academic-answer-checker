from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(model_answer, student_answer):

    model_embedding = model.encode(
        [model_answer]
    )

    student_embedding = model.encode(
        [student_answer]
    )

    similarity = cosine_similarity(
        model_embedding,
        student_embedding
    )[0][0]

    return round(
        similarity * 100,
        2
    )