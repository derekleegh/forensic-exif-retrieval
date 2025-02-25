import customtkinter
from forensic  import Forensic
from tkinter import filedialog

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

def button_function():
    print("button pressed")
    forensics = Forensic()


# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)

button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"File selected: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)


upload_button = customtkinter.CTkButton(master=app, text="Upload File", command=upload_file)
upload_button.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)
app.mainloop()

