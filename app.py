import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from region_growing import RegionGrowing
import cv2
import numpy as np
import random
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Region Growing App")
        self.geometry("1200x920")
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

        self.seed_label = tk.Label(self,
                                   text='Enter your seed (e.g. : 100x100 or 100x100, 120x120):',
                                   font=('Arial', 16),
                                   ).grid(row=2, column=0, padx=(10, 5), pady=(12, 12), sticky='e')
        self.seed_entry = tk.Entry(self,
                                   font=('Arial', 16))
        self.seed_entry.grid(row=2, column=1, padx=(5, 10), pady=(12, 12), sticky='w')
        
        self.selection_label = tk.Label(self,
                                        text='OR',
                                        font=('Arial', 16),
                                        ).grid(row=3, column=0, padx=(10, 5), pady=(12, 12), sticky='e')
        self.automatic_seed_selection = tk.Button(self,
                                                  text='RANDOM SEEDS SELECTION',
                                                  font=('Comic Sans', 13),
                                                  command=self.random_seeds)
        self.automatic_seed_selection.grid(row=3, column=1, padx=(5, 10), pady=(12, 12), sticky='w')
        
        self.load_button = tk.Button(self,
                                     text="Upload your image here",
                                     font=('Comic Sans', 13),
                                     command=self.load_image,
                                     ).grid(row=4, column=0, columnspan=2)
        
        self.use_algorithm_button = tk.Button(self,
                                              text='Use Algorithm',
                                              font=('Comic Sans', 13),
                                              command=self.use_region_growing).grid(row=5, column=0, pady=(12, 12), columnspan=2)
        
        self.user_upload_image_label = tk.Label(self,
                                                text='Original Image',
                                                font=('Arial', 14),
                                                bg='#E7ECF0',
                                                ).grid(row=6, column=0, padx=10, pady=20, sticky='n')
        
        self.processed_image_label = tk.Label(self,
                                              text='Processed Image',
                                              font=('Arial', 14),
                                              bg='#E7ECF0',
                                              ).grid(row=6, column=1, padx=10, pady=20, sticky='n')
        
    def load_image(self):
        self.image_path = filedialog.askopenfilename(title='Select an Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png')])
        if not self.image_path:
            messagebox.showerror('Error', 'No image selected')
            return
        try:
            img = Image.open(self.image_path)
            img = img.resize((500, 450), Image.LANCZOS)
            self.original_image = ImageTk.PhotoImage(img)
            self.user_upload_image_label = tk.Label(image=self.original_image, text='').grid(row=6, column=0, padx=10, pady=20, sticky='n')
        except Exception as e:
            messagebox.showerror('Error', f'Fail to open image. {str(e)}')
    
    def random_seeds(self):
        if not hasattr(self, 'image_path') or self.image_path is None:
            messagebox.showerror('Error', 'Please upload an image first')
            return
        
        image = cv2.imread(self.image_path)
        height, width, _ = image.shape
        
        num_seeds = random.randint(1, 5)
        seeds = []
        for _ in range(num_seeds):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            seeds.append(f'{x}x{y}')
        
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, ', '.join(seeds))

    def use_region_growing(self):
        if not hasattr(self, 'image_path') or self.image_path is None:
            messagebox.showerror('Error', 'Please upload an image first')
            return

        threshold = self.threshold_entry.get()
        if not threshold.isdigit():
            messagebox.showerror('Error', 'Please enter a valid threshold')
            return
        
        seed_input = self.seed_entry.get()
        seeds = []
        for seed_str in seed_input.split(","):
            try:
                x, y = map(int, seed_str.strip().split("x"))
                seeds.append((x, y))
            except ValueError:
                print(f"Invalid seed format: {seed_str}")
                continue
        
        region_growing = RegionGrowing(self.image_path, int(threshold))
        region_growing.apply_region_growing(seeds)

        segmeted_image = region_growing.get_segmented_image()
        processed_image = Image.fromarray(segmeted_image.astype(np.uint8))
        processed_image = processed_image.resize((500, 450), Image.LANCZOS)
        self.after_using_algo = ImageTk.PhotoImage(processed_image)
        self.processed_image_label = tk.Label(image=self.after_using_algo, text='').grid(row=6, column=1, padx=10, pady=20, sticky='n')
if __name__ == "__main__":
    app = App()
    app.mainloop()
        