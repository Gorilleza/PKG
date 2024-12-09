import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing Application")

        self.image_label = Label(master)
        self.image_label.pack()

        self.load_button = Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.filter_frame = LabelFrame(master, text="Filters", padx=10, pady=10)
        self.filter_frame.pack(padx=10, pady=10)

        self.median_filter_button = Button(self.filter_frame, text="Median Filter", command=self.apply_median_filter)
        self.median_filter_button.pack(side=LEFT)

        self.bilateral_filter_button = Button(self.filter_frame, text="Bilateral Filter", command=self.apply_bilateral_filter)
        self.bilateral_filter_button.pack(side=LEFT)

        self.threshold_frame = LabelFrame(master, text="Thresholding", padx=10, pady=10)
        self.threshold_frame.pack(padx=10, pady=10)

        self.global_threshold_button = Button(self.threshold_frame, text="Global Threshold", command=self.global_threshold)
        self.global_threshold_button.pack(side=LEFT)

        self.adaptive_threshold_button = Button(self.threshold_frame, text="Adaptive Threshold", command=self.adaptive_threshold)
        self.adaptive_threshold_button.pack(side=LEFT)

        self.save_button = Button(master, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.image = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, img):
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def apply_median_filter(self):
        if self.image is not None:
            self.processed_image = cv2.medianBlur(self.image, 5)
            self.display_image(self.processed_image)

    def apply_bilateral_filter(self):
        if self.image is not None:
            self.processed_image = cv2.bilateralFilter(self.image, 9, 75, 75)
            self.display_image(self.processed_image)

    def global_threshold(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            _, self.processed_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
            self.display_image(self.processed_image)

    def adaptive_threshold(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            self.processed_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY, 11, 2)
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                         ("JPEG files", "*.jpg"),
                                                                                         ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))
                messagebox.showinfo("Image Saved", "Image saved successfully!")


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
