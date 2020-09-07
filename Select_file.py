from tkinter import *
import asyncio
import shutil

from os import remove

from checkFiles import check_sd_files
from checkFiles import check_usb_files
from alert_windows import ask_delete

send_file = None
content_size_font = 12
sd_selected = True
usb_selected = False


def pack_list_box(lst_box_archivos,list_files):
    for i in list_files:
        print("Archivos disponibles : " + i)
        lst_box_archivos.insert(1,i)  
    lst_box_archivos.config(font = ("",content_size_font))
    lst_box_archivos.grid(padx=20, pady=10,row = 2, column = 0,columnspan = 4, sticky="nsew" )


def usb_list(lst_box_archivos,btn_sd, btn_USB):
    global sd_selected
    global usb_selected

    sd_selected = False
    usb_selected = True

    lst_box_archivos.delete(0,"end")
    btn_sd["state"] = ACTIVE
    btn_USB["state"] = DISABLED
    list_files = check_usb_files()
    pack_list_box(lst_box_archivos,list_files,)


def sd_list(lst_box_archivos,btn_sd, btn_USB):
    global sd_selected
    global usb_selected

    sd_selected = True
    usb_selected = False

    lst_box_archivos.delete(0,"end")
    btn_sd["state"] = DISABLED
    btn_USB["state"] = ACTIVE
    list_files = check_sd_files()
    pack_list_box(lst_box_archivos, list_files)




def select_file(lst_box_archivos, select_window):
    global send_file
    print("conectar")
    try:
        select = lst_box_archivos.curselection()
        select = lst_box_archivos.get(select)
        send_file = select
        select_window.destroy()
    except:
        pass


def move_file(lst_box_archivos, select_window,btn_sd, btn_USB):
    global sd_selected
    global usb_selected
    try:
        select = lst_box_archivos.curselection()
        select = lst_box_archivos.get(select)

        #mover de usb a sd
        if usb_selected:
            rute = os.listdir("/media/pi")
            copy_ruta = "/media/pi/" + rute[0] + "/"
            copy = copy_ruta + select
            #paste  = "/home/rafael/gcodes/"+ select
            paste  = "/home/pi/gcodes/"+ select

            shutil.copyfile(copy,paste)
            print("copiado")
            sd_list(lst_box_archivos,btn_sd, btn_USB)
            
        #mover de sd a usb
        else:
            copy = "/home/pi/gcodes/"+ select
            
            rute = os.listdir("/media/pi")
            paste_ruta = "/media/pi/" + rute[0] + "/"
            copy = paste_ruta + select
            paste  = "/home/rafael/usb/"+ select

            shutil.copyfile(copy, paste)
            print("copiado")
            usb_list(lst_box_archivos,btn_sd, btn_USB)
            
    except:
        print("error")


def remove_file(lst_box_archivos, select_window,btn_sd, btn_USB):
    global sd_selected
    global send_file
    #try:
    file_name = lst_box_archivos.curselection()
    file_name = lst_box_archivos.get(file_name)

    ask_window = Toplevel(select_window)
    result = ask_delete(ask_window,select_window,file_name) 

    #borrar archivo de sd
    if result:
        if sd_selected:
            #delete_file = "/home/rafael/gcodes/" + file_name
            delete_file = "/home/pi/gcodes/" + file_name
            print("Borrado")
            remove(delete_file)
            sd_list(lst_box_archivos,btn_sd, btn_USB)
        #borrar archivo de usb
        else:
            #delete_file = "/home/rafael/usb/" + file_name
            #file_list = os.listdir("/media/pi/"+rute[0])

            rute = os.listdir("/media/pi")
            delete_ruta = "/media/pi/" + rute[0] + "/"

            delete_file = delete_ruta + file_name

            print("Borrado")
            remove(delete_file)
            usb_list(lst_box_archivos,btn_sd, btn_USB)

def cerrar_w(select_window):
    global send_file
    send_file = "cerrar"
    select_window.destroy()
    


