import os
from datetime import datetime
from tkinter import simpledialog, Tk, messagebox
from tkinter import Toplevel, Label
from PIL import Image, ImageTk
import requests
from io import BytesIO

def check_easter_image(root):
    easter_file = "Easter"

    if not os.path.exists(easter_file):
        return

    with open(easter_file, "r") as file:
        content = file.read().strip()

    image_urls = {
        "I love china": "https://img.997pp.com/Tu/202104/b4431e35643b8cee4128efb77f4f3aeb.jpg",
        "Entering China without regrets in this life": "https://img.997pp.com/Tu/202104/9f60b5017813edd918c733dc3d1f4f85.jpg",
        "I will still be Chinese in the next life": "https://img.997pp.com/Tu/202104/9379015f07ca7ee247e2225d1ebc7e63.jpg"
    }

    image_url = image_urls.get(content)
    if image_url:
        try:
            response = requests.get(image_url)
            response.raise_for_status()

            # 从响应内容中创建一个图像对象
            image_data = BytesIO(response.content)
            image = Image.open(image_data)

            # 创建一个 Toplevel 窗口并显示图像
            top = Toplevel(root)
            top.title("Easter Image")

            # 获取图像原始尺寸
            original_width, original_height = image.size

            # 设定窗口宽高比
            window_width = 800
            aspect_ratio = original_height / original_width
            window_height = int(window_width * aspect_ratio)

            # 调整窗口大小
            top.geometry(f"{window_width}x{window_height}")

            # 调整图像大小以适应窗口
            image = image.resize((window_width, window_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label = Label(top, image=photo)
            label.photo = photo  # 保持对图像的引用
            label.pack()

            print(f"Successfully loaded image: {image_url}")
        except Exception as e:
            print(f"Error opening image from URL: {e}")
    else:
        print(f"No image URL for content: {content}")
def check_affection_status():
    affection_file = "affection_points_total.txt"

    if not os.path.exists(affection_file):
        return

    # Initialize the Tkinter root window (hidden)
    root = Tk()
    root.withdraw()

    with open(affection_file, "r") as file:
        points = int(file.read().strip())

    if points < -40:
        message = "理我远些。"
    elif -40 <= points < -30:
        message = "你让我觉得很恶臭。"
    elif -30 <= points < -20:
        message = "抓紧时间努努力吧。"
    elif -20 <= points < -10:
        message = "你让我有些厌恶。"
    elif -10 <= points < 0:
        message = "废物。"
    elif 0 <= points < 10:
        message = ".......\n密码1：我爱中国"
    elif 10 <= points < 20:
        message = "你好啊。初次见面。"
    elif 20 <= points < 30:
        message = "嗯？干嘛？"
    elif 30 <= points < 40:
        message = "我记住你了！"
    elif 40 <= points < 50:
        message = "我开始对你有些兴趣了喔"
    elif 50 <= points < 60:
        message = "最近你还蛮努力的嘛...... \n密码2：Entering China without regrets in this life"
    elif 60 <= points < 70:
        message = "是不是很想要我为你记录时间呢？"
    elif 70 <= points < 80:
        message = "才没有想要被你使用呢！"
    elif 80 <= points < 90:
        message = "为什么才来？我，我有些想你了。"
    elif 90 <= points < 100:
        message = "再多爱我一点❤再多一点....再多一点"
    else:  # points >= 100
        message = "您的好感度已经达到了满级。谢谢主人。\n密码3：I will still be Chinese in the next life"

    # Display the message in a message box
    messagebox.showinfo("好感度对话", message)
    root.destroy()

if __name__ == "__main__":
    check_affection_status()


def check_and_set_daily_goal():
    current_date = datetime.now().strftime("%Y-%m-%d")
    goal_file = "daily_goal.txt"
    goal_set = False

    if os.path.exists(goal_file):
        with open(goal_file, "r") as file:
            for line in file:
                date, goal = line.strip().split(": ")
                if date == current_date:
                    goal_set = True
                    break

    if not goal_set:
        root = Tk()
        root.withdraw()
        goal_time = simpledialog.askinteger("Daily Goal", "输入今天的目标专注时间（分钟）：")
        if goal_time is not None:
            with open(goal_file, "a") as file:
                file.write(f"{current_date}: {goal_time}\n")
            messagebox.showinfo("Goal Set", f"今天的目标时间设置为 {goal_time} 分钟")
        root.destroy()

def get_affection_points():
    affection_file = "affection_points_total.txt"
    if os.path.exists(affection_file):
        with open(affection_file, "r") as file:
            return int(file.read().strip())
    return 0

def set_affection_points(points):
    affection_file = "affection_points_total.txt"
    with open(affection_file, "w") as file:
        file.write(str(points))

def increase_affection_points():
    affection_file = "affection_points.txt"
    last_increase_date = ""
    points_to_add = 9

    if os.path.exists(affection_file):
        with open(affection_file, "r") as file:
            lines = file.readlines()
            if lines:
                last_increase_date = lines[-1].strip()

    current_date = datetime.now().strftime("%Y-%m-%d")

    if last_increase_date != current_date:
        with open(affection_file, "a") as file:
            file.write(f"{current_date}\n")

        points = get_affection_points()
        points += points_to_add

        # Ensure affection points do not exceed 100
        if points > 100:
            points = 100
            messagebox.showinfo("好感度上限", "好感度已达到上限 100 点！")

        set_affection_points(points)

        return True
    return False

if __name__ == "__main__":
    increase_affection_points()  # 运行示例