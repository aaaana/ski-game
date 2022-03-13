#configuraiton file
import os

# FPS
FPS = 40

#game screen size
SCREENSIZE = (640,640)

#image path
SKIER_IMAGE_PATHS = [
    os.path.join(os.getcwd(),'resources/images/skier_forward.png'),
    os.path.join(os.getcwd(),'resources/images/skier_right1.png'),
    os.path.join(os.getcwd(),'resources/images/skier_right2.png'),
    os.path.join(os.getcwd(),'resources/images/skier_left1.png'),
    os.path.join(os.getcwd(),'resources/images/skier_left2.png'),
    os.path.join(os.getcwd(),'resources/images/skier_fall.png')
]

OBSTACLE_PATHS = {
    'tree':os.path.join(os.getcwd(),'resources/images/tree.png'),
    'flag':os.path.join(os.getcwd(),'resources/images/flag.png')
}

# background music path
BGM_PATH = os.path.join(os.getcwd(),'resources/music/bgm.mp3')

# font path
FONT_PATH = os.path.join(os.getcwd(), 'resources/font/fzstk.TTF')