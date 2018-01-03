### WeChat_JumpGame_Aid
This repo contains some code to assist playing WeChat Jump game, using three methods to help you get higher scores. 

NO SIMUllLATOR needed.

### Tools used
In this case, to run my code, you need some requried tools.

① A software that connect&control yr PC and cellphone is "Total Control", which can project your cellphone screen on yr PC and control it, Baidu knows that.

② Some python packages are needed, like most basicly numpy, matplotlib, pillow, and some a little bit more complex packages like os, pywin32, opencv, pymouse.

### These three methods are:
① In jumpManual.py, you can manually select the centers of the player and target, then it knows the distance and press time.

② In jumpRGB.py, it automatically jumps, 'cause the algorithm itself identify the centers using the RGB information contained in the grabbed picture of yr cellphone screen.

③ In jumpCV.py, it also automatically jumps, however, different from the above, it uses opencv to match the templates and get the centers.

### Recommendation
Actually, I recommend the first methods, although it lacks efficiency, it's the most reliable.The last two are not mature yet, it may fail, because sometimes it'll get the wrong or inaccurate  centers.


