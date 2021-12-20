import face_recognition


def face_embed(image, convert_to_rgb=False):
    if convert_to_rgb:
        image = image[:, :, ::-1]

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings
