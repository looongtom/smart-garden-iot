from tkinter import *
import paho.mqtt.client as mqtt
# Khai báo topic sub, địa chỉ broker và kết nối với broker.
pub = "S"
sub = "S_tt"
broker_address="192.168.1.10"
client = mqtt.Client("P1")
client.connect(broker_address)
client.subscribe(sub)

#Khởi tạo Gui
is_on = False
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    if msg == "1":
        on_button.config(image=on)
        is_on = True
        window.update()
    else:
        on_button.config(image=off)
        is_on = False
        window.update()
client.on_message = on_message

window=Tk()
window.title('Chương trình điều khiển bóng đèn by Dr.AnhNguyen')
window.geometry('500x300+400+300')
my_label = Label(window,
                 text="Bật Tắt Bóng đèn",
                 fg="green",
                 font=("Helvetica", 32))
my_label.pack()
# tải hỉnh ảnh nút ấn
off = PhotoImage(file="images/on.png")
on = PhotoImage(file="images/off.png")
def switch():
    global is_on
    if is_on:
        on_button.config(image=off)
        is_on = False
        client.publish(pub, "0")
    else:
        on_button.config(image=on)
        is_on = True
        client.publish(pub, "1")
on_button = Button(window, image=off, bd=0,command=switch)
on_button.pack(pady=50)

client.loop_start()
window.mainloop()