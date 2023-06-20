# 自动完成每日存在感以及10分钟在线任务
# written by Zhenlin Tan
# 基于图像识别，每操作一次都要检查是否闪退，是否正在联网
# 需要关闭模拟器的按键提示（F12）

import random
import pyautogui as pa
import time as ti
import os
import cv2
import easyocr as eo
import numpy as np
from datetime import datetime


def ocr_ch(x0, y0, x1, y1):  # 识别中文
    img = pa.screenshot(region=[x0, y0, x1, y1])
    reader = eo.Reader(['ch_sim'])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    res = np.array(reader.readtext(img))
    return res


def loc_str(res, string):  # 如果有多个结果，返回第一个结果的坐标
    # result[:, 0] 里面是坐标信息
    try:
        index = np.argwhere(res[:, 1] == string).squeeze()[0]  # 需要试试是否能加0
    except:
        index = np.argwhere(res[:, 1] == string).squeeze()
    xloc = (res[index][0][0][0] + res[index][0][2][0]) / 2
    yloc = (res[index][0][0][1] + res[index][0][2][1]) / 2
    return xloc, yloc


def start_simulator():
    os.startfile(simu_path)
    ti.sleep(sleep_l)
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '忽略本次更新' in result[:, 1]:
        xloc, yloc = loc_str(result, '忽略本次更新')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '立即下载' in result[:, 1]:
        pa.click(zpx + 1486, zpy + 68)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    while '崩坏学园2' not in result[:, 1]:
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '接受' in result[:, 1]:
        xloc, yloc = loc_str(result, '接受')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)


def select_account(iaccount):  # 对第i个账号启动游戏, iaccount为 [0, 3]
    # 打开游戏
    pa.click(im_path + 'benghuaixueyuan2.png')  # png图片为崩崩icon，程序会点击icon中心启动游戏
    ti.sleep(sleep_l)
    while pa.locateOnScreen(im_path + 'tuichutanchuang.png'):
        pa.click(im_path + 'tuichutanchuang.png')
    ti.sleep(sleep_l * 2 + random.random())  # sleep_s0为模拟器大致启动时间，秒

    # 进入抚摸界面，点击切换账号
    i = 0
    while i < 1:
        # 识别文字，要么需要下载资源，要么需要账号切换
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '接受' in result[:, 1]:  # 用户同意清单
            xloc, yloc = loc_str(result, '接受')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)

        elif '账号切换' in result[:, 1]:
            xloc, yloc = loc_str(result, '账号切换')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            while not pa.locateOnScreen(im_path + 'qiehuan.png'):
                ti.sleep(sleep_s)
            pa.click(im_path + 'qiehuan.png')  # png图片为快给我下icon
            ti.sleep(sleep_s)

            # 切换过程
            yloc = 275 + 0.5 * account_width
            pa.click(zpx + simulator[0] / 2, zpy + yloc)  # 选择账号
            ti.sleep(sleep_s)
            yloc = 275 + (iaccount + 0.5) * account_width
            pa.click(zpx + simulator[0] / 2, zpy + yloc)  # 选择账号
            ti.sleep(sleep_s)

            if pa.locateOnScreen(im_path + 'jinruyouxi.png'):
                pa.click(im_path + 'jinruyouxi.png')
                ti.sleep(sleep_s)
            while not pa.locateOnScreen(im_path + 'queding.png'):
                ti.sleep(sleep_s)
            pa.click(im_path + 'queding.png')
            ti.sleep(sleep_s)
            pa.click(zpx + simulator[0] / 2, zpy + simulator[1] / 2)
            ti.sleep(sleep_l)
            i += 1
        elif '快给我下' in result[:, 1]:
            # 或许需要下载资源
            # 过程中要check是否闪退了
            xloc, yloc = loc_str(result, '快给我下')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_l)

        elif pa.locateOnScreen(im_path + 'benghuaixueyuan2.png'):
            i += 1
            select_account(iaccount)
        else:
            ti.sleep(sleep_s)


