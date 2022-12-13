import shutil
import face_recognition
import os
import time

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
SAVE_IMAGE_AT = 'images_sorted'
TOLERANCE = 0.5
MODEL = 'cnn'


def run():
    print('Loading known faces...')
    known_faces = []
    known_names = []

    # We organize known faces from  sub-folders of KNOWN_FACES_DIR
    # Each sub-folder's name in KNOWN_FACES_DIR becomes our label (name)
    for name in os.listdir(KNOWN_FACES_DIR):
        #  make sub-folder for each child only if it's not already exist
        if not os.path.exists(f'{SAVE_IMAGE_AT}/{name}'):
            os.makedirs(f'{SAVE_IMAGE_AT}/{name}')

        # Next we load every file of faces of known person
        for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
            # Load an image
            image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
            # Get a list of found faces, for this purpose we take first face only because you can't be twice in the
            # same image
            encoding = face_recognition.face_encodings(image)[0]
            # Append encodings and name
            known_faces.append(encoding)
            known_names.append(name)

    print('Processing unknown faces...')
    # Now let's loop over a folder of faces we want to label
    for filename in os.listdir(UNKNOWN_FACES_DIR):

        # Load image
        print(f'Filename {filename}', end='')
        image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')

        # This time we first grab face locations - we'll need them to draw boxes
        locations = face_recognition.face_locations(image, model=MODEL)

        # Now since we know the locations, we can pass them to face_encodings as second argument
        # Without that it will search for faces once again and slow down the whole process
        encodings = face_recognition.face_encodings(image, locations)

        # But this time we assume that there might be more faces in an image - we can find faces of different people
        print(f', found {len(encodings)} face(s)')
        for face_encoding, face_location in zip(encodings, locations):

            # We use compare_faces (but might use face_distance as well)
            # Returns array of True/False values in order of passed known_faces
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            # Since order is being preserved, we check if any face was found then grab index
            # then label (name) of first matching known face withing a tolerance
            match = None
            if True in results:  # If at least one is true, get a name of first of found labels
                timestamp = time.time()
                match = known_names[results.index(True)]
                print(f'{filename} belongs to {match}')
                shutil.copyfile(fr'{UNKNOWN_FACES_DIR}\{filename}', fr'{SAVE_IMAGE_AT}\{match}\{timestamp}.jpg')


if __name__ == '__main__':
    run()
