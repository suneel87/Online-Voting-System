import cv2


def image_equalize(imgA, imgB):

    new_size = max(imgA.shape, imgB.shape)

    new_imgA = cv2.resize(imgA, new_size)
    new_imgB = cv2.resize(imgB, new_size)

    return new_imgA, new_imgB