def home_page():
    # # 等待进入登陆界面
    # 1.领7天循环的每日奖励； 2.生日； 3.今日不再提醒 * n； 4.关闭公告； 5.某些活动
    # 新增活动如转转乐的判断并没有加入
    i = 0
    while i < 1:
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '领取' in result[:, 1] or '今曰不再提示' in result[:, 1] or '系统公告' in result[:, 1] or '生曰快乐' in result[:, 1] or pa.locateOnScreen(
                    im_path + 'zhuangbei_hei.png'):
            i += 1
        else:
            pa.click([screen.width / 2, screen.height / 2])  # 注意顺序??
            ti.sleep(sleep_s)

    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '领取' in result[:, 1]:
        xloc, yloc = loc_str(result, '领取')
        pa.click(zpx + xloc, zpy + yloc)

        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '生曰快乐' in result[:, 1]:
        xloc, yloc = loc_str(result, '生曰快乐')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '确定' in result[:, 1]:  # 溢出
            xloc, yloc = loc_str(result, '确定')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '领取' in result[:, 1]:  # 溢出
            xloc, yloc = loc_str(result, '领取')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '今曰不再提示' in result[:, 1]:
        xloc, yloc = loc_str(result, '今曰不再提示')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '活动公告' in result[:, 1]:
        pa.click(zpx + 1490, zpy + 100)  # x 处， 无法识别
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    if pa.locateOnScreen(im_path + 'lingquhuodongqiandao.png'):  # 活动签到
        pa.click(im_path + 'lingquhuodongqiandao.png')
        ti.sleep(sleep_s)

    # 试图越过新获得cg或头像
    while not pa.locateOnScreen(im_path + 'tuichutanchuang.png') and '装备' not in result[:, 1]:
        pa.click(zpx + 1518, zpy + 33)  # x 处， 无法识别
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '确定' in result[:, 1]:
        xloc, yloc = loc_str(result, '确定')

        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])


def qianghuashimo():
    # 强化使魔
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '装备' in result[:, 1]:
        xloc, yloc = loc_str(result, '装备')
        pa.click(zpx + xloc, zpy + yloc)

        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '装备仓库' in result[:, 1]:
        xloc, yloc = loc_str(result, '装备仓库')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '确认' in result[:, 1]:
            xloc, yloc = loc_str(result, '确认')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '使魔' in result[:, 1]:
            xloc, yloc = loc_str(result, '使魔')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '下条' in result[:, 1]:
            xloc, yloc = loc_str(result, '下条')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '返回' in result[:, 1]:
            xloc, yloc = loc_str(result, '返回')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

        # 识别文字，强化
        while '强化' not in result[:, 1]:
            pa.click([zpx + 265, zpy + 330])  # 某个使魔， 无法定位
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        xloc, yloc = loc_str(result, '强化')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        pa.click(clicks=2)
        ti.sleep(sleep_s)
    
        # 寻找光碟作为材料
        i = 0
        while i < 1:
            if pa.locateOnScreen(im_path + 'guangdie.png') or pa.locateOnScreen(im_path + 'guangdie1.png'):
                i += 1
            else:
                ti.sleep(2)
                pa.mouseDown([zpx + 85, zpy + 85])
                pa.moveTo([zpx + 85, zpy + 400], duration=2)
                pa.mouseUp([zpx + 85, zpy + 400], duration=1)
                ti.sleep(2)
        try:
            pa.click(im_path + 'guangdie.png')
        except:
            pa.click(im_path + 'guangdie1.png')
        ti.sleep(sleep_s)

        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '选择_' in result[:, 1] or '选择' in result[:, 1]:  ##
            try:
                xloc, yloc = loc_str(result, '选择_')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
            except:
                xloc, yloc = loc_str(result, '选择')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '开始强化 ' in result[:, 1]:  ##
            xloc, yloc = loc_str(result, '开始强化 ')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '确定' in result[:, 1]:
            xloc, yloc = loc_str(result, '确定')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)


def shijie_boss():
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '战斗' in result[:, 1]:
        xloc, yloc = loc_str(result, '战斗')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '剧情关卡' in result[:, 1]:
        xloc, yloc = loc_str(result, '剧情关卡')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)

    if pa.locateOnScreen(im_path + 'huodong_bai.png'):
        pa.click(im_path + 'huodong_bai.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'huakuai.png'):
        pa.click(im_path + 'huakuai.png')
        ti.sleep(2)
        pa.mouseDown()
        pa.moveTo(zpx + 1565, zpy + 900, duration=2)
        pa.mouseUp()
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'duoyuanliefeng2.png'):
        pa.click(im_path + 'duoyuanliefeng2.png')
        ti.sleep(sleep_s)

    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '返回' in result[:, 1]:  ##周年庆活动，增加了一层说明
        xloc, yloc = loc_str(result, '返回')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '使魔爱' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '使魔爱')
        pa.click(zpx + xloc, zpy + yloc + 100)
        ti.sleep(sleep_s)

        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '使魔的爱' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '使魔的爱')
        pa.click(zpx + xloc, zpy + yloc + 100)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '使魔的爱 5' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '使魔的爱 5')
        pa.click(zpx + xloc, zpy + yloc + 100)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    if '快捷战斗' in result[:, 1]:
        xloc, yloc = loc_str(result, '快捷战斗')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '碾' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '碾')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)

    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '确定' in result[:, 1]:
        xloc, yloc = loc_str(result, '确定')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    if pa.locateOnScreen(im_path + 'shimodeai_fanhui.png'):
        pa.click(im_path + 'shimodeai_fanhui.png')
        ti.sleep(sleep_s)

    # 下面开始虚轴之庭
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '虚轴2屣' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '虚轴2屣')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '出' in result[:, 1]:  ##
        xloc, yloc = loc_str(result, '出')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    while '快捷战斗' in result[:, 1]:
        if '碾' in result[:, 1] or '确定' in result[:, 1]:  ##
            try:
                xloc, yloc = loc_str(result, '碾')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
                result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
            except:
                xloc, yloc = loc_str(result, '确定')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
                result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
            while '确定' in result[:, 1]:
                xloc, yloc = loc_str(result, '确定')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
                result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '快捷战斗' in result[:, 1]:
            xloc, yloc = loc_str(result, '快捷战斗')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    # 如果升级，这样可行吗？
    while '确定' in result[:, 1]:
        xloc, yloc = loc_str(result, '确定')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
    ti.sleep(sleep_s)


