import time
from ultralytics import YOLO
import cv2
from time import perf_counter

if __name__ == "__main__":
    
    # Initialize the YOLOv8 model
    model = YOLO("/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect/detect1280b16ep200/weights/best.pt")  # Adjust the model path and name as necessary

    # Capture video
    cap = cv2.VideoCapture('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0208.MP4')
    frame_count=0
    start_time2 = perf_counter()
    try:
        while True:
            
            ret, frame = cap.read()
            if not ret:
                break
            frame_count+=1
  
            start_time = perf_counter()  # Get the current time before the command executes

            # Call the function whose duration you want to measure
            model.predict(frame)
            cv2.imshow('Video', frame)
            end_time = perf_counter()  # Get the current time after the command has executed
            duration = end_time - start_time  # Calculate the duration

            print(f"The command took {duration} seconds to execute.")

            # Break the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
            
                end_time2 = perf_counter()
                duration2 = end_time2 - start_time2
                print(duration2)
                print(frame_count)
                
                print(f"{frame_count/duration2} FPS")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()