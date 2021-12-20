import numpy as np
from FaceEmbeddings import face_embed
from ImageSizeEqualizer import image_equalize


def image_sim(imgA, imgB):
    _, face_embA = face_embed(imgA, True)
    feat_vecA = np.matrix(face_embA)

    _, face_embB = face_embed(imgB, True)
    feat_vecB = np.matrix(face_embB)

    try:
        return (1 - np.linalg.norm(feat_vecA - feat_vecB, ord=2, axis=1)[0]) * 100
    except ValueError:
        emb1, emb2 = image_equalize(feat_vecA, feat_vecB)
        return (1 - np.linalg.norm(emb1 - emb2, ord=2, axis=1)[0]) * 100
