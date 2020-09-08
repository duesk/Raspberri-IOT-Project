from tkinter import *

cancel = False

def  close(win):
    global cancel
    cancel = True
    win.destroy()


def CancelWindow(win, root):
    global cancel

    #variables de stylo
    title_size_font = 16
    content_size_font = 12
    #color_theme = "snow"
    color_button = "deepskyblue3"
    color_text_button = "gray99"
    font = "Garuda"
    color_font_activate_button = "gray25"
    color_bg_activate_button = "deep sky Blue"



    #win.title('Peligro')
    win.minsize(800, 480)
    win.attributes("-type","splash")
    win.attributes("-zoomed", True)
    win.fullScreenState = True
    win.attributes('-fullscreen')
    win.focus_force()
    win.resizable(0,0)

    message = "¿Seguro que deseas cancelar la impresion?"
    #Label(win, text=message).pack()
    frame = Frame(win,pady = 100, padx = 100)
    Label(frame, text=message).pack()
    Button(frame, text="Si", command= lambda : close(win),activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")

    Label(frame, text = "   ", font = (font ,content_size_font)).pack(side = "left",pady = 15)

    Button(frame, text="No", command=win.destroy,activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")
    frame.pack()
    root.wait_window(win)
    return cancel


