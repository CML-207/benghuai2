# 自动完成每日存在感以及10分钟在线任务
# written by Zhenlin Tan
# 暂未解决的问题： 如果模拟器卡死则无法操作
# 暂未解决的问题： 升级时出现额外界面
# 暂未解决的问题： 同意信息清单 （ 点击“确定”）
# 暂未解决的问题： 新获得头像， 需要点击
# 基于图像识别，每操作一次都要检查是否闪退，是否正在联网
# 需要关闭模拟器的按键提示（F12）

import random
import pyautogui as pa
import time as ti
import os
import cv2
import easyocr as eo
import numpy as np


def check_st():
    if pa.locateOnScreen(im_path + 'benghuaixueyuan2.png'):
        return True
    else:
        return False


def check_net():
    if pa.locateOnScreen(im_path + 'wangluolianjiezhong.png'):
        return True
    else:
        return False


def qianghuashimo():
    # 强化使魔
    if pa.locateOnScreen(im_path + 'zhuangbei_bai.png'):
        pa.click(im_path + 'zhuangbei_bai.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'zhuangbei_hei.png'):
        pa.click(im_path + 'zhuangbei_hei.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'zhuangbeicangku.png'):
        pa.click(im_path + 'zhuangbeicangku.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'shimo.png')
        ti.sleep(sleep_s)
        if pa.locateOnScreen(im_path + 'xiayitiao.png'):
            pa.click(im_path + 'xiayitiao.png')
            ti.sleep(sleep_s)
            pa.click(im_path + 'xiayitiaofanhui.png')
            ti.sleep(sleep_s)

        pa.click([zpx + 265, zpy + 330])
        ti.sleep(sleep_s)
        # 识别文字，强化
        img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
        reader = eo.Reader(['ch_sim'])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        result = np.array(reader.readtext(img))

        while '强化' not in result[:, 1]:
            pa.click([zpx + 265, zpy + 330])  # 左上角使魔 的位置，无法通过识图点击
            ti.sleep(sleep_s)
            img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
            reader = eo.Reader(['ch_sim'])
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            result = np.array(reader.readtext(img))

        # result[:, 0] 里面是坐标信息
        index = np.argwhere(result[:, 1] == '强化').squeeze()
        xloc = (result[index][0][0][0] + result[index][0][2][0]) / 2
        yloc = (result[index][0][0][1] + result[index][0][2][1]) / 2
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
        pa.click(clicks=2)
        ti.sleep(sleep_s)

        # 寻找光碟作为材料
        i = 0
        while i < 1:
            if pa.locateOnScreen(im_path + 'guangdie.png'):
                i += 1
            else:
                ti.sleep(2)
                pa.mouseDown([zpx + 85, zpy + 85])
                pa.moveTo([zpx + 85, zpy + 400], duration=2)
                pa.mouseUp([zpx + 85, zpy + 400], duration=1)
                ti.sleep(2)
        pa.click(im_path + 'guangdie.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'xuanze.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'kaishiqianghua.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'qianghuaqueding.png')
        ti.sleep(7)

    if pa.locateOnScreen(im_path + 'shouye.png'):
        pa.click(im_path + 'shouye.png')
        ti.sleep(sleep_s)


def shijie_boss():
    if pa.locateOnScreen(im_path + 'zhandou.png') or pa.locateOnScreen(im_path + 'zhandou_bai.png'):
        try:
            pa.click(im_path + 'zhandou.png')
            ti.sleep(sleep_s)
        except:
            pa.click(im_path + 'zhandou_bai.png')
            ti.sleep(sleep_s)
        if pa.locateOnScreen(im_path + 'juqingguanqia.png'):
            pa.click(im_path + 'juqingguanqia.png')
            ti.sleep(sleep_s)
        if pa.locateOnScreen(im_path + 'huodong_hei.png'):
            pa.click(im_path + 'huodong_hei.png')
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

    if pa.locateOnScreen(im_path + 'shimodeai.png'):
        pa.click(im_path + 'shimodeai.png')
        pa.move(0, 100)
        ti.sleep(sleep_s)
        pa.click()
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'kuaijiezhandou.png'):
        pa.click(im_path + 'kuaijiezhandou.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'kuaijiezhandou_queding.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'shimodeai_queding.png')
        ti.sleep(sleep_s)
        pa.click(im_path + 'shimodeai_fanhui.png')
        ti.sleep(sleep_s)

    # 下面开始虚轴之庭
    if pa.locateOnScreen(im_path + 'xuzhouzhiting.png'):
        pa.click(im_path + 'xuzhouzhiting.png')
        ti.sleep(sleep_s)
        pa.click(zpx + 866, zpy + 666)  # "出击" 的位置，无法通过识图点击
        ti.sleep(sleep_s)
        while pa.locateOnScreen(im_path + 'kuaijiezhandou.png'):
            pa.click(im_path + 'kuaijiezhandou.png')
            ti.sleep(sleep_s)
            pa.click(im_path + 'kuaijiezhandou_queding.png')
            ti.sleep(10)
            pa.click(im_path + 'shimodeai_queding.png')
            ti.sleep(sleep_s)
        pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
        ti.sleep(sleep_s)


def lingshimo():
    # 已经返回，现在点击进入每日任务
    # 界面仍在世界boss界面
    pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
    ti.sleep(sleep_s)

    # 识别文字，使魔探险
    img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
    reader = eo.Reader(['ch_sim'])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    result = np.array(reader.readtext(img))

    while '使魔探险' not in result[:, 1]:
        pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
        ti.sleep(sleep_s)
        img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
        reader = eo.Reader(['ch_sim'])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        result = np.array(reader.readtext(img))

    # result[:, 0] 里面是坐标信息
    index = np.argwhere(result[:, 1] == '使魔探险').squeeze()
    xloc = (result[index][0][0][0] + result[index][0][2][0]) / 2
    yloc = (result[index][0][0][1] + result[index][0][2][1]) / 2
    pa.click(zpx + xloc, zpy + yloc)
    ti.sleep(sleep_s)

    # 开始领取体力
    for loop in ['jin', 'zi', 'lan', 'lv']:
        if pa.locateOnScreen(im_path + 'dianjilingqujiangli_%s.png' % loop):
            pa.click(im_path + 'dianjilingqujiangli_%s.png' % loop)
            ti.sleep(sleep_s)
            if pa.locateOnScreen(im_path + 'queding.png'):
                pa.click(im_path + 'queding.png')
                ti.sleep(sleep_s)
            else:
                pa.click()
                ti.sleep(sleep_s)
    # 领完后放使魔
    for loop in ['jin', 'zi', 'lan', 'lv']:
        if pa.locateOnScreen(im_path + 'dianjixuanzeshimo_%s.png' % loop):
            pa.click(im_path + 'dianjixuanzeshimo_%s.png' % loop)
            ti.sleep(sleep_s)
            if pa.locateOnScreen(im_path + 'yijianpaiqian.png'):
                pa.click(im_path + 'yijianpaiqian.png')
                ti.sleep(sleep_s)
            if pa.locateOnScreen(im_path + 'chufa.png'):
                pa.click(im_path + 'chufa.png')
                ti.sleep(sleep_s)
            # 识别文字，使魔探险
            img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
            reader = eo.Reader(['ch_sim'])
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            result = np.array(reader.readtext(img))
            if '使魔探险' not in result[:, 1]:
                pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
                ti.sleep(sleep_s)
                break
    # 识别文字，使魔探险
    img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
    reader = eo.Reader(['ch_sim'])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    result = np.array(reader.readtext(img))
    if '使魔探险' not in result[:, 1]:
        pa.click(zpx + 72, zpy + 164)  # "返回" 的位置，无法通过识图点击
        ti.sleep(sleep_s)


def cunzaigan():  # 领存在感以及社团体力
    # 识别文字，存在感
    img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
    reader = eo.Reader(['ch_sim'])
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    result = np.array(reader.readtext(img))
    # 领存在感并截图
    if '存在感' in result[:, 1]:
        # result[:, 0] 里面是坐标信息
        index = np.argwhere(result[:, 1] == '存在感').squeeze()
        xloc = (result[index][0][0][0] + result[index][0][2][0]) / 2
        yloc = (result[index][0][0][1] + result[index][0][2][1]) / 2
        pa.click(zpx + xloc, zpy + yloc)
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'yijianlingqu.png'):
        pa.click(im_path + 'yijianlingqu.png')
        ti.sleep(sleep_s)
        timenow = ti.gmtime()
        num = timenow.tm_year * 1e8 + timenow.tm_mon * 1e6 + int(st_time / 1e2) * 1e4 + int(st_time % 1e2) * 1e2 + timenow.tm_min
        pa.screenshot(im_path + "..\\data\\%d.png" % num)
        pa.click(clicks=2)
        ti.sleep(sleep_s)
    # 领社团体力
    if pa.locateOnScreen(im_path + 'shejiao.png'):
        pa.click(im_path + 'shejiao.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'wodeshetuan.png'):
        pa.click(im_path + 'wodeshetuan.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'keling.png'):
        pa.click(im_path + 'keling.png')
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'shetuan_lingqu.png'):
        pa.click(im_path + 'shetuan_lingqu.png')
        ti.sleep(sleep_s)
    while pa.locateOnScreen(im_path + 'queding.png'):
        pa.click(im_path + 'queding.png')
        ti.sleep(sleep_s)


def qidongyouxi(iaccount):  # 对第i个账号启动游戏, iaccount为 [0, 3]
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
        img = pa.screenshot(region=[zpx, zpy, zpx + simulator[0], zpy + simulator[1]])
        reader = eo.Reader(['ch_sim'])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        result = np.array(reader.readtext(img))
        if '账号切换' in result[:, 1] or '适龄提示' in result[:, 1]:
            # result[:, 0] 里面是坐标信息
            index = np.argwhere(result[:, 1] == '账号切换').squeeze()
            xloc = (result[index][0][0][0] + result[index][0][2][0]) / 2
            yloc = (result[index][0][0][1] + result[index][0][2][1]) / 2
            pa.click(zpx + xloc, zpy + yloc)
            ti.sleep(sleep_s)
            if pa.locateOnScreen(im_path + 'qiehuan.png'):
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
            if pa.locateOnScreen(im_path + 'kuaigeiwoxia.png'):
                pa.click(im_path + 'kuaigeiwoxia.png')  # png图片为快给我下icon
                ti.sleep(sleep_l * 2)
            else:
                ti.sleep(sleep_s)
        elif pa.locateOnScreen(im_path + 'benghuaixueyuan2.png'):
            i += 1
            qidongyouxi(iaccount)
        else:
            ti.sleep(sleep_s)

    # # 等待进入登陆界面
    # 角色过生日的判断、新增活动如转转乐的判断并没有加入
    i = 0
    while i < 1:
        if pa.locateOnScreen(im_path + 'lingqumeiriqiandao.png') or pa.locateOnScreen(
                im_path + 'jinribuzaitishi.png') or pa.locateOnScreen(im_path + 'gonggao.png') or pa.locateOnScreen(im_path + 'zhuangbei_hei.png'):
            i += 1
        else:
            pa.click([screen.height / 2, screen.width / 2])  # 注意顺序??
            ti.sleep(sleep_s)

    while pa.locateOnScreen(im_path + 'lingqumeiriqiandao.png'):
        pa.click(im_path + 'lingqumeiriqiandao.png')
        ti.sleep(sleep_s)
    while pa.locateOnScreen(im_path + 'jinribuzaitishi.png'):
        pa.click(im_path + 'jinribuzaitishi.png')
        ti.sleep(sleep_s)
    while pa.locateOnScreen(im_path + 'gonggao.png'):
        pa.click(im_path + 'gonggao.png')
        ti.sleep(sleep_s)
    while pa.locateOnScreen(im_path + 'lingquhuodongqiandao.png'):  # 活动签到
        pa.click(im_path + 'lingquhuodongqiandao.png')
        ti.sleep(sleep_s)


# start
sleep_s = 5  # sec
sleep_l = 15  # sec

ti.sleep(sleep_s)
timenow = ti.gmtime()
if timenow.tm_hour < 16:
    st_time = int(timenow.tm_mday * 1e2 + timenow.tm_hour + 8)
else:
    st_time = int((timenow.tm_mday + 1) * 1e2 + timenow.tm_hour - 16)
print('Program start at: %d 月 %d 日 %d 时 %d 分 \t' % (int(timenow.tm_mon), int(st_time / 1e2), int(st_time % 1e2),
                                                    int(timenow.tm_min)))

im_path = "C:\\Users\\90686\\Desktop\\benghuai_mnq\\meirirenwu\\"
simulator = [1600, 900]  # 模拟器窗口的分辨率，在模拟器设置中可查看，【宽，高】
screen = pa.size()
zpx = screen.width / 2 - simulator[0] / 2  # zero point, width
zpy = screen.height / 2 - simulator[1] / 2  # zero point, height
n_accounts = 4
need_run = n_accounts  ##
account_width = 123  # pix, 账号在选择时的宽度

for loop1 in range(need_run):  # 以n个账号循环，最多4个，n_max=3
    # 启动应用
    os.startfile("D:\\software\\mumu_mnq\\emulator\\nemu9\\EmulatorShell\\NemuPlayer.exe")
    ti.sleep(20)

    # 以推荐游戏按钮确认是否打开，并收起推荐
    while not (pa.locateOnScreen(im_path + 'shouqituijian.png') or pa.locateOnScreen(im_path + 'jinrireyoutuijian.png')):
        ti.sleep(sleep_s)
    if pa.locateOnScreen(im_path + 'shouqituijian.png'):
        pa.click(im_path + 'shouqituijian.png')
    ti.sleep(sleep_s)

    # 启动游戏
    qidongyouxi(n_accounts)
    # 开始计时
    start_time = ti.time()
    qianghuashimo()
    shijie_boss()
    lingshimo()
    cunzaigan()
    used_time = ti.time() - start_time
    # if used_time < 660:  # 补全11分钟在线时间
    #     ti.sleep(660 - used_time)

    timenow = ti.gmtime()
    num = timenow.tm_year * 1e8 + timenow.tm_mon * 1e6 + int(st_time / 1e2) * 1e4 + int(
        st_time % 1e2) * 1e2 + loop1
    pa.screenshot(im_path + "..\\data\\%d.png" % num)

    pa.keyDown('alt')
    ti.sleep(1 + random.random())
    pa.press('f4')
    ti.sleep(1 + random.random())
    pa.keyUp('alt')
    ti.sleep(1 + random.random())
    if pa.locateOnScreen(im_path + "tuichu.png"):
        pa.click(im_path + "tuichu.png")
    ti.sleep(10 + random.random())
