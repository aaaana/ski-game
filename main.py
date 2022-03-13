'''
FUNCTION:
    SKI GAME
AUTHOR:
    ANNA
'''

import sys
import config
import pygame
import random

#create class Skier
class Skier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # skier's moving direction(-2,2)
        self.direction = 0
        self.imagepaths = config.SKIER_IMAGE_PATHS[:-1]
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320,100]
        self.speed = [self.direction, 6 - abs(self.direction)*2]

    #change direction, negative for left, positive for right, 0 for move
    def turn(self,num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image. get_rect()
        self.rect.center = center
        self.speed =[self.direction, 6 - abs(self.direction)*2]
        return self.speed

    # skier's move
    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)

    # fall class
    def fall(self):
        self.image = pygame.image.load(config.SKIER_IMAGE_PATHS[-1])

    #forward class
    def forward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagepaths[self.direction])

'''
FUNCTION:
    class OBSTACLE 
INPUT:
    image_path: image path of obstacle
    position: obstacle position
    attribute: attributes of obstacle
'''

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,img_path, position, attribute):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.attribute = attribute
        self.passed = False

    def move(self,num):
        self.rect.centery = self.position[1] - num

def createObstacle(s,e,num = 10):
    obstacles = pygame.sprite.Group()
    positions = []
    for i in range(num):
        row = random.randint(s,e)
        col = random.randint(0,9)
        position = [col * 64 + 20, row * 64 +20]
        if position not in positions:
            positions.append(position)
            attribute = random.choice(list(config.OBSTACLE_PATHS.keys()))
            img_path = config.OBSTACLE_PATHS[attribute]
            obstacle = Obstacle(img_path,position,attribute)
            obstacles.add(obstacle)
    return obstacles

# Add obstacles
def addObstacles(obstacles0,obstacles1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles

    #interface
def showStartInterface(screen,screensize):
    screen.fill((255,255,255))
    tfont = pygame.font.Font(config.FONT_PATH,screensize[0]//5)
    cfont = pygame.font.Font(config.FONT_PATH,screensize[0]//20)
    title = tfont.render(u'Ski Game',True,(255,0,0))
    content = cfont.render(u'Press any key to start the game',True,(0,0,255))
    trect = title.get_rect()
    trect.midtop = (screensize[0]/2, screensize[1]/5)
    crect = content.get_rect()
    crect.midtop = (screensize[0]/2, screensize[1]/2)
    screen.blit(title, trect)
    screen.blit (content, crect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()

    # show scores
def showScore(screen,score, pos=(10,10)):
    font = pygame.font.Font(config.FONT_PATH,30)
    score_text = font.render("Score: %s" %score, True,(0, 0, 0))
    screen.blit(score_text,pos)

    # update the game screen
def updateScreen(screen, obstacles, skier, score):
    screen.fill((255,255,255))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen,score)
    pygame.display.update()

#main program 
def main():
    # initialize game 
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(config.BGM_PATH)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    # set up screen
    screen = pygame.display.set_mode(config.SCREENSIZE)
    pygame.display.set_caption('Ski Game -- created by Anna')
    
    # Game Start Interface 
    showStartInterface(screen,config.SCREENSIZE)

    # Initialize Game sprites
    # Skier
    skier = Skier()

    # Create obstacle
    obstacle0 = createObstacle(20,29)
    obstacle1 = createObstacle(10,19)
    obstacleflag = 0
    obstacles =addObstacles(obstacle0,obstacle1)

    # Game timer
    timer = pygame.time.Clock()

    # record distance
    distance = 0
    # Record current score
    score = 0

    # Record current speed
    speed = [0,6]

    # for loop the game
    running =True
    while running:
        # capture event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                     speed = skier.turn(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    speed = skier.turn(1)
                elif event.key ==pygame.K_SPACE:
                    running = False

        # update the game of the current data
        skier.move()
        distance += speed[1]
        if distance >= 640 and obstacleflag == 0:
            obstacleflag = 1
            obstacles0 =createObstacle(20,29)
            obstacles = addObstacles(obstacle0,obstacle1)
        if distance >= 1280 and obstacleflag == 1:
            obstacleflag = 0
            distance -= 1280
            for obstacle in obstacle0:
                obstacle.position[1] = obstacle.position[1] - 1280
            obstacle1 = createObstacle(10,19)
            obstacles = addObstacles(obstacle0,obstacle1)
        for obstacle in obstacles:
             obstacle.move(distance)

        # check collide
        hitted_obstacles = pygame.sprite.spritecollide(skier,obstacles,False)
        if hitted_obstacles:
            if hitted_obstacles[0].attribute == "tree" and not hitted_obstacles[0].passed:
                score -= 50
                skier.fall()
                updateScreen(screen,obstacles,skier,score)
                pygame.time.delay(1000)
                skier.forward()
                speed = [0,6]
                hitted_obstacles[0].passed = True
            elif hitted_obstacles[0].attribute == "flag" and not hitted_obstacles[0].passed:
                score += 10
                obstacles.remove(hitted_obstacles[0])

        # update screen
        updateScreen(screen, obstacles, skier, score)
        timer.tick(config.FPS)

if __name__=="__main__":
    main()





