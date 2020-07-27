from tkinter import *
from Port_connect import serial_ports

import sys 

sys_mac     =   False
sys_win     =   False
sys_linux   =   False
if sys.platform.startswith('darwin'):
    from tkmacosx import Button
    sys_mac = True

if sys.platform.startswith('win'):
    sys_win = True

if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    sys_linux = True


sys_mac     =   False
sys_win     =   False
sys_linux   =   False
if sys.platform.startswith('darwin'):
    from tkmacosx import Button
    sys_mac = True

if sys.platform.startswith('win'):
    sys_win = True

if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    sys_linux = True

puerto = []
send_port = None




def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   



def connect(lst_box_puertos, root):
    global send_port
    try:
        port = lst_box_puertos.curselection()
        port = lst_box_puertos.get(port)
        send_port = port
        root.destroy()
    except:
        pass

def update(lst_box_puertos):
    lst_box_puertos.delete(0,"end")
    puerto = serial_ports()
    for i in puerto :
        print("puerto disponibles : " + i)
        lst_box_puertos.insert(1,i)  
    lst_box_puertos.config(font = ("",content_size_font))
    lst_box_puertos.pack()

def cerrar_w(root):
    global send_port
    send_port = "cerrar"
    root.destroy()
    


def w_select_port():
    global sys_linux
    global sys_mac
    global sys_win

    if sys_mac:
        #variables de estilo
        title_size_font = 16
        content_size_font = 12
        color_theme = "snow"
        color_button = "deepskyblue3"
        color_text_button = "gray99"
        font = "Garuda"
    if sys_linux or sys_win:
        #variables de stylo
        title_size_font = 16
        content_size_font = 12
        color_theme = "snow"
        color_button = "deepskyblue3"
        color_text_button = "gray99"
        font = "Garuda"
        color_font_activate_button = "gray25"
        color_bg_activate_button = "deep sky Blue"

    
    root = Tk()
    if sys_mac or sys_win:
        root.iconbitmap("icon.ico")
    root.minsize(400, 150 )
    root.config(bg = color_theme)
    root.protocol("WM_DELETE_WINDOW", lambda : cerrar_w(root)) #accion al cerrar la ventana 
    


    #Preparacion de los puertos 
    puerto = serial_ports()
    #print("Puerto :" + str(puerto))

    #preparacion de la listbox para seleccionar los puertos 
    Label(text = "Selecciona el puerto donde esta conectada la impresora", bg = color_theme, font = (font, content_size_font)).pack(pady = 15, padx = 15)
    lst_box_puertos = Listbox(root)
    for i in puerto :
        print("puerto disponibles : " + i)
        lst_box_puertos.insert(1,i)  
    lst_box_puertos.config(font = ("",content_size_font))
    lst_box_puertos.pack()

    #interfaz grafica
    root.title("Colibri 3D")
    

    btn_connect = Button(text ="Conectar", command = lambda : connect(lst_box_puertos, root), )
    btn_connect.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    if sys_win or sys_linux:
        btn_connect.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_connect.pack(padx = 15, pady = 10)

    btn_update = Button(text ="Actualizar", command = lambda : update(lst_box_puertos) )
    btn_update.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    if sys_linux or sys_win:
        btn_update.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_update.pack(padx = 15, pady = 10)


    root.mainloop()


def run_select_port():
    w_select_port()
    return send_port

if __name__ == "__main__":
    run_select_port()