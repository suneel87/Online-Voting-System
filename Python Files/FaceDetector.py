import cv2


def detect_face(path):
    face_cascade = cv2.CascadeClassifier('face_detection.xml')
    img = cv2.imread(path)
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    x, y, w, h = faces[0]

    crop_img = img[y:y + h, x:x + w]
    return crop_img

