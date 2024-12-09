from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_tfidf_for_articles(articles_sentences, titles):
    """
    對多篇文章的句子分別計算 TF-IDF，返回每篇文章中權重最高的 20 句。
    返回值：
    - ranked_sentences_per_article: 每篇文章的前 20 句排序結果。
    """
    ranked_sentences_per_article = []

    for sentences in articles_sentences:
        if not sentences:
            continue

        # 計算 TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()

        # 計算每個句子的總分
        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            words = sentence.split()
            score = sum(
                tfidf_matrix[idx, feature_names.index(word)]
                for word in words if word in feature_names
            )
            sentence_scores.append((sentence, score))

        # 排序並取前 20 句
        ranked_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:20]
        ranked_sentences_per_article.append(ranked_sentences)

    return ranked_sentences_per_article
