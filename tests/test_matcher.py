import numpy as np

from app.vision.matcher import find_best_match


def test_matching():
    embedding = np.ones(128, dtype=np.float32)

    candidates = [
        (1, np.ones(128, dtype=np.float32)),
        (2, np.zeros(128, dtype=np.float32)),
    ]

    participant_id, distance = find_best_match(
        embedding,
        candidates,
        threshold=1.0,
    )

    assert participant_id == 1
    assert distance == 0.0