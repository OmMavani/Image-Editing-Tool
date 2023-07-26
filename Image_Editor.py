import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os
import cv2

original_img = ''
current_color = ''
prev_color = ''
cv_img = ''
previous_img = []
img_path = ''
img_width = ''
img_height = ''
img = ''
screen_h = ''
screen_w = ''


# allow user to load an image and update global image variables
def browse_img():
    global original_img
    global cv_img
    global img_width
    global img_height
    filename = filedialog.askopenfilename(initialdir="Desktop", title="Select Image File",
                                          filetypes=(
                                          ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("PNG files", "*.png"),
                                          ("GIF files", "*.gif"), ("ICON files", "*.ico"), ("All Files", "*.*")))

    # original_img is created to keep a referene to the unmodified image
    original_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    # this is the image we will modify
    cv_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    img_width = int(original_img.shape[1])
    img_height = int(original_img.shape[0])

    # make sure image will fit in our workspace label frame
    check_img_dimension(img_height, img_width)


# checks to make sure the image dimensions are within our labelFrame size
# if not then the image dimensions are changed
def check_img_dimension(height, width):
    global cv_img
    global img_width
    global img_height
    global screen_h
    global screen_w

    if (width > screen_w):
        percent_decrease = (screen_w - 20) / width
        img_height = img_height * percent_decrease
        img_width = screen_w
        if (img_height > screen_h):
            percent_decrease = (screen_h - 20) / img_height
            img_width = img_width * percent_decrease
            img_height = screen_h
        cv_img = cv2.resize(cv_img, (int(img_width), int(img_height)), interpolation=cv2.INTER_AREA)

    elif (height > screen_h):
        percent_decrease = (screen_h - 20) / height
        img_width = img_width * percent_decrease
        img_height = screen_h
        if (img_width > screen_w):
            percent_decrease = (screen_w - 20) / img_width
            img_height = img_height * percent_decrease
            img_width = screen_w
        cv_img = cv2.resize(cv_img, (int(img_width), int(img_height)), interpolation=cv2.INTER_AREA)


def check_img_color():
    global cv_img
    global current_color
    global prev_color

    if (current_color == "GRAY"):
        prev_color = "GRAY"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
        current_color = "BRG"
    elif (current_color == "HSV"):
        prev_color = "HSV"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_HSV2BGR)
        current_color = "BRG"
    elif (current_color == "HLS"):
        prev_color = "HLS"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_HLS2BGR)
        current_color = "BRG"
    elif (current_color == "LUV"):
        prev_color = "LUV"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_LUV2BGR)
        current_color = "BRG"
    elif (current_color == "YUV"):
        prev_color = "YUV"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_YUV2BGR)
        current_color = "BRG"
    elif (current_color == "LAB"):
        prev_color = "LAB"
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_LAB2RGB)
        current_color = "BRG"


