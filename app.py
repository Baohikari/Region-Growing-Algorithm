import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from region_growing import RegionGrowing
import cv2
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Region Growing App")
        self.geometry("1200x740")
        self.config(background=('#E7ECF0'))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.app_title = tk.Label(self,
                                  text="REGION GROWING ALGORITHM",
                                  font=('Arial', 25),
                                  ).grid(row=0, column=0, pady=(12, 4), columnspan=2)
        self.threshold_label = tk.Label(self,
                                    text="Please, enter threshold here:",
                                    font=('Arial', 16),
                                    ).grid(row=1, column=0, padx=(10, 5), pady=(12, 12), sticky='e')
        
        self.threshold_entry = tk.Entry(self,
                                        font=('Arial', 16))
        self.threshold_entry.grid(row=1, column=1, padx=(5, 10), pady=(12, 12), sticky='w')
        
        self.load_button = tk.Button(self,
                                     text="Upload your image here",
                                     bg='#E0FBFF',
                                     fg='#2CAFFE',
                                     font=('Comic Sans', 13),
                                     command=self.load_image,
                                     ).grid(row=2, column=0, columnspan=2)
        
        self.use_algorithm_button = tk.Button(self,
                                              text='Use Algorithm',
                                              font=('Comic Sans', 13),
                                              command=self.use_region_growing).grid(row=3, column=0, pady=(12, 12), columnspan=2)
        
        self.user_upload_image_label = tk.Label(self,
                                                text='Original Image',
                                                font=('Arial', 14),
                                                bg='#E7ECF0',
                                                ).grid(row=4, column=0, padx=10, pady=20, sticky='n')
        
        self.processed_image_label = tk.Label(self,
                                              text='Processed Image',
                                              font=('Arial', 14),
                                              bg='#E7ECF0',
                                              ).grid(row=4, column=1, padx=10, pady=20, sticky='n')
        
    def load_image(self):
        self.image_path = filedialog.askopenfilename(title='Select an Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png')])
        if not self.image_path:
            messagebox.showerror('Error', 'No image selected')
            return
        try:
            img = Image.open(self.image_path)
            img = img.resize((500, 450), Image.LANCZOS)
            self.original_image = ImageTk.PhotoImage(img)
            self.user_upload_image_label = tk.Label(image=self.original_image, text='').grid(row=4, column=0, padx=10, pady=20, sticky='n')
        except Exception as e:
            messagebox.showerror('Error', f'Fail to open image. {str(e)}')

    def use_region_growing(self):
        if not hasattr(self, 'image_path') or self.image_path is None:
            messagebox.showerror('Error', 'Please upload an image first')
            return

        threshold = self.threshold_entry.get()
        if not threshold.isdigit():
            messagebox.showerror('Error', 'Please enter a valid threshold')
            return

        region_growing = RegionGrowing(self.image_path, int(threshold))
        seeds = [(100, 100)]
        region_growing.apply_region_growing(seeds)

        segmented_image = region_growing.get_segmented_image()

        # Chuyển đổi numpy array sang PIL Image
        processed_image = Image.fromarray(segmented_image.astype(np.uint8))

        # Resize và hiển thị hình ảnh
        processed_image = processed_image.resize((500, 450), Image.LANCZOS)
        self.after_using_algo = ImageTk.PhotoImage(processed_image)
        self.processed_image_label = tk.Label(image=self.after_using_algo, text='').grid(row=4, column=1, padx=10, pady=20, sticky='n')



if __name__ == "__main__":
    app = App()
    app.mainloop()
        