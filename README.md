### WeChat_JumpGame_Aid
This repo contains some code to assist playing WeChat Jump game, using three methods to help you get higher scores.

### Tools Used
In this case, to run my code, you need some requried tools.

① A sofyware that connect&control your PC and cellphone is total_control, which can project your cellphone screen on yr PC and control it, Baidu knows that.

② Some python packages are needed, like most basicly numpy, matplotlib, pillow, and some a little bit more complex packages like os, pywin32, opencv, pymouse

### These three methods are:
① In jumpManual.py, you can manually select the centers of the player and target, then it knows the distance and press time.

② In jumpRGB.py, it automatically jumps, 'cause the algorithm itself identify the centers.

③ In jumpCV.py, it also automatically jumps, however, different from the above, it uses opencv to match the templates and get the center.

### Recommdation
Actually, I recommend the first methods, 'cause the last two are not mature yet, it may fail, because sometimes it'll get the wrong or inaccurate  centers.


