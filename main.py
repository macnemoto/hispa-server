from typing import Union
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from fastapi.middleware.cors import CORSMiddleware
# import httpx

from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:5173",
    # Puedes agregar más orígenes permitidos aquí
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    print('Dame la ip a sincronizar:')
    ip = input()
    print(f'Ip sincronizada con exito {ip}')
    return {"Hello": "World Neko"}

@app.get("/post/{post_id}")
def post_messages(post_id):
    comments = []
    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(f"https://8chan.moe/arepa/res/{post_id}.html")
            button = page.locator("body > div > fieldset > h1:nth-child(10) > a")
            button.click()
            # page.wait_for_timeout(10000)
            page.wait_for_load_state("load")
            
            op_numbers = page.query_selector("div.innerOP > div.opHead.title > span.spanId > span")
            comment_op_number = op_numbers.inner_text()
            id_numbers = page.query_selector_all("div > div.postInfo.title > span.spanId > span")
            comments_elements = page.query_selector_all("div > div.divMessage")
            for index, (comments_element,id_number)  in enumerate(zip(comments_elements, id_numbers)):
                # comment_id_number = id_number.inner_text()
                comment_content = comments_element.inner_text()
                if index == 0:
                    comments.append({f'idOp':comment_op_number,
                                        'messageOp':comment_content})
                else:
                    # print("a and b are equal")
                    true_numbers = index - 1
                    # print(id_numbers[true_numbers].inner_text())
                    id_final = id_numbers[true_numbers].inner_text()
                    comments.append({'id': id_final,
                                        'message':comment_content})
                    # comments.append({id_final:comment_content})
                    # comments.append({id_numbers[true_numbers].inner_text():comment_content})
            browser.close()
            return {"posts": comments}



# @app.get("/post/{post_id}")
# def post_messages(post_id: str):
#     # url = f"https://pokeapi.co/api/v2/pokemon/{post_id}"
#     url_terminos = 'https://8chan.moe/.static/pages/disclaimer.html'
#     url = f"https://8chan.moe/arepa/res/{post_id}.html"
    
#     sesscion = requests.Session()
#     response_terminos =  requests.get(url_terminos)
    
#     if response_terminos.status_code == 200:
#         soup_terminos = BeautifulSoup(response_terminos.content,'html.parser')
#         print(soup_terminos)
    
    
#         response =  requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print(soup)
#         try:
#             response.raise_for_status()
#             comments = soup.find_all('h2')
#             print(comments)
#             for comment in comments:
            
#                 print(comment.text)
#             return {"res": comment.text}
#         except requests.HTTPError as e:
#             print(e)
#             return {"Error": e}