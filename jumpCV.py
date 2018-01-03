import os, win32api, win32con,win32gui, time, math, cv2
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
from matplotlib import pyplot as plt
from pymouse import PyMouse

'''
	描述：自动识别自动跳跃，本代码使用OpenCV模板匹配进行小人和目标中心点坐标的提取
	作者：Alan Brown
	时间：2018-1-3
'''

def get_center(img_canny, ):
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    y_top = np.nonzero([max(row) for row in img_canny[400:]])[0][0] + 250
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))
    y_bottom = y_top - 55
    for row in range(y_bottom, H):
        if canny_img[row, x_top] != 0:
            y_bottom = row
            break
    plt.plot(list(range(200)), np.ones((200,))*y_top)
    plt.plot(list(range(200)), np.ones((200,))*y_bottom)
    print(x_top, y_top, y_bottom)
    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return img_canny, x_center, y_center

# 匹配小跳棋的模板
temp1 = cv2.imread('temp_player.jpg', 0)
w1, h1 = temp1.shape[::-1]
# 匹配小圆点的模板
temp_white_circle = cv2.imread('temp_white_circle.jpg', 0)
w2, h2 = temp_white_circle.shape[::-1]

# 循环100次
count = 0
while True:

	image = ImageGrab.grab(bbox=(6, 70, 330, 630))  # 抓取屏幕
	# image = ImageGrab.grab(bbox=(90, 510, 243, 558))  # 再玩一局
	# image = ImageGrab.grab(bbox=(95, 335, 120, 400))  # 小人
	# image = ImageGrab.grab(bbox=(112, 315, 125, 328))  # 白点
	plt.imshow(image)
	image.save('screen.jpg')
	img_rgb = cv2.imread('screen.jpg', cv2.IMREAD_GRAYSCALE)

	# 显示截图
	# cv2.namedWindow('lena',cv2.WINDOW_AUTOSIZE)
	# cv2.imshow('lena',img_rgb)
	# k=cv2.waitKey(0)
	# if k==27:
	#     cv2.destroyAllWindows()

	# 匹配截图中小人的位置
	res1 = cv2.matchTemplate(img_rgb, temp1, cv2.TM_CCOEFF_NORMED)
	min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
	center1_loc = (max_loc1[0] + 12, max_loc1[1] + 56)

	# 先尝试匹配目标的中心，
	# 如果匹配值没有达到0.95，则使用边缘检测匹配物块上沿
	res2 = cv2.matchTemplate(img_rgb, temp_white_circle, cv2.TM_CCOEFF_NORMED)
	min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
	if max_val2 > 0.95:
	    x_center, y_center = max_loc2[0] + w2 // 2, max_loc2[1] + h2 // 2
	else:
	    # 边缘检测
	    img_rgb = cv2.GaussianBlur(img_rgb, (5, 5), 0)
	    canny_img = cv2.Canny(img_rgb, 1, 10)
	    H, W = canny_img.shape
	    # 消去小跳棋轮廓对边缘检测结果的干扰
	    for k in range(max_loc1[1], max_loc1[1] + 65):
	        for b in range(max_loc1[0], max_loc1[0] + 25):
	            canny_img[k][b] = 0
	    img_rgb, x_center, y_center = get_center(canny_img)

	plt.plot(x_center, y_center, 'b.')
	plt.plot(center1_loc[0], center1_loc[1], 'r.')

	distance = np.sqrt( (center1_loc[0] - x_center) ** 2 + (center1_loc[1] - y_center) ** 2 )

	# 激活total_control界面
	title=u'UNKNOWN-GENERIC_A15 (仅限非商业用途)'
	w1hd=win32gui.FindWindow(0,title)
	w2hd=win32gui.FindWindowEx(w1hd,None,None,None)
	win32gui.SetForegroundWindow(w2hd)  # 窗口置于前端

	m = PyMouse()
	m.move(300,600)  # 鼠标移动到x,y位置
	# dragTime = 0.0042*distance + 0.0118
	dragTime = 0.0035*distance + 0.0132
	pag.dragTo(300,600, dragTime)  # 按压

	count += 1
	if count > 100 : break