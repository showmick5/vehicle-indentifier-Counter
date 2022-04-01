import cv2
import numpy as np


# Web camera
cap = cv2.VideoCapture('video.mp4')

min_width_react = 88  # min width reactangle
min_hight_react = 88  # min width reactangle

count_line_position = 550
# Initialize Substructor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()


def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy


detect = []
offset = 6  # Allowable error between pixel
total_counter = 0
Heavy_vechicle =0
Honda=0
car=0
van_count=0

while True:
    ret, frame1 = cap.read()
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    counterSahpe, h = cv2.findContours(
        dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, count_line_position),
             (1200, count_line_position), (255, 127, 0), 3)

    for(i, c) in enumerate(counterSahpe):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_react) and (h >= min_hight_react)
        if not validate_counter:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
          
        if x>850:
             van_count+=1
             cv2.putText(frame1, "van"+str(Heavy_vechicle), (x, y-20),
               cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)
        elif x*y >200*65 and x*y<=250*70:
            cv2.putText(frame1, "Honda"+str(Honda), (x, y-20),
               cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)
        else:
            
            cv2.putText(frame1, "car"+str(car), (x, y-20),
               cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)       
        
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

        for (x, y) in detect:
            
            if y < (count_line_position+offset) and y > (count_line_position-offset):

                total_counter += 1
                cv2.line(frame1, (25, count_line_position),
                        (1200, count_line_position), (0, 127, 255), 3)
                 
                if x> 950 :
                    Heavy_vechicle+=1
                          
                
                elif x>250 :
                    car+=1 
                else:
                    Honda+=1                
                detect.remove((x, y))
                print("Vehicle Counter:"+str(total_counter))
                print("Heavy_vechicle_count:"+str(Heavy_vechicle))
                print("Honda_counter:"+str(Honda))
                print("car_count"+str(car))

    cv2.putText(frame1, "Total VEHICLE COUNTER :"+str(total_counter), (400, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.putText(frame1, "CAR COUNTER :"+str(car), (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)  
    cv2.putText(frame1, "HEAVY VEHICLE COUNTER :"+str(Heavy_vechicle), (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)                        

    #cv2.imshow('Detecter', dilatada)
    cv2.imshow('video original', frame1)

    if cv2.waitKey(1) == 13:
        break
   

cv2.destroyAllWindows()
cap.release()
