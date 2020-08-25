from tkinter import *
import asyncio

from checkFiles import check_sd_files
from checkFiles import check_usb_files


send_file = None
content_size_font = 12
select_sd = False


def usb_list(lst_box_archivos,btn_sd, btn_USB):
    global select_sd
    
    lst_box_archivos.delete(0,"end")

    if select_sd :
        select_sd = False
        btn_sd["state"] = DISABLED
        btn_USB["state"] = ACTIVE
        list_files = check_sd_files()
    else:
        select_sd = True
        btn_sd["state"] = ACTIVE
        btn_USB["state"] = DISABLED
        list_files = check_usb_files()

    for i in list_files:
        print("puerto disponibles : " + i)
        lst_box_archivos.insert(1,i)  
    lst_box_archivos.config(font = ("",content_size_font))
    lst_box_archivos.grid(padx=20, pady=10,row = 2, column = 0,columnspan = 3, sticky="nsew" )



def connect(lst_box_archivos, selectWindow):
    global send_file
    print("conectar")
    try:
        port = lst_box_archivos.curselection()
        port = lst_box_archivos.get(port)
        send_file = port
        selectWindow.destroy()
    except:
        pass

def update(lst_box_archivos):
    pass
"""    lst_box_archivos.delete(0,"end")
    puerto = serial_ports()
    for i in puerto :
        print("puerto disponibles : " + i)
        lst_box_archivos.insert(1,i)  
    lst_box_archivos.config(font = ("",content_size_font))
    lst_box_archivos.pack()"""

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

    #selectWindow.title("Colibrgyti 3D")

    selectWindow.minsize(800, 480 )
    #selectWindow.attributes("-type","splash")
    #selectWindow.attributes("-zoomed", True)
    selectWindow.config(bg = color_theme)
    selectWindow.protocol("WM_DELETE_WINDOW", lambda : cerrar_w(selectWindow)) #accion al cerrar la ventana 
    


    #Preparacion de los puertos 
    #print("Puerto :" + str(puerto))
    
    #preparacion de la listbox para seleccionar los puertos 
    titlep = Label(selectWindow, text = "Selecciona el archivo para imprimir", bg = color_theme, 
                font = (font, content_size_font))
    titlep.grid(padx=10, pady=10, row = 0, column = 0, columnspan = 2)
    

    lst_box_archivos = Listbox(selectWindow)


    btn_USB = Button(selectWindow,text ="    USB    ", command = lambda : usb_list(lst_box_archivos,btn_sd,btn_USB), )
    btn_USB.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_USB.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button,
            font = (font,content_size_font))
    # 3 b btn_USB["state"] = DISABLED
    btn_USB.grid(padx=10, pady=10,row = 1, column = 0)
    
        
    btn_sd = Button(selectWindow,text ="IMPRESORA", command = lambda : usb_list(lst_box_archivos,btn_sd,btn_USB), )
    btn_sd.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_sd.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    #btn_sd.pack(padx = 15, pady = 10)
    btn_sd.grid( pady=10,row = 1, column = 1 )
    btn_sd["state"] = DISABLED    

    selectWindow.columnconfigure(2,weight=1)#configura la columna para que se estire
    #selectWindow.rowconfigure(2,weight=1)    #configura la columna para que se estire

    #lst_box_archivos.grid(row=0, column=0)
    sdFile = check_sd_files()
    for i in sdFile :
        print("puerto disponibles : " + i)
        lst_box_archivos.insert(1,i)  
    lst_box_archivos.config(font = ("",content_size_font))
    lst_box_archivos.grid(padx=20, pady=10,row = 2, column = 0,columnspan = 3, sticky="nsew" )

    """
    #interfaz grafica
    btn_connect = Button(selectWindow,text ="seleccionar", command = lambda : connect(lst_box_archivos, selectWindow), )
    btn_connect.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_connect.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    btn_connect.pack(padx = 15, pady = 10)

    btn_update = Button(selectWindow, text ="Actualizar", command = lambda : update(lst_box_archivos) )
    btn_update.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_update.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_update.pack(padx = 15, pady = 10)

    """

    root.wait_window(selectWindow)
    send_file = "/home/rafael/gcodes/"+send_file
    return send_file
    print("asdasdfasdfasd")



def run():
    root = Tk()
    selectWindow = Toplevel(root)
    run_select_file(selectWindow,root)

    root.mainloop()


if __name__ == "__main__":
    run()