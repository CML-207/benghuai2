import cv2
import numpy as np
import pyautogui
import tkinter as tk
import time
from multiprocessing import Manager, Pool
import threading
import keyboard


# def capture_screen(region):
#     # 截取屏幕指定区域
#     screenshot = pyautogui.screenshot(region=region)
#     frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#     return frame


def compare_images(imageA, imageB):
    # 创建一个掩码，排除黑色或偏黑色区域
    mask = cv2.inRange(imageA, np.array([0, 0, 0]), np.array(black_threshold))
    # 将掩码应用于图像
    imageA[mask != 0] = [0, 0, 0]
    mask = cv2.inRange(imageB, np.array([0, 0, 0]), np.array(black_threshold))
    imageB[mask != 0] = [0, 0, 0]
    # 移除黑色区域
    # imageA_clean = remove_black_areas(imageA, black_threshold)
    # imageB_clean = remove_black_areas(imageB, black_threshold)
    # 计算颜色直方图的相似性
    histA = cv2.calcHist([imageA], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    histB = cv2.calcHist([imageB], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(histA, histA)
    cv2.normalize(histB, histB)
    score = cv2.compareHist(histA, histB, cv2.HISTCMP_CORREL)
    return score


# def remove_black_areas(image, threshold):
#     # 创建一个掩码，排除黑色或偏黑色区域
#     mask = cv2.inRange(image, np.array([0, 0, 0]), np.array(threshold))
#     # 将掩码应用于图像
#     image[mask != 0] = [0, 0, 0]
#     return image

"""  # 多线程，延迟时间不统一无法控制
def perform_key_action1(key_now):
    keyboard.release(key_now)
    # time.sleep(short_sleep)
    # pyautogui.press(key_now)
    keyboard.press(key_now)
    time.sleep(press_sleep)
    keyboard.release(key_now)

def perform_key_action11(key_now):
    keyboard.press(key_now)
    time.sleep(press_sleep)
    keyboard.release(key_now)

def perform_key_action2(key_now):
    keyboard.release(key_now)

def perform_key_action22(key_now):
    keyboard.press(key_now)

def detection_loop(ikey):
    # 定义监控区域的坐标和大小
    region = (int(region0[0] - region0[2] / 2 + delta_key*ikey), region0[1] - pre_pixel - region0[3], region0[2],
              region0[3])  # (left, top, width, height)
    key_now = keys[ikey]
    region_x = region[0]
    region_y = region[1]
    region_width = region[2]
    region_height = region[3]
    # create_overlay(region_x, region_y, region_width, region_height)  # show search region

    down = False
    while True:
        # 捕获屏幕
        frame = capture_screen(region)
        # 比较与已知截图1
        score1 = compare_images(frame, known_image1)
        # 比较与已知截图2
        score2 = compare_images(frame, known_image2)
        # 检查匹配度是否达到阈值
        if score1 >= threshold1[ikey]:
            # 启动新线程执行按键操作
            if down:
                threading.Thread(target=perform_key_action1, args=(key_now)).start()
                down = False
            else:
                threading.Thread(target=perform_key_action11, args=(key_now)).start()
        if score2 >= threshold2[ikey]:
            if down:
                threading.Thread(target=perform_key_action2, args=(key_now)).start()
                down = False
            else:
                threading.Thread(target=perform_key_action22, args=(key_now)).start()
                down = True
        # 等待一段时间再进行下一次检测
        # time.sleep(0.1)
"""

# def press_key(ikey):
#     # 定义监控区域的坐标和大小
#     region = (int(region0[0] - region0[2] / 2 + delta_key*ikey), region0[1] - pre_pixel - region0[3], region0[2],
#               region0[3])  # (left, top, width, height)
#     key_now = keys[ikey]
#     region_x = region[0]
#     region_y = region[1]
#     region_width = region[2]
#     region_height = region[3]
#     # create_overlay(region_x, region_y, region_width, region_height)  # show search region
#
#     while True:
#         # 捕获屏幕
#         frame = capture_screen(region)
#         # 比较与已知截图1
#         score1 = compare_images(frame, known_image1)
#         # 比较与已知截图2
#         score2 = compare_images(frame, known_image2)
#         # 检查匹配度是否达到阈值
#         if score1 >= threshold1[ikey]:
#             time.sleep(short_sleep)
#             pyautogui.press(key_now)
#             time.sleep(long_sleep)
#         if score2 >= threshold2[ikey]:
#             time.sleep(short_sleep)
#             pyautogui.keyDown(key_now)
#             time.sleep(long_sleep)
#         # 等待一段时间再进行下一次检测
#         # time.sleep(0.05)

def press_key(ikey):
    # 定义监控区域的坐标和大小
    region = (int(region0[0] - region0[2] / 2 + delta_key*ikey), region0[1] - pre_pixel - region0[3], region0[2],
              region0[3])  # (left, top, width, height)
    key_now = keys[ikey]
    region_x = region[0]
    region_y = region[1]
    region_width = region[2]
    region_height = region[3]
    # create_overlay(region_x, region_y, region_width, region_height)  # show search region

    down = False
    # 更好的办法：检测一个函数，按键一个函数
    while True:
        # 捕获屏幕
        screenshot = pyautogui.screenshot(region=region)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # frame = capture_screen(region)
        # 比较与已知截图1
        score1 = compare_images(frame, known_image1)
        # 比较与已知截图2
        score2 = compare_images(frame, known_image2)
        # 检查匹配度是否达到阈值
        if score1 >= threshold1:
            if down:
                pyautogui.keyUp(key_now)
                # keyboard.release(key_now)
                pyautogui.press(key_now)
                down = False
                # time.sleep(short_sleep)

                # keyboard.press(key_now)
                # time.sleep(press_sleep)
                # keyboard.release(key_now)
            else:
                time.sleep(short_sleep)
                pyautogui.press(key_now)
                # keyboard.press(key_now)
                # time.sleep(press_sleep)
                # keyboard.release(key_now)
            # time.sleep(long_sleep)
        if score2 >= threshold2:
            if down:
                pyautogui.keyUp(key_now)
                # keyboard.release(key_now)
                down = False
            else:
                # time.sleep(short_sleep)
                pyautogui.keyDown(key_now)
                # keyboard.press(key_now)
                # time.sleep(0.1)
                down = True
            # time.sleep(long_sleep)
        # 等待一段时间再进行下一次检测
        # time.sleep(0.05)


def create_overlay(x, y, width, height):
    # 创建一个Tkinter窗口
    root = tk.Tk()
    root.title("Monitoring Overlay")

    # 设置窗口大小和位置
    root.geometry(f"{width}x{height}+{x}+{y}")

    # 使窗口透明
    root.attributes("-alpha", 0.5)  # 透明度
    root.attributes("-topmost", True)  # 保持在最上层
    root.overrideredirect(True)  # 去掉窗口边框

    # 设置背景颜色
    frame = tk.Frame(root, bg='red')
    frame.pack(fill=tk.BOTH, expand=True)

    # 运行Tkinter主循环
    root.mainloop()


keys = ['s', 'd', 'f', 'j', 'k', 'l']
region0 = (576, 822, 85, 85)  # 最左边按钮的中心位置+检测框宽度、高度
delta_key = 154  # 两键间距像素
pre_pixel = -10  # 提前3~5像素检测

# 读取已知截图
known_image1 = cv2.imread('C:\\Users\\Administrator\\Desktop\\benghuai_mnq\\map_test\\short_0.png')
known_image2 = cv2.imread('C:\\Users\\Administrator\\Desktop\\benghuai_mnq\\map_test\\long_0.png')

# 定义黑色阈值
black_threshold = (50, 50, 50)  # RGB值小于此阈值的区域被视为黑色
# 定义匹配度阈值(困难）：
# threshold1 = 0.905
# threshold2 = 0.815
# # long_sleep = 0
# short_sleep = 0.011
# press_sleep = 0.05
# 定义匹配度阈值(简单）：
threshold1 = 0.95
threshold2 = 0.9
# long_sleep = 0
short_sleep = 0.011
# press_sleep = 0.05
#
# def main():
#     threads = []
#     index = [1, 4]
#     for i in index:
#         thread = threading.Thread(target=press_key, args=(i,))
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()

if __name__ == "__main__":
    # main()
    # press_key(4)

    index = [0, 1, 2, 3, 4, 5]
    pool = Pool(processes=6)
    pool.map(press_key, index)
    pool.close()
    pool.join()
