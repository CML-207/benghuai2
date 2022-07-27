# 自动花水晶补体力肝阵营战，包含卡图检测自动退出，闪退检测自动启动崩崩
# 暂未解决的问题： 如果模拟器卡死则无法操作

import random
import pyautogui as pa
import time as ti
import cv2
import easyocr as eo
import numpy as np


clickinterval = 1  # 鼠标点击间隔，秒
loopinterval = 62  # 脚本完整循环时间，秒
looptime = 100  # 执行完整脚本的次数
screen = pa.size()
simulator = [1440, 810]  # 模拟器窗口的分辨率，在模拟器设置中可查看，【宽，高】
tl_min = 50  # 体力下限，小于这个值则花水晶补充体力
info_width = 500  # 信息框长度
info_height = 120  # 信息框高度
click1 = [1027, 1003]  # 按钮 ’操作录制‘ 的鼠标位置： x=1027, y=1003 # 使用函数 print(pa.position())
click2 = [775, 861]  # 按钮 ’执行‘ 的鼠标位置： x=775, y=861
keys = ['h', 'y', 'c', 'tab', 'z', 'r', 'e']
'''
keys_mean = ['点击任意花费体力大于下限的关卡', 'h',
            '点击选择助战好友', 'y',
            '点击确定', 'c',
            '点击返回', 'tab',
            '点击暂停', 'z',
            '点击退出', 'r',
            '点击战斗', 'e']  # 需要在模拟器设置对应快捷键,如需改正，反正keys中的几个按键即可
'''
ti.sleep(3)  # 切屏出模拟器，等待时间，当前界面需要在脚本执行界面


timenow = ti.gmtime()
if timenow.tm_hour < 16:
    st_time = int(timenow.tm_mday * 1e2 + timenow.tm_hour + 8)
else:
    st_time = int((timenow.tm_mday + 1) * 1e2 + timenow.tm_hour - 16)

img = pa.screenshot(region=[screen.width/2 - simulator[0]/2, screen.height/2 - simulator[1]/2, info_width, info_height])
reader = eo.Reader(['en'])
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
result = reader.readtext(img)
'''
# 检查从信息框中识别出的内容，应当包含名字、水晶、金币、体力等数字内容，中文内容错误识别为正常现象
for i in result:
    print(i[1])
'''
shuijing = np.array(result[2][1]).astype(np.int_)  # 如水晶不是第3个识别内容，谨慎调整数字“2”
print('Program strat at: %d 月 %d 日 %d 时 %d 分 \t' % (int(timenow.tm_mon), int(st_time/1e2), int(st_time%1e2), int(timenow.tm_min)), '水晶： %d' % shuijing)

word = result[-1][1]
try:
    tl = np.array(word[0:len(word) - 4]).astype(np.int_)
except:
    tl = 200

if tl < tl_min:
    pa.press('%s' % keys[0])  # 模拟器快捷键，点击某界面中的关卡
    ti.sleep(1 + random.random())
    pa.press('%s' % keys[1])  # 模拟器快捷键，点击补充体力（与选择助战好友位置一致）
    ti.sleep(1 + random.random())
    pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
    ti.sleep(1 + random.random())
    pa.press('%s' % keys[3])  # 模拟器快捷键，点击“返回”（与游戏内切换助战位置一致）
    ti.sleep(1 + random.random())

suc = 0  # 成功次数
unsuc = 0  # 失败次数（闪退或者卡图）

for i in range(looptime):
    pa.click(click1)
    ti.sleep(1 + random.random())
    pa.click(click2)
    ti.sleep(1 + random.random())
    ti.sleep(loopinterval + random.random())
    pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，如不需要可去除
    ti.sleep(1 + random.random())
    img = pa.screenshot(region=[screen.width / 2 - simulator[0] / 2, screen.height / 2 - simulator[1] / 2, info_width, info_height])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    result = reader.readtext(img)
    words = []
    for j in result:
        words.append(j[1])
    if len(words):
        try:
            word = np.array(result[2][1]).astype(str)
        except:
            word = -1
        if word in words:  # 正常结束
            word = result[-1][1]
            try:
                tl = np.array(word[0:len(word) - 4]).astype(np.int_)
            except:
                tl = 200
            if tl < 50:
                pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，进入战斗界面，如不需要可去除
                ti.sleep(1 + random.random())
                pa.press('%s' % keys[0])  # 模拟器快捷键，点击某界面中的关卡
                ti.sleep(1 + random.random())
                pa.press('%s' % keys[1])  # 模拟器快捷键，点击补充体力（与选择助战好友位置一致）
                ti.sleep(1 + random.random())
                pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
                ti.sleep(1 + random.random())
                pa.press('%s' % keys[3])  # 模拟器快捷键，点击返回（与游戏内切换助战位置一致）
                ti.sleep(1 + random.random())
            del img, result, words, word
            suc += 1
        elif len(words) != 0:  # 可能识别了血量，代表卡图了，需要退出关卡
            pa.press('%s' % keys[4])  # 模拟器快捷键，点击“暂停”
            ti.sleep(1 + random.random())
            pa.press('%s' % keys[5])  # 模拟器快捷键，点击“退出”
            ti.sleep(1 + random.random())
            pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
            ti.sleep(5 + random.random())
            unsuc += 1
    else:
        ti.sleep(10 + random.random())
        pa.click('C:\\Users\\90686\\Desktop\\icon0.png')  # png图片为崩崩icon，程序会点击icon中心启动游戏
        ti.sleep(60 + random.random())  # 60为模拟器大致启动时间，秒
        for a in range(5):
            pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，如不需要可去除
            ti.sleep(1 + random.random())
        unsuc += 1

# 结束部分
timenow = ti.gmtime()
if timenow.tm_hour < 16:
    st_time = int(timenow.tm_mday * 1e2 + timenow.tm_hour + 8)
else:
    st_time = int((timenow.tm_mday + 1) * 1e2 + timenow.tm_hour - 16)

img = pa.screenshot(region=[screen.width/2 - simulator[0]/2, screen.height/2 - simulator[1]/2, info_width, info_height])
reader = eo.Reader(['en'])
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
result = reader.readtext(img)
shuijing = np.array(result[2][1]).astype(np.int_)
print('Program end at: %d 月 %d 日 %d 时 %d 分 \t' % (int(timenow.tm_mon), int(st_time/1e2), int(st_time%1e2), int(timenow.tm_min)), '水晶： %d' % shuijing)
