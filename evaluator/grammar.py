import language_tool_python


tool = language_tool_python.LanguageTool(
    "en-US"
)


def calculate_grammar_score(
    student_answer
):

    if not student_answer.strip():

        return 0


    matches = tool.check(
        student_answer
    )

    words = len(
        student_answer.split()
    )


    if words == 0:

        return 0


    errors = len(matches)

    error_rate = (
        errors / words
    ) * 100


    score = (
        100 - (error_rate * 5)
    )


    return round(
        max(
            0,
            min(100, score)
        ),
        2
    )