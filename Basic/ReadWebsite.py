import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv


def getWebsiteContent(webUrl):
    readPage = requests.get(webUrl)
    fullContent = readPage.text

    soup = BeautifulSoup(fullContent,"html.parser")

    if soup.body:
        for tags in soup.body.find_all(["script","atyle","img","input"]):
            tags.decompose()
        
        content = soup.get_text(separator="\n",strip=True)
        print(content)

def getWebSiteLink(webUrl):
    readPage = requests.get(webUrl)
    fullContent = readPage.text

    soup = BeautifulSoup(fullContent,"html.parser")
    if soup.body:
        links = [link.get("href") for link in soup.find_all(["a"]) if link]

        print(links)
        for link in links:
           
            if link.startswith("/"):
                link = "https://www.scientificgames.com"+link

            if link.startswith("https://www.scientificgames.com"):
                print("-------------")
                print(link)
                print("#######################################################")
                getWebsiteContent(link)

getWebsiteContent("https://www.scientificgames.com/")
getWebSiteLink("https://www.scientificgames.com/")
