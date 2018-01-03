import os, win32api, win32con, win32gui, time
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
from matplotlib import pyplot as plt
from pymouse import PyMouse

'''
	描述：本代码使用手动点击小人和目标中心获取距离
	作者：Alan Brown
	时间：2018-1-3
'''

count = 0
while True:
	time.sleep(1.5)
	# 抓取屏幕截图
	image = ImageGrab.grab(bbox=(6, 200, 326, 500))
	image = np.array(image.getdata(), np.uint8).reshape(image.size[1], image.size[0], 3)
	plt.imshow( image )
	pos = plt.ginput(2)
	dis = np.sqrt( (pos[0][0]-pos[1][0])**2 + (pos[0][1]-pos[1][1])**2 )
	if dis < 50: dis -= 10
	print("距离：", dis, end= ' ')

	title=u'UNKNOWN-GENERIC_A15 (仅限非商业用途)'
	w1hd=win32gui.FindWindow(0,title)
	w2hd=win32gui.FindWindowEx(w1hd,None,None,None)
	# 获取窗口焦点
	win32gui.SetForegroundWindow(w2hd)

	m = PyMouse()
	m.move(300,600)  # 鼠标移动
	time.sleep(0.5)

	dragTime = 0.0035*dis + 0.0132
	print('时间：', dragTime)
	pag.dragTo(300,600, dragTime)
	m.move(1000, 500)

	count += 1
	if count > 50: break

	plt.close()


