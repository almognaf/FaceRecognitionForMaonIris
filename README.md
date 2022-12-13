# FaceRecognitionForMaonIris
a face detection script I've build to help my mom sorting all the images of her kindergarten's kids she collected amoung the year

explenation: Python script to run over uknown images, detecting faces by given images of people in known_faces sub-folder when each sub-folder's name representing the
name of the person, will sort all the images of the detected faces to a new or exist sub-folder under the name of the detected person.

imported packages:
os - iteratin over dir
shutil - copy images to another dir
face_detection - for detection
time - use timestamp to name every copied image with uniqe name to ensure we won't have the same name twice in one folder 
