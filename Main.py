"""
Source: https://effbot.org/tkinterbook/photoimage.htm, https://www.tutorialspoint.com/python/python_gui_programming.htm,
https://pythonbasics.org/tkinter-image/, https://effbot.org/tkinterbook/button.htm
https://stackoverflow.com/questions/48723923/align-a-button-to-the-bottom-using-tkinter,
https://www.python-course.eu/tkinter_buttons.php, http://effbot.org/tkinterbook/label.htm
https://www.python-course.eu/tkinter_layout_management.php
https://stackabuse.com/python-gui-development-with-tkinter-part-2/
https://stackoverflow.com/questions/42600739/how-do-i-upload-an-image-on-python-using-tkinter
https://stackoverflow.com/questions/50123315/how-do-i-create-an-import-file-button-with-tkinter
https://docs.python.org/3/library/tk.html,  https://www.tutorialsteacher.com/python/os-module

"""
from tkinter import *
from tkinter import messagebox, Tk
from tkinter import filedialog

import os

import face_recognition

from PIL import ImageTk, Image

# constructor Tk() will build our main window
base = Tk()
base.title('Matchmaking The Image')


# Icon can be used under free licence taken from https://icon-icons.com/icon/face-recognition-exploration/2443#32

base.iconbitmap('icons&images/face_recognition_exploration_3005.ico')


# adjust size of GUI main window in tkinter
# base.geometry("600x600")


# function to display the message in about section
def about_message():
    # file = Toplevel(base)
    # button = Button(file, text="Do nothing button")
    # button.pack()
    messagebox.showinfo("ABOUT ",
                        "'Matchmaking the image' : Created in October 2019 as a Python mini student project")


# Base Menu
menu = Menu(base)

# File menu
menu_file = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=menu_file)
menu_file.add_command(label="Exit", command=base.quit)

# About Menu
about_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label='About', command=about_message)

# Listing all the images present in given path, listdir will list all the photos present in directory
img = os.listdir('images_compared')

# Create Canvas
canvas = Canvas(base, width=207, height=307)
# Add Canvas text
canvas.create_text(100, 150, fill="black", font="Times 10 italic bold",
                   text="Image goes here")

# Give canvas an outline  through shapes
canvas.create_rectangle(2, 2, 207, 307, outline='black')
canvas.pack(padx=10, pady=50)


def select_image():
    global img_to_match
    global directory
    # load the image from the directory in tkinter
    base.match = filedialog.askopenfilename(initialdir="images_to_match/",
                                            title='Please Select The Image You Want To Match',
                                            filetypes=(("jpeg Files", "*.jpg"), ("png Files", "*.png")))

    # Get the path of the image in the directory at index 1, also we can use something like askdirectory()
    directory = os.path.split(base.match)[1]

    # Resize the loaded image, source : https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
    # Image.ANTIALIAS - a high-quality downsampling filter

    img_loaded = Image.open(base.match)
    img_resized = img_loaded.resize((200, 300), Image.ANTIALIAS)
    # open the image in tkinter window
    img_to_match = ImageTk.PhotoImage(img_resized)
    canvas.create_image(5, 5, image=img_to_match, anchor=NW)
    # img_to_match_label = Label(image=img_to_match).pack()


# Button for selection of an image
my_img_button = Button(base, text='Select an Image', command=select_image)
my_img_button.pack()


# function to load the compared images onto the screen

def loading_matched_img():
    global frame_img

    frame_img = LabelFrame(base, text='Results...', padx=5, pady=5)
    frame_img.pack(padx=5, pady=5, side=LEFT)
    load_img = Image.open("images_compared/" + image)
    loaded = load_img.resize((100, 150), Image.ANTIALIAS)
    display = ImageTk.PhotoImage(loaded)

    label = Label(frame_img, image=display)

    # source : https://effbot.org/tkinterbook/photoimage.htm,
    # When a PhotoImage object is garbage-collected by Python (e.g. when you return from a function which stored
    # an image in a local variable), the image is cleared even if it�s being displayed by a Tkinter widget.
    # To avoid this, the program must keep an extra reference to the image object
    label.img = display
    label.pack()


# Functions to output the results of the matched and unmatched images
def img_results_match():

    loading_matched_img()
    my_match_label = Label(frame_img, text="Matched : " + image, bg='#50FF33')
    my_match_label.pack()


def img_results_unmatch():

    loading_matched_img()

    my_match_label = Label(frame_img, text="Not Matched : " + image, bg='#F53213')
    my_match_label.pack()


# function for match button
def find_image_match():
    global image

    my_match_label = Label(base, text="Matching Completed", bg='#1B0DE3')
    my_match_label.pack()

    #  img_to_load = imageio.imread('images_to_match/' + directory)
    # imageio.imread also returns a NumPy array value if used as an alternative to face_recognition.load_image_file
    #  source : https://stackoverflow.com/questions/3493092/convert-image-to-a-matrix-in-python

    # load the image to match
    img_to_load = face_recognition.load_image_file('images_to_match/' + directory)

    # convert the previously loaded image into the feature vector which will return the value in array
    img_to_match_vectored = face_recognition.face_encodings(img_to_load)[0]

    # loop over every image

    for image in img:
        # load the image from directory img
        current_img = face_recognition.load_image_file('images_compared/' + image)

        # convert loaded image into a feature vector
        current_img_vectored = face_recognition.face_encodings(current_img)[0]

        # match the images in directory with the image that is to be matched and check if they both match
        match_outcome = face_recognition.compare_faces(
            [img_to_match_vectored], current_img_vectored)

        # check if both images matched

        if match_outcome[0]:

            img_results_match()


        else:
            img_results_unmatch()


# creating a Match button for the image to be matched
# Add frame to Match button

frame = LabelFrame(base, text='Click to Match...', padx=5, pady=5)
frame.pack(padx=15, pady=15)

matchButton = Button(frame, text='Match', padx=50, pady=10, command=find_image_match)
matchButton.pack()

# config is used to access an object's attributes after its initialisation
base.config(menu=menu)

# Display the GUI results
base.mainloop()
