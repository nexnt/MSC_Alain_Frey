import time
from ultralytics import YOLO
import cv2
from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    # Initialize the YOLOv8 model
    model = YOLO("/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect/detect1280b16ep200/weights/best.pt")  # Adjust the model path and name as necessary

    # Capture video    
    #cap = cv2.VideoCapture('/Users/alainfrey/Downloads/temp_video_for_share 2.mp4')
    cap = cv2.VideoCapture('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0208.MP4')
    frame_count = 0
    frame_times = []
    fps_values = []
    start_time2 = perf_counter()
    detections_made=[]
    
    try:
        cv2.namedWindow('hidden', cv2.WINDOW_NORMAL)
        cv2.moveWindow('hidden', 10000, 10000)  # Move the window out of the screen
        while True:
            
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            start_time = perf_counter()
  
              # Get the current time before the command executes

            # Call the function whose duration you want to measure
            #result = model(frame,stream=True, device='mps', imgsz=1280, show=True)
            results = model.predict(frame, stream=True,  device='mps', imgsz=1280)
            
            for res in results:

                if len(res.boxes) > 0:
                    detections_made.append(True)
                else:
                    detections_made.append(False)
            # Check if detections were made
            
            
                
            end_time = perf_counter()  # Get the current time after the command has executed
            

        # Display the annotated frame
            
            #cv2.imshow('Video', frame)
            
            
            duration = end_time - start_time  # Calculate the duration
            frame_times.append(duration)  # Store the duration
            fps = 1 / duration  # Calculate FPS for the current frame
            fps_values.append(fps)  # Store the FPS

            print(f"The command took {duration} seconds to execute. FPS: {fps}")

            # Break the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                end_time2 = perf_counter()
                duration2 = end_time2 - start_time2
                print(f"Total duration: {duration2} seconds")
                print(f"Total frames: {frame_count}")
                print(f"{frame_count/duration2} FPS")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

        # Calculate mean and standard deviation for frame processing times
        mean_duration = np.mean(frame_times)
        std_deviation_duration = np.std(frame_times)

        # Calculate mean and standard deviation for FPS
        mean_fps = np.mean(fps_values)
        std_deviation_fps = np.std(fps_values)

        print(f"Mean duration per frame: {mean_duration} seconds")
        print(f"Standard deviation of duration: {std_deviation_duration} seconds")
        print(f"Mean FPS: {mean_fps}")
        print(f"Standard deviation of FPS: {std_deviation_fps}")


        fps_indices = np.arange(len(fps_values))

        # Plot FPS values with detections highlighted
        plt.figure(figsize=(12, 6))
        colors = ['red' if detection else 'blue' for detection in detections_made]

        plt.subplot(1, 2, 1)
        plt.scatter(fps_indices, fps_values, c=colors)
        plt.axhline(y=mean_fps, color='r', linestyle='-', label=f'Mean: {mean_fps:.2f} FPS')
        plt.axhline(y=mean_fps + std_deviation_fps, color='g', linestyle='--', label=f'Std Dev: {std_deviation_fps:.2f} FPS')
        plt.axhline(y=mean_fps - std_deviation_fps, color='g', linestyle='--')
        plt.xlabel('Frame')
        plt.ylabel('FPS')
        plt.title('FPS Values with Detection Highlighted')
        red_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Detections Made')
        blue_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='No Detections')
        plt.legend(handles=[red_patch, blue_patch], loc='upper right')

        # Plot FPS values all in the same color
        plt.subplot(1, 2, 2)
        plt.scatter(fps_indices, fps_values, color='blue')
        plt.axhline(y=mean_fps, color='r', linestyle='-', label=f'Mean: {mean_fps:.2f} FPS')
        plt.axhline(y=mean_fps + std_deviation_fps, color='g', linestyle='--', label=f'Std Dev: {std_deviation_fps:.2f} FPS')
        plt.axhline(y=mean_fps - std_deviation_fps, color='g', linestyle='--')
        plt.xlabel('Frame')
        plt.ylabel('FPS')
        plt.title('FPS Values')
        plt.legend()

        plt.tight_layout()
        plt.show()