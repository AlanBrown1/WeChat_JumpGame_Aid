import os, win32api, win32con,win32gui, time, math
import numpy as np
import pyautogui as pag
from PIL import ImageGrab, Image
from matplotlib import pyplot as plt
from pymouse import PyMouse

'''
	描述：自动识别自动跳跃，本代码使用截图的RGB进行小人和目标中心点坐标的提取
	作者：Alan Brown
	时间：2018-1-3
'''

# 判断小人的中心点坐标
def getPlayerCenter():
	resR = [image[x,y][0] for x in range(height) for y in range(width)]  # R
	resG = [image[x,y][1] for x in range(height) for y in range(width)]  # G
	resR = np.array(resR).reshape(height, width)[100:220,5:-4]
	resG = np.array(resG).reshape(height, width)[100:220,5:-4]
	range1 = list(range(55,75))
	range2 = list(range(60,71))
	ind1, ind2 = [], []
	for colInd in range(resR.shape[1]):
		temp = resR[:,colInd]
		for pixInd,pix in enumerate(temp):
			if (pix in range1) and (resG[pixInd,colInd] in range2):
				ind1.append(colInd)
				ind2.append(pixInd)
				break
	ind2 = np.array(ind2)
	tempInd = np.where(ind2==min(ind2))[0]
	tempInd = int(sum(tempInd)/len(tempInd))
	renColInd = ind1[tempInd]
	print(renColInd)
	plt.plot(np.ones((300,))*renColInd, list(range(300)), 'r-')

	resR = [image[x,y][0] for x in range(height) for y in range(width)]  # R
	resG = [image[x,y][1] for x in range(height) for y in range(width)]  # G
	resR = np.array(resR).reshape(height, width)[150:220,5:-4]
	resG = np.array(resG).reshape(height, width)[150:220,5:-4]
	resR = resR[::-1] # 数组转180度
	resG = resG[::-1] # 数组转180度
	rangePix = list(range(55,66))
	ind1 = 0
	ind2 = []
	isFound = False
	for rowInd,row in enumerate( resR ):
		for pixInd,pix in enumerate( row ):
			if pix in rangePix:
				ind1 = rowInd
				ind2.append( pixInd )
				isFound = True
		if isFound:
			tempWidthInd = int(sum(ind2)/len(ind2) + 5)
			tempCount1 = tempCount2 = 0
			for i in resR[:,tempWidthInd]:
				if i in list(range(55,75)):
					tempCount1 += 1
			for i in resG[ind1, :]:
				if i in list(range(60,70)):
					tempCount2 += 1
			if tempCount1 > 10 and tempCount2 > 10:
				break
			else:
				isFound = False
				ind2 = []
	RenHeightInd = 220 - ind1 - 4   # 小人中心点的纵坐标
	RenWidthInd = sum(ind2)/len(ind2) + 5   # 小人中心点的横坐标
	# plt.plot(RenWidthInd, RenHeightInd, 'r.')
	return RenWidthInd, RenHeightInd

# 判断目标中心点
def getTargetCenter():
	resR = np.array( [image[x,y][0] for x in range(height) for y in range(width)])  # R
	res = resR.reshape(height, width)[50:250,5:-4]
	ind1, ind2 = [], []
	for colInd in range(res.shape[1]):
		temp = res[:,colInd]
		for pixInd, pix in enumerate( temp[:-1] ): 
			cha = np.abs( int(temp[pixInd+1])-int(temp[pixInd]) )
			if cha > 5:
				ind1.append( pixInd ) # 每一列第一个差>5的像素所在的行索引
				ind2.append( colInd ) # 该像素所在的列索引
				break
	ind1 = np.array(ind1)
	tempInd = np.where(ind1==min(ind1))[0]
	tempInd = int( sum(tempInd)/len(tempInd) )
	trueColInd = ind2[tempInd] + 5  # 最小值所在的列索引
	plt.plot(np.ones((300,))*trueColInd, list(range(300)), 'r-')
	ind = []
	temp = res[:, trueColInd]
	for index,i in enumerate( temp ):
		cha = np.abs( int(i) - int(temp[min(ind1)+5]) )
		if cha < 5:
			ind.append( index )
	ind = np.array(ind)
	if len(ind)>40:
		truePos = (ind[0]+ind[-5])/2 + 50
	else:
		truePos = (ind[0]+ind[-1])/2 + 50
	# plt.plot(list(range(320)), np.ones((320,))*truePos, 'r-')


if __name__ == '__main__':

	image = ImageGrab.grab(bbox=(6, 200, 326, 500))  # 抓取截图
	image = np.array(image.getdata(), np.uint8).reshape(image.size[1], image.size[0], 3)
	# plt.imshow( image )
	height, width = image.shape[:2]  # 图像的高度、宽度
	RenWidthInd， RenHeightInd = getPlayerCenter()
	truePos, trueColInd = getTargetCenter()
	dis = np.sqrt( (RenWidthInd-trueColInd)**2 + (RenHeightInd-truePos)**2 ) # 距离
	if dis < 50: dis -= 10
	print("距离：", dis)

	# 激活total_control界面
	title=u'UNKNOWN-GENERIC_A15 (仅限非商业用途)'
	w1hd=win32gui.FindWindow(0,title)
	w2hd=win32gui.FindWindowEx(w1hd,None,None,None)
	win32gui.SetForegroundWindow(w2hd)  # 获取窗口焦点

	m = PyMouse()
	m.move(300,600)#鼠标移动到xy位置
	time.sleep(0.5)

	dragTime = 0.0035*dis + 0.0132
	# dragTime = 0.0042*dis + 0.0118
	pag.dragTo(300,600, dragTime)
	# plt.show()
