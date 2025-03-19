import tkinter as tk
from tkinter import filedialog, messagebox
import os
import stat
import ctypes

# Windows API 常量
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_ARCHIVE = 0x20
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x2000
# Windows API 函数
SHGetSetSettings = ctypes.windll.shell32.SHGetSetSettings
SHGetFileInfoW = ctypes.windll.shell32.SHGetFileInfoW

class AttributeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("属性编辑")
        self.root.geometry("325x100")

        self.path_label = tk.Label(root, text="选择路径:")
        self.path_label.grid(row=0, column=0, padx=5, pady=3)

        self.path_entry = tk.Entry(root, width=18)
        self.path_entry.grid(row=0, column=1, padx=5, pady=3)

        self.select_file_button = tk.Button(root, text="选择文件", command=self.select_file)
        self.select_file_button.grid(row=0, column=2, padx=5, pady=3)

        self.read_only_var = tk.IntVar()
        self.read_only_checkbox = tk.Checkbutton(root, text="只读属性", variable=self.read_only_var)
        self.read_only_checkbox.grid(row=1, column=0, padx=5, pady=1)

        self.system_var = tk.IntVar()
        self.system_checkbox = tk.Checkbutton(root, text="系统属性", variable=self.system_var)
        self.system_checkbox.grid(row=1, column=1, padx=5, pady=1)

        self.hidden_var = tk.IntVar()
        self.hidden_checkbox = tk.Checkbutton(root, text="隐藏属性", variable=self.hidden_var)
        self.hidden_checkbox.grid(row=2, column=0, padx=5, pady=1)

        self.no_index_var = tk.IntVar()
        self.no_index_checkbox = tk.Checkbutton(root, text="无内容索引文件属性", variable=self.no_index_var)
        self.no_index_checkbox.grid(row=2, column=1, padx=5, pady=1)

        self.archive_var = tk.IntVar()
        self.archive_checkbox = tk.Checkbutton(root, text="存档属性", variable=self.archive_var)
        self.archive_checkbox.grid(row=2, column=2, padx=5, pady=1)
        
        self.start_button = tk.Button(root, text="开始", command=self.start_edit)
        self.start_button.grid(row=1, column=2, padx=5, pady=1)

    def select_file(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, file_path)
                self.read_attributes(file_path)
        except Exception as e:
            messagebox.showerror(f"选择文件失败: {str(e)}")

    def read_attributes(self, path):
        # 读取文件属性
        try:
            if os.path.isfile(path):
                file_stat = os.stat(path)
                if not (file_stat.st_mode & stat.S_IWRITE):
                    self.read_only_var.set(1)
                else:
                    self.read_only_var.set(0)
                if os.name == 'nt':
                    file_attributes = ctypes.windll.kernel32.GetFileAttributesW(path)
                    if file_attributes & FILE_ATTRIBUTE_HIDDEN:
                        self.hidden_var.set(1)
                    else:
                        self.hidden_var.set(0)
                    if file_attributes & FILE_ATTRIBUTE_SYSTEM:
                        self.system_var.set(1)
                    else:
                        self.system_var.set(0)
                    if file_attributes & FILE_ATTRIBUTE_ARCHIVE:
                        self.archive_var.set(1)
                    else:
                        self.archive_var.set(0)
                    if file_attributes & FILE_ATTRIBUTE_NOT_CONTENT_INDEXED:
                        self.no_index_var.set(1)
                    else:
                        self.no_index_var.set(0)
        except Exception as e:
            messagebox.showerror(f"读取属性失败：{str(e)}")

    def start_edit(self):
        # 选择文件
        path = self.path_entry.get()
        if not path:
            messagebox.showerror("请先选择文件。")
            return
        if not os.path.exists(path):
            messagebox.showerror("路径不存在，请重新选择。")
            return
        # 拼接命令
        attributes = ""
        if self.read_only_var.get():
            attributes += "+r "
        else:
            attributes += "-r "
        if self.system_var.get():
            attributes += "+s "
        else:
            attributes += "-s "
        if self.archive_var.get():
            attributes += "+a "
        else:
            attributes += "-a "
        if self.hidden_var.get():
            attributes += "+h "
        else:
            attributes += "-h "
        if self.no_index_var.get():
            attributes += "+i "
        else:
            attributes += "-i "
        # 执行命令
        command = f'cmd /c attrib {attributes}"{path}"'
        try:
            os.system(command)
            messagebox.showinfo("成功", "属性编辑成功。")
        except Exception as e:
            messagebox.showerror("错误", f"属性编辑失败：{str(e)}")

root = tk.Tk()
app = AttributeEditorApp(root)
root.mainloop()