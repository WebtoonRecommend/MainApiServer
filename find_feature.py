from gensim.models import Word2Vec
from konlpy.tag import Okt
import pandas as pd

data = pd.read_csv('webtoon_comment.csv')
print(data)