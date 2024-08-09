from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from datetime import datetime
import charm  # 导入charm模块
from charm import check_easter_image, check_affection_status
class FocusApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        #ID
        self.nickname = self.load_or_ask_nickname()
        #设定目标
        self.check_and_set_daily_goal()

        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.focus_duration = 0
        self.focus_content = ""
        self.remaining_time = 0
        self.paused = False
        self.start_time = None
        self.elapsed_time = 0
        self.daily_focus_data = self.load_focus_data()

        self.default_font_size = 48  # 设置默认字体大小
        self.default_window_size = (250, 100)  # 设置默认窗口大小

        self.check_and_decrease_affection()  # 检查并减少好感度

        self.ask_focus_info()

    def load_or_ask_nickname(self):
        nickname_file = "nickname.txt"
        if os.path.exists(nickname_file):
            with open(nickname_file, "r") as file:
                return file.read().strip()
        else:
            nickname = simpledialog.askstring("输入昵称", "请输入你的昵称：")
            if nickname:
                with open(nickname_file, "w") as file:
                    file.write(nickname)
                return nickname
            else:
                self.root.quit()

    def check_and_set_daily_goal(self):
        charm.check_and_set_daily_goal()
    def ask_focus_info(self):
        self.focus_duration = simpledialog.askinteger("番茄钟", "多久：")
        self.focus_content = simpledialog.askstring("番茄钟", "干哈：")

        if self.focus_duration is None or self.focus_content is None:
            self.root.quit()
        else:
            self.remaining_time = self.focus_duration * 60
            self.start_time = datetime.now().strftime("%H:%M:%S")
            self.elapsed_time = 0
            self.show_timer_window()

    def show_timer_window(self):
        self.timer_window = tk.Toplevel(self.root)
        self.timer_window.title("I am Watching！")

        self.timer_window.resizable(True, True)

        window_width, window_height = self.default_window_size
        screen_width = self.timer_window.winfo_screenwidth()
        screen_height = self.timer_window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.timer_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        frame = tk.Frame(self.timer_window)
        frame.pack(expand=True, fill='both')

        # 定义颜色和字体颜色的字典
        theme_colors = {
            "pink": ("pink", "black"),
            "red": ("red", "black"),
            "green": ("green", "black"),
            "blue": ("blue", "white"),
            "yellow": ("yellow", "black"),
            "purple": ("purple", "white"),
            "orange": ("orange", "black"),
            "cyan": ("cyan", "black"),
            "indigo": ("indigo", "white"),
            "gray": ("gray", "black"),
            "darkred": ("darkred", "white"),
            "darkgreen": ("darkgreen", "white"),
            "darkblue": ("darkblue", "white"),
            "gold": ("gold", "black"),
            "silver": ("silver", "black"),
            "brown": ("brown", "white"),
            "lightpink": ("lightpink", "black"),
            "lightgreen": ("lightgreen", "black"),
            "lightblue": ("lightblue", "black"),
            "lightyellow": ("lightyellow", "black"),
            "lightpurple": ("lightpurple", "black")
        }

        # 检查 theme.txt 文件并设置背景和字体颜色
        theme_file = "theme.txt"
        if os.path.exists(theme_file):
            with open(theme_file, "r") as file:
                theme = file.read().strip()
                bg_color, fg_color = theme_colors.get(theme, ("white", "black"))
        else:
            current_hour = datetime.now().hour
            if 0 <= current_hour < 18:
                bg_color, fg_color = "white", "black"
            else:
                bg_color, fg_color = "black", "white"

        frame.config(bg=bg_color)

        self.timer_label = tk.Label(frame, text=self.format_time(self.remaining_time),
                                    font=("Helvetica", self.default_font_size),
                                    fg=fg_color, bg=bg_color, anchor="center")
        self.timer_label.pack(expand=True, fill='both')

        self.pause_button = tk.Button(self.timer_window, text="暂停", command=self.toggle_pause, fg=fg_color,
                                      bg=bg_color)
        self.pause_button.pack(side=tk.LEFT)

        self.end_button = tk.Button(self.timer_window, text="结束", command=self.end_focus, fg=fg_color, bg=bg_color)
        self.end_button.pack(side=tk.RIGHT)

        self.always_on_top_button = tk.Button(self.timer_window, text="置顶", command=self.toggle_always_on_top,
                                              fg=fg_color, bg=bg_color)
        self.always_on_top_button.pack(side=tk.TOP)

        self.update_timer()

    def update_timer(self):
        if not self.paused:
            self.remaining_time -= 1
            self.timer_label.config(text=self.format_time(self.remaining_time))

            if self.remaining_time <= 0:
                self.end_focus()
            else:
                self.root.after(1000, self.update_timer)

        self.adjust_font_size()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="继续")
        else:
            self.pause_button.config(text="暂停")
            self.update_timer()

    def end_focus(self):
        self.elapsed_time = self.focus_duration * 60 - self.remaining_time
        self.timer_window.destroy()
        self.save_focus_data()
