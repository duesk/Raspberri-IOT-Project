from tkinter import *
import asyncio

from checkFiles import checkSDFiles
from checkFiles import checkUSBFiles


send_file = None
content_size_font = 12


def connect(lst_box_puertos, selectWindow):
    global send_file
    print("conectar")
    try:
        port = lst_box_puertos.curselection()
        port = lst_box_puertos.get(port)
        send_file = port
        selectWindow.destroy()
    except:
        pass

def update(lst_box_puertos):
    pass
"""    lst_box_puertos.delete(0,"end")
    puerto = serial_ports()
    for i in puerto :
        print("puerto disponibles : " + i)
        lst_box_puertos.insert(1,i)  
    lst_box_puertos.config(font = ("",content_size_font))
    lst_box_puertos.pack()"""

def cerrar_w(selectWindow):
    global send_file
    send_file = "cerrar"
    selectWindow.destroy()
    


def run_select_file(selectWindow, root):
    global send_file
    global file_list


    #variables de stylo
    title_size_font = 16
    content_size_font = 12
    color_theme = "snow"
    color_button = "deepskyblue3"
    color_text_button = "gray99"
    font = "Garuda"
    color_font_activate_button = "gray25"
    color_bg_activate_button = "deep sky Blue"

    selectWindow.title("Colibrgyti 3D")

    selectWindow.minsize(400, 150 )
    selectWindow.attributes("-type","splash")
    selectWindow.attributes("-zoomed", True)
    selectWindow.config(bg = color_theme)
    selectWindow.protocol("WM_DELETE_WINDOW", lambda : cerrar_w(selectWindow)) #accion al cerrar la ventana 
    


    #Preparacion de los puertos 
    #print("Puerto :" + str(puerto))

    #preparacion de la listbox para seleccionar los puertos 
    Label(selectWindow, text = "Selecciona el archivo para imprimir", bg = color_theme, font = (font, content_size_font)).pack(pady = 15, padx = 15)
    lst_box_puertos = Listbox(selectWindow)
    sdFile = checkSDFiles()
    for i in sdFile :
        print("puerto disponibles : " + i)
        lst_box_puertos.insert(1,i)  
    lst_box_puertos.config(font = ("",content_size_font))
    lst_box_puertos.pack()

    #interfaz grafica
    btn_connect = Button(selectWindow,text ="seleccionar", command = lambda : connect(lst_box_puertos, selectWindow), )
    btn_connect.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_connect.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_connect.pack(padx = 15, pady = 10)

    btn_update = Button(selectWindow, text ="Actualizar", command = lambda : update(lst_box_puertos) )
    btn_update.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_update.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_update.pack(padx = 15, pady = 10)

    root.wait_window(selectWindow)
    send_file = "/home/rafael/gcodes/"+send_file
    return send_file
    print("asdasdfasdfasd")
