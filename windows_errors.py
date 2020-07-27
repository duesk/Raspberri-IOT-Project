from tkinter import *


#variables de stylo
title_size_font = 16
content_size_font = 12
color_theme = "snow"
color_button_w = "firebrick1"
color_text_button_w = "gray12"
font = "Garuda"
color_font_activate_button_w = "gray8"
color_bg_activate_button_w = "firebrick3"

color_button = "deepskyblue3"
color_text_button = "gray99"
font = "Garuda"
color_font_activate_button = "gray25"
color_bg_activate_button = "deep sky Blue"

response = "hola"

def kill_error(list_error,root):
    root1 = Tk()
    root1.title("Error")
    root1.minsize (100,150)
    root1.resizable(0,0)
    root1.config(bg =color_theme)

    frame = Frame(root1, pady = 15,padx = 15,bg = color_theme )
    Label(frame,text = "Error detectado: ",font = (font,content_size_font),bg = color_theme).pack()

    for i in range(0,len(list_error)):
        error = list_error[i]
        error = error[0:len(error)-2]
        Label(frame,text = error, font = (font,content_size_font),bg = color_theme).pack()
        print("error: " + error)
    frame.pack()

    Button(frame, text = "Aceptar" , activebackground = color_bg_activate_button_w, activeforeground = color_font_activate_button_w, 
            font = (font ,content_size_font),bg = color_button_w, fg = color_text_button_w, command = root1.destroy).pack()

    root1.mainloop()
    root.destroy()




