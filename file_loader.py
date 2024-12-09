import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer

def load_json(file_path):
    """
    讀取 JSON 文件，提取每篇文章的 content 並分句。
    返回值：
    - articles_sentences: 每篇文章的句子列表。
    - titles: 每篇文章的標題列表（用於顯示）。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    articles_sentences = []
    titles = []

    tokenizer = PunktSentenceTokenizer()

    for article in data:
        content = article.get("content", "")
        if content:
            title = article.get("title", "Untitled")
            sentences = tokenizer.tokenize(content)
            articles_sentences.append(sentences)
            titles.append(title)

    return articles_sentences, titles
