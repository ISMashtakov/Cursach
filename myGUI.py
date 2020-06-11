import threading
import io
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter import messagebox

from PIL import Image, ImageTk

from VK import VK
from user import User
from users_comparator import UsersComparator


def destroy_all_objects(objects):
    for i in objects:
        i.destroy()
    objects.clear()


class MyWindow:

    def __init__(self, font="Arial Bold"):
        self.vk = VK()
        self.me = None
        self.users = None
        self.window = Tk()
        self.wait = False
        self.window.title("Шаблон курсача")
        self.window.geometry('780x500')
        self.draw_first_page(font)
        self.window.mainloop()

    def draw_first_page(self, font):
        all_objects = []
        text_mail = Label(self.window, text="Логин", font=(font, 15))
        text_mail.place(x=250, y=100)
        all_objects.append(text_mail)
        mail_input = Entry(self.window, font=(font, 15), width=16)
        mail_input.place(x=250, y=130)
        all_objects.append(mail_input)

        text_password = Label(self.window, text="Пароль", font=(font, 15))
        text_password.place(x=250, y=160)
        all_objects.append(text_password)
        password_input = Entry(self.window, font=(font, 15), width=16)
        password_input.place(x=250, y=190)
        all_objects.append(password_input)

        def click_enter():
            self.vk.login = "89063577290" # mail_input.get(),
            self.vk.password = "Gariktron1" # password_input.get()
            if not self.vk.create_api():
                messagebox.showwarning('Ошибка', 'Логин или пароль введены неверно!')
            else:
                self.vk.create_api()
                self.me = User(self.vk.api.users.get()[0]["id"])
                destroy_all_objects(all_objects)
                threading.Thread(target=self.first_download_page, args=[font]).start()

        accept_button = Button(self.window, text="Войти", font=(font, 15), command=click_enter)
        accept_button.place(x=250, y=230)
        all_objects.append(accept_button)

    def draw_second_page(self, font):
        im = Image.open(io.BytesIO(self.me.image))
        render = ImageTk.PhotoImage(im)
        img1 = Label(self.window, image=render)
        img1.image = render
        img1.place(x=10, y=10)

        img2 = Label(self.window, image=render)
        img2.image = render
        img2.place(x=250, y=10)
        for_destroy = []

        def update_image(arg):
            ind = names.index(combobox1.get())
            im = Image.open(io.BytesIO(self.users[ind].image))
            render = ImageTk.PhotoImage(im)
            img1.configure(image=render)
            img1.image = render
            ind = names.index(combobox2.get())
            im = Image.open(io.BytesIO(self.users[ind].image))
            render = ImageTk.PhotoImage(im)
            img2.configure(image=render)
            img2.image = render

        def click_get_general():
            if not self.wait:
                self.wait = True
                threading.Thread(target=create_result, args=[]).start()

        def create_result():
            nonlocal for_destroy
            destroy_all_objects(for_destroy)
            ind1 = names.index(combobox1.get())
            ind2 = names.index(combobox2.get())
            user1 = self.users[ind1]
            user2 = self.users[ind2]

            bar = Progressbar(self.window, length=200)
            bar['value'] = 0
            bar["maximum"] = 100
            bar.place(x=200, y=200)
            score, description = UsersComparator(user1, user2, bar).compare()
            description += "\n\n Итоговый счёт: " + str(int(score))
            text = Label(self.window, text="Результаты сравнения", font=(font, 18))
            text.place(x=200, y=150)
            for_destroy.append(text)

            text = Label(self.window, text=description, font=(font, 10))
            text.place(x=5, y=180)
            for_destroy.append(text)
            self.wait = False

        names = [user.first_name["I"] + " " + user.last_name["I"] for user in self.users]
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
        text.place(x=250, y=160)
        all_objects.append(text)
        self.users = self.me.friends + [self.me]
        bar = Progressbar(self.window, length=200)
        all_objects.append(bar)
        bar['value'] = 0
        bar["maximum"] = len(self.users)
        bar.place(x=252, y=200)
        for i, user in enumerate(self.users):
            image = user.image
            name = user.first_name
            bar['value'] = i
        self.vk.save_cache()
        destroy_all_objects(all_objects)
        self.draw_second_page(font)


if __name__ == '__main__':
    MyWindow()