from fastapi import FastAPI
from scraper import Scraper

app = FastAPI()
quotes = Scraper()

@app.get("/{url}")

async def read_item(url:str):

    return quotes.scrapedata(url)