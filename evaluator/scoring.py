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