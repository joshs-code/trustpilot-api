import requests
from lxml import html
import json


class Trustpilot_Scraper():
    
    def __init__(self) -> None:
        self.data = []
        self.page = 1
    
    def check_reviews(self):

        print(f'Checking page {self.page}')
        base_url = f"https://www.trustpilot.com/review/pokeboost.net?page={self.page}"

        r = requests.get(base_url)

        tree = html.fromstring(r.text)
        
        review_card = tree.xpath('//div[@class="styles_reviewCardInner__EwDq2"]')
        while True:
            print(f'Review Cards Length = {len(review_card)}')
            if len(review_card) < 1:
                print(self.data)
                print(len(self.data))
            else:
                self.page+=1
                self.get_reviews(tree)
            break
            
    
    def get_reviews(self, tree):
        names = tree.xpath('//div[@class="styles_reviewCardInner__EwDq2"]//span[contains(@class, "typography_heading-xxs__QKBS8 typography_appearance-default__AAY17")]')
        dates = tree.xpath('//div[@class="styles_reviewCardInner__EwDq2"]//time')
        review_titles = tree.xpath('//div[@class="styles_reviewCardInner__EwDq2"]//h2')
        review_paragraph = tree.xpath('//div[@class="styles_reviewCardInner__EwDq2"]//p[@class="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"]')

        for name, date, title, comment in zip(names, dates, review_titles, review_paragraph):
            self.data.append({
                "name": name.text,
                "date": date.text,
                "title": title.text,
                "comment": comment.text
            })
            
        self.check_reviews()
        
s = Trustpilot_Scraper()
s.check_reviews()