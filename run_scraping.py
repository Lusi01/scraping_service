import asyncio
import codecs
import os, sys
import datetime as dt
from django.db import DatabaseError
#from sqlite3 import DatabaseError

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()  # получим пользователя по умолчанию

parsers = (
    (work, 'work'),  #     (work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (dou, 'dou'),  #     (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'djinni'),  #     (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'),
    (rabota, 'rabota')  #     (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2')
)

jobs, errors = [], []

async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


# получение уникальных наборов пар city-language из БД My_users
def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

# получение url's заданных для пользователей
def get_urls(_settings):
    qs = Url.objects.all().values()  # получаем значения: id's
#qs = <QuerySet [{'id': 1, 'city_id': 3, 'language_id': 1, 'url_data': {'work':"'https://www.work.ua/ru/jobs-kyiv-python/", 'rabota': 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2', 'dou': 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python', 'djinni': 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'}}]>
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls


settings = get_settings()   # q: {(3, 1)}  # только уникальные пары!
url_list = get_urls(settings)
#u= [{'city': 3, 'language': 1, 'url_data': {'work': "'https://www.work.ua/ru/jobs-kyiv-python/", 'rabota':
# 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2', 'dou': 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python', 'djinni': 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'}}]

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

# import time
# start = time.time()
loop = asyncio.get_event_loop()
# создать список задач
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
                for data in url_list
                for func, key in parsers]
# запустить task на выполнение
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         # здесь происходит блокировка выполнения, пока не будет получен ответ на request
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()
#print(time.time() - start)

i = 0
j = 0
for job in jobs:
    j += 1
    # url = job['url']
    # title =job['title']
    # company =job['company']
    # description = job['description']
    #
    # Vacancy.objects.create(url=url, title=title, company=company, description=description,  city=city.name,
    #                        language=language.name)
    # job['city_id'] = city.id
    # job['language_id'] = language.id
    v = Vacancy(**job)  #, city_id=city.id, language_id=language.id)
  #  print(city)
    try:
    #    Vacancy.objects.create(**job, city_id=1, language_id=1)
        v.save() #update_fields=['url'])
        i+=1
    except DatabaseError:
        #print(str(DatabaseError))
        pass

if errors:
    er = Error(data=f'errors:{errors}').save()

print("Количество обработанных записей: ", i)
print("Количество записей всего: ", j)
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=errors).save()

# удалить записи из БД старше 10 дней
ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()



# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()