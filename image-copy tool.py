import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# 対象拡張子（ネット画像向け）
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# 対象フォルダ
BASE_DIRS = [
    Path.home() / "Downloads",
    Path.home() / "Pictures",
]

def unique_path(dst: Path) -> Path:
    if not dst.exists():
        return dst
    stem = dst.stem
    suffix = dst.suffix
    parent = dst.parent
    i = 1
    while True:
        new_path = parent / f"{stem}_{i}{suffix}"
        if not new_path.exists():
            return new_path
        i += 1

def collect_images():
    images = []
    for base in BASE_DIRS:
        if not base.exists():
            continue
        for root, _, files in os.walk(base):
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in IMAGE_EXTS:
                    images.append(p)
    return images

def run_copy():
    dst_dir = filedialog.askdirectory(title="コピー先フォルダを選択")
    if not dst_dir:
        return

    dst_dir = Path(dst_dir)
    images = collect_images()

    if not images:
        messagebox.showinfo("結果", "")
        return

    count = 0
    for img in images:
        try:
            dst = unique_path(dst_dir / img.name)
            shutil.copy2(img, dst)
            count += 1
        except Exception:
            pass

    messagebox.showinfo("完了", f"{count} 枚の画像をコピーしました")

# ---- UI ----
root = tk.Tk()
root.title("ネット画像コピー整理ツール")
root.geometry("420x200")
root.resizable(False, False)

label = tk.Label(
    root,
    text=(
        "ダウンロード・ピクチャにある\n"
        "ネット保存画像をコピーします\n\n"
        "※ 元ファイルは消えません"
    ),
    justify="center"
)
label.pack(pady=20)

btn = tk.Button(
    root,
    text="コピー先フォルダを選んで実行",
    command=run_copy,
    width=30,
    height=2
)
btn.pack()

root.mainloop()