def run_select_file(select_window, root):
    global send_file
    global file_list
    global sd_selected


    #variables de stylo
    title_size_font = 16
    content_size_font = 12
    color_theme = "snow"
    color_button = "deepskyblue3"
    color_text_button = "gray99"
    font = "Garuda"
    color_font_activate_button = "gray25"
    color_bg_activate_button = "deep sky Blue"

    #select_window.title("Colibrgyti 3D")

    select_window.minsize(800, 480 )
    select_window.attributes("-type","splash")
    select_window.attributes("-zoomed", True)
    select_window.fullScreenState = True
    select_window.attributes('-fullscreen')
    select_window.focus_force()
    select_window.resizable(0,0)

    
    #select_window.attributes("-type","splash")
    #select_window.attributes("-zoomed", True)
    select_window.config(bg = color_theme)
    select_window.protocol("WM_DELETE_WINDOW", lambda : cerrar_w(select_window)) #accion al cerrar la ventana 
    


    #Preparacion de los puertos 
    #print("Puerto :" + str(puerto))
    
    #preparacion de la listbox para seleccionar los puertos 
    titlep = Label(select_window, text = "Selecciona el archivo para imprimir", bg = color_theme, 
                font = (font, content_size_font))
    titlep.grid(padx=10, pady=10, row = 0, column = 0, columnspan = 2)
    

    lst_box_archivos = Listbox(select_window)


    btn_USB = Button(select_window,text ="    USB    ", command = lambda : usb_list(lst_box_archivos,btn_sd,btn_USB), )
    btn_USB.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_USB.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button,
            font = (font,content_size_font))
    # 3 b btn_USB["state"] = DISABLED
    btn_USB.grid(padx=10, pady=10,row = 1, column = 0)
    
        
    btn_sd = Button(select_window,text ="IMPRESORA", command = lambda : sd_list(lst_box_archivos,btn_sd,btn_USB), )
    btn_sd.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_sd.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    #btn_sd.pack(padx = 15, pady = 10)
    btn_sd.grid( pady=10,row = 1, column = 1 )
    btn_sd["state"] = DISABLED    

    select_window.columnconfigure(3,weight=1)#configura la columna para que se estire
    #select_window.rowconfigure(2,weight=1)    #configura la columna para que se estire

    #lst_box_archivos.grid(row=0, column=0)
    sd_list(lst_box_archivos,btn_sd,btn_USB)
    


    btn_select = Button(select_window,text ="Seleccionar", command = lambda : select_file(lst_box_archivos,select_window), )
    btn_select.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_select.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    #btn_sd.pack(padx = 15, pady = 10)
    btn_select.grid( pady=10,row = 3, column = 0 )
    #btn_select["state"] = DISABLED   
    


    btn_move = Button(select_window,text ="Mover", command = lambda : move_file(lst_box_archivos,select_window,btn_sd, btn_USB), )
    btn_move.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_move.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    #btn_sd.pack(padx = 15, pady = 10)
    btn_move.grid( pady=10,row = 3, column = 1 )
    #btn_select["state"] = DISABLED  

    btn_move = Button(select_window,text ="Borrar", command = lambda : remove_file(lst_box_archivos,select_window,btn_sd, btn_USB), )
    btn_move.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_move.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    #btn_sd.pack(padx = 15, pady = 10)
    btn_move.grid( pady=10,row = 3, column = 2 )
    #btn_select["state"] = DISABLED  


    """ 
    #interfaz grafica
    btn_connect = Button(select_window,text ="seleccionar", command = lambda : connect(lst_box_archivos, select_window), )
    btn_connect.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_connect.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, 
                font = (font,content_size_font))
    btn_connect.pack(padx = 15, pady = 10)

    btn_update = Button(select_window, text ="Actualizar", command = lambda : update(lst_box_archivos) )
    btn_update.config(bg = color_button, fg = color_text_button ,font =(font,content_size_font))
    btn_update.config( activebackground = color_bg_activate_button, activeforeground =color_font_activate_button, font = (font,content_size_font))
    btn_update.pack(padx = 15, pady = 10)

    """

    root.wait_window(select_window)
    #send_file = "/home/rafael/gcodes/"+send_file
    if sd sd_selected:
        send_file = "/home/pi/gcodes/"+send_file
    else:
        rute = os.listdir("/media/pi")
        ruta = "/media/pi/" + rute[0] + "/"
        send_file = ruta + send_file  
    print("Archivo enviado: "+send_file)
    return send_file






