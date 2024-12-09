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
        self.left_import_button.pack(pady=5)
        self.left_treeview = self.create_treeview(self.left_frame)
        self.left_treeview.pack(fill=tk.BOTH, expand=True)

        # 右區域
        self.right_label = tk.Label(self.right_frame, text="右邊文章")
        self.right_label.pack()
        self.right_import_button = tk.Button(self.right_frame, text="匯入 JSON", command=self.load_right_json)
        self.right_import_button.pack(pady=5)
        self.right_treeview = self.create_treeview(self.right_frame)
        self.right_treeview.pack(fill=tk.BOTH, expand=True)

    def create_treeview(self, parent):
        # 創建 Treeview 顯示區
        treeview_frame = tk.Frame(parent)
        treeview = ttk.Treeview(treeview_frame, columns=("sentence", "score", "title"), show="headings", height=20)
        treeview.heading("sentence", text="句子")
        treeview.heading("score", text="權重")
        treeview.heading("title", text="標題")
        treeview.column("sentence", width=400, anchor="w")
        treeview.column("score", width=100, anchor="center")
        treeview.column("title", width=200, anchor="w")

        # 添加 Y 軸滑動條
        scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        treeview_frame.pack(fill=tk.BOTH, expand=True)

        # 隱藏滑動條
        scrollbar.pack_forget()

        # 綁定顯示滑動條事件
        treeview.bind("<Configure>", lambda e: self.toggle_scrollbar(treeview, scrollbar))

        return treeview

    def toggle_scrollbar(self, treeview, scrollbar):
        # 檢查資料顯示的長度是否超過視窗範圍
        if treeview.get_children():  # 檢查是否有任何項目
            if treeview.bbox("end") and treeview.bbox("end")[1] > treeview.winfo_height():
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                scrollbar.pack_forget()
        else:
            scrollbar.pack_forget()

    def load_json_and_display(self, treeview):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            # 1. 讀取 JSON 文件
            articles_sentences, titles = load_json(file_path)
            # 2. 計算 TF-IDF
            ranked_sentences_per_article = calculate_tfidf_for_articles(articles_sentences, titles)
            # 3. 顯示第一篇文章結果
            if ranked_sentences_per_article:
                self.display_results(treeview, ranked_sentences_per_article)

    def load_left_json(self):
        self.load_json_and_display(self.left_treeview)

    def load_right_json(self):
        self.load_json_and_display(self.right_treeview)

    def display_results(self, treeview, ranked_sentences):
        # 清空舊結果
        treeview.delete(*treeview.get_children())
        # 插入新結果
        for item in ranked_sentences:
            title = item['title']
            sentence = item['sentence']
            score = item['score']
            treeview.insert("", "end", values=(sentence, round(score, 4), title))

if __name__ == "__main__":
    root = tk.Tk()
    app = TfIdfApp(root)
    root.mainloop()
