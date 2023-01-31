# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# 自动花水晶补体力肝阵营战，包含卡图检测自动退出，闪退检测自动启动崩崩
# 暂未解决的问题： 如果模拟器卡死则无法操作

import random
import pyautogui as pa
import time as ti
import cv2
import easyocr as eo
import numpy as np


def qidongyouxi():
    # 打开游戏
    pa.click(im_path + 'benghuaixueyuan2.png')  # png图片为崩崩icon，程序会点击icon中心启动游戏
    ti.sleep(3)
    if pa.locateOnScreen(im_path + 'tuichutanchuang.png'):
        pa.click(im_path + 'tuichutanchuang.png')
    ti.sleep(60 + random.random())  # 60为模拟器大致启动时间，秒
    # 或许需要下载资源
    try:
        pa.click(im_path + 'kuaigeiwoxia.png')  # png图片为快给我下icon
        ti.sleep(30)
    except:
        ti.sleep(3)
    # # 等待进入登陆界面

    # 还有每日第一次登陆的领取
    i = 0
    while i < 1:
        if pa.locateOnScreen(im_path + 'lingqumeiriqiandao.png') or pa.locateOnScreen(
                im_path + 'jinribuzaitishi.png') or pa.locateOnScreen(im_path + 'gonggao.png') or pa.locateOnScreen(im_path + 'zhuangbei_hei.png'):
            i += 1
        else:
            pa.click([screen.height / 2, screen.width / 2])  # 注意顺序??
            ti.sleep(5)

    while pa.locateOnScreen(im_path + 'lingqumeiriqiandao.png'):
        pa.click(im_path + 'lingqumeiriqiandao.png')
        ti.sleep(3)
    while pa.locateOnScreen(im_path + 'jinribuzaitishi.png'):
        pa.click(im_path + 'jinribuzaitishi.png')
        ti.sleep(3)
    while pa.locateOnScreen(im_path + 'gonggao.png'):
        pa.click(im_path + 'gonggao.png')
        ti.sleep(3)


clickinterval = 1  # 鼠标点击间隔，秒
loopinterval = 55  # 脚本完整循环时间，秒
looptime = 80  # 执行完整脚本的次数
screen = pa.size()
simulator = [1600, 900]  # 模拟器窗口的分辨率，在模拟器设置中可查看，【宽，高】
tl_min = 50  # 体力下限，小于这个值则花水晶补充体力，如果大于50，需要额外点击双倍券
info_width = 550  # 信息框长度
info_height = 135  # 信息框高度
# click1 = [1027, 1003]  # 按钮 ’操作录制‘ 的鼠标位置： x=1027, y=1003 # 使用函数 print(pa.position())
# click2 = [775, 861]  # 按钮 ’执行‘ 的鼠标位置： x=775, y=861
im_path = "C:\\Users\\90686\\Desktop\\benghuai_mnq\\meirirenwu\\"

keys = ['h', 'y', 'c', 'tab', 'z', 'r', 'e']
'''
keys_mean = ['点击任意花费体力大于下限的关卡', 'h',
            '点击选择助战好友', 'y',
            '点击确定', 'c',
            '点击返回', 'tab',
            '点击暂停', 'z',
            '点击退出', 'r',
            '点击战斗', 'e'
            '点击双倍券', 't']  # 需要在模拟器设置对应快捷键,如需改正，反正keys中的几个按键即可
'''
ti.sleep(3)  # 切屏出模拟器，等待时间，当前界面需要在脚本执行界面

timenow = ti.gmtime()
if timenow.tm_hour < 16:
    st_time = int(timenow.tm_mday * 1e2 + timenow.tm_hour + 8)
else:
    st_time = int((timenow.tm_mday + 1) * 1e2 + timenow.tm_hour - 16)

img = pa.screenshot(
    region=[screen.width / 2 - simulator[0] / 2, screen.height / 2 - simulator[1] / 2, info_width, info_height])
reader = eo.Reader(['en'])
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
result = reader.readtext(img)
'''
# 检查从信息框中识别出的内容，应当包含名字、水晶、金币、体力等数字内容，中文内容错误识别为正常现象
for i in result:
    print(i[1])
'''
shuijing0 = np.array(result[2][1]).astype(np.int_)  # 如水晶不是第3个识别内容，谨慎调整数字“2”
print('Program start at: %d 月 %d 日 %d 时 %d 分 \t' % (
int(timenow.tm_mon), int(st_time / 1e2), int(st_time % 1e2), int(timenow.tm_min)), '水晶： %d' % shuijing0)

