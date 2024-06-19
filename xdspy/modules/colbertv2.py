from typing import Any
import requests
from xdspy.utils import dotdict


class Colbertv2:
    def __init__(self, url="http://0.0.0.0", port=None) -> None:
        self.url = f"{url}:{port}" if port else url
        self.headers = {"Content-Type": "applications/json; charset=utf-8"}

    def post(self, query, k):
        payload = {"query": query, "k": k}
        res = requests.post(self.url, json=payload, headers=self.headers)
        # print(res)
        return res.json()["topk"][:k]

    def __call__(self, query, k=10, simplify=False) -> Any:
        topk = colbertv2_request(self.url, query, k)
        topk = [dotdict(psg) for psg in topk]
        if simplify:
            topk = [psg.long_text for psg in topk]
        return topk


def colbertv2_request(url, query, k):
    payload = {"query": query, "k": k}
    res = requests.get(url, params=payload)
    topk = res.json()["topk"][:k]
    return topk

    return res


{
    "topk": [
        {
            "text": 'Gary Zukav | Gary Zukav (born October 17, 1942) is an American spiritual teacher and the author of four consecutive New York Times Best Sellers. Beginning in 1998, he appeared more than 30 times on "The Oprah Winfrey Show" to discuss transformation in human consciousness concepts presented in his book "The Seat of the Soul". His first book, "The Dancing Wu Li Masters" (1979), won a U.S. National Book Award.',
            "pid": 3973781,
            "rank": 1,
            "score": 25.031627655029297,
            "prob": 0.9475815089744171,
            "long_text": 'Gary Zukav | Gary Zukav (born October 17, 1942) is an American spiritual teacher and the author of four consecutive New York Times Best Sellers. Beginning in 1998, he appeared more than 30 times on "The Oprah Winfrey Show" to discuss transformation in human consciousness concepts presented in his book "The Seat of the Soul". His first book, "The Dancing Wu Li Masters" (1979), won a U.S. National Book Award.',
        },
        {
            "text": 'The Dancing Wu Li Masters | The Dancing Wu Li Masters is a 1979 book by Gary Zukav, a popular science work exploring modern physics, and quantum phenomena in particular. It was awarded a 1980 U.S. National Book Award in category of Science. Although it explores empirical topics in modern physics research, "The Dancing Wu Li Masters" gained attention for leveraging metaphors taken from eastern spiritual movements, in particular the Huayen school of Buddhism with the monk Fazang\'s treatise on The Golden Lion, to explain quantum phenomena and has been regarded by some reviewers as a New Age work, although the book is mostly concerned with the work of pioneers in western physics down through the ages.',
            "pid": 2371226,
            "rank": 2,
            "score": 21.79088592529297,
            "prob": 0.03708346670173687,
            "long_text": 'The Dancing Wu Li Masters | The Dancing Wu Li Masters is a 1979 book by Gary Zukav, a popular science work exploring modern physics, and quantum phenomena in particular. It was awarded a 1980 U.S. National Book Award in category of Science. Although it explores empirical topics in modern physics research, "The Dancing Wu Li Masters" gained attention for leveraging metaphors taken from eastern spiritual movements, in particular the Huayen school of Buddhism with the monk Fazang\'s treatise on The Golden Lion, to explain quantum phenomena and has been regarded by some reviewers as a New Age work, although the book is mostly concerned with the work of pioneers in western physics down through the ages.',
        },
        {
            "text": 'Zukiswa Wanner | Zukiswa Wanner (born 1976) is a South African journalist and novelist, born in Zambia and now based in Kenya. Since 2006, when she published her first book, her novels have been shortlisted for awards including the South African Literary Awards (SALA) and the Commonwealth Writers\' Prize. In 2015 she won the K Sello Duiker Memorial Literary Award for "London Cape Town Joburg" (2014). In 2014 Wanner was named on the Africa39 list of 39 Sub-Saharan African writers aged under 40 with potential and talent to define trends in African literature.',
            "pid": 3664763,
            "rank": 3,
            "score": 20.907854080200195,
            "prob": 0.015335024323846005,
            "long_text": 'Zukiswa Wanner | Zukiswa Wanner (born 1976) is a South African journalist and novelist, born in Zambia and now based in Kenya. Since 2006, when she published her first book, her novels have been shortlisted for awards including the South African Literary Awards (SALA) and the Commonwealth Writers\' Prize. In 2015 she won the K Sello Duiker Memorial Literary Award for "London Cape Town Joburg" (2014). In 2014 Wanner was named on the Africa39 list of 39 Sub-Saharan African writers aged under 40 with potential and talent to define trends in African literature.',
        },
    ],
    "latency": 208.8487148284912,
}
