# sudo sysctl -w net.inet.udp.maxdgram=65535
# Run this every time before running the program to change the max value

import socket

import zfec
import sys
import numpy as np
import cv2
import mss
from PIL import Image
from customtkinter import *
from tkinter.messagebox import askokcancel
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys

print(os.listdir())



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
# Server IP: 192.168.1.38

# Define the directory to monitor (the entire file system)
directory_to_watch = "/Users"

system_number = 5

# Paths to exclude in mac
exclude_paths = [
    ""
]

#exclude_paths = []

# Function to check if a path should be excluded
def should_exclude(path):
    for exclude_path in exclude_paths:
        if os.path.abspath(path).startswith(os.path.abspath(exclude_path)):
            return True
    return False

def is_inside_hidden_directory(path):
    # Get the directory part of the path
    directory = os.path.dirname(path)
    print(os.path.basename(directory))
    # Check if the last component of the directory starts with a dot
    return os.path.basename(directory).startswith('.')


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global server
        if server == None:
            return
        if should_exclude(event.src_path):
            return
        # Code to execute when a file is modified
        if is_inside_hidden_directory(event.src_path):
            pass
        else:
            message.sendto(f"----13---- File {event.src_path} has been modified".encode("utf-8"), server)

    def on_created(self, event):
        global server
        if server == None:
            return
        if should_exclude(event.src_path):
            return
        # Code to execute when a new file is created
        if is_inside_hidden_directory(event.src_path):
            pass
        else:
            message.sendto(f"----13---- File {event.src_path} has been created".encode("utf-8"), server)

        #print(f"File {event.src_path} has been created")

    def on_deleted(self, event):
        global server
        if server == None:
            return
        if should_exclude(event.src_path):
            return
        # Code to execute when a file is deleted
        if is_inside_hidden_directory(event.src_path):
            pass
        else:
            message.sendto(f"----13---- File {event.src_path} has been deleted".encode("utf-8"), server)


    def on_moved(self, event):
        global server
        if server == None:
            return
        if should_exclude(event.src_path) or should_exclude(event.dest_path):
            return
        # Code to execute when a file is moved (renamed)
        if is_inside_hidden_directory(event.src_path):
            pass
        else:
            message.sendto(f"----13---- File {event.src_path} has been moved to {event.dest_path}".encode("utf-8"), server)

        #print(f"File {event.src_path} has been moved to {event.dest_path}")

def watch():
    #time.sleep(3)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=True)  # Set recursive=True to monitor subdirectories

    observer.start()
    try:
        while True:
            time.sleep(5)  # Adjust the sleep interval as needed
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200000)

message = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000)


message.bind(("127.0.0.1", 4000))

s.sendto(str(port).encode("utf-8"), ("127.0.0.1", 7387))
s.sendto(f"Computer {system_number}".encode("utf-8"), ("127.0.0.1", 7387))



basewidth = 300
wpercent = (basewidth / float(bounding_box["width"]))
hsize = int((float(bounding_box["height"]) * float(wpercent)))
print(basewidth, hsize)

server = None
share_screen = False # False is default. Will only be True when a message is recieved from the ITLMS
def recieve():
    global message, server, share_screen, basewidth, wpercent, hsize
    while True:
        data, addr = message.recvfrom(100000)
        if server is None:
            server = addr
        val = data.decode("utf-8")
        if val == "Share":
            share_screen = True
            print("Sharing")
        elif val == "DontShare" and basewidth != 800:
            share_screen = False
            print("Not Sharing")
        elif val == "FullScreen":
            print("FullScreen")
            basewidth = 800
            wpercent = (basewidth / float(bounding_box["width"]))
            hsize = int((float(bounding_box["height"]) * float(wpercent)))
            print(basewidth, hsize)
        elif val == "StopFullScreen":
            print("StopFullScreen")
            basewidth = 300
            wpercent = (basewidth / float(bounding_box["width"]))
            hsize = int((float(bounding_box["height"]) * float(wpercent)))
            print(basewidth, hsize)
        elif val.startswith("-----MESSAGE-----"):
            m = val[18::]
            askokcancel("Message From Teacher", m)


        print(server)
        print(val)

t1 = threading.Thread(target=recieve)
t1.start()
def func():
    global img
    try:
        while True:
            if share_screen != False:

                with mss.mss() as sct:
                    sct_img = sct.grab(bounding_box)
                img = Image.frombytes(
                    'RGB',
                    (sct_img.width, sct_img.height),
                    sct_img.rgb,
                )
                #img = Image.open(resource_path(f"OS/OS{system_number}.png"))

                img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                img2 = cv2.putText(np.array(img), f"Computer {system_number}", (0, hsize-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                ret, buffer = cv2.imencode(".jpg", img2, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                #print(type(buffer))
                img_bytes = buffer.tobytes()
                k = 10  # Adjust k according to your needs
                block_size = len(img_bytes) // k  # Calculate the block size

                # Split the image data into k equal-sized blocks
                data_blocks = [img_bytes[i * block_size:(i + 1) * block_size] for i in range(k)]

                # Encode the data blocks
                encoder = zfec.Encoder(k=k, m=15)
                encoded_data = encoder.encode(data_blocks)
                #img2 = pickle.dumps(buffer)
                #print(len(img2))
                for packet in encoded_data:
                    s.sendto(packet, ("127.0.0.1", 7387))


    except OSError as e:
        print(e)
        func()



t2 = threading.Thread(target=watch)
t2.start()
t3 = threading.Thread(target=func)
t3.start()

root = CTk()

root.title(f"Computer {system_number}")
quit_btn = CTkButton(root, text=f"Quit Computer {system_number}", command=lambda : os._exit(0))
quit_btn.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()
