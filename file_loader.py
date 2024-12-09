import json
import spacy

def load_json(file_path):
    """
    讀取 JSON 文件，提取每篇文章的 content 並分句。
    返回值：
    - articles_sentences: 每篇文章的句子列表。
    - titles: 每篇文章的標題列表（用於顯示）。
    - article_data: 每篇文章的標題和內容對應的列表。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    articles_sentences = []
    titles = []
    article_data = {}

    nlp = spacy.load("en_core_web_sm")

    for article in data:
        content = article.get("content", "")
        if content:
            title = article.get("title", "Untitled")
            doc = nlp(content)
            sentences = [sent.text for sent in doc.sents]
            articles_sentences.append(sentences)
            titles.append(title)
            article_data[title] = content

    return articles_sentences, titles, article_data
