from gensim.models import KeyedVectors
import pickle
import pandas as pd
import random


model = KeyedVectors.load_word2vec_format("descrip_w2v")  # 저장한 Word2Vec 모델 가져오기
Description = []

with open("Descrip.pkl", "rb") as f:  # pickle 파일에서 전처리한 Description 불러오기
    while True:
        try:
            data = pickle.load(f)
        except EOFError:
            break
        Description.append(data)

Title = []
with open("Title.pkl", "rb") as f:  # pickle 파일에서 전처리한 Title 불러오기
    while True:
        try:
            data = pickle.load(f)
        except EOFError:
            break
        Title.append(data)

Title = pd.DataFrame(Title, columns=["Title"])  # 리스트를 데이터프레임으로 변환

document = []
with open("document.pkl", "rb") as f:  # pickle 파일에서 전처리한 Title 불러오기
    while True:
        try:
            data = pickle.load(f)
        except EOFError:
            break
        document.append(data)

story_cosine = []
with open("Story_Cosine.pkl", "rb") as f:  # pickle 파일에서 전처리한 Title 불러오기
    while True:
        try:
            data = pickle.load(f)
        except EOFError:
            break
        story_cosine.append(data)

########################################################################## 함수

WebToon = Title[["Title"]]


def Recommendations10(titles, days):  # https://wikidocs.net/102705 참고
    if days > 100:  # days가 너무 커서 추천 목록을 넘어가는 경우를 보정
        days = random.randint(0, 100)

    indices = list(WebToon.index)
    doc2vec = 0
    for i in titles:
        idx = list(WebToon.index[WebToon["Title"] == i])
        idx = indices[idx[0]]
        doc2vec += document[idx]

    doc2vec = doc2vec / len(titles)

    sim_scores = list(enumerate(story_cosine[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    if days == 0:
        sim_scores = sim_scores[1:11]
    else:
        sim_scores = sim_scores[days * 10 : 10 * (days + 1)]

    WebToon_indices = [i[0] for i in sim_scores]

    recommend = WebToon.iloc[WebToon_indices].reset_index(drop=True)
    recommend = [["0", recommend["Title"][i]] for i in range(len(recommend["Title"]))]

    for i in range(len(recommend)):
        if i == len(recommend):
            break
        for j in titles:
            if recommend[i][1] == j:
                recommend.pop(i)
                break

    return recommend


def FirstRecommendations(
    words, days
):  # https://wikidocs.net/102705 참고, 처음 입력 받은 단어를 기반으로 추천, 처음 받은 단어의 word2vec값을 평균내어 입력
    if days > 19:  # days가 너무 커서 추천 목록을 넘어가는 경우를 보정
        days = random.randint(0, 20)
    doc2vec = 0  # word2vec의 평균을 저장할 변수

    for i in words:  # 추천받은 단어의 word2vec들을 모두 합하여 평균을 냄
        doc2vec += model[i]

    doc2vec = doc2vec / len(words)

    sim_scores = list(enumerate(doc2vec))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[days * 10 : (days + 1) * 10]

    WebToon_indices = [i[0] for i in sim_scores]

    recommend = WebToon.iloc[WebToon_indices].reset_index(drop=True)
    recommend = [["0", recommend["Title"][i]] for i in range(len(recommend["Title"]))]

    for i in range(len(recommend)):
        if i == len(recommend):
            break
        for j in words:
            if recommend[i][1] == j:
                recommend[i].pop(i)

    return recommend


# print(FirstRecommendations(["연애", "대학", "사랑"], 0))
# print(FirstRecommendations(["연애", "대학", "사랑"], 10000))

# print(Recommendations10(["나노리스트", "이두나!"], 10000))
# print(Recommendations10(["나노리스트", "이두나!"], 2))

# print(model.most_similar('대학원'))