####测试 删去not为无限制增加
        if not self.has_increased_affection_today():
            self.check_goal_and_increase_affection()  # 检查目标并增加好感度
        else:
            messagebox.showinfo("好感度限制", f"虽然{self.nickname}很棒。但是今天已经不能获得更多好感度啦")

        # 弹出提示框，询问用户是否继续
        if messagebox.askyesno("Focus Timer", f"{self.nickname}，再来？"):
            messagebox.showinfo("Focus Timer", f"{self.nickname}，想不到你意外的能坚持嘛！")
            self.ask_focus_info()
        else:
            messagebox.showinfo("Focus Timer", f"{self.nickname}，杂鱼！杂鱼！杂鱼！")
            self.root.quit()  # 使用 quit() 退出主循环，确保弹窗先显示

    def update_timer(self):
        if not self.paused:
            self.remaining_time -= 1
            self.timer_label.config(text=self.format_time(self.remaining_time))

            if self.remaining_time <= 0:
                self.end_focus()
            else:
                self.root.after(1000, self.update_timer)

        self.adjust_font_size()

    # def timer_finished(self):
    #     self.elapsed_time = self.focus_duration * 60
    #     self.end_focus()

    def load_focus_data(self):
        daily_data = {}
        if os.path.exists("focus_data.txt"):
            with open("focus_data.txt", "r") as file:
                lines = file.readlines()
                current_date = ""
                for line in lines:
                    if line.startswith("日期:"):
                        current_date = line.split("日期: ")[1].strip()
                        if current_date not in daily_data:
                            daily_data[current_date] = {"total_time": 0, "projects": {}}
                    elif "专注内容" in line:
                        parts = line.split("，")
                        content = parts[2].split("专注内容: ")[1].strip()
                        minutes = int(parts[1].split("专注时间: ")[1].strip("分钟"))
                        if content not in daily_data[current_date]["projects"]:
                            daily_data[current_date]["projects"][content] = 0
                        daily_data[current_date]["projects"][content] += minutes
                        daily_data[current_date]["total_time"] += minutes
        return daily_data

    def save_focus_data(self):
        elapsed_minutes = self.elapsed_time // 60

        if self.current_date not in self.daily_focus_data:
            self.daily_focus_data[self.current_date] = {"total_time": 0, "projects": {}}

        if self.focus_content not in self.daily_focus_data[self.current_date]["projects"]:
            self.daily_focus_data[self.current_date]["projects"][self.focus_content] = 0

        self.daily_focus_data[self.current_date]["total_time"] += elapsed_minutes
        self.daily_focus_data[self.current_date]["projects"][self.focus_content] += elapsed_minutes

        with open("focus_data.txt", "a") as file:

            file.write(f"日期: {self.current_date}\n")
            file.write(f"开始时间: {self.start_time}，专注时间: {elapsed_minutes}分钟，专注内容: {self.focus_content}\n")
            file.write(
                f"当天该内容总时长: {self.daily_focus_data[self.current_date]['projects'][self.focus_content]}分钟\n")
            file.write(f"一天内总专注时长: {self.daily_focus_data[self.current_date]['total_time']}分钟\n\n")

    def has_increased_affection_today(self):
        record_file = "affection_record.txt"
        if os.path.exists(record_file):
            with open(record_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    date, _ = line.strip().split(": ")
                    if date == self.current_date:
                        return True
        return False

    def check_goal_and_increase_affection(self):
        goal_file = "daily_goal.txt"
        if os.path.exists(goal_file):
            with open(goal_file, "r") as file:
                for line in file:
                    date, goal = line.strip().split(": ")
                    if date == self.current_date:
                        if self.daily_focus_data[self.current_date]["total_time"] >= int(goal):
                            messagebox.showinfo("爱你！", f"对{self.nickname}大人的好感度增加 9 点！")
                            charm.increase_affection_points()  # 直接调用增加好感度的函数
                            self.record_affection_increase()  # 记录好感度增加


    def record_affection_increase(self):
        record_file = "affection_record.txt"
        with open(record_file, "a") as file:
            file.write(f"{self.current_date}: Increased\n")

    def check_and_decrease_affection(self):
        last_opened_file = "last_opened.txt"
        if os.path.exists(last_opened_file):
            with open(last_opened_file, "r") as file:
                last_opened_date = file.read().strip()
                if last_opened_date != self.current_date:
                    current_affection = charm.get_affection_points()  # 获取当前好感度
                    decrease_amount = 10
                    new_affection = max(current_affection - decrease_amount, -50)  # 计算新的好感度，确保不低于 -50
                    charm.set_affection_points(new_affection)  # 设置新的好感度值
                    messagebox.showinfo("好感度减少", f"由于{self.nickname}的冷落，好感度-5！{self.nickname}坏！")
        with open(last_opened_file, "w") as file:
            file.write(self.current_date)

    def adjust_font_size(self):
        window_width = self.timer_window.winfo_width()
        window_height = self.timer_window.winfo_height()

        if window_width > self.default_window_size[0] or window_height > self.default_window_size[1]:
            new_font_size = min(window_width, window_height) // 3
        else:
            new_font_size = self.default_font_size

        self.timer_label.config(font=("Helvetica", new_font_size))

    def toggle_always_on_top(self):
        if self.timer_window.attributes("-topmost"):
            self.timer_window.attributes("-topmost", False)
            self.always_on_top_button.config(text="置顶")
        else:
            self.timer_window.attributes("-topmost", True)
            self.always_on_top_button.config(text="不置顶")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口以避免干扰

    # # 尝试检查并显示 Easter 图片
    # try:
    #     check_easter_image(root)
    # except Exception as e:
    #     messagebox.showerror("错误", f"在检查或显示 Easter 图片时发生错误: {e}")
    #
    # # 尝试检查并显示好感度状态
    # try:
    #     check_affection_status()
    # except Exception as e:
    #     messagebox.showerror("错误", f"在检查好感度状态时发生错误: {e}")

    # 创建 FocusApp 实例
    app = FocusApp(root)

    # 显示主窗口
     # 显示主窗口
    root.mainloop()