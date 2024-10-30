import tkinter
from tkinter import *

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://127.0.0.1/api/v1/actuators/"
id = 1111

count = 0
flag = False


def check_update():
    global count
    global flag
    print(count)
    if count == 60:
        traffic_sign.config(fg="black")
        count = 0
        flag = False

    try:
        response = requests.get(f"{url}{str(id)}", verify=False)
        print(response.status_code, response.text)
        if response.status_code == 200:
            if "display" in response.json():
                if response.json()["display"]:
                    count = 0
                    flag = True
                    traffic_sign.config(fg="#d84b20")
    except Exception:
        print("exception")
        pass

    if flag:
        count += 1
    root.after(5000, check_update)


root = Tk()  # create root window
root.title("WADAS TRAFFIC SIGN")  # title of the GUI window
root.maxsize(1000, 1000)  # specify the max size the window can expand to
root.config(bg="white")  # specify background color

# Create left and right frames
upper_frame = Frame(root, width=600, height=300, bg="white")
# upper_frame.grid(row=0, column=0, padx=10, pady=5)

lower_frame = Frame(root, width=600, height=300, bg="grey")
# lower_frame.grid(row=1, column=0, padx=10, pady=(5, 30))

# Create frames and labels in left_frame
upper_label = Label(upper_frame, text="WADAS", bg="white", font=("Sans-Serif", 24, "bold"))
upper_label.pack()
# upper_label.grid(row=0, column=0, padx=5, pady=5)

# # load image to be "edited"
image = PhotoImage(file="road_sign.png")
new_image = image.zoom(2, 2)
final_image = new_image.subsample(3, 3)  # resize image using subsample
image_label = Label(upper_frame, image=final_image)
image_label.pack(fill="x", expand=True)
# lower_label.grid(row=1, column=0, padx=5, pady=5)

# Create frames and labels in left_frame
traffic_sign = Label(
    lower_frame,
    text="ATTENZIONE ANIMALI\nSELVATICI VAGANTI",
    bg="black",
    fg="black",
    font=("Sans-Serif", 32, "bold"),
)
traffic_sign.pack(padx=10, pady=10)
upper_frame.pack(side="top", fill="both", expand=True)
lower_frame.pack(side="bottom", pady=(5, 30), padx=10)
# traffic_sign.grid(row=0, column=0, padx=10, pady=10)

root.after(5000, check_update)

root.mainloop()
