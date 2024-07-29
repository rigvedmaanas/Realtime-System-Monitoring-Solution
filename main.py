import numpy
import zfec
from customtkinter import *
from Inspector import InspectorWidget
import socket
import cv2
import threading
from CTkSlideView import CTkSlideView
from PIL import Image, ImageTk
import time
import os
import sys

print(os.listdir())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

print(resource_path("placeholder.png"))

def force_exit():
    root.destroy()
    os._exit(0)

def disconnected_check():
    while True:

        for computer in list(ComputerManager.computers.keys()):
            if ComputerManager.computers[computer].last_image == None:
                pass
            elif time.time() - ComputerManager.computers[computer].last_image > 5:
                print(f"We think that {ComputerManager.computers[computer].name} is disconnected")
                ComputerManager.computers[computer].display.configure(text="Disconnected")
                ComputerManager.computers[computer].last_image = None


        time.sleep(10)

DISCONNECTED = False
def receiver():
    global FrameController, DISCONNECTED
    time.sleep(2)
    while True:



        data, addr = s.recvfrom(200000)
        val = ComputerManager.check_with_addr(addr)

        if val == None:
            print(f"New Connection {addr}")

            data2, addr2 = s.recvfrom(10000)
            print(data2.decode())
            check = False
            for key in list(ComputerManager.computers.keys()):
                if ComputerManager.computers[key].name.decode("utf-8") == data2.decode("utf-8"):
                    print("Found the disconnected person")
                    ComputerManager.computers[key].display.configure(text="")
                    k = ComputerManager.add(IP=addr, frame=ComputerManager.computers[key].frame, display=ComputerManager.computers[key].display, name=ComputerManager.computers[key].name)

                    val2 = ComputerManager.check_with_addr(addr)
                    val2.messageIP = (addr[0], int(data.decode("utf-8")))
                    print(val2.messageIP, data.decode("utf-8"))
                    val2.logs = ComputerManager.computers[key].logs
                    addr = val2.IP
                    e = None
                    val2.display.bind("<Button-1>", lambda e=e, addr=addr: change_properties(addr))

                    message.sendto("Hello Welcome To ITLMS".encode("utf-8"), val2.messageIP)
                    callback_show(slide_menu.current_frame)
                    check = True
                    break
            if check == False:
                FrameController.add_frame(addr, data2)
                val2 = ComputerManager.check_with_addr(addr)
                val2.messageIP = (addr[0], int(data.decode("utf-8")))
                print(val2.messageIP, data.decode("utf-8"))

                message.sendto("Hello Welcome To ITLMS".encode("utf-8"), val2.messageIP)
                callback_show(slide_menu.current_frame)



        else:
   
            img = val.add_byte(data)

            if img != None:
                width, height = img.size
                im_pil = img
                if width == 800 and DISCONNECTED == False:
              
                    photo = ImageTk.PhotoImage(im_pil)
                    FullScreenDisplay.configure(image=photo)
                    FullScreenDisplay.image = photo
                    
                    val.display.configure(text="Opened in Full Screen")
                else:
                    photo = ImageTk.PhotoImage(im_pil)

                    val.display.configure(image=photo)
                    val.display.image = photo

                    if val.display.cget("text") != "":
                        val.display.configure(text="")





s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200000)
s.bind(("0.0.0.0", 7387))

message = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 200000)
message.bind(("0.0.0.0", 4000))

def recieve_logging():
    time.sleep(3)
    while True:

        data, addr = message.recvfrom(100000)
        val = data.decode("utf-8")
        if val.startswith("----13----"):
            log = val[11::]
            print(log)
            for computer in list(ComputerManager.computers.keys()):
                if ComputerManager.computers[computer].messageIP == addr:
                    print("Found addr", ComputerManager.computers[computer].messageIP)
                    ComputerManager.computers[computer].logs += log + "\n"
                    print(ComputerManager.computers[computer].logs)
                    for property in Inspector.inspect_frames:

                        if property[2] == ComputerManager.computers[computer].name:
                            txtbox = property[1].text_box
                            print(txtbox.master, txtbox)
                            try:
                                txtbox.configure(state="normal")
                                txtbox.delete(0.0, "end")
                                txtbox.insert(0.0, ComputerManager.computers[computer].logs)
                                txtbox.canvas.yview_moveto(1)
                                txtbox.configure(state="disabled")
                            except Exception as e:
                                print(e)


t1 = threading.Thread(target=receiver)
t1.start()

t2 = threading.Thread(target=recieve_logging)
t2.start()



class DisplayWidgetControl:
    def __init__(self, slide_view, max_frame_per_slide):
        self.slide_view = slide_view
        self.num = 0
        self.max_frame_per_slide = max_frame_per_slide

        self.num_slide = 1


    def add_frame(self, addr, name):

        if self.num % (self.max_frame_per_slide-1) == 0:

            self.current_slide = self.slide_view.create_tab()
            self.fake_display_frame = CTkFrame(self.current_slide,
                                               fg_color="transparent")  # For centering the displayed video frames
            self.fake_display_frame.place(anchor="center", relx=0.5, rely=0.5)

        frame = CTkFrame(self.fake_display_frame, width=300, height=168, fg_color="grey10")
        frame.grid(row=0, column=self.num % (self.max_frame_per_slide-1), padx=10, pady=10)

        display = CTkLabel(frame, text="")
        display.place(relx=0.5, rely=0.5, anchor=CENTER)
        id = ComputerManager.add(IP=addr, frame=frame, display=display, name=name)
        e = None
        display.bind("<Button-1>", lambda e=e, id=id: change_properties(id))

        self.num += 1



