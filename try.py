from PIL import Image, ImageTk
import tkinter as tk


def check_and_display_image(image_path):
    try:
        # 尝试打开图片
        with Image.open(image_path) as img:
            img.verify()  # 验证图片文件是否有效

        # 打开图片并显示在 Tkinter 窗口中
        root = tk.Tk()
        root.title("显示图片")

        # 加载图片
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)

        # 创建一个标签来显示图片
        label = tk.Label(root, image=img_tk)
        label.pack()

        # 运行 Tkinter 主循环
        root.mainloop()

        print(f"图片 '{image_path}' 能够成功打开并显示。")

    except Exception as e:
        print(f"无法打开或显示图片 '{image_path}'。错误: {e}")


if __name__ == "__main__":
    image_path = "Easter3.jpg"
    check_and_display_image(image_path)
