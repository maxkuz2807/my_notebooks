import pandas as pd
import numpy as np
import random

# def get_conclusion():
df = pd.read_json(r'C:\Users\Максим\Desktop\Аналитика данных\Notebooks\conclusions.json', lines=True)
df.columns = ['Название книги', 'Категория', 'Вывод']

# Удаляем лишнее из текста
def filter_function(x):
    if len(x)>20:
        x = x.partition('<')[0]
        x = x.partition('Удобно не только читать, но и слушать?')[0]
        return x
    else:
        return np.nan

df['Вывод'] = df['Вывод'].apply(filter_function)
df = df.dropna()


# Получение данных для вывода
def get_data(query_type, categories):
    if query_type == '1':
        data = df[df['Категория'].isin(categories)].reset_index(drop=True)
        c = data.iloc[random.randint(0, len(data))]
        print(c['Вывод'])
        print('***')
        print(f"Название книги: {c['Название книги']}")
        print(f"Категория: {c['Категория']}")

    elif query_type == '0':
        data = df[~df['Категория'].isin(categories)].reset_index(drop=True)
        c = data.iloc[random.randint(0, len(data))]
        print(c['Вывод'])
        print('***')
        print(f"Название книги: {c['Название книги']}")
        print(f"Категория: {c['Категория']}")

    else:
        print('Ошибка')

# Получение случайного вывода с учетом желаемых категорий
def get_random_conslusion():
    query_type = input('Нажми 0, чтобы исключить категории выводов, которые тебе неинтересны.\nНажми 1, чтобы выбрать интересующие категории\n')
    unique_categories = list(df['Категория'].unique())

    try:
        # Если нужно выбрать интересующие категории выводов
        if query_type=='1':
            # Вывод на экран доступных категорий
            print()
            print('Доступные категории:')
            print('0 - Любая')
            for n, i in enumerate((unique_categories), start=1):
                print(f"{str(n)} - {str(i)}")

            # Ввод интересующих категорий
            ci = list(set(str(input('Перечисли интересующие тебя категории (ввод через пробел)\n')).split()))
            print()
            print('***')
            # Для каждой цифры в указанных пользователем категориях
            cat_include = []
            categories = cat_include
            for i in ci:
                if i.isdigit():
                    i = int(i)
                    if i in range(1, len(unique_categories)+1):
                        cat_include.append(unique_categories[int(i)-1])
                        cat_include = categories

                    elif i==0 and ci==['0']:
                        categories = unique_categories
                    elif i==0 and len(ci)>1:
                        print('Неверно указаны(а) категории(я)')
                        break
                    else:
                        print('Неверно указаны(а) категории(я)')
                        break
                else:
                    print('Неверно указаны(а) категории(я)')
            get_data(query_type, categories)

        # Если нужно исключить неинтересующие категории выводов
        elif query_type=='0':
            print()
            print('Доступные категории:')
            for n, i in enumerate((unique_categories), start=1):
                print(f"{str(n)} - {str(i)}")

            ce = list(set(str(input('Перечисли категории, которые тебе неинтересны (ввод через пробел)\n')).split()))
            print()
            print('***')
            cat_exclude = []
            if len(ce)<5:
                for i in ce:
                    if i.isdigit():
                        i = int(i)
                        if i in range(1, len(unique_categories)+1):
                            cat_exclude.append(unique_categories[int(i)-1])
                            categories = cat_exclude
                        else:
                            print('Неверно указаны(а) категории(я)')
                            break
                    else:
                        print()
                        print('Неверно указаны(а) категории(я)')
                get_data(query_type, categories)
            else:
                print('Неверно указаны(а) категории(я)')

        else:
            print('Неверное значение. Необходимо выбрать 0 или 1')
    except:
        print()

get_random_conslusion()



