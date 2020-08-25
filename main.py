from tkinter import *
from tkinter import ttk
from tkinter import filedialog as Filedialog
from tkinter import messagebox as Messagebox

import PIL
from PIL import Image
from PIL import ImageTk

from Select_port import run_select_port
from Select_file import run_select_file
from printrun.printcore import printcore
from printrun.gcoder import LightGCode as LightGCode 
from windows_errors import kill_error as kill_error
import asyncio
import sys 


import threading
import time

from status import Status as Status
from secuencias import Secuencias as Secuencias 
from autoconect import autoconnect_port 
from cancel_Window import CancelWindow

status = Status()
secuencia = Secuencias()

############################################################
###### Verificar que sistema operativo esta corriendo ######
############################################################
if sys.platform.startswith('darwin'):
    from tkmacosx import Button
    status.is_MAC = True
if sys.platform.startswith('win'):
    status.is_WIN = True
if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    status.is_LNX = True
#print("sistema LNX:" + str(status.is_LNX))
#print("sistema WIN:" + str(status.is_WIN))
#print("sistema MAC:" + str(status.is_MAC))

def select_file(archivo_selected,root):
    print("seleccionar archivo")

    selectWindow = Toplevel()
    status.ruta =  run_select_file(selectWindow, root)

    status.process_name()

    if status.ruta != "":
    
        archivo_selected.set("Seleccionado: "+ status.archivo)
        lb_Select_file.pack()
        if status.is_MAC:
            btn_start_print["state"] = NORMAL
            btn_calibrate["state"] = NORMAL
        if status.is_WIN or status.is_LNX:
            btn_start_print["state"] = ACTIVE
            btn_calibrate["state"] = ACTIVE

    else:
        archivo_selected.set("Ningún archivo seleccionado")
        lb_Select_file.pack()
        btn_start_print["state"] = DISABLED
        btn_cancel["state"] = DISABLED
        if status.is_MAC:
            btn_calibrate["state"] = NORMAL
        if status.is_WIN or status.is_LNX:
            btn_calibrate["state"] = ACTIVE



def start_print():
    if status.is_printing:
        if status.is_pause:
            is_pause = False 
            printer.resume()
            btn_start_print["text"] = "Pausar"
        else:
            is_pause = True
            printer.pause()
            printer.send_now(secuencia.pause_position)
            btn_start_print["text"] = "Reanudar"

    else:
        if status.ruta != "":
            archivo = open(status.ruta, "r")
            status.gcode = archivo.readlines()
            archivo.close()
            #print(gcode)
            printer.send("G28")
            status.gcode = [i.strip() for i in open(status.ruta)]
            status.gcode = LightGCode(status.gcode)
            status.st_print = True
            btn_calibrate["state"] = DISABLED
            bt_select_file["state"]=DISABLED


def cancel_window():

    win = Toplevel()
    response = CancelWindow(win)
    if response:
        cancel_print()


def cancel_print():
    
    status.is_pause
    status.response
    status.is_printing = False
    printer.queueindex = 0
    printer.cancelprint()
    printer.send_now(secuencia.cancel_position)
    is_pause = False
    btn_start_print["text"] = "Imprimir"
    btn_cancel["state"] = DISABLED
    if status.is_MAC:
        bt_select_file["state"]=NORMAL
    if status.is_WIN or status.is_LNX:
        bt_select_file["state"]=ACTIVE
        btn_calibrate["state"] = ACTIVE
    status_label.set("Status: Impresion cancelada.")
    progressbar["value"] = 0
    progressbar.pack()