class OpenCVGUI(tk.Tk):

    # Basic view initialization
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, " Image Editor")

        # Setup container for all views
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store mutliple frames
        self.frames = {}
        # For loop to initialize all pages and add to frames dictionary
        for Frame in (MainPage, QuitPage):
            frame = Frame(container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    # Functions that the controller can use:
    # Bring whatever frame 'cont' is to the front of the window so it is visible
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit_GUI(self):
        self.destroy()

    def main(self):
        # Infinite loop to run tkinter until window is closed
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
        self.mainloop()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def open_img():
            global cv_img
            global img
            global prev_color
            browse_img()

            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
            prev_color = "BGR"

            img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x=0, y=0)

            # once an image is loaded activate buttons
            resize_button.config(state="normal")
            rotate_button.config(state="normal")
            blur_button.config(state="normal")
            color_button.config(state="normal")
            revert_button.config(state="normal")
            save_button.config(state="normal")
            undo_button.config(state="normal")

        # opens a new window for resizing image
        def open_resize_window():
            global img_width
            global img_height

            def recalculate():
                global img_width
                global img_height
                p = int(percent.get())
                img_width = img_width * p / 100
                img_height = img_height * p / 100
                resize.config(state="normal")

            def set_new_size():
                global img_width
                global img_height
                img_width = int(width.get())
                img_height = int(height.get())
                resize.config(state="normal")

            def resize_img():
                global cv_img
                global img
                global previous_img

                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

                cv_img = cv2.resize(cv_img, (int(img_width), int(img_height)), interpolation=cv2.INTER_AREA)

                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def back():
                top.destroy()

            top = tk.Toplevel()
            top.title("Resize Image")

            img_info = tk.Label(top,text="Image Dimensions\n Height: " + str(img_height) + "\nWidth: " + str(img_width))
            img_info.pack()

            pixel_safe = tk.LabelFrame(top, text="Pixel Safe", borderwidth=2, width=100)
            pixel_safe.pack(fill="both", expand="yes", ipadx=30, ipady=20, padx=10, pady=5)

            label4 = tk.Label(pixel_safe, text="Percentage:")
            label4.pack(side=tk.LEFT, padx=10, pady=10)

            percent = tk.StringVar()
            ent = tk.Entry(pixel_safe, textvariable=percent)
            ent.pack(side=tk.LEFT, padx=10, pady=10)

            recalculate = ttk.Button(pixel_safe, text="Recalulate", width=15, command=recalculate)
            recalculate.pack(side=tk.LEFT, padx=10, pady=10)

            custom = tk.LabelFrame(top, text="Custom", borderwidth=2, width=100)
            custom.pack(fill="both", expand="yes", ipadx=30, padx=10, pady=5)

            new_h = tk.Label(custom, text="New Height:")
            new_h.grid(row=0, column=0, padx=10, pady=10)

            height = tk.StringVar()
            height_ent = tk.Entry(custom, textvariable=height)
            height_ent.grid(row=0, column=1, padx=10, pady=10)

            width = tk.StringVar()
            new_w = tk.Label(custom, text="New Width:")
            new_w.grid(row=1, column=0, padx=10, pady=10)

            width_ent = tk.Entry(custom, textvariable=width)
            width_ent.grid(row=1, column=1, padx=10, pady=10)

            set_size = ttk.Button(custom, text="Set New Dimensions", width=15, command=set_new_size)
            set_size.grid(row=1, column=2, padx=10, pady=10)

            resize = tk.Button(top, text="Resize", width=15, state="disabled", command=resize_img)
            resize.pack(side=tk.TOP, padx=10, pady=10)

            back_button = ttk.Button(top, text="Back", width=4, command=back)
            back_button.pack(pady=3)

        def open_rotate_window():
            global cv_img
            global img_height
            global img_width

            top = tk.Toplevel()
            frame = tk.LabelFrame(top, text="Rotate", width=290, height=170)
            frame.pack(padx=10, pady=10)
            top.title("Rotate Image")

            def rotate_right():
                global cv_img
                global img
                global previous_img
                global img_width
                global img_height
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
                img_width = int(cv_img.shape[1])
                img_height = int(cv_img.shape[0])
                check_img_dimension(img_height, img_width)

                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)

            def flip_vertical():
                global cv_img
                global img
                global previous_img
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

                cv_img = cv2.flip(cv_img, 0)

                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)

            def flip_horizontal():
                global cv_img
                global img
                global previous_img
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

                cv_img = cv2.flip(cv_img, 1)

                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)

            def rotate_left():
                global cv_img
                global img
                global previous_img
                global img_width
                global img_height

                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                img_width = int(cv_img.shape[1])
                img_height = int(cv_img.shape[0])
                check_img_dimension(img_height, img_width)

                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)

            def back():
                top.destroy()

            rotate_label = ttk.Label(frame, text="Rotate 90 Degrees")
            rotate_label.place(x=90, y=18)

            rotate_l_button = ttk.Button(frame, text="Left", width=8, command=rotate_left)
            rotate_l_button.place(x=30, y=38)

            rotate_r_button = ttk.Button(frame, text="Right", width=8, command=rotate_right)
            rotate_r_button.place(x=150, y=38)

            flip_label = ttk.Label(frame, text="Flip")
            flip_label.place(x=132, y=80)

            flip_button = ttk.Button(frame, text="Vertical", width=8, command=flip_vertical)
            flip_button.place(x=30, y=100)

            flip_button = ttk.Button(frame, text="Horizontal", width=8, command=flip_horizontal)
            flip_button.place(x=150, y=100)

            back_button = ttk.Button(top, text="Back", width=4, command=back)
            back_button.pack(pady=3)

        def blur_img():
            global cv_img
            global img
            global previous_img
            previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

            cv_img = cv2.blur(cv_img, (5, 5))

            img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x=0, y=0)

        def open_change_color():
            global cv_img
            global img

            top = tk.Toplevel()
            top.title("Change Image Color")

            def gray():
                global cv_img
                global img
                global previous_img
                global current_color

                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                prev_color = "GRAY"
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                current_color = "GRAY"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def hsv(): # hue,saturation,value
                global cv_img
                global img
                global previous_img
                global current_color

                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
                current_color = "HSV"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def lab(): # luminance, a=> green to red, b=> blue to yellow
                global cv_img
                global img
                global previous_img
                global current_color
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
                current_color = "LAB"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def luv(): # luminance, uv=> chromaticity
                global cv_img
                global img
                global previous_img
                global current_color
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LUV)
                current_color = "LUV"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def hls(): # hue saturation luminance
                global cv_img
                global img
                global previous_img
                global current_color
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HLS)
                current_color = "HLS"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def yuv():
                global cv_img
                global img
                global previous_img
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2YUV)
                current_color = "YUV"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def convert_to_bw():
                global cv_img
                global img
                global previous_img
                previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
                check_img_color()

                min = int(min_threshold.get())
                max = int(max_threshold.get())
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                ret, cv_img = cv2.threshold(cv_img, min, max, cv2.THRESH_BINARY)

                current_color = "GRAY"
                img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0)
                top.destroy()

            def back():
                top.destroy()

            color_frame = tk.LabelFrame(top, text="Color Options", borderwidth=2)
            color_frame.pack(fill="both", expand="yes", padx=10, pady=10)

            gray_button = ttk.Button(color_frame, text="GRAY", command=gray)
            gray_button.grid(row=0, column=0, padx=10, pady=10)

            hsv_button = ttk.Button(color_frame, text="HSV", command=hsv)
            hsv_button.grid(row=1, column=0, padx=10, pady=10)

            lab_button = ttk.Button(color_frame, text="LAB", command=lab)
            lab_button.grid(row=0, column=1, padx=10, pady=10)

            luv_button = ttk.Button(color_frame, text="LUV", command=luv)
            luv_button.grid(row=1, column=1, padx=10, pady=10)

            hls_button = ttk.Button(color_frame, text="HLS", command=hls)
            hls_button.grid(row=2, column=0, padx=10, pady=10)

            yuv_button = ttk.Button(color_frame, text="YUV", command=yuv)
            yuv_button.grid(row=2, column=1, padx=10, pady=10)

            bw_frame = tk.LabelFrame(top, text="Black and White Options", borderwidth=2)
            bw_frame.pack(fill="both", expand="yes", padx=10, pady=10)

            frame = tk.Frame(bw_frame)
            frame.grid(row=0, column=0)

            frame2 = tk.Frame(bw_frame)
            frame2.grid(row=1, column=0)

            frame3 = tk.Frame(bw_frame)
            frame3.grid(row=2, column=0)

            frame4 = tk.Frame(bw_frame)
            frame4.grid(row=3, column=0)

            threshold_label = tk.Label(frame, text="Enter Values For Threshold:")
            threshold_label.pack(pady=5)

            min_label = tk.Label(frame2, text="Min:")
            min_label.pack(side=tk.LEFT, padx=2, pady=5)

            min_threshold = tk.StringVar()
            min_entry = tk.Entry(frame2, textvariable=min_threshold, width=12)
            min_entry.pack(side=tk.LEFT)

            max_label = tk.Label(frame3, text="Max:")
            max_label.pack(side=tk.LEFT, padx=2, pady=5)

            max_threshold = tk.StringVar()
            max_entry = tk.Entry(frame3, textvariable=max_threshold, width=12)
            max_entry.pack(side=tk.LEFT)

            bw_button = ttk.Button(frame4, text="Convert to Black and White", command=convert_to_bw)
            bw_button.pack(side=tk.BOTTOM, padx=5, pady=5)

            back_button = ttk.Button(top, text="Back", width=4, command=back)
            back_button.pack(pady=3)

        def undo():
            global cv_img
            global img_height
            global img_width
            global img
            check_img_color()
            cv_img = previous_img.pop(-1)

            img_width = int(cv_img.shape[1])
            img_height = int(cv_img.shape[0])
            check_img_dimension(img_height, img_width)

            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x=0, y=0)

        def revert_img():
            global cv_img
            global img_height
            global img_width
            global img
            global previous_img

            check_img_color()
            previous_img.append(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

            cv_img = original_img
            img_width = int(original_img.shape[1])
            img_height = int(original_img.shape[0])
            check_img_dimension(img_height, img_width)

            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x=0, y=0)

        def save_img():
            global cv_img
            filename = filedialog.asksaveasfilename(initialdir="Desktop", title="Save Image",
                                                    filetypes=(("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"),
                                                               ("PNG files", "*.png"),
                                                               ("GIF files", "*.gif")))
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, cv_img)
            messagebox.showinfo("Image Saved",
                                "Image has been saved as " + os.path.basename(filename) + " successfully")

        # def open_histogram():
        #     def back():
        #         top.destroy()
        #     top = tk.Toplevel()
        #     frame = tk.LabelFrame(top, text="Histogram", width=290, height=170)
        #     frame.pack(padx=10, pady=10)
        #     top.title("Histogram")
        #     hist= cv2.calcHist
        #     hist1 = cv2.calcHist([previous_img], [0], None, [256], [0, 256])
        #     hist2 = cv2.calcHist([previous_img], [1], None, [256], [0, 256])
        #     hist3 = cv2.calcHist([previous_img], [2], None, [256], [0, 256])
        #     plt.subplot(221), plt.imshow(previous_img)
        #     plt.subplot(222), plt.plot(hist1), plt.plot(hist2), plt.plot(hist3)
        #     fig = Figure(figsize=(5, 5),dpi=100)
        #     canvas = FigureCanvasTkAgg(fig,master = top)
        #     back_button = ttk.Button(top, text="Back", width=4, command=back)
        #     back_button.pack(pady=3)

        def quit():
            controller.show_frame(QuitPage)

        main_background = tk.Frame(self, bg="#282828")
        main_background.pack(expand=True,fill="both")
        # expand aligns text in center on the other hand fill fills the background

        label = tk.Label(main_background, text="Image Editor", bg='#282828', fg='white', font="comicsansms 30 bold")
        label.grid(row=0, column=1, columnspan=20, pady=10, padx=10, sticky="WE")

        getting_started = tk.LabelFrame(main_background, text="Getting Started",fg='white',  bg='#535353',font="comicsansms 10 bold", relief=tk.SUNKEN)
        getting_started.grid(row=1, column=0, columnspan=10, ipadx=30, padx=20, pady=20, sticky="NSEW")

        open_button = ttk.Button(getting_started, text="Open A New Image", width=18, command=open_img)
        open_button.pack(anchor="center", pady=5)

        image_ops = tk.LabelFrame(main_background, text="Image Operations", bg='#535353', fg='white', relief=tk.SUNKEN, font="comicsansms 10 bold")
        image_ops.grid(row=2, rowspan=49, column=0, columnspan=10, padx=20, pady=20, sticky="NSEW")

        resize_button = ttk.Button(image_ops, text="Resize Image", width=18, state="disabled",
                                   command=open_resize_window)
        resize_button.pack(pady=5)

        rotate_button = ttk.Button(image_ops, text="Rotate Image", width=18, state="disabled",
                                   command=open_rotate_window)
        rotate_button.pack(pady=5)

        blur_button = ttk.Button(image_ops, text="Blur Image", width=18, state="disabled", command=blur_img)
        blur_button.pack(pady=5)

        color_button = ttk.Button(image_ops, text="Change Colorspace", width=18, state="disabled",
                                  command=open_change_color)
        color_button.pack(pady=5)

        quit_button = ttk.Button(image_ops, text="Quit", width=18, command=quit)
        quit_button.pack(side=tk.BOTTOM, pady=5)

        save_button = ttk.Button(image_ops, text="Save Image", width=18, state="disabled", command=save_img)
        save_button.pack(side=tk.BOTTOM, pady=5)

        revert_button = ttk.Button(image_ops, text="Revert To Original", width=18, state="disabled", command=revert_img)
        revert_button.pack(side=tk.BOTTOM, pady=5)

        undo_button = ttk.Button(image_ops, text="Undo Last Operation", width=18, state="disabled", command=undo)
        undo_button.pack(side=tk.BOTTOM, pady=5)

        screen_height = int(main_background.winfo_screenheight() * .4)
        screen_width = int(main_background.winfo_screenwidth() * .38)

        workspace = tk.LabelFrame(main_background, text="Workspace", bg='FloralWhite', borderwidth=3, relief=tk.SUNKEN, font="comicsansms 10 bold")
        workspace.grid(row=1, rowspan=50, column=10, columnspan=10, ipadx=screen_width, ipady=screen_height, padx=20,
                       pady=20, sticky="NSEW")

        global screen_h
        global screen_w
        screen_h = int(workspace.winfo_screenheight() * .75)
        screen_w = int(workspace.winfo_screenwidth() * .75)


class QuitPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text="Thanks for using Image Editor", font=("Adobe Arabicy", 20, "bold"))
        label1.pack(padx=140, pady=140)
        label2 = tk.Label(self, text="20BCE081 : DARSHIL GOTI\n20BCE082   :    MEET GOTI\n20BCE157   :   OM MAVANI\n",
                          font=("Lucida Calligraphy", 25, "bold"))
        label2.pack(padx=10, pady=10)

        button = ttk.Button(self, text="EXIT", command=controller.quit_GUI)
        button.pack(padx=10, pady=10)


app = OpenCVGUI()
app.main()