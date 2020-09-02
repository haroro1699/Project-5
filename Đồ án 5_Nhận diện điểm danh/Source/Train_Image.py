import os
import cv2
import numpy as np
from PIL import Image

# -------------- image labesl ------------------------
def getImagesAndLabels(path):
    # Lấy đường dẫn của toàn bộ file ở trong folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # Tạo danh sách faces và Ids rỗng
    faces = []
    Ids = []
    # Lặp qua tất cả đường dẫn hình ảnh đã lấy và load cái ID với bức ảnh đó 
    for imagePath in imagePaths:
        # load ảnh và convert ảnh đó qua gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Convert pilImage thành mảng numpy
        imageNp = np.array(pilImage, 'uint8')
        # Lấy Id từ ảnh
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # Trích xuất khuôn mặt từ ảnh training extract the face from the training image sample
        faces.append(imageNp) # dùng để thêm một phần tử vào vị trí cuối cùng của List hiện tại
        Ids.append(Id) # dùng để thêm một phần tử vào vị trí cuối cùng của List hiện tại
    return faces, Ids

# ----------- train images function ---------------
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create() # Tạo đối tượng nhận dạng recognizer
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    # Train recognizer
    recognizer.train(faces, np.array(Id))
    # Sắp xếp và lưu đối tượng recognizer vào file Trainner.yml
    recognizer.save("TrainingImageLabel"+os.sep+"Trainner.yml")
    print("Images Trained")
