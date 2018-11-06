import cv2, time, pandas
from datetime import datetime
video = cv2.VideoCapture(0)
first_frame = None
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=["Start","End"])
# in_time = []
# out_time=[]
# status = 0
value = 1
while True:
    ret,frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        # print("Pratyush")
        first_frame=gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame,40,255,cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta,None,iterations=2)
    # cv2.imshow("Gray_Capture",gray)
    (cnts,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # prev_status = status
    for contour in cnts:
        # if cv2.contourArea(contour) < 1000:
        #     #object is not there
        #     if value == 0:
        #         value=1
        #         out_time.append(datetime.now())
        #         print("The out time is ")
        #         print(datetime.now())
        #         print(value)
        #         print("121212")


        #     continue
        # elif value  == 1 and cv2.contourArea(contour) > 1000:    
        #     # status = 1  
        #     value = 0
        #     in_time.append(datetime.now())
        #     print("The in time is ")
        #     print(datetime.now())
        #     print(value)
        #     print("pofsdfdsfdsfdsfsdfsdfdsfdsfsdfdsfdsfds")
        # else:
        #     continue  
        #     print("pol")
        #     print(value)    
        if cv2.contourArea(contour) < 2000:
            continue
        status=1    



    # if status == 1    

        (x,y,w,h) = cv2.boundingRect(contour)    
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)
    
    if status_list[len(status_list)-1]==1 and status_list[len(status_list)-2]==0:
        times.append(datetime.now())
        print("object appeared")
    elif status_list[len(status_list)-1]==0 and status_list[len(status_list)-2]==1:
        times.append(datetime.now())
        print("object dissapeared")        

    cv2.imshow("Capturing",thresh_delta)
    cv2.imshow("Object_detection",frame)
    # print(delta_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    # print(status)    


print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)



df.to_csv("Times.csv")

video.release()        
cv2.destroyAllWindows()        
        