word = result[-1][1]
try:
    tl = np.array(word[0:len(word) - 4]).astype(np.int_)
except:
    tl = 200

if tl < tl_min:
    pa.press('%s' % keys[0])  # 模拟器快捷键，点击某界面中的关卡
    ti.sleep(2 + random.random())

    pa.press('T')  ###
    ti.sleep(2 + random.random())

    pa.press('%s' % keys[1])  # 模拟器快捷键，点击补充体力（与选择助战好友位置一致）
    ti.sleep(2 + random.random())
    pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
    ti.sleep(2 + random.random())
    pa.press('%s' % keys[3])  # 模拟器快捷键，点击“返回”（与游戏内切换助战位置一致）
    ti.sleep(2 + random.random())

suc = 0  # 成功次数
unsuc = 0  # 失败次数（闪退或者卡图）

for i in range(looptime):
    pa.click(im_path + "..\\zhenyingzhan\\caozuoluzhi.png")
    ti.sleep(2 + random.random())
    pa.click(im_path + "..\\zhenyingzhan\\zhixing.png")
    ti.sleep(1 + random.random())
    ti.sleep(loopinterval + random.random())
    pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，如不需要可去除
    ti.sleep(1 + random.random())
    img = pa.screenshot(
        region=[screen.width / 2 - simulator[0] / 2, screen.height / 2 - simulator[1] / 2, info_width, info_height])
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
            if tl < tl_min:
                pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，进入战斗界面，如不需要可去除
                ti.sleep(2 + random.random())
                pa.press('%s' % keys[0])  # 模拟器快捷键，点击某界面中的关卡
                ti.sleep(2 + random.random())

                pa.press('T')  ###
                ti.sleep(2 + random.random())

                pa.press('%s' % keys[1])  # 模拟器快捷键，点击补充体力（与选择助战好友位置一致）
                ti.sleep(2 + random.random())
                pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
                ti.sleep(2 + random.random())
                pa.press('%s' % keys[3])  # 模拟器快捷键，点击返回（与游戏内切换助战位置一致）
                ti.sleep(2 + random.random())
            del img, result, words, word
            suc += 1
        elif len(words) != 0 and pa.locateOnScreen(im_path + "..\\zhenyingzhan\\benghuaixueyuan2_chang.png"):
            # 可能识别了血量，代表卡图了，需要退出关卡
            pa.press('%s' % keys[4])  # 模拟器快捷键，点击“暂停”
            ti.sleep(1 + random.random())
            pa.press('%s' % keys[5])  # 模拟器快捷键，点击“退出”
            ti.sleep(1 + random.random())
            pa.press('%s' % keys[2])  # 模拟器快捷键，点击“确定”
            ti.sleep(5 + random.random())
            unsuc += 1
        elif pa.locateOnScreen(im_path + "benghuaixueyuan2.png"):
            qidongyouxi()
            for a in range(5):
                pa.press('%s' % keys[6])  # 模拟器快捷键，点击“战斗”，如不需要可去除
                ti.sleep(1 + random.random())
            unsuc += 1
    elif pa.locateOnScreen(im_path + "benghuaixueyuan2.png"):
        qidongyouxi()
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

img = pa.screenshot(
    region=[screen.width / 2 - simulator[0] / 2, screen.height / 2 - simulator[1] / 2, info_width, info_height])
reader = eo.Reader(['en'])
img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
result = reader.readtext(img)
shuijing1 = np.array(result[2][1]).astype(np.int_)
print('Program end at: %d 月 %d 日 %d 时 %d 分 \t' % (
int(timenow.tm_mon), int(st_time / 1e2), int(st_time % 1e2), int(timenow.tm_min)), '水晶： %d' % shuijing1)
print('花费水晶： %d' % (shuijing0 - shuijing1))
print('成功次数： %d / %d， 失败次数： %d / %d' % (suc, looptime, unsuc, looptime))

pa.keyDown('alt')
ti.sleep(1 + random.random())
pa.press('f4')
ti.sleep(1 + random.random())
pa.keyUp('alt')
ti.sleep(1 + random.random())
if pa.locateOnScreen(im_path + "chongqi.png"):
    pa.click(im_path + "chongqi.png")