def thread_set(printer,temp_label_extruder):
    status.temp_state
    status.is_pause
    #status.is_printing = False
    status.is_pause = False
    temp_saved = 0
    kill = False
    fase = True
    #printing = False

    while True:
        #print("temp set: " + str(status.temp_set))
        #print("temp saved: " + str(temp_saved))
        if (status.temp_set != temp_saved):
            temp_saved = status.temp_set
            printer.send_now("M104 S%d" %status.temp_set)
            print("Temperatura enviada")
        printer.send_now("M105")
        time.sleep(3)
        temp_label_extruder.set("Actual:     %s°C     de     " %status.temp_state)
        print(status.temp_state)
        lb_temp.pack()
        error = printer.errorcb
        list_error =list(error)
        for i in range(0,len(list_error)):
            print("error :" + list_error[i])
            stop_or_kill   = list_error[i].find("kill()")
            if stop_or_kill != -1 :
                print("Error temp:  kill() is called ")
                kill = True
        if kill:
            kill_error(list_error,root)
            break
        #format_error(error)
        #print(error)
        if status.st_print:
            min_temp = status.temp_set -5
            if float(status.temp_state) >= min_temp:
                status.st_print = False  
                printer.send_now("G28")
                printer.startprint(status.gcode)
                printer.send_now("G90")
                #status.is_printing = True
                if  status.is_LNX or status.is_WIN:
                    btn_cancel["state"] = ACTIVE
                if status.is_MAC:
                    btn_cancel["state"]=NORMAL
                bt_select_file["state"]=DISABLED
                btn_start_print["text"] = "pausa"
                status_label.set("Status: Imprimiendo ")
                print("imprimiendo")
            else:
                if fase:
                    fase = False
                    status_label.set("Status: Calentando . . .")
                    print("calentando")
                else:
                    fase = True
                    status_label.set("Status: Calentando. . .")
                    print("calentando")
        b = printer.queueindex
        print("index:"+str(b))
        if b >= 1:
            status.is_printing = True
        if status.is_printing:
            if status.is_pause:
                printer.send_now(secuencia.pause_position)
                print("printer pausada enviando gcode de posicion de pausa")
            try:
                a = len(printer.mainqueue)
                progress = 100 * b / a
                progress = round(progress,2)
                print(progress)
                avance = "Status: Imprimiendo " + str(progress)
                status_label.set(avance + "%")
                progressbar["value"] = progress
                progressbar.pack()
            except:
                print("except : Progress bar")
            if b == 0:
                #printing=False
                status.is_printing = False
                print("ya entre")
                status_label.set("Status: Impresion terminada")
                printer.send_now("G28")
                status.is_printing = False
                progressbar["value"] = 99.9
                progressbar.pack()
                btn_start_print["text"] = "Imprimir"
                btn_cancel["state"] = DISABLED
                if status.is_LNX or status.is_WIN:
                    btn_calibrate["state"] = ACTIVE
                    bt_select_file["state"]=ACTIVE
                if status.is_MAC:
                    btn_calibrate["state"] = NORMAL
                    bt_select_file["state"]=NORMAL
        #else:
            #status_label.set("Status: Impresora lista para imprimir")
        print("Status : thread is working")

def temp_callback(a):
    status.temp_state 
    status.temp_state = ""
    print('temp_callback', a)
    status.temp_state = a[5:8]
    #print("Parse:" + temp_state)

def high_temp():
    status.temp_set +=1
    status.temp_set_var.set(str(status.temp_set))
    lb_set_temp.pack()

def low_temp():
    status.temp_set -=1
    status.temp_set_var.set(str(status.temp_set))
    lb_set_temp.pack()
    

def position_1():
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_1_position)

def position_2():
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_2_position)

def position_3():
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_3_position)

def cerrar(root,win):
    printer.send_now("G28")
    root.deiconify()
    win.destroy()



def calibrate(root):
    win = Toplevel()
    if status.is_MAC or status.is_WIN:
        win.iconbitmap("icon.ico")
    #win.attributes("-type","notification")   #eliminar marco de sistema para cerrar
    #win.overrideredirect(True)
    win.protocol("WM_DELETE_WINDOW", lambda : cerrar(root,win)) #accion al cerrar la ventana 
    win.title('Calibracion')
    message = "Selecciona un boton para iniciar la calibracion "
    printer.send_now("G28")
    Label(win, text=message).pack()
    frame = Frame(win,pady = 50, padx = 50)

    if status.is_MAC:
        Button(frame, text="posición 1", command=position_1, 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 0, column = 0)
        
        Button(frame, text="posición 2", command=position_2, 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 0, column = 2)
        
        Button(frame, text="posición 3", command=position_3, 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 1, column = 1)
        
        sub_frame = Frame(win, ) 
        Label(sub_frame, text = "Para salir de la calibracion presione cerrar").pack()
        Button(sub_frame, text="cerrar", command= lambda : cerrar(root,win), 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack()
    else:
        Button(frame, text="posición 1", command= position_1,activebackground = color_bg_activate_button, 
                    activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 1, column = 0 )
        
        Button(frame, text="posición 2", command=position_2,activebackground = color_bg_activate_button, 
                    activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 1, column = 2)
        
        Button(frame, text="posición 3", command=position_3,activebackground = color_bg_activate_button, 
                    activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 0, column = 1)
        
        sub_frame = Frame(win, ) 
        Label(sub_frame, text = "Para salir de la calibracion presione cerrar").pack()
        Button(sub_frame, text="cerrar", command= lambda : cerrar(root,win),activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack()
    frame.pack()
    sub_frame.pack( )
    status_label.set("Status: Calibrando ")
    root.withdraw()
    

def close_all(root):
    pass

def cancel_and_quit(win,root):

    status.is_pause
    status.response
    win.destroy()
    printer.cancelprint()
    root.destroy()

def close_window(root):

    if status.is_printing or status.st_print:
        win = Toplevel()
        if status.is_MAC or status.is_WIN:
            win.iconbitmap("icon.ico")
        win.title('Peligro')
        message = "¿Seguro que deseas cancelar la impresion y cerrar la ventana?"
        Label(win, text=message).pack()
        frame = Frame(win)

        if status.is_MAC:
            Button(frame, text="Si", command= lambda : cancel_and_quit(win,root), font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")
            
            Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)
            
            Button(frame, text="No", command=win.destroy, font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")
        else:
            Button(frame, text="Si", command= lambda : cancel_and_quit(win,root),activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")
            
            Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

            Button(frame, text="No", command=win.destroy,activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
                    font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack(side = "left")

        frame.pack()
    else:
        root.destroy()






#########################################################################
##################               init               #####################
#########################################################################


if __name__ == "__main__":


    while True:
        if status.is_MAC:
                    #variables de estilo
            title_size_font = 32
            content_size_font = 24
            color_theme = "snow"
            color_button = "deepskyblue3"
            color_text_button = "gray99"
            font = "Garuda"
        else:
                    #variables de estilo
            title_size_font = 16
            content_size_font = 12
            color_theme = "snow"
            color_button = "deepskyblue3"
            color_text_button = "gray99"
            font = "Garuda"
            color_font_activate_button = "gray25"
            color_bg_activate_button = "deepskyblue"
        
        
        ##################################
        ## Autoconect para Raspberri Pi ##
        ##################################

        if status.is_LNX and status.is_RBpi:
            puerto = autoconnect_port()
        else:                                                                                                                                                                                                                                                                                                                                                                                                              
            puerto = run_select_port()
        is_conect = False

        if puerto is not None:
            if puerto == "cerrar":
                break

            print("puerto recibido : " + puerto)
            #init printer
            printer =  printcore( puerto, 115200)
            #printer.online
            printer.tempcb = temp_callback
            for i in range(0,30):
                if printer.online:
                    is_conect = True
                    break
                else:
                    print("impresora no online")
                    time.sleep(0.5)
            if is_conect == False:
                init_window = Tk()
                init_window.title("Error de conexión ")
                if status.is_MAC or status.is_WIN:
                    init_window.iconbitmap("icon.ico")
                init_window.config(bg = color_theme)
                Label(init_window, text= "Error el programa no pudo conectarse ",font = (font ,content_size_font), bg = color_theme).pack(side = "left", anchor = "nw", pady = 30,padx = 30)
                if status.is_MAC:
                    Button(init_window, text = "Reiniciar" , font = (font ,content_size_font),bg = color_button, fg = color_text_button, command = init_window.destroy).pack(side = "left")
                else:
                    Button(init_window, text = "Reiniciar" , activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, font = (font ,content_size_font),bg = color_button, fg = color_text_button, command = init_window.destroy).pack(side = "left")
                init_window.mainloop()
            if is_conect:
                break

        
    if is_conect:
        #########################################################################
        ##################            interfaz             ######################
        #########################################################################
        root = Tk()

        if status.is_MAC or status.is_WIN:
            root.iconbitmap("icon.ico")
        root.title( "Colibri 3D")
        root.minsize(800,480)
        #root.attributes('-type', 'dock')
        root.attributes("-type","splash")
        root.attributes("-zoomed", True)
        

        root.fullScreenState = True
        #root.wm_attributes('-type', 'splash')
        #root.maxsize(500,700)

        root.attributes('-fullscreen')
        root.focus_force()

        root.resizable(0,0)
        root.config(bg = color_theme)
        root.protocol("WM_DELETE_WINDOW", lambda : close_window(root)) #accion al cerrar la ventana 

        
        im = PIL.Image.open("assets/colibri.png")
        logo = PIL.ImageTk.PhotoImage(im)


        #######################################
        ###             Textvar             ###
        #######################################

        temp_label_extruder = StringVar()
        temp_label_extruder.set("Actual:     --°C     de     ")

        status.temp_set_var = StringVar()
        status.temp_set_var.set(str(status.temp_set))

        archivo_selected = StringVar()
        archivo_selected.set("Ningún archivo seleccionado")

        status_label = StringVar()
        status_label.set("Impresora lista para imprimir")

        #frame con padiing 15px
        frame = Frame(root)
        frame.config(bg = color_theme)
        frame.pack(side = "top", anchor = "nw", padx = 15, pady = 15,fill = "both")
        
        #######################################
        ###           Temperatura           ###
        #######################################

        #frame  titulo e imagen
        sub_frame_1 = Frame(frame,)
        sub_frame_1.config(bg = color_theme)
        sub_frame_1.pack(side = "top", anchor = "nw",fill = "both")
        
        #Label title TEMPERATURA
        lb_title_temp = Label(sub_frame_1, text = "Temperatura",font = (font ,title_size_font),)
        lb_title_temp.config(bg = color_theme)
        lb_title_temp.pack(side = "left",anchor = "s")

        #Label IMAGEN LOGO.png
        lb_logo = Label(sub_frame_1, image = logo, )
        lb_logo.config(bg = color_theme)
        lb_logo.pack(side = "right",anchor = "n")

        #frame separador
        frame_2 = Frame(frame,)
        frame_2.config(bg = color_theme)
        frame_2.pack( fill = "both", expand = 1)

        ttk.Separator(frame_2, orient='horizontal').pack(side='top', fill='x') #linea separadora

        #label Temperatura 
        lb_temp = Label(frame_2, textvar = temp_label_extruder,font = (font ,content_size_font) )
        lb_temp.config(bg = color_theme)
        lb_temp.pack(side = "left", anchor = "nw", pady = 15)

        #Label(frame_2, text = "   /   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)
        
        btn_lower_temp = Button(frame_2, text = "—",font = (font ,content_size_font+6),bg = color_button, fg = color_text_button, command = lambda: low_temp() )
        if status.is_WIN or status.is_LNX:
            btn_lower_temp.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
        btn_lower_temp.pack(side = "left", anchor = "nw", pady = 10)

        #separador
        Label(frame_2, text = " ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

        lb_set_temp = Label(frame_2, textvar = status.temp_set_var, font = (font ,content_size_font))
        lb_set_temp.config(bg = "gray87")
        lb_set_temp.pack(side = "left", anchor = "nw", pady = 15)

        #separador
        Label(frame_2, text = " ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

        btn_higher_temp = Button(frame_2, text = "+",font = (font ,content_size_font+6),bg = color_button, fg = color_text_button, command = lambda: high_temp() )
        if status.is_WIN or status.is_LNX:
            btn_higher_temp.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)

        btn_higher_temp.pack(side = "left", anchor = "nw",pady= 10)

        ########################################
        ###             Archivo             ####
        ########################################
        
        frame_3 = Frame(frame,)
        frame_3.config(bg = color_theme)
        frame_3.pack( side ="top", fill = "both", expand = 1)
        
        lb_title_archivo = Label(frame_3, text = "Archivo", font=(font ,title_size_font))
        lb_title_archivo.config(bg = color_theme)
        lb_title_archivo.pack(side = "top",anchor = "nw")

        ttk.Separator(frame_3, orient='horizontal').pack( fill='x') #linea separadora

        bt_select_file = Button(frame_3, text = " Seleccionar ",font = (font ,content_size_font),bg = color_button, fg = color_text_button, command = lambda: select_file(archivo_selected, root))
        if status.is_WIN or status.is_LNX:
            bt_select_file.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
        bt_select_file.pack(side = "left", pady = 10)

        Label(frame_3, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)


        lb_Select_file = Label(frame_3, textvar = archivo_selected, font = (font ,content_size_font))
        lb_Select_file.config(bg = color_theme)
        lb_Select_file.pack(side = "left",pady = 15)
        ########################################
        ###             imprimir             ###
        ########################################

        frame_4 = Frame(frame,)
        frame_4.config(bg = color_theme)
        frame_4.pack( side ="top", fill = "both", expand = 1)
        

        ttk.Separator(frame_4, orient='horizontal').pack( fill='x') #linea separadora

        btn_start_print = Button(frame_4, text = "Imprimir", font = (font ,content_size_font),bg = color_button, 
                                fg = color_text_button, state = DISABLED, command =  start_print)
        
        if status.is_WIN or status.is_LNX:
            btn_start_print.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
        btn_start_print.pack(side = "left", pady = 10)

        Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)


        btn_cancel = Button(frame_4, text = "Cancelar",font = (font ,content_size_font),bg = color_button, 
                            fg = color_text_button, state = DISABLED, command = cancel_window )
        if status.is_WIN or status.is_LNX:
            btn_cancel.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
        btn_cancel.pack(side = "left", pady = 10)        

        Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

        btn_calibrate = Button(frame_4, text = "Calibrar",font = (font ,content_size_font),bg = color_button,
                                fg = color_text_button, command = lambda: calibrate(root))
        if status.is_WIN or status.is_LNX:
            btn_calibrate.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
        btn_calibrate.pack(side = "left", pady = 10)
        
        if status.is_debug_mode:
            btn_close = Button(frame_4, text = "Cerrar",font = (font ,content_size_font),bg = color_button,
                                fg = color_text_button, command = root.destroy)
            if status.is_WIN or status.is_LNX:
                btn_close.config(activebackground = color_bg_activate_button, activeforeground = color_font_activate_button)
            btn_close.pack(side = "left", pady = 10)
        
        

        ########################################
        ###             imprimir             ###
        ########################################
        frame_5 = Frame(frame,)
        frame_5.config(bg = color_theme)
        frame_5.pack(side= "left", fill = "both", expand = 1)

        Label(frame_4, text = "   ", font = (font ,content_size_font), bg = color_theme).pack(side = "left",pady = 15)

        progressbar = ttk.Progressbar(frame_5, length = 100.0, mode = "determinate", style = "red.Horizontal.TProgressbar")
        progressbar.pack(fill = "both", expand = 1, )
        #progressbar.step(90.0)

        lb_status = Label(frame_5, textvar = status_label,font = (font ,content_size_font) )
        lb_status.config(bg = color_theme)
        lb_status.pack(side = "left", anchor = "nw", pady = 15)
        

        #########################################################################
        ##################        inicio del thread        ######################
        #########################################################################

        #inicio del thread.
        thread_1 = threading.Thread(target = thread_set, args = (printer, temp_label_extruder, ) )
        thread_1.start()
        

        root.mainloop()
        printer.send_now("G28")
        printer.send_now("M104 S0")
        printer.disconnect()

