import yagmail
import os

receiver = "a1k49@gmail.com"
body = "Attendence File"
filename = "Attendance"+os.sep+"Attendance_2020-08-01_15-54-25.csv"

yag = yagmail.SMTP("a1k49@gmail.com", "pw123456")

yag.send(
    to=receiver,
    subject="Attendance Report",  
    contents=body,  
    attachments=filename,  
)
