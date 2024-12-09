import tkinter as tk
from tkinter import ttk, filedialog
import threading

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

        self.article_data = {}  # 新增 article_data 屬性

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
        treeview.bind("<Double-1>", self.show_details)

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
            # 使用 threading 來避免阻塞主線程
            threading.Thread(target=self.process_file, args=(file_path, treeview)).start()

    def process_file(self, file_path, treeview):
        # 1. 讀取 JSON 文件
        articles_sentences, titles, article_data = load_json(file_path)
        self.article_data = article_data  # 儲存 article_data
        # 2. 計算 TF-IDF
        ranked_sentences_per_article = calculate_tfidf_for_articles(articles_sentences, titles)
        # 3. 顯示第一篇文章結果
        if ranked_sentences_per_article:
            # 使用 tkinter 的 after 方法在主線程中更新 UI
            self.root.after(0, self.display_results, treeview, ranked_sentences_per_article)

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

    def show_details(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        values = item['values']
        if values:
            title = values[2]
            sentence = values[0]
            score = values[1]
            # 根據標題找到對應的文章資料
            article = self.article_data.get(title, "")
            detail_window = tk.Toplevel(self.root)
            detail_window.title("詳細資料")
            detail_text = tk.Text(detail_window, wrap=tk.WORD)
            detail_text.insert(tk.END, f"標題: {title}\n\n句子: {sentence}\n\n權重: {score}\n\n文章內容:\n\n{article}")
            detail_text.tag_configure("highlight", background="yellow")
            start_idx = article.find(sentence)
            if start_idx != -1:
                # Adjust the start and end index based on the actual content
                start_idx += len(f"標題: {title}\n\n句子: {sentence}\n\n權重: {score}\n\n文章內容:\n\n")
                end_idx = start_idx + len(sentence)
                detail_text.tag_add("highlight", f"1.0+{start_idx}c", f"1.0+{end_idx}c")
            detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            detail_text.config(state=tk.DISABLED)

            # 添加 Y 軸滾動條
            scrollbar = ttk.Scrollbar(detail_window, orient="vertical", command=detail_text.yview)
            detail_text.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # 調整視窗大小以符合內容
            detail_text.update_idletasks()
            detail_window.geometry(f"{detail_text.winfo_reqwidth()}x{detail_text.winfo_reqheight()}")
            # 確保滑鼠可以拉動滾動條
            detail_text.bind("<Enter>", lambda e: detail_text.bind_all("<MouseWheel>", lambda event: detail_text.yview_scroll(int(-1*(event.delta/120)), "units")))
            detail_text.bind("<Leave>", lambda e: detail_text.unbind_all("<MouseWheel>"))

if __name__ == "__main__":
    root = tk.Tk()
    app = TfIdfApp(root)
    root.mainloop()
