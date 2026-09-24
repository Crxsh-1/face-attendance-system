import numpy as np

from app.vision.matcher import cosine_similarity, find_best_match


def test_cosine_similarity():
    a = np.ones(128, dtype=np.float32)
    b = np.ones(128, dtype=np.float32)

    score = cosine_similarity(a, b)

    assert score > 0.99


def test_matching():
    embedding = np.ones(128, dtype=np.float32)

    candidates = [
        (1, np.ones(128, dtype=np.float32)),
        (2, -np.ones(128, dtype=np.float32)),
    ]

    participant_id, similarity = find_best_match(
        embedding,
        candidates,
        threshold=0.5,
    )

    assert participant_id == 1
    assert similarity > 0.99


def test_unknown_face():
    embedding = np.ones(128, dtype=np.float32)

    candidates = [
        (1, -np.ones(128, dtype=np.float32)),
    ]

    participant_id, similarity = find_best_match(
        embedding,
        candidates,
        threshold=0.5,
    )

    assert participant_id is None
    assert similarity < 0.5