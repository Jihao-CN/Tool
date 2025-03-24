import piexif
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path
    
def clone_attributes():
    first_file = select_file()
    if not first_file:
        messagebox.showinfo("提示", "未选择文件，程序结束。")
        sys.exit()
    second_file = select_file()
    try:
        exif_dict = piexif.load(first_file)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, second_file)
        messagebox.showinfo("提示", "属性克隆成功")
    except Exception as e:
        messagebox.showerror("提示", f"发生错误: {e}")

clone_attributes()