def lingshimo():
    # 已经返回，现在点击进入每日任务
    # 界面仍在世界boss界面
    # 识别文字，使魔探险
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '使魔探险' not in result[:, 1]:
        pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    xloc, yloc = loc_str(result, '使魔探险')
    pa.click(zpx + xloc, zpy + yloc)
    ti.sleep(sleep_s)

    # 开始领取体力
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '点击领取奖励' in result[:, 1]:
        xloc, yloc = loc_str(result, '点击领取奖励')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        pa.click()
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        while '确定' in result[:, 1]:
            xloc, yloc = loc_str(result, '确定')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    # 领完后放使魔
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '点击选择使魔' in result[:, 1]:
        xloc, yloc = loc_str(result, '点击选择使魔')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
        if '键派遣' in result[:, 1]:
            xloc, yloc = loc_str(result, '键派遣')
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
            if '出发' in result[:, 1]:
                xloc, yloc = loc_str(result, '出发')
                pa.click(zpx + xloc, zpy + yloc)
                ti.sleep(sleep_s)
                result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '使魔探险' not in result[:, 1]:
        pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
        ti.sleep(sleep_s)


def cunzaigan():  # 领存在感以及社团体力
    # 识别文字，存在感
    # 领存在感并截图
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '存在感' in result[:, 1]:

        xloc, yloc = loc_str(result, '存在感')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '键领取' in result[:, 1]:
        xloc, yloc = loc_str(result, '键领取')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        t0 = datetime.now().strftime('%Y%m%d_%H%M%S')
        pa.screenshot(im_path + "..\\data\\%s.png" % t0)
        pa.click(clicks=2)
        ti.sleep(sleep_s)

        pa.click(clicks=2)
        ti.sleep(sleep_s)

    # 20230616 新增, 因为存在感溢出的体力也会存到邮箱，需要点击确定
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    while '确定' in result[:, 1]:
        xloc, yloc = loc_str(result, '确定')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])

    # 领社团体力
    result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '{交' in result[:, 1]:
        xloc, yloc = loc_str(result, '{交')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '我的社团' in result[:, 1]:
        xloc, yloc = loc_str(result, '我的社团')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '可领' in result[:, 1]:
        xloc, yloc = loc_str(result, '可领')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        result = ocr_ch(zpx, zpy, zpx + simulator[0], zpy + simulator[1])
    if '领取' in result[:, 1]:
        xloc, yloc = loc_str(result, '领取')
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)


# start
sleep_s = 5  # sec
sleep_l = 15  # sec

ti.sleep(sleep_s)

print('Program start at: ', ti.ctime())
program_start = ti.time()

im_path = "C:\\Users\\Administrator\\Desktop\\benghuai_mnq\\meirirenwu\\"
simu_path = "E:\\MUMUmnq\\emulator\\nemu9\\EmulatorShell\\NemuPlayer.exe"
simulator = [1600, 900]  # 模拟器窗口的分辨率，在模拟器设置中可查看，【宽，高】
screen = pa.size()
zpx = screen.width / 2 - simulator[0] / 2  # zero point, width
zpy = screen.height / 2 - simulator[1] / 2  # zero point, height

n_accounts = 4

need_run = 4  ##
account_width = 123  # pix, 账号在选择时的宽度

for loop1 in range(need_run):  # 以n个账号循环，最多4个，n_max=3
    # 启动应用
    start_simulator()
    # 启动游戏
    select_account(n_accounts)
    home_page()
    # 开始计时
    start_time = ti.time()
    qianghuashimo()
    shijie_boss()
    lingshimo()
    cunzaigan()

    used_time = ti.time() - start_time
    if used_time < 660:  # 补全11分钟在线时间
        ti.sleep(660 - used_time)

    t1 = datetime.now().strftime('%Y%m%d_%H%M%S')
    pa.screenshot(im_path + "..\\data\\%s.png" % t1)

    pa.keyDown('alt')
    ti.sleep(1 + random.random())
    pa.press('f4')
    ti.sleep(1 + random.random())
    pa.keyUp('alt')
    ti.sleep(1 + random.random())
    if pa.locateOnScreen(im_path + "tuichu.png"):
        pa.click(im_path + "tuichu.png")
    ti.sleep(sleep_l + random.random())

print('Program end at: ', ti.ctime())
print('Used time: ', ti.time() - program_start)
