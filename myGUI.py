from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter import messagebox
import threading
import os
import requests
import io

from PIL import Image, ImageTk

import WorkWithVK as myVk


def destroy_all_objects(objects):
    for i in objects:
        i.destroy()
    objects.clear()


class MyWindow:
    session = False
    vk = False
    friends = []
    friends_fot = []

    def draw_first_page(self, font):
        all_objects = []
        text_mail = Label(self.window, text="Логин", font=(font, 15))
        text_mail.place(x=200, y=50)
        all_objects.append(text_mail)
        mail_input = Entry(self.window, font=(font, 15), width=16)
        mail_input.place(x=200, y=80)
        all_objects.append(mail_input)

        text_password = Label(self.window, text="Пароль", font=(font, 15))
        text_password.place(x=200, y=110)
        all_objects.append(text_password)
        password_input = Entry(self.window, font=(font, 15), width=16)
        password_input.place(x=200, y=140)
        all_objects.append(password_input)

        def click_enter():
            # self.session = myVk.create_session(mail_input.get(), password_input.get())
            self.session = myVk.create_session("89063577290", "Gariktron1")
            if not self.session:
                messagebox.showwarning('Ошибка', 'Логин или пароль введены неверно!')
            else:
                # self.vk = myVk.create_vk(mail_input.get(), password_input.get())
                self.vk = myVk.create_vk("89063577290", "Gariktron1")
                destroy_all_objects(all_objects)
                threading.Thread(target=self.first_download_page, args=[font]).start()

        accept_button = Button(self.window, text="Войти", font=(font, 15), command=click_enter)
        accept_button.place(x=200, y=170)
        all_objects.append(accept_button)

    def draw_second_page(self, font):
        im = Image.open(io.BytesIO(i))
        render = ImageTk.PhotoImage(im)
        img = Label(self.window, image=render)
        img.image = render
        img.place(x=10, y=10)
        combobox1 = Combobox(self.window, font=(font, 10))
        combobox1.place(x=70, y=30)
        combobox1['values'] = [i["first_name"] + " " + i["last_name"] for i in self.friends["items"]]


        """for i in self.friends_fot:
            im = Image.open(io.BytesIO(i))
            render = ImageTk.PhotoImage(im)
            img = Label(self.window, image=render)
            img.image = render
            img.place(x=10, y=10)"""

    def first_download_page(self, font):
        all_objects = []
        text = Label(self.window, text="Загрузка списка друзей", font=(font, 15))
        text.place(x=200, y=110)
        all_objects.append(text)
        self.friends = myVk.get_all_friends(self.vk)
        self.friends["count"] += 1
        print(self.vk.users.get(fields="photo_50"))
        self.friends["items"].append(self.vk.users.get(fields="photo_50")[0])
        number_download = 0
        bar = Progressbar(self.window, length=200)
        all_objects.append(bar)
        bar['value'] = 0
        bar["maximum"] = self.friends['count']
        bar.place(x=200, y=140)
        for i in self.friends['items']:
            self.friends_fot.append(requests.get(i['photo_50']).content)
            number_download += 1
            bar['value'] = number_download
        destroy_all_objects(all_objects)
        self.draw_second_page(font)

    def __init__(self, font="Arial Bold"):
        self.window = Tk()
        self.window.title("Шаблон курсача")
        self.window.geometry('580x500')
        self.draw_first_page(font)
        self.window.mainloop()

