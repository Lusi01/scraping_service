import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
domain = 'https://www.work.ua/'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
resp = requests.get(url, headers=headers)
jobs = []
errors = []
if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', id='pjax-job-list')
    if main_div:
        div_list = main_div.find_all('div', attrs={'class': 'job-link'})
        # если поиск по id, которые все разные => (берем значение, которое просто есть:
        # div_list = main_div.find_all('div', attrs={'id': True})

        for div in div_list:
            title = div.find('h2')
            href = title.a['href']
            content = div.p.text
            company = 'No name'
            logo = div.find('img')
            if logo:
                company = logo['alt']
            jobs.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': content,
                    'company': company
                         })
    else:
        errors.append({'url': url, 'title': "Div does not exists"})
else:
    errors.append({'url': url, 'title': "Page do not response"})

h = codecs.open('work.text', 'w', 'utf-8')
h.write(str(jobs))

# сохранить в файл всю страницу в виде html
# h = codecs.open('work.html', 'w', 'utf-8')
# h.write(str(resp.text))

h.close()
