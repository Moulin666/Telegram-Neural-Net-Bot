import datetime
import face_recognition

from PIL import Image

def GetFaces(img):
    image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(image, model="cnn")
    
    result = []
    i = 0

    for face_location in face_locations:
        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        with open('data/recognized/face_{}_{}.jpg'.format(i, datetime.datetime.now().isoformat()), 'w') as resImage:
            pil_image.save(resImage)

        result.append(resImage)

        i = i + 1

    return result
