from customtkinter import *
from tkinter.colorchooser import askcolor
from tkinter import font
from datetime import datetime
from pathlib import Path


class InspectorFrame(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 toggle=True,
                 options,
                 callback,
                 name,
                 messageIP,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.toggle = toggle
        self.messageIP = messageIP
        self.options = options
        self.configure(fg_color="grey10")
        self.w = width
        self.callback = callback
        #self.pack_propagate(False)
        #Example with Sample Values
        #{"Type": "Spinbox", "Heading": "Zoom", "Input Heading": ["X", "Y"]}
        #{"Type": "Slider", "Heading": "Rotation Angle", "Min": -360, "Max": 360, "Step": 1}
        self.text_box = None
        self.name = name
        self.widget = options["_widget"]
        for option in options:

            try:
                val = None
                print(option)
                if option == "_show_type":
                    self.add_show_options(display_text=option, default_text=options[option])
                elif option == "LOG File System Changes":
                    self.add_log_input(display_text="Changes in File System", default_text=options[option])
                elif option == "Send Message":
                    self.add_message_input(display_text="Send Message")



                elif type(options[option]) == int:

                    self.add_int_input(display_text=option, default_text=options[option], callback=lambda val=val, option=option: self.command_({option: val}))
                elif type(options[option]) == str:
                    self.add_str_input(display_text=option, default_text=options[option], callback=lambda val=val, option=option: self.command_({option: val}))
                elif type(options[option]) == tuple and type(options[option][0]) == str and type(options[option][1]) == str:
                    self.add_option_box(options[option], display_text=option, callback=lambda val=val, option=option: self.command_({option: val}))
                elif type(options[option]) == tuple and type(options[option][0]) == bool and type(options[option][1]) == bool:
                    self.add_option_box_bool(options[option], display_text=option, callback=lambda val=val, option=option: self.command_({option: val}))
                elif type(options[option]) == list:
                    print(option)
                    self.add_list_input(display_text=option, default_colors=options[option], callback=lambda val=val, option=option: self.command_({option: val}))
                elif type(options[option]) == tuple and type(options[option][0]) == str and type(options[option][1]) == int:
                    self.add_option_int(font.families(), display_text=option, callback=lambda val=val, option=option: self.command_({option: val}))
                else:
                    print(options[option])

            except KeyError as e:
                print(e)

    def command_(self, kwargs):
        self.options[list(kwargs.keys())[0]] = kwargs[list(kwargs.keys())[0]]

        self.callback(kwargs)

    def get_color(self, func, btn, color_btns):
        color = askcolor()
        if color[1] != None:
            btn.configure(fg_color=color[1])
            print([color_btns[0].cget("fg_color"), color_btns[1].cget("fg_color")])
            func([color_btns[0].cget("fg_color"), color_btns[1].cget("fg_color")])
        print(color)

    def add_option_int(self, fonts, root=None, callback=None, display_text="Display Text", default_num=13, padx=(10, 20)):
        if root == None:
            root = self
        input_frame = CTkFrame(root, width=self.w - 20, height=40*2, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)

        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0), rowspan=2)

        optionmenu = CTkOptionMenu(empty_input_frame, values=fonts, anchor="w", fg_color="#1f538d",
                                   button_color="#14375e", button_hover_color="#1e2c40", dropdown_fg_color="gray20",
                                   dropdown_hover_color="gray28", dropdown_text_color="gray84", text_color="#DCE4EE", width=140, dynamic_resizing=False)
        optionmenu.grid(row=0, column=1, pady=5, padx=padx)
        vcmd = (empty_input_frame.register(self.int_check))

        int_input = CTkEntry(empty_input_frame, validate='all', validatecommand=(vcmd, '%P'), justify="center",
                             fg_color="#343638", border_color="#565B5E", text_color="gray84")
        int_input.grid(row=1, column=1, padx=(10, 20))

        int_input.insert(0, default_num)
        if callback != None:
            int_input.bind("<FocusOut>", lambda e: callback((optionmenu.get(), int(int_input.get()))))
            optionmenu.configure(command=lambda e: callback((optionmenu.get(), int(int_input.get()))))


    def add_list_input(self, default_colors, root=None, callback=None, display_text="Display Text"):
        if root == None:
            root = self
        input_frame = CTkFrame(root, width=self.w - 20, height=40, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0))
        light_color = CTkButton(empty_input_frame, text="", width=64, height=30, hover=False, fg_color=default_colors[0], border_color="White", border_width=2, border_spacing=2)
        light_color.grid(row=0, column=1, padx=(10, 10), pady=5)
        dark_color = CTkButton(empty_input_frame, text="", width=64, height=30, hover=False, fg_color=default_colors[1], border_color="White", border_width=2, border_spacing=2)
        dark_color.grid(row=0, column=2, padx=(0, 20), pady=5)
        light_color.configure(command=lambda light_color=light_color, dark_color=dark_color: self.get_color(callback, light_color, [light_color, dark_color]))
        dark_color.configure(command=lambda dark_color=dark_color, light_color=light_color: self.get_color(callback, dark_color, [light_color, dark_color]))

        #if callback != None:
            #light_color.configure(command=lambda: callback([light_color.cget("fg_color"), dark_color.cget("fg_color")]))
    def add_int_input(self, root=None, callback=None, display_text="Display Text", default_text="", padx=(10, 20)):
        if root == None:
            root = self
        input_frame = CTkFrame(root, width=self.w - 20, height=40, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0))
        vcmd = (empty_input_frame.register(self.int_check))

        int_input = CTkEntry(empty_input_frame, validate='all', validatecommand=(vcmd, '%P'), justify="center", fg_color="#343638", border_color="#565B5E", text_color="gray84")
        int_input.grid(row=0, column=1, padx=padx)
        int_input.insert(0, default_text)
        if callback != None:
            int_input.bind("<FocusOut>", lambda e: callback(int(int_input.get())))
    def add_option_box(self, options, root=None, callback=None, display_text="Display Text", padx=(10, 20), default_text=None):
        if root == None:
            root = self
        input_frame = CTkFrame(root, width=self.w - 20, height=40, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="grey84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0))
        optionmenu = CTkOptionMenu(empty_input_frame, values=options, anchor="center", fg_color="#1f538d", button_color="#14375e", button_hover_color="#1e2c40", dropdown_fg_color="gray20", dropdown_hover_color="gray28", dropdown_text_color="gray84", text_color="#DCE4EE")
        optionmenu.grid(row=0, column=1, pady=5, padx=padx)
        #print(f", fg_color={optionmenu.cget('fg_color')[1]}, button_color={optionmenu.cget('button_color')[1]}, button_hover_color={optionmenu.cget('button_hover_color')[1]}, dropdown_fg_color={optionmenu.cget('dropdown_fg_color')[1]}, dropdown_hover_color={optionmenu.cget('dropdown_hover_color')[1]}, dropdown_text_color={optionmenu.cget('dropdown_text_color')[1]}, text_color={optionmenu.cget('text_color')[1]}")
        if default_text != None:
            optionmenu.set(default_text)
        if callback != None:
            optionmenu.configure(command=lambda e: callback(e))
        print(options)

    def add_option_box_bool(self, options, root=None, callback=None, display_text="Display Text", padx=20, default_text=None):
        if root == None:
            root = self
        print("Running add options box bool function")
        input_frame = CTkFrame(root, width=self.w - 20, height=40, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0))
        optionmenu = CTkOptionMenu(empty_input_frame, values=options, anchor="center", fg_color="#1f538d", button_color="#14375e", button_hover_color="#1e2c40", dropdown_fg_color="gray20", dropdown_hover_color="gray28", dropdown_text_color="gray84", text_color="#DCE4EE")
        #print(f", fg_color={optionmenu.cget('fg_color')}, button_color={optionmenu.cget('button_color')}, button_hover_color={optionmenu.cget('button_hover_color')}, dropdown_fg_color={optionmenu.cget('dropdown_fg_color')}, dropdown_hover_color={optionmenu.cget('dropdown_hover_color')}, dropdown_text_color={optionmenu.cget('dropdown_text_color')}, text_color={optionmenu.cget('text_color')}")
        optionmenu.grid(row=0, column=1, pady=5, padx=padx)
        if default_text != None:
            optionmenu.set(default_text)
        print("Starting If function")
        if callback != None:
            print("Running")
            optionmenu.configure(command=lambda e: callback(e))
            print("Ran")

        print(options)

    def add_str_input(self, root=None, callback=None, display_text="Display Text", default_text="", padx=(10, 20)):
        if root == None:
            root = self

        input_frame = CTkFrame(root, width=self.w - 20, height=40, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, width=10, height=40 - 5, fg_color="grey10")
        empty_input_frame.pack(side="right", padx=10)
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.grid(row=0, column=0, pady=5, padx=(5, 0))

        int_input = CTkEntry(empty_input_frame, justify="center", fg_color="#343638", border_color="#565B5E", text_color="gray84")
        int_input.grid(row=0, column=1, padx=padx)
        int_input.insert(0, default_text)
        int_input.configure(state="disabled")

        if callback != None:
            int_input.bind("<FocusOut>", lambda e: callback(int_input.get()))

    def add_log_input(self, root=None, callback=None, display_text="Display Text", default_text="", padx=(10, 0)):
        if root == None:
            root = self

        input_frame = CTkFrame(root, width=self.w-20, height=300, fg_color="grey10")
        input_frame.pack(padx=10)
        input_frame.grid_propagate(False)
        input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, height=400, fg_color="grey10")
        empty_input_frame.pack(padx=10, fill="x")
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.pack(pady=5)

        int_input = CTkTextbox(empty_input_frame, fg_color="#343638", border_color="#565B5E", text_color="gray84")
        int_input.pack(pady=5, padx=padx, fill="both", expand=True)
        int_input.insert(0.0, default_text)
        int_input.configure(state="disabled")
        self.text_box = int_input

        download_btn = CTkButton(empty_input_frame, text="Download the log file", command=lambda : self.download(self.text_box))
        download_btn.pack(pady=5, padx=padx, fill="x")

    def add_message_input(self, root=None, callback=None, display_text="Display Text", padx=(10, 20)):
        if root == None:
            root = self

        input_frame = CTkFrame(root, width=self.w-20, height=200, fg_color="grey10")
        input_frame.pack(padx=10, expand=True, fill="both", pady=(0, 10))
        #input_frame.grid_propagate(False)
        #input_frame.pack_propagate(False)
        empty_input_frame = CTkFrame(input_frame, height=200, fg_color="grey10")
        empty_input_frame.pack(padx=5, fill="x")
        heading = CTkLabel(empty_input_frame, text=display_text.capitalize(), justify="right", text_color="gray84")
        heading.pack(pady=5)

        int_input = CTkTextbox(empty_input_frame, fg_color="#343638", border_color="#565B5E", text_color="gray84", height=100)
        int_input.pack(pady=5, padx=padx, fill="both", expand=True)



        message_btn = CTkButton(empty_input_frame, text="Send Message", command=lambda int_input=int_input: self.send_message(int_input))
        message_btn.pack(pady=5, padx=padx, fill="x")





    def download(self, text_box):
        text = text_box.get(0.0, "end")
        t = str(datetime.now().strftime('%d-%m-%Y-%H.%M.%S'))
        home_dir = str(Path.home())
        with open(f"{home_dir}/{self.name.decode('utf-8')} -{t}.log", "w") as f:
            f.write(text)
        """
        client.create_notification(
            title="Log Saved Successfully",
            subtitle=f"The Log has been saved in {home_dir}/{self.name.decode('utf-8')}-{t}.log",
        )
        """
        #askokcancel("Info", f"The Log has been saved in {home_dir}/{self.name.decode('utf-8')}-{t}.log")
    def send_message(self, message):
        print(message.get(0.0, "end"), self.messageIP)
        self.messageIP[0].sendto(f"-----MESSAGE----- {message.get(0.0, 'end')}".encode("utf-8"), self.messageIP[1])
        message.delete(0.0, "end")





    def int_check(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def disable(self, state):
        if state == "off":
            for child in self.winfo_children():
                child = child.winfo_children()[0]
                for c in child.winfo_children():

                    print(c)
                    c.configure(state="disabled")

        else:
            for child in self.winfo_children():
                child = child.winfo_children()[0]
                for c in child.winfo_children():
                    print(c)
                    c.configure(state="normal")


class InspectorWidget(CTkScrollableFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.chr = 0
        self.w = width
        self.inspect_frames = []
        self.configure(fg_color="gray16")


    def _toggle_menu(self, event, index, c, options):
        if self.inspect_frames[index][1].toggle == True:
            self.inspect_frames[index][1].toggle = False
            self.inspect_frames[index][1].grid_forget()

        elif self.inspect_frames[index][1].toggle == False:
            self.inspect_frames[index][1].toggle = True
            self.inspect_frames[index][1].grid(row=c, column=0)




    def add_option(self, display_text, options, callback, messageIP):
        global inspect
        new_frame = CTkFrame(self, width=self.w-(2*10), height=50, fg_color="grey10")
        new_frame.grid(column=0, row=self.chr, pady=(10, 0), padx=10)
        new_frame.pack_propagate(False)


        # Adding a new text instead of the default text with the CTKSwitch to add a bind to the text and frame only
        text = CTkLabel(new_frame, text=display_text, text_color="grey84")
        text.pack(side="left", padx=10)
        chr = self.chr
        i = None
        frames = [new_frame, InspectorFrame(self, width=self.w-(2*10), toggle=False, options=options, callback=callback, name=display_text, messageIP=messageIP), display_text]
        self.inspect_frames.append(frames)
        index = self.inspect_frames.index(self.inspect_frames[-1])
        self._toggle_menu(i, index, chr+1, options)

        text.bind("<Button-1>", lambda i=i, index=index, chr=chr, options=options: self._toggle_menu(i, index, chr+1, options))
        new_frame.bind("<Button-1>", lambda i=i, index=index,  chr=chr, options=options: self._toggle_menu(i, index, chr+1, options))
        self.chr += 2

    def clear_frames(self):
        self.inspect_frames[0][1].destroy()
        self.inspect_frames[0][0].destroy()
        self.chr = 0

