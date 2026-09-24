import cv2
import numpy as np


def distance(a, b):
    a = np.asarray(a, dtype=np.float32).reshape(1, -1)
    b = np.asarray(b, dtype=np.float32).reshape(1, -1)
    return float(cv2.norm(a, b, cv2.NORM_L2))


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32).reshape(1, -1)
    b = np.asarray(b, dtype=np.float32).reshape(1, -1)

    a = cv2.normalize(a, None)
    b = cv2.normalize(b, None)

    return float((a @ b.T).item())


def find_best_match(embedding, candidates, threshold=0.363):
    best_id = None
    best_score = -1.0

    for participant_id, stored_embedding in candidates:
        score = cosine_similarity(embedding, stored_embedding)

        if score > best_score:
            best_score = score
            best_id = participant_id

    if best_score >= threshold:
        return best_id, best_score

    return None, best_score