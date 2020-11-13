from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import csv
from multiprocessing import Pool
"""
получаю названия команд
получаю кол-во нападающих и полузащитников
получаю число угловых
объединяю результаты в список
записываю в файл
"""

"""
делаю функцию make_all, которая объединяет все прошлые функции
делаю multiprocessing через функцию map, которая применяет make_all на список номеров страниц (range(13170, 13710)
"""




def get_names(num_page):
    req = requests.get(f"https://premierliga.ru/match/match_{num_page}.html")
    soup = BeautifulSoup(req.text, "lxml")
    dev1 = soup.find_all("div", class_="club home")
    team1 = dev1[1].text.split(" ")[0].strip()
    dev2 = soup.find_all("div", class_="club away")
    team2 = dev2[1].text.split(" ")[0].strip()
    return [team1, team2]


def count_hav_and_bomb(num_page):
    req = requests.get(f"https://premierliga.ru/match/match_{num_page}.html")
    soup = BeautifulSoup(req.text, "lxml")
    dev = soup.find("table", class_="staff-club").text
    b = dev.split("(")
    b.pop(0)
    count_forward_1 = sum(["НАП" in b[i] for i in range(0, len(b), 2)])
    count_forward_2 = sum(["НАП" in b[i] for i in range(1,len(b), 2)])
    count_hav_1 = sum(["П/З" in b[i] for i in range(0,len(b), 2)])
    count_hav_2 = sum(["П/З" in b[i] for i in range(1,len(b), 2)])
    return [count_forward_1, count_forward_2, count_hav_1, count_hav_2]



#получение количества угловых
def corners_count(num_page):
    #настройка входа
    chromedriver = '/Windows/ChromeDriver/chromedriver'
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)

    #получение индекса iframe
    url = f"https://premierliga.ru/match/match_{num_page}.html"
    driver.get(url)
    e = driver.find_element_by_tag_name("indexarea")
    disqus_iframe = e.find_element_by_tag_name('iframe')
    iframe_url = disqus_iframe.get_attribute('src')
    driver.get(iframe_url)

    #получение количества угловых
    wait = WebDriverWait(driver, 5)
    count_corners_present = presence_of_element_located((By.CLASS_NAME, "t-compare__stats-row"))
    wait.until(count_corners_present)
    corners_count_span = driver.find_elements_by_class_name('t-compare__stats-row')
    a = corners_count_span[5].text.split()
    target = int(a[0])+int(a[2])

    driver.quit()

    return [target]

def write_csv(data):
    with open("resul.csv", "a", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def make_all(num_page):
    try:
        data = get_names(num_page) + count_hav_and_bomb(num_page) + corners_count(num_page)
        print(data)
        write_csv(data)
    except:
        pass
if __name__ == "__main__":
   """ all_pages = range(13170, 13736)
    with Pool(10) as p:
        p.map(make_all, all_pages)"""