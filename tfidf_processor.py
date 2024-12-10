from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_tfidf_for_articles(articles_sentences, titles):
    """
    對多篇文章的句子分別計算 TF-IDF，返回所有文章中權重最高的 20 句。
    加入長度懲罰，避免長句因累積過多權重而過度占優。
    返回值：
    - top_sentences: 前 20 句排序結果，包含文章標題、句子和分數。
    """
    # 合併所有文章的句子並保留其對應的標題
    all_sentences = []
    sentence_to_title = []
    for i, sentences in enumerate(articles_sentences):
        for sentence in sentences:
            all_sentences.append(sentence)
            sentence_to_title.append(titles[i])

    # 計算 TF-IDF，排除 stop words
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_sentences)
    feature_names = vectorizer.get_feature_names_out()
    feature_index = {word: idx for idx, word in enumerate(feature_names)}  # 使用字典加速查找

    # 計算每個句子的總分並加入長度懲罰
    avg_length = sum(len(sentence.split()) for sentence in all_sentences) / len(all_sentences)
    alpha = 0.1  # 長度懲罰係數

    sentence_scores = []
    for idx, sentence in enumerate(all_sentences):
        words = sentence.split()
        if words:  # 避免空句子
            raw_score = sum(
                tfidf_matrix[idx, feature_index[word]]
                for word in words if word in feature_index
            )
            # 長度懲罰
            length_penalty = 1 + alpha * max(0, len(words) - avg_length)
            adjusted_score = raw_score / length_penalty
            sentence_scores.append({
                "sentence": sentence,
                "title": sentence_to_title[idx],
                "score": adjusted_score
            })

    # 移除重複的句子
    unique_sentences = {sentence["sentence"]: sentence for sentence in sentence_scores}.values()

    # 排序並取前 30 句
    top_sentences = sorted(unique_sentences, key=lambda x: x["score"], reverse=True)[:30]

    return top_sentences