class Computer_Manager:
    def __init__(self):
        self.computers = {}
        self.id = 0
    def add(self, **kwargs):

  
        self.computers[kwargs["IP"]] = Computer(self.id, **kwargs)

        self.id += 1
        return kwargs["IP"]
    def check_with_addr(self, addr):
        try:
            return self.computers[addr]
        except KeyError as e:
            print(e)
            return None



class Computer:
    def __init__(self, id, IP, frame, display, name):
        self.id = id
        self.IP = IP
        self.frame = frame
        self.display = display
        self.name = name
        self.messageIP = None
        self.logs = ""
        self.bytes = []
        self.last_image = time.time()

    def add_byte(self, byte):
        self.bytes.append(byte)

        return self.decode_img()
    def decode_img(self):
        if len(self.bytes) >= 15:
            try:
                decoder = zfec.Decoder(k=15, m=15)
                blocknums = tuple(range(15))

                decoded_data = decoder.decode(self.bytes, blocknums)
                

                v = numpy.frombuffer(b"".join(decoded_data), numpy.uint8)

                data2 = cv2.imdecode(v, -1)
                im_pil = Image.fromarray(data2)
                self.bytes = []

                return im_pil
            except Exception as e:
                print(e, "Decryption")
                self.bytes = []
            finally:
                self.last_image = time.time()


        else:
            return None
def change_properties(id):
    global ComputerManager, DISCONNECTED
    DISCONNECTED = False
    computer = ComputerManager.computers[id]
    try:
        Inspector.clear_frames()
    except IndexError as e:
        print(e)
    Inspector.add_option(display_text=computer.name, options={"_widget": None, "IP": computer.IP[0], "LOG File System Changes": computer.logs, "Send Message": ""}, callback=lambda x: print(x), messageIP=[message, ComputerManager.computers[id].messageIP])
    for key in list(ComputerManager.computers.keys()):
        computer2 = ComputerManager.computers[key]
        message.sendto("StopFullScreen".encode("utf-8"), computer2.messageIP)
    if computer.display.cget("text") == "Disconnected":
        img = Image.open(resource_path("placeholder.png"))

        photo = ImageTk.PhotoImage(img)
        FullScreenDisplay.configure(image=photo)
        FullScreenDisplay.image = photo
    print(id)
    print(f"Sending To {computer.messageIP}")
    message.sendto("FullScreen".encode("utf-8"), computer.messageIP)

def change_properties_only(id):
    global ComputerManager, DISCONNECTED
    DISCONNECTED = True
    computer = ComputerManager.computers[id]
    try:
        Inspector.clear_frames()
    except IndexError as e:
        print(e)
    Inspector.add_option(display_text=computer.name, options={"_widget": None, "IP": computer.IP[0], "LOG File System Changes": computer.logs, "Send Message": ""}, callback=lambda x: print(x), messageIP=[message, ComputerManager.computers[id].messageIP])
    print("Updated")
    for key in list(ComputerManager.computers.keys()):
        computer2 = ComputerManager.computers[key]
        message.sendto("StopFullScreen".encode("utf-8"), computer2.messageIP)








ComputerManager = Computer_Manager()

def callback_show(tab):
    global ComputerManager
    
    keys = ComputerManager.computers.keys()

    for key in list(keys):
        computer = ComputerManager.computers[key]
        if computer.frame.master.master == tab[0]:
            print("Visible")
            print(computer.messageIP)
            message.sendto("Share".encode("utf-8"), computer.messageIP)
        else:
            print("Not Visible")
            message.sendto("DontShare".encode("utf-8"), computer.messageIP)



root = CTk()
root.geometry("1920x1080")
root.title("Real Time System Monitoring Solution")
root.protocol("WM_DELETE_WINDOW", force_exit)
display_frame = CTkFrame(root, width=1200)
display_frame.pack(side="left", padx=20, pady=20, fill="y")
display_frame.pack_propagate(False)


slide_menu = CTkSlideView(display_frame, height=300, width=1200, check_callback=callback_show)
slide_menu.pack(side="top", padx=10, pady=(10, 0))

FullScreenFeed = CTkFrame(display_frame, width=1200)
FullScreenFeed.pack(side="bottom", fill="y", expand=True, padx=10, pady=10)

FullScreenDisplay = CTkLabel(FullScreenFeed, text="")
FullScreenDisplay.place(relx=0.5, rely=0.5, anchor=CENTER)

FrameController = DisplayWidgetControl(slide_menu, 4)



properties_frame = CTkFrame(root)
properties_frame.pack(side="right", padx=(0, 20), pady=20, fill="both", expand=True)


Inspector = InspectorWidget(properties_frame, width=640)
Inspector.pack(fill="both", side="right", expand=True, padx=10, pady=10)



disconnector = threading.Thread(target=disconnected_check)
disconnector.start()

root.mainloop()
