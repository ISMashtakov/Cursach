from user import User
from VK import VK
from users_comparator import UsersComparator
from YaMusic import YaMusic

from pymorphy2 import MorphAnalyzer

vk = VK()
vk.login = "89063577290"
vk.password = "Gariktron1"
vk.create_api()

u = User(420205723)
milena = User(191776959)
ta = User(112349156)
to = User(151384038)
m = User(235832830)
v = User(228354023)
me = User(220697751)
i = User(116598269)

#com = UsersComparator(to, milena).compare_music()
#com = UsersComparator(me, v).compare_music()
#com = UsersComparator(me, milena).compare_music()
#print(UsersComparator(i, to).compare_user_information())
#print(UsersComparator(me, to).compare_user_information())

com = UsersComparator(me, milena).compare_groups()
pass