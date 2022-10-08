import os
import time
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from PIL import ImageTk, Image
import GifToFrames as gtf


button_padding = {'padx': 4, 'pady': 4}
scrollbar_color = {"bg": "#d9d9d9", "troughcolor": "#d9d9d9","highlightcolor": "#d9d9d9" 
                   ,"activebackground":"light steel blue", "highlightbackground":"light steel blue"}  
scrollbar_width = 10

canvas_Scheme = {"background": "#2F2F2F", "borderwidth":1,"highlightthickness":1, "highlightbackground":"black","relief":"sunken"}
frame_Scheme = {"background": "#2F2F2F", "borderwidth":0}

main_color = "#2F2F2F"
main_color_light = "#404040"

preview_thumbnail_width=96;
preview_thumbnail_height=96;
geometry_width, geometry_height = (332, 360)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Gif to Frames")
        self.geometry(f"{geometry_width}x{geometry_height}")
        # set min size
        self.minsize(geometry_width, geometry_height)
        self.resizable(False, False)


        self.configure_style()
        self.create_menu_bar()
        


        self.preview_images = []
        self.raw_images = []
        
        self.thumbnails = []
        self.max_cols = int(geometry_width/preview_thumbnail_width)
        self.filename = "file_name"
        self.current_preview_width=0
        self.current_preview_height=0
        
    
        
        # # create a label
        label = ttk.Label(self, text="Gif to Frames", font=("Arial", 16),style="BW.TLabel", foreground="white", background="#404040")
        label.grid(row=0, column=1,  sticky="news",pady=0)

        self.initial_row = 1
        current_col = 0
        current_row = self.initial_row 
        
        self.img_preview_frame = tk.Frame(self, width=preview_thumbnail_width,**canvas_Scheme)
        self.img_preview_frame.grid(row=0, column=0,  sticky="wn",**button_padding)
        
        self.img_preview_frame.grid_columnconfigure(0, weight=1)
        self.img_preview_frame.grid_rowconfigure(0, weight=1)

        self.img_preview_canvas = tk.Canvas(self.img_preview_frame, width=96, height=96,background="#2F2F2F",highlightthickness=0,borderwidth=0)
        self.img_preview_canvas.grid(row=0, column=0, columnspan=1, sticky="ewsn")
        
        self.preview_image_frame = tk.Frame(self.img_preview_canvas,width=preview_thumbnail_width,**frame_Scheme)
        
        self.img_preview_img = ttk.Label(self.preview_image_frame, image=None,**frame_Scheme)
        
        self.img_preview_img.grid(row=0, column=0, sticky="ewsn",ipadx=0,ipady=0)
        
        self.img_preview_canvas.create_window((0, 0), window=self.preview_image_frame, anchor="nw", tags="IMG_PREVIEW")
        
        #####
        
        self.scroll_frame = tk.Frame(self,**canvas_Scheme)
        self.scroll_frame.grid(row=current_row, column=current_col, columnspan=self.max_cols, sticky="ews",**button_padding)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.scroll_frame.grid_columnconfigure(2, weight=1)
        self.scroll_frame.grid_rowconfigure(0, weight=1)
        self.scroll_frame.grid_rowconfigure(1, weight=1)
        self.scroll_frame.grid_rowconfigure(2, weight=1)

        self.scroll_canvas = tk.Canvas(self.scroll_frame,  height=96*2,background="#2F2F2F",highlightthickness=0,borderwidth=0)
        self.scroll_canvas.grid(row=3, column=0, columnspan=3, sticky="ews")
        #self.scroll_canvas.configure(background="white")
        #create a frame to contain the images
        self.image_frame = tk.Frame(self.scroll_canvas,**frame_Scheme)
            
        #create a scrollbar horizontal and vertical 
        self.scroll_x = ttk.Scrollbar(self.scroll_frame, orient="horizontal", command=self.scroll_canvas.xview)
        self.scroll_y = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.scroll_canvas.yview)

        # scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_y.grid(row=3, column=3, sticky="ns")
        #bottom scroller
        self.scroll_x.grid(row=4, column=0, columnspan=3, sticky="ew")
        # scroll_bar.grid(row=3, column=3, sticky="ns")
        #configure the scrollable canvas to use the scrollbar
        self.scroll_canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        #add the scrollbar to the canvas
        # self.scroll_canvas.configure(yscrollcommand=scroll_bar.set)
        #add the frame to the canvas
        self.scroll_canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", self.on_frame_resized)
        
        

    def configure_style(self):
        self.configure(background=main_color_light)
        self.style = ttk.Style(self)
        # self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12,'bold'),foreground="#404040",bgcolor="red")
        self.style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="yellow")
        self.style.configure("Horizontal.TScrollbar",background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                troughcolor="gray", bordercolor="blue", arrowcolor="white")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
    def create_menu_bar(self):
        
        self.menu_bar = tk.Menu(self)
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Open", command=self.on_file_open)
        self.menu_file.add_command(label="Export", command=self.on_export)
        self.menu_file.add_command(label="Export Sheet", command=self.on_export_sheet)

        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.exit_button)
        self.menu_bar.add_cascade(label="File", menu=self.menu_file)
        self.menu_help = tk.Menu(self.menu_bar, tearoff=0)  
        self.menu_help.add_command(label="About", command=self.about_button)
        self.config(menu=self.menu_bar)
        #disable export options if raw images is empty or null
        self.menu_file.entryconfig("Export", state="disabled")
        self.menu_file.entryconfig("Export Sheet", state="disabled")



    def on_img_loaded(self):
        width,height,imgs = gtf.get_frames(self.filename)
        self.current_preview_width=width
        self.current_preview_height=height
        #check if imgs is empty or null
        self.raw_images = imgs
        if imgs is None or len(imgs) == 0:
            return
        self.menu_file.entryconfig("Export", state="normal")
        self.menu_file.entryconfig("Export Sheet", state="normal")
        self.preview_images=[]
        for img in imgs:
            img.thumbnail((preview_thumbnail_width,preview_thumbnail_height), Image.ANTIALIAS)
            self.preview_images.append(ImageTk.PhotoImage(img))
        
        self.thumbnails = []
        for i in range(len(self.preview_images)):
            self.thumbnails.append(ttk.Label(self.image_frame, image=self.preview_images[i],**frame_Scheme))
            
        self.refresh_preview_area()
        self.on_gif_preview()
    
    def refresh_preview_area(self):
        current_col = 0
        current_row = self.initial_row 
        for i in range(len(self.preview_images)):
            self.thumbnails[i].grid(row=current_row, column=current_col, sticky="nw")
            current_col += 1
            if current_col == self.max_cols:
                current_col = 0
                current_row += 1

    def on_gif_preview(self):
        current_frame = 0;
        time_between_frames = 0.1
        last_time = time.time()
        while True:
            if time.time() < last_time + time_between_frames:
                continue
            current_preview = self.preview_images[current_frame]
            self.img_preview_img.configure(image=current_preview)
            self.img_preview_img.image = current_preview
            self.img_preview_img.update()
            current_frame =  (current_frame + 1) % len(self.preview_images)
            last_time = time.time()


    def on_frame_resized(self,value):
        self.max_cols = int(value.width/preview_thumbnail_width)
        self.refresh_preview_area()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        
    def on_file_open(self):
        # get directory and filename from dialog box
        path = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("GIF files", "*.gif"), ("all files", "*.*")))
        # split filename into directory and filename
        self.filename = path
        self.on_img_loaded()
        
    def on_export(self):
        #trim file extension from filename
        
        gtf.export_frames(self.raw_images,self.filename,"/output")
        #show file directory
        dir, file_name = os.path.split(self.filename)
        filename = dir+"/output/"
        path = os.path.realpath(filename)
        os.startfile(path)

    def on_export_sheet(self):
        gtf.make_frames(self.filename,"/output")
        #show file directory
        dir, file_name = os.path.split(self.filename)
        filename = dir+"output/"
        path = os.path.realpath(filename)
        os.startfile(path)
        
    def exit_button(self):
        self.destroy()
        return

    def about_button(self):
        messagebox.showinfo("About", "Gif to Frames")
        return



app = Application()
app.mainloop()
 