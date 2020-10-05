from urllib import request
from bs4 import BeautifulSoup 
import time
import math
import random
import os
import logging
import codecs
import re

def print_str_code(str):
    print(str)
    for char in str:
        print("%X " % ord(char), end="")
    print("")

    
class Poetry:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
    

def crawl_url(url, poetry_list):
    with request.urlopen(url) as page:
        data = page.read()
        contents=data.decode()
        # print('Data:', contents)
        
        soup = BeautifulSoup(contents,"html.parser")
        
        article=soup.select_one(".shici_card")
        for poem in article.select("div"):
            author=poem.select_one(".list_num_info")
            poem_main=poem.select_one(".shici_list_main")
            
            if author:
                author=author.get_text().splitlines()
                if(len(author) != 5):
                    print("line %d" % len(author))
                author=author[4].replace('\n', '').replace(' ', '')
                
                title=poem_main.select_one("a").get_text()
                
                content=poem_main.select_one(".shici_content")
                
                content=content.decode_contents()
                content=content.replace("<br/>", "\n")
                content=re.sub("<.*\\n", "", content)
                content=content.replace(" ", "")
                
                poetry_list.append(Poetry(title, author, content))
                # print(title)
                # print(author)
                # print(content)


POETRY_DELI='----------------------------------'

poetry_list=[]
for i in range(1, 3):
    url='https://www.shicimingju.com/shicimark/gaozhong_%d_0__0.html' % i
    try:
        crawl_url(url, poetry_list)
        print("poetry_list %d" % len(poetry_list))
    except Exception as e:
        print(url)
        logging.exception(e)
    else:
        time.sleep(random.randint(1,3))
        
def take_author(poetry):
    return poetry.author

poetry_list.sort(key=take_author)

with codecs.open("school2.txt", "w", "utf-8") as out:
    for i in range(len(poetry_list)):
        poetry=poetry_list[i]
        print(poetry.title, file=out)
        print(poetry.author, file=out)
        try:
            print(poetry.content, file=out)
        except Exception as e:
            print(poetry.content)
            logging.exception(e)
            
            
        if i != len(poetry_list)-1:
            print(POETRY_DELI, file=out)
            print("", file=out)
    
# catch_poetry('https://www.shicimingju.com/shicimark/tangshisanbaishou_%d_0__0.html', 2, 'tang300.txt')