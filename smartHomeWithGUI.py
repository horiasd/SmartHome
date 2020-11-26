from guizero import App, Box, Text, TextBox, PushButton
from datetime import datetime
import time
#import serial

#Megmondja, hogy melyik usb portpn keresztül lehet csatlakozni Raspberry PI-hoz
#USB_PORT = "/dev/ttyACM0"
#Megpróbál csatlakozni, ha nem sikerül, akkor ezt jelzi a program és kilép.
#try:
#    usb = serial.Serial(USB_PORT, 9600, timeout=2)
#except:
#    print("ERROR - Could not open USB serial port.  Please check your port name and permissions.")
#    print("Exiting program.")
#    exit()

#initcializálja a redőny fel és lehúzási idejét tároló listát
init = datetime.now()
#   0. index - felhúzás ideje
#   1. index - lehúzás  ideje
set_times = [init, init]


#ellenőrzi, hogy az adott bemenet megfelelő formátumú e
#PL elfogadja a 17:00 vagy a 03:12, de a 9:1-et vagy az asdasd-t nem
def isTimeFormat(is_time):
    try:
        time.strptime(is_time, '%H:%M')
        return True
    except ValueError:
        return False


#"lámpát" vezérli, és változtatja a gomb szövegét annak megfelelően, hogy mit csinál
def lamp_on_off_comm():
    if lamp_onoff.text == "Lamp off":
        print("Lamp off")
         #usb.write(b'ledCommand')
        lamp_onoff.text = "Lamp on"   
    else:
        print("Lamp on")
        #usb.write(b'ledCommand')
        lamp_onoff.text = "Lamp off"


#"Pull upp" parancs küldése az Arduino-nak
def blinds_up_comm():
    print("Blinds up")
    #usb.write(b'pull_up')


#"Pull down" parancs küldése az Arduinonak
def blinds_down_comm():
    print("Blinds down")
    #usb.write(b'pull_down')


#Redőny felhúzási idejének beállítása, ha megfelelő formátumú, akkor a set_times tömb 0. indexű eleme felülírásra kerül, az adott inputtal.
def set_time_up_comm():
    print(blinds_up_txtbox.value)
    if isTimeFormat(blinds_up_txtbox.value):
        blinds_up_label.value = "Set time: " + blinds_up_txtbox.value
        time_up = blinds_up_txtbox.value
        datetime_time_up = datetime.strptime(time_up, "%H:%M")
        set_times[0] = datetime_time_up
        print(f"set time up {set_times[0]}")
    blinds_up_txtbox.value = ""


#Redőny lehúzási idejének beállítása, ha megfelelő formátumú, akkor a set_times tömb 1. indexű eleme felülírásra kerül, az adott inputtal.
def set_time_down_comm():
    print(blinds_down_txtbox.value)
    if isTimeFormat(blinds_down_txtbox.value):
        blinds_down_label.value = "Set time: " + blinds_down_txtbox.value
        time_down = blinds_down_txtbox.value
        datetime_time_down = datetime.strptime(time_down, "%H:%M")
        set_times[1] = datetime_time_down
        print(f"set time down {set_times[1]}")
    blinds_down_txtbox.value = ""


#Másodpercenként meghívódik és ha az adott időpontra van beállítva redőny fel/lehúzás beállítva, akkor végrehajtja azt.
#lehet elég lenne csak percenként meghívni, de akkor nem lenne pontosan 00 másodperckor
def timing():
    now = datetime.now()
    current_h = now.hour
    current_m = now.minute
    current_s = now.second
    if set_times[0].year != init.year or set_times[0].year != init.year:
        print(current_h, current_m, current_s)
        if set_times[0].hour == current_h and set_times[0].minute == current_m and current_s == 0:
            print("blinders up")
             #usb.write(b'pull_up')
        elif set_times[1].hour == current_h and set_times[1].minute == current_m and current_s == 0:
            print("blinders down")
             #usb.write(b'pull_down')

#App létrehozása, különböző Text-ek, TextBox-ok és PushButton-ok hozzáadása az App-hoz
app = App(title="Smart Home")

margin1 = Text(app, size=10, text="")
welcome_message = Text(app, size=20, text="Control your smart home")
margin2 = Text(app, size=10, text="")

buttons_box = Box(app, width="fill", height=100, align="top")
lamp_onoff = PushButton(buttons_box, command=lamp_on_off_comm, text="Lamp off", align="left", width="fill", height="fill")
blinds_up = PushButton(buttons_box, command=blinds_up_comm, text="Blinds up", align="left", width="fill", height="fill")
blinds_down = PushButton(buttons_box, command=blinds_down_comm, text="Blinds down", align="left", width="fill", height="fill")

margin3 = Text(app, size=10, text="")

blinds_box = Box(app, align="top", layout="grid")
blinds_up_label = Text(blinds_box, grid=[0, 0], text="Time for raising blinders: ", align="left")
blinds_up_txtbox = TextBox(blinds_box, grid=[1, 0], align="left")
blinds_up_setbtn = PushButton(blinds_box, grid=[2, 0], command=set_time_up_comm, text="Set", align="left")


blinds_down_label = Text(blinds_box, grid=[0, 1], text="Set time for lowering blinders: ", align="left")
blinds_down_txtbox = TextBox(blinds_box, grid=[1, 1], align="left")
blinds_down_setbtn = PushButton(blinds_box, grid=[2, 1], command=set_time_down_comm, text="Set", align="left")

timer_label = Text(app, text="")
timer_label.repeat(1000, timing)

#app megjelenítése
app.display()
