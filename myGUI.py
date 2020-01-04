from tkinter import *
from tkinter import messagebox
import WorkWithVK as myVk


class MyWindow:
    session = False
    vk = False

    def draw_first_page(self,font):
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
            self.session = myVk.create_session(mail_input.get(), password_input.get())
            if self.session == False:
                messagebox.showwarning('Ошибка', 'Логин или пароль введены неверно!')
            else:
                vk = myVk.create_vk(mail_input.get(), password_input.get())
                for i in all_objects:
                    i.destroy()
                all_objects.clear()

        accept_button = Button(self.window, text="Войти", font=(font, 15), command=click_enter)
        accept_button.place(x=200, y=170)
        all_objects.append(accept_button)

    def draw_second_page(self,font):
        pass

    def __init__(self, font="Arial Bold"):
        self.window = Tk()
        self.window.title("Шаблон курсача")
        self.window.geometry('580x500')
        self.draw_first_page(font)
        self.window.mainloop()





