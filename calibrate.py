from tkinter import*
from printrun.printcore import printcore
from secuencias import Secuencias





def position_1(printer, secuencia):
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_1_position)

def position_2(printer, secuencia):
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_2_position)

def position_3(printer, secuencia):
    #printer.send_now("G28")
    printer.send_now(secuencia.cal_3_position)

def cerrar(root,win_calibrate, printer):
    printer.send_now("G28")
    root.deiconify()
    win_calibrate.destroy()



def init_calibrate_window(root, win_calibrate, printer):
    secuencia = Secuencias()
    #variables de stylo
    title_size_font = 16
    content_size_font = 12
    color_theme = "snow"
    color_button = "deepskyblue3"
    color_text_button = "gray99"
    font = "Garuda"
    color_font_activate_button = "gray25"
    color_bg_activate_button = "deep sky Blue"
    win_calibrate.config(bg = color_theme)

    win_calibrate.minsize(800, 480 )
    win_calibrate.attributes("-type","splash")
    win_calibrate.attributes("-zoomed", True)
    win_calibrate.fullScreenState = True
    win_calibrate.attributes('-fullscreen')
    win_calibrate.focus_force()
    win_calibrate.resizable(0,0)

    win_calibrate.protocol("WM_DELETE_WINDOW", lambda : cerrar(root,win_calibrate)) #accion al cerrar la ventana 
    win_calibrate.title('Calibracion')
    #message = "Selecciona un boton para iniciar la calibracion "
    printer.send_now("G28")
    #Label(win_calibrate, text=message).pack()
    frame = Frame(win_calibrate,pady = 50, padx = 50)
    frame["bg"] = color_theme

    Label(win_calibrate, text = "Selecciona un boton para iniciar la calibracion", bg = color_theme).pack()

    Button(frame, text="posición 1", command=  lambda : position_1(printer,secuencia ),activebackground = color_bg_activate_button, 
                activeforeground = color_font_activate_button, 
            font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 0, column = 0 )
    
    Button(frame, text="posición 2", command= lambda : position_2(printer,secuencia ),activebackground = color_bg_activate_button, 
                activeforeground = color_font_activate_button, 
            font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 0, column = 2)
    
    Button(frame, text="posición 3", command= lambda : position_3(printer,secuencia ),activebackground = color_bg_activate_button, 
                activeforeground = color_font_activate_button, 
            font = (font ,content_size_font),bg = color_button, fg = color_text_button).grid(row = 1, column = 1)
    
    sub_frame = Frame(win_calibrate, ) 
    sub_frame["bg"] = color_theme
    Label(sub_frame, text = "Para salir de la calibracion presione cerrar",bg = color_theme).pack()
    Button(sub_frame, text="cerrar", command= lambda : cerrar(root,win_calibrate, printer),activebackground = color_bg_activate_button, activeforeground = color_font_activate_button, 
            font = (font ,content_size_font),bg = color_button, fg = color_text_button).pack()
    frame.pack()
    sub_frame.pack( )
    status_label.set("Status: Calibrando ")
    root.withdraw()