import tkinter as tk
from tkinter import ttk, filedialog

from file_loader import load_json
from tfidf_processor import calculate_tfidf_for_articles

class TfIdfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TF-IDF 關鍵句分析工具")

        # 左右區域框架
        self.left_frame = tk.Frame(root)
        self.right_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左區域
        self.left_label = tk.Label(self.left_frame, text="左邊文章")
        self.left_label.pack()
        self.left_import_button = tk.Button(self.left_frame, text="匯入 JSON", command=self.load_left_json)
        self.left_import_button.pack()
        self.left_treeview = self.create_treeview(self.left_frame)
        self.left_treeview.pack(fill=tk.BOTH, expand=True)

        # 右區域
        self.right_label = tk.Label(self.right_frame, text="右邊文章")
        self.right_label.pack()
        self.right_import_button = tk.Button(self.right_frame, text="匯入 JSON", command=self.load_right_json)
        self.right_import_button.pack()
        self.right_treeview = self.create_treeview(self.right_frame)
        self.right_treeview.pack(fill=tk.BOTH, expand=True)

    def create_treeview(self, parent):
        # 創建 Treeview 顯示區
        treeview = ttk.Treeview(parent, columns=("sentence", "score"), show="headings", height=20)
        treeview.heading("sentence", text="句子")
        treeview.heading("score", text="權重")
        treeview.column("sentence", width=400, anchor="w")
        treeview.column("score", width=100, anchor="center")
        return treeview

    def load_left_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            # 1. 讀取 JSON 文件
            articles_sentences, titles = load_json(file_path)
            # 2. 計算 TF-IDF
            ranked_sentences_per_article = calculate_tfidf_for_articles(articles_sentences, titles)
            # 3. 顯示第一篇文章結果
            if ranked_sentences_per_article:
                self.display_results(self.left_treeview, ranked_sentences_per_article[0], titles[0])

    def load_right_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            # 1. 讀取 JSON 文件
            articles_sentences, titles = load_json(file_path)
            # 2. 計算 TF-IDF
            ranked_sentences_per_article = calculate_tfidf_for_articles(articles_sentences)
            # 3. 顯示第一篇文章結果
            if ranked_sentences_per_article:
                self.display_results(self.right_treeview, ranked_sentences_per_article[0], titles[0])

    def display_results(self, treeview, ranked_sentences, title):
        # 清空舊結果
        treeview.delete(*treeview.get_children())
        # 插入新結果
        treeview.insert("", "end", values=("標題: " + title, ""))
        for sentence, score in ranked_sentences:
            treeview.insert("", "end", values=(sentence, round(score, 4)))

if __name__ == "__main__":
    root = tk.Tk()
    app = TfIdfApp(root)
    root.mainloop()
