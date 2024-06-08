import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the model
model = load_model('Age_Sex_Detection.keras')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age and Gender Detector')
top.configure(background='#CDCDCD')

# Initializing the labels (1 for age and 1 for sex)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

# Defining Detect function which detects the age and gender of the person in image using the model
def Detect(file_path):
    try:
        image = Image.open(file_path)
        image = image.resize((48, 48))  # Resize image to the size expected by the model
        image = np.array(image)
        image = np.expand_dims(image, axis=0)
        image = image / 255.0  # Normalize the image
        
        pred = model.predict(image)
        age = int(np.round(pred[1][0]))
        sex = int(np.round(pred[0][0]))
        sex_f = ["Male", "Female"]
        
        print('Predicted age is ' + str(age))
        print('Predicted Gender is ' + sex_f[sex])
        
        label1.configure(foreground="#011638", text=f"Age: {age}")
        label2.configure(foreground="#011638", text=f"Gender: {sex_f[sex]}")
    except Exception as e:
        print(f"Error during detection: {e}")

# Defining Show_detect button function
def show_Detect_Button(file_path):
    Detect_b = Button(top, text="Detect image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Upload image function
def Upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text=' ')
        label2.configure(text=' ')
        show_Detect_Button(file_path)
    except Exception as e:
        print(f"Error loading image: {e}")

upload = Button(top, text="Upload an image", command=Upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)

label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text='Age and Gender Detector', pady=20, font=("arial", 20, 'bold'))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

top.mainloop()
