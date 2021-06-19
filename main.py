import requests
from bs4 import BeautifulSoup as bs
import time
from settings import URL, CHECK_INTERVAL
from database import DatabaseInterface

db = DatabaseInterface() #database interface

def get_response(url=URL, pars=""):
    r = requests.get(url+pars)
    return r

def pretty_post_print(title, description, href, data_post_id):
    print(f"""{' NEW POST '.center(30, '-')}
    Title: {title}\n
    Description: {description}\n
    Data-news-id: {data_post_id}\n
    Original link: {href}\n{'-'*30}\n\n
        """)

def parse():
    response = get_response(pars='news/') #get response form '/news/'
    soup = bs(response.text, 'lxml')

    post_set = soup.find("div", class_="r24NewsList")
                                                #VVVVVVVVVVVV we can use re.compile("^r24_article") insead of lambda function
    last_post_id = post_set.find("div", class_=lambda article: article and article.startswith("r24_article")).get("data-newsid") 

    #loop check whether new posts are uploaded or not
    while 1:
        response = get_response(pars='news/')
        soup = bs(response.text, 'lxml')

        post_set = soup.find("div", class_="r24NewsList")
        posts = post_set.find_all("div", class_=lambda article: article and article.startswith("r24_article"))

        #get the current post id
        #after what we will compare it with the last post id to check for new posts
        current_post_id = posts[0].get("data-newsid")

        print("last_post_id:", last_post_id)
        if current_post_id != last_post_id:
            #go through all posts
            for post in posts:
                data_post_id = post.get("data-newsid")
                #check whether post is new or not
                if data_post_id != last_post_id:

                    #print new post
                    href = post.find("div", class_="r24_body").find('a').get("href")
                    title = post.find("h3").find("span").text.strip()
                    description = post.find("span", class_="r24_desc").text.strip()
                
                    #insert post to database and commit changes
                    db.add_post((title, description, href, int(data_post_id)))
                    pretty_post_print(title, description, href, data_post_id)

                elif data_post_id == last_post_id:
                    break
            last_post_id = current_post_id
        
        time.sleep(CHECK_INTERVAL)



        
if __name__ == "__main__":
    parse()