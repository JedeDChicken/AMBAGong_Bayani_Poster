import cv2
from PIL import Image, ImageTk
from tkinter import Tk, Label  # Creates app/window...
# import time

def poster(img_path, img_resize_perc, webcam_resize_perc, cam):
    # Main
    main = Tk()
    main.title('AMBAGong Bayani Poster')

    # Resize img
    img = Image.open(img_path)
    
    width, height = img.size
    new_width = int(width * img_resize_perc / 100)
    new_height = int(height * img_resize_perc / 100)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # LANCZOS- resampling...

    # Initialize webcam
    cap = cv2.VideoCapture(cam)

    img_copy = None  # Variable to store the latest img copy with webcam feed
    # Function to update img with webcam feed
    def update_image():
        nonlocal img_copy  # Nearest local scope, not global...
        ret, frame = cap.read()

        if ret:  # If frame was read...
            frame = cv2.flip(frame, 1)  # Horizontal flip, frame- typically NumPy array
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            frame_pil = Image.fromarray(frame_rgb)  # Convert to PIL Image- for img manipulation...

            # Crop frame to square
            webcam_orig_width, webcam_orig_height = frame_pil.size
            webcam_new_size = webcam_orig_height
            
            crop_x = (webcam_orig_width - webcam_new_size) // 2  # Floor div
            frame_cropped = frame_pil.crop((crop_x, 0, crop_x + webcam_new_size, webcam_new_size))  # Crop- left, upper, right, lower

            # Resize the cropped frame
            webcam_new_size = int(webcam_new_size * webcam_resize_perc / 100)
            frame_resized = frame_cropped.resize((webcam_new_size, webcam_new_size), Image.Resampling.LANCZOS)  # Square

            # Position webcam feed to center of img
            x_center = (new_width - webcam_new_size) // 2
            y_center = (new_height - webcam_new_size) // 2

            img_copy = img_resized.copy()
            img_copy.paste(frame_resized, (x_center, y_center))

            # Convert img to a format Tkinter can use
            img_tk = ImageTk.PhotoImage(img_copy)

            # Update label with the new img
            label.config(image=img_tk)
            label.image = img_tk  # Keep a reference, avoids garbage collection

        # Schedule the update_image function call, every 10 ms
        main.after(10, update_image)

    # Function to take snapshot of bg img with the webcam feed, 
    def take_snapshot(event):
        if img_copy:
            # Save the snapshot
            # timestamp = time.strftime("%Y%m%d-%H%M%S")
            # snapshot_filename = f"snapshot_{timestamp}.png"
            # img_copy.save('Ambagong Bayani Snap')
            # print(f'Snapshot taken and saved as {snapshot_filename}')
            img_copy.save('AMBAGong Bayani Snap.png')
            print('Snapshot taken')

    # Create a label to display img
    label = Label(main)
    label.pack()

    main.geometry(f'{new_width}x{new_height}')  # Set window size to match resized img
    update_image()  # Update img w/ webcam feed
    main.bind('<c>', take_snapshot)  # C- to take snapshot
    main.mainloop()  # Run Tkinter event loop

    cap.release()  # Release webcam

# Function call
img_path = 'AMBAGong Bayani Poster.png'
img_resize_perc = 35
webcam_resize_perc = 70
cam = 2  # Used Droidcam, 0- default?
poster(img_path, img_resize_perc, webcam_resize_perc, cam)