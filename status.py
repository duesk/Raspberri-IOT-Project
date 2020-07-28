from tkinter import filedialog as Filedialog


class Status:

    """Clase Printer que gestiona los datos de la impresion e impresora conectada al puerto"""
    ruta = ""
    gcode = []
    temp_global = ""
    temp_state = ""
    temp_set = 180
    is_printing = False
    is_pause = False
    response = False
    st_print = False

    len_gcode = 0.0
    index_actual = 0.0
    is_WIN = False
    is_LNX = False
    is_MAC = False
    archivo = ""
    
    def process_name(self): 
        if self.ruta != "":
            self.archivo = ""
            for i in range(len(self.ruta),0,-1):
                if self.ruta[i-1] != "/":
                    index = i-1
                else:
                    self.archivo = self.ruta[index:len(self.ruta)]
                    print(self.archivo)
                    break
            print("archivo seleccioado: " + str(self.archivo))
        else:
            self.archivo = ""
            print(self.archivo)

