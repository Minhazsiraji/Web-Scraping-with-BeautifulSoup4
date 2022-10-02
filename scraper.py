import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
question_list = []

def main(tag,page):
    url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={page}&pagesize=15'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status
        time.sleep(2)
        
        soup = BeautifulSoup(response.content, 'lxml')
        questions = soup.find_all('div', class_="s-post-summary js-post-summary")
        
        for item in questions:
            questions = {
                'tag': tag,
                'title': item.find('a', class_="s-link").text,
                'link': 'https://stackoverflow.com' + item.find('a', class_="s-link")['href'],
                'vote': item.find('span', class_="s-post-summary--stats-item-number").text,
                'date': item.find('span', class_="relativetime")['title']
            }
            question_list.append(questions)
        return
    except Exception as e:
        print(e)
        
# From page 1 to 10 we are using the range (1,11) as our function takes two param one is tag & another is page no#
for x in range(1,11):
    main('java', x)


df = pd.DataFrame(question_list)
excel = df.to_excel('stackOverFlow_quastions.xlsx')

