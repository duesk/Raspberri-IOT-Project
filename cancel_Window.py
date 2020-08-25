from tkinter import *

def  close(win,cancel):
    cancel = True
    win.destroy()


def CancelWindow(win):

    #win.title('Peligro')
    win.minsize(400, 150 )
    win.attributes("-type","splash")
    win.attributes("-zoomed", True)

    cancel = False


    message = "¿Seguro que deseas cancelar la impresion?"
    Label(win, text=message).pack()
    frame = Frame(win)
    Button(frame, text="Si", command= lambda : close(win,cancel),activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")

    Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

    Button(frame, text="No", command=win.destroy,activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")
    frame.pack()
    root.wait_window(selectWindow)
    return cancel
