#from myGUI import MyWindow


#window = MyWindow()

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://yandex.ru/")
driver.execute_script("window.scrollBy(" + str(0) + "," + str(500) + ");")

pass
