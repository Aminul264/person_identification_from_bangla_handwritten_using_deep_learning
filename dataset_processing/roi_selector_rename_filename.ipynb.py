import cv2
import os


class ROISelector:
    def __init__(self, image):
        self.image = image
        self.roi = None
        self.selection_started = False


        cv2.namedWindow("ROI Selector", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("ROI Selector", self.mouse_callback)


    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.roi = [x, y, 0, 0]
            self.selection_started = True


        elif event == cv2.EVENT_LBUTTONUP:
            self.selection_started = False


        elif event == cv2.EVENT_MOUSEMOVE:
            if self.selection_started:
                self.roi[2] = x - self.roi[0]
                self.roi[3] = y - self.roi[1]
                self.display_image()


    def display_image(self):
        img_with_roi = self.image.copy()
        if self.roi is not None:
            x, y, w, h = self.roi
            cv2.rectangle(img_with_roi, (x, y), (x + w, y + h), (0, 0, 255), 10)


            # Display size information
            size_info = f"Size: {w} x {h+10}"
            cv2.putText(img_with_roi, size_info, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)


        cv2.imshow("ROI Selector", img_with_roi)
        cv2.setWindowProperty("ROI Selector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def select_roi(image):
    roi_selector = ROISelector(image)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 13 and roi_selector.roi is not None:  # Enter key
            cv2.destroyAllWindows()
            return tuple(roi_selector.roi)
        elif key == 27:  # Escape key
            cv2.destroyAllWindows()
            return None


def crop_selected_areas(input_folder, output_folder, selected_roi):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    segment = 100001  # Starting counter value
    age = 10
    gender = 1
    ethnicity = 0 

    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        if os.path.isfile(file_path):
            image = cv2.imread(file_path)


            # Crop and save the image based on the selected ROI
            x, y, w, h = selected_roi
            cropped_image = image[int(y):int(y+h), int(x):int(x+w)]


            # Constructing output file name
            output_filename = f"{age}_{gender}_{ethnicity}_{segment}.jpg"


            output_path = os.path.join(output_folder, output_filename)
            cv2.imwrite(output_path, cropped_image)
            print(f"{file_path} - Selected ROI cropped and saved as {output_path}")


            segment += 10000
            # Increment segment for next iteration
            age += 1  # Increment age for next iteration


def main():
    input_folder = "./images/"
    output_folder = "./characters0/"


    # Allow the user to select a common ROI for all images
    first_image_path = os.path.join(input_folder, os.listdir(input_folder)[0])
    first_image = cv2.imread(first_image_path)
    selected_roi = select_roi(first_image)


    if selected_roi is not None:
        # Crop selected areas from images based on the common ROI
        crop_selected_areas(input_folder, output_folder, selected_roi)
        print(f"All images have been cropped based on the selected area and saved in '{output_folder}'.")
    else:
        print("ROI selection canceled.")


if __name__ == "__main__":
    main()



