# Documentacion



### Problemas para dar permisos linux
    
    
    sudo usermod -a -G dialout $USER    cerrar sesion e iniciar para activar los cambios
    
    
    ~ sudo chmod a+rw /dev/tty*

ubuntu main.spec
    datas=[('/usr/lib/python3/dist-packages/PIL/','PIL'),],



# MacOS
py2applet --make-setup MyApplication.py
Wrote setup.py

python3 setup.py py2app -A


# windows 

pyinstaller --windowed --onefile --icon=icon.ico main.py

# Linux
pyinstaller --windowed --onefile --icon=icon.ico main.py

ubuntu main.spec
    datas=[('/usr/lib/python3/dist-packages/PIL/','PIL'),],

    pyinstaller --windowed --onefile --icon=icon.ico main.spec