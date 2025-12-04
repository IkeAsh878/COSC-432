# Contains the extracted text from Lecture1.pptx
# Chunked so we can retrieve relevant pieces
#Data to take from Lecture1.pptx
LECTURE_CHUNKS = [
    # chunk 1
    """COSC 432 Requirements Engineering...
    Introduction, instructor info, agenda, definition of requirements...""",

    # chunk 2
    """What are requirements: functionality, constraints, technology-neutral,
    abstraction, behavior discovery...""",

    # chunk 3
    """Requirements vs Design: business need vs implementation, iterative loops...""",

    # chunk 4
    """Requirements gathering & system modeling, user models, overlapping artifacts...""",

    # chunk 5
    """Evolution of requirements, agile influence, adapting to change...""",

    # chunk 6
    """Functional requirements: examples, amended de-icing schedule...""",

    # chunk 7
    """Non-functional requirements: performance, usability, security, legal...""",

    # chunk 8
    """Constraints: global issues shaping requirements...""",

    # chunk 9
    """Class format, project goals, evaluation criteria..."""
]

import difflib
#how to retrieve relevant chunks based on a query
def retrieve_relevant_chunks(query, max_chunks=3):
    scores = []

    for chunk in LECTURE_CHUNKS:
        score = difflib.SequenceMatcher(None, query.lower(), chunk.lower()).ratio()
        scores.append((score, chunk))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [chunk for _, chunk in scores[:max_chunks]]
