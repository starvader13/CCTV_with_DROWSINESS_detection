import cv2 as cv
import time as tm
import win32gui as wg
import win32con as wc


def minimizeWindow():
    tab = wg.GetForegroundWindow()
    wg.ShowWindow(tab, wc.SW_MINIMIZE)


def maximizeWindow():
    tab = wg.GetForegroundWindow()
    wg.ShowWindow(tab, wc.SW_MAXIMIZE)


def capture_cctv():
    capture_video = cv.VideoCapture(0)

    capture_video.set(3, 640)  # width #height
    capture_video.set(4, 480)  # length #height

    width = capture_video.get(3)
    height = capture_video.get(4)

    print("\nVideo resolution definition : ", width, ' X ', height, end='\n')
    print("\nHelp -- \n.Press esc to exit the capturing process.", end='\n\n')

    # create a video format with using video-writer of cv2
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')

    # %D - same as %m/%d/%y #%T - current time, equal to %H:%M:%S
    timestamp = tm.strftime("Recording -%D -%T ")

    capture_output = cv.VideoWriter(
        'Capture_cctv_video/'+timestamp+'.avi', fourcc, 20.0, (640, 480))

    while (capture_video.isOpened()):  # isOpened method is called to check whether camera is or not
        check_frame, capture_frame = capture_video.read()  # check frame by frame
        if check_frame == True:
            # positive value (for example, 1) means flipping around y-axis.
            # flipping the frame with right frame
            capture_frame = cv.flip(capture_frame, 1)

            current_time = tm.ctime()  # taking the current time input in current_time

            #v2.rectangle(image, start_point, end_point, color, thickness)
            # cordinates (x,y,100ofx,20ofy),(colour),making it as a filled rectangle
            cv.rectangle(capture_frame, (5, 5, 100, 20),
                         (255, 255, 255), cv.FILLED)

            # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
            # setting the cordinates        #size #color#thickness
            cv.putText(capture_frame, "Camera 1", (20, 20),
                       cv.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)
            cv.putText(capture_frame, current_time, (420, 460),
                       cv.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)

            # show our video
            cv.imshow('CCTV Camera', capture_frame)
            capture_output.write(capture_frame)

            # 27 for esc key
            if cv.waitKey(1) == 27:
                print("Video footage saved in current directory.")
                break

            elif cv.waitKey(1) == ord('s'):
                minimizeWindow()

            elif cv.waitKey(1) == ord('w'):
                maximizeWindow()

        else:
            print("Can't Open Camera , check configuration")
            break

    # When every operation is completed , capture is released
    capture_video.release()
    capture_output.release()
    cv.destroyAllWindows()


print("*"*80+"\n"+" "*30+"Welcome to cctv software\n"+"*"*80, end='\n\n')

user_input = int(input("Enter the OTP : "))
if user_input > 999 and user_input < 10000:
    capture_cctv()
else:
    print("You have entered the wrong OTP.")
    exit
