from scraper import scrape
from model import run_model

def run(create_df=False):
    if create_df:
        scrape(start=20)
    run_model()

if __name__ == '__main__':
    run(create_df=False)

