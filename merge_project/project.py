import cv2 as cv
import time as tm
import win32gui as wg
import win32con as wc
from scipy.spatial import distance
from imutils import face_utils
import simpleaudio as sa
import imutils
import dlib

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

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
thresh = 0.25
frame_check = 20
wave_object = sa.WaveObject.from_wave_file('alarm1.wav')
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag=0

def call():
	while True:
		ret, frame=cap.read()
		frame = imutils.resize(frame, width=450)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		subjects = detect(gray, 0)
		for subject in subjects:
			shape = predict(gray, subject)
			shape = face_utils.shape_to_np(shape)#converting to NumPy Array
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)
			ear = (leftEAR + rightEAR) / 2.0
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
			if ear < thresh:
				flag += 1
				#print (flag)
				if flag >= frame_check:
					cv2.putText(frame, "*****ALERT!*****", (10, 30),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					cv2.putText(frame, "*****ALERT!*****", (10,325),
						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					play_object = wave_object.play()
					play_object.wait_done()	
			else:
				flag = 0
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			cv2.destroyAllWindows()
			cap.release()
			break

user_input = int(input("Enter the OTP : "))
if user_input > 999 and user_input < 10000:
    capture_cctv()
    call()
else:
    print("You have entered the wrong OTP.")
    exit