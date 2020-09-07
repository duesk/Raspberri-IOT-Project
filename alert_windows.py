from tkinter import *

respuesta = False


def delete(ask_window ):
    global respuesta
    respuesta = True
    ask_window.destroy()

def ask_delete(ask_window,select_window,file_name):
    global respuesta

        #variables de stylo
    title_size_font = 16
    content_size_font = 12
    color_theme = "snow"
    color_button = "deepskyblue3"
    color_text_button = "gray99"
    font = "Garuda"
    color_font_activate_button = "gray25"
    color_bg_activate_button = "deep sky Blue"

    #ask_window.title("Colibrgyti 3D")

    ask_window.attributes("-type","splash")
    ask_window.attributes("-zoomed", True)
    ask_window.fullScreenState = True
    ask_window.attributes('-fullscreen')
    ask_window.focus_force()
    ask_window.resizable(0,0)

    ask_window.minsize(800, 480 )
    #ask_window.attributes("-type","splash")
    #ask_window.attributes("-zoomed", True)
    ask_window.config(bg = color_theme)
    ask_window.protocol("WM_DELETE_WINDOW", lambda : ask_window.destroy()) #accion al cerrar la ventana 
    ask_window.columnconfigure(3,weight=1)#configura la columna para que se estire
    ask_window.columnconfigure(0,weight=1)#configura la columna para que se estire
    ask_window.rowconfigure(0,weight=1)
    ask_window.rowconfigure(3,weight=1)


    alert_text= "Seguro que quieres borrar el archivo" + file_name +"?"

    Label(ask_window,text = alert_text, bg = color_theme, 
                font = (font, content_size_font)).grid(padx=10, pady=10, row = 1, column = 1, columnspan = 2)

    btn_connect = Button(ask_window,text ="    Si    ", command = lambda : delete(ask_window), )
    btn_connect.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_connect.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    btn_connect.grid(padx=10, pady=10, row = 2, column = 1,)

    btn_update = Button(ask_window, text ="    No    ", command = lambda : ask_window.destroy() )
    btn_update.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_update.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_update.grid(padx=10, pady=10, row = 2, column = 2,)


    select_window.wait_window(ask_window)
    return respuesta