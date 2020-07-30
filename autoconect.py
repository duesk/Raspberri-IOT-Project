from Port_connect import serial_ports



def autoconnect_port():
    puerto = []
    send_port = None

    puerto = serial_ports()
    for i in puerto :
        print("puerto disponibles : " + i)
        if send_port is None:
            send_port=i;
        else:
            break

    return send_port

if __name__ == "__main__":
    run_select_port()