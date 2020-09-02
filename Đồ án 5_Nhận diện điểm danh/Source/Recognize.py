import datetime
import os
import time
import cv2
import pandas as pd # Thư viện pandas cho phépđọc/ ghi dữ liệu giữa bộ nhớ và nhiều định dạng file: csv, text, excel, sql database


def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create() 
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    # Đọc dữ liệu từ file StudentDetails
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    # Tạo đối tượng Camera
    cam = cv2.VideoCapture(0)
    # Phông chữ sans-serif kích thước bình thường
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Tạo dataframe mới cho file Attendance.csv
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            # Dự đoán, đối sánh đối tượng recognizer với ảnh nhận dạng được
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values #Truy cập hàng và cột trong dataframe df
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp] #Truy cập và lưu vào trong dataframe attendace

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown"+os.sep+"Image"+str(noOfFile) +
                            ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        # Bỏ những giá trị trùng lặp, coi Id đầu tiên là duy nhất, các Id có giá trị tương tự là trùng lặp
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    
    
    #-------------------Tên file Attendance csv-------------------------------
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()

    print("Attendance Successfull")
