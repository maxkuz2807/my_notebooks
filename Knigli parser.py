# Программа для извлечения полезных выводов и идей из книг с сайта https://knigli.ru/

import json
import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36')

# Получение выводов

self_development = 'https://knigli.ru/samorazvitie/'
psychology = 'https://knigli.ru/psihologiya/'
marketing = 'https://knigli.ru/marketing-i-prodazhi/'
conversation = 'https://knigli.ru/peregovory/'
successful_stories = 'https://knigli.ru/istorii-uspeha/'

all_categories = [self_development, psychology, marketing, conversation, successful_stories]

def get_links(category):
    # Запуск браузера
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get(category)

    # Всего страниц
    pages = max([int(num.text) for num in driver.find_elements_by_xpath('//a[@class="page-numbers"]')])
    # Ссылки на выводы из книг для каждой книги
    links = []
    for page in range(1, pages+1):
        driver.get(category + f'page/{page}')
        time.sleep(3)
        links += [i.get_attribute('href') for i in driver.find_elements_by_class_name('post-title')]
    driver.close()
    return links

def flatten(l):
    return [item for sublist in l for item in sublist]

all_links = []
for i in all_categories:
    all_links.append(get_links(i))

all_links = flatten(all_links)

with open("Conclusions_links.txt", "w") as f:
    f.write("\n".join(all_links))

with open('Conclusions_links.txt') as f:
    all_links = f.readlines()
    all_links = [x.strip() for x in all_links]


# Получить выводы из книги
def write_conclusions_to_json(book_link):
    conclusions_dicts = []
    book_name = driver.find_element_by_tag_name('h1').text.partition('«')[2][:-1]
    book_category = driver.find_element_by_class_name('post-categories-container').text
    conclusions = [i.text for i in driver.find_elements_by_class_name('vc_column-inner') if
                   i.text and i.text[0].isdigit()]

    for i in range(len(conclusions)):
        conclusions_dict = {}
        conclusions_dict['book'] = book_name
        conclusions_dict['category'] = book_category
        conclusions_dict['conclusion'] = conclusions[i]
        conclusions_dicts.append(conclusions_dict)
        with open('conclusions1.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(conclusions_dict, ensure_ascii=False) + '\n')


# Повторный запуск браузера
all_conclusions = []
for link in all_links[:3]:
    driver = webdriver.Chrome(executable_path=r'C:\Users\Максим\Desktop\Аналитика данных\Notebooks\chromedriver.exe')
    driver.get(link)

    write_conclusions_to_json(link)

    time.sleep(3)
    driver.close()
    driver.quit()