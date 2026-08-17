def generate_feedback(
    similarity,
    coverage,
    grammar,
    clarity,
    missing_points
):

    feedback = []


    if similarity >= 80:

        feedback.append(
            "Your answer is highly "
            "similar in meaning to "
            "the model answer."
        )

    elif similarity >= 60:

        feedback.append(
            "Your answer is reasonably "
            "similar in meaning to "
            "the model answer."
        )

    else:

        feedback.append(
            "Your answer differs "
            "significantly from the "
            "model answer."
        )


    if coverage >= 80:

        feedback.append(
            "You covered most of "
            "the important concepts."
        )

    elif coverage >= 50:

        feedback.append(
            "You covered some important "
            "concepts, but several "
            "points could be added."
        )

    else:

        feedback.append(
            "Several important concepts "
            "from the model answer "
            "are missing."
        )


    if grammar >= 80:

        feedback.append(
            "Your grammar is generally good."
        )

    elif grammar >= 60:

        feedback.append(
            "There are some grammar "
            "issues that should be corrected."
        )

    else:

        feedback.append(
            "Your answer contains "
            "significant grammar issues."
        )


    if clarity >= 80:

        feedback.append(
            "Your answer is clear "
            "and easy to understand."
        )

    elif clarity >= 60:

        feedback.append(
            "Your answer is understandable "
            "but could be clearer."
        )

    else:

        feedback.append(
            "Try using shorter and "
            "clearer sentences."
        )


    if missing_points:

        feedback.append(
            "Important missing concepts: "
            + " ".join(
                missing_points
            )
        )


    return feedback