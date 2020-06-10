from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter import messagebox
import threading
import requests
import io

from PIL import Image, ImageTk

from VK import VK


def destroy_all_objects(objects):
    for i in objects:
        i.destroy()
    objects.clear()


class MyWindow:
    def __init__(self, font="Arial Bold"):
        self.vk = VK()
        self.friends = {}
        self.friends_fot = []
        self.window = Tk()
        self.window.title("Шаблон курсача")
        self.window.geometry('580x500')
        self.draw_first_page(font)
        self.window.mainloop()

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
            self.vk.login = "89063577290" # mail_input.get(),
            self.vk.password = "Gariktron1" # password_input.get()
            if not self.vk.create_api():
                messagebox.showwarning('Ошибка', 'Логин или пароль введены неверно!')
            else:
                self.vk.create_api()
                destroy_all_objects(all_objects)
                threading.Thread(target=self.first_download_page, args=[font]).start()

        accept_button = Button(self.window, text="Войти", font=(font, 15), command=click_enter)
        accept_button.place(x=200, y=170)
        all_objects.append(accept_button)

    def draw_second_page(self, font):
        im = Image.open(io.BytesIO(self.friends_fot[-1]))
        render = ImageTk.PhotoImage(im)
        img1 = Label(self.window, image=render)
        img1.image = render
        img1.place(x=10, y=10)

        img2 = Label(self.window, image=render)
        img2.image = render
        img2.place(x=250, y=10)

        def update_image(arg):
            ind = names.index(combobox1.get())
            im = Image.open(io.BytesIO(self.friends_fot[ind]))
            render = ImageTk.PhotoImage(im)
            img1.configure(image=render)
            img1.image = render
            ind = names.index(combobox2.get())
            im = Image.open(io.BytesIO(self.friends_fot[ind]))
            render = ImageTk.PhotoImage(im)
            img2.configure(image=render)
            img2.image = render

        def click_get_general():
            pass
            # index1 = names.index(combobox1.get())
            # index2 = names.index(combobox2.get())
            #
            # main_text = "Общие сообщества:\n "
            # general_groups = list(myVk.get_general_groups(self.vk, self.friends['items'][index1]['id'],
            #                                               self.friends['items'][index2]['id']))
            # groups = self.vk.groups.getById(group_ids=general_groups)
            # main_text += "\n".join([group['name'] for group in groups])
            # text = Label(self.window, text=main_text, font=(font, 10))
            # text.place(x=10, y=140)

        names = [i["first_name"] + " " + i["last_name"] for i in self.friends["items"]]
        combobox1 = Combobox(self.window, font=(font, 10))
        combobox1.place(x=70, y=30)
        combobox1['values'] = names
        combobox1.set(combobox1['values'][-1])
        combobox1.bind("<<ComboboxSelected>>", update_image)

        combobox2 = Combobox(self.window, font=(font, 10))
        combobox2.place(x=310, y=30)
        combobox2['values'] = names
        combobox2.set(combobox2['values'][-1])
        combobox2.bind("<<ComboboxSelected>>", update_image)

        button_get_general = Button(self.window, text="Найти общее", font=(font, 15), command=click_get_general)
        button_get_general.place(x=10, y=100)

    def first_download_page(self, font):
        all_objects = []
        text = Label(self.window, text="Загрузка списка друзей", font=(font, 15))
        text.place(x=200, y=110)
        all_objects.append(text)
        self.friends = self.vk.get_all_friends()
        self.friends["count"] += 1
        self.friends["items"].append(self.vk.get_info(0, "photo_50"))
        bar = Progressbar(self.window, length=200)
        all_objects.append(bar)
        bar['value'] = 0
        bar["maximum"] = self.friends['count']
        bar.place(x=200, y=140)
        for i, item in enumerate(self.friends['items']):
            self.friends_fot.append(requests.get(item['photo_50']).content)
            bar['value'] = i
        destroy_all_objects(all_objects)
        self.draw_second_page(font)


if __name__ == '__main__':
    MyWindow()