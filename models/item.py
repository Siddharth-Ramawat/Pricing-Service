import requests
import re
import uuid
from typing import Dict
from bs4 import BeautifulSoup
from .model import Model
from dataclasses import dataclass, field


@dataclass
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    # URL = 'https://www.johnlewis.com/kin-slim-fit-suit-jacket-black/p3399265'
    # self.url = 'https://www.johnlewis.com/richard-james-mayfair-pick-and-pick-suit-trousers-navy/p1877570'

    def __repr__(self):
        return f"<Item {self.url}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d*\.?\d?\d?)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        # print(price)
        return self.price

    # This is done to make the code more generic
    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price" : self.price,
            "query": self.query
        }
