import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

# 加载Spacy模型
nlp = spacy.load("en_core_web_sm")

# 将所有操作票转换为操作项的列表
tickets = [
    "核对相关设备的运行方式\n将六竹线1187开关的控制把手切换到“就地”位置\n检查六竹线1187开关在分闸位置\n合上六竹线刀闸操作电源空气开关\n拉开六竹线线路侧11874刀闸",
    "核对相关设备的运行方式\n将六竹线1187开关的控制把手切换到“就地”位置\n检查六竹线1187开关在分闸位置\n合上六竹线刀闸操作电源空气开关\n合上六竹线线路侧11874刀闸"
]
items = set()
for ticket in tickets:
    items.update(ticket.split("\n"))
items.discard("")
items = list(items)

# 使用Spacy分析操作项之间的关系
def analyze_item(item):
    doc = nlp(item)
    return pd.Series({
        "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"]
    })
df = pd.DataFrame(items, columns=["item"])
df = df.join(df["item"].apply(analyze_item))

# 使用CountVectorizer将操作项转换为特征向量
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["item"])

# 训练随机森林分类器
y = df.index
clf = RandomForestClassifier()
clf.fit(X, y)

# 使用分类器确定正确的顺序
order = []
for i in range(len(items)-1):
    x = vectorizer.transform([items[i]])
    j = clf.predict(x)[0]
    order.append(items[j])
order.append(items[-1])

print(order)