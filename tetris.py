#encoding:utf-8
import pygame, sys
import random
import os

pygame.init()

GRID_WIDTH = 20
GRID_NUM_WIDTH = 15
GRID_NUM_HEIGHT = 25
WIDTH, HEIGHT = GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT
SIDE_WIDTH = 200
SCREEN_WIDTH = WIDTH + SIDE_WIDTH
WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
CUBE_COLORS = [
    (0xcc, 0x99, 0x99), (0xff, 0xff, 0x99), (0x66, 0x66, 0x99),
    (0x99, 0x00, 0x66), (0xff, 0xcc, 0x00), (0xcc, 0x00, 0x33),
    (0xff, 0x00, 0x33), (0x00, 0x66, 0x99), (0xff, 0xff, 0x33),
    (0x99, 0x00, 0x33), (0xcc, 0xff, 0x66), (0xff, 0x99, 0x00)
]

# 颜色矩阵，底板矩阵
screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
# 分数和等级
score = 0
level = 1


# 设置游戏的根目录为当前文件夹
base_folder = os.path.dirname(__file__)
# 设置屏幕宽高
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
# 设置程序名字
pygame.display.set_caption("俄罗斯方块")


#设置速度
clock = pygame.time.Clock()
FPS = 3
running = True
gameover = True
counter = 0
live_cube = None
new_cube = None
pause = False
# 暂停时的计数，用于展示闪动的屏幕
pause_count = 0
heightScore = None
colorBool = True
dead = False
class Wall():
    global GRID_NUM_WIDTH
    global LINE_COLOR
    global HEIGHT
    global HEIGHT

    def __init__(self):
        pass

    def draw_grids(self):
        for i in range(GRID_NUM_WIDTH):
            pygame.draw.line(screen, LINE_COLOR,
                             (i * GRID_WIDTH, 0), (i * GRID_WIDTH, HEIGHT))

        for i in range(GRID_NUM_HEIGHT):
            pygame.draw.line(screen, LINE_COLOR,
                             (0, i * GRID_WIDTH), (WIDTH, i * GRID_WIDTH))

        pygame.draw.line(screen, WHITE,
                         (GRID_WIDTH * GRID_NUM_WIDTH, 0),
                         (GRID_WIDTH * GRID_NUM_WIDTH, GRID_WIDTH * GRID_NUM_HEIGHT))

    def draw_matrix(self):
        for i, row in zip(range(GRID_NUM_HEIGHT), screen_color_matrix):
            for j, color in zip(range(GRID_NUM_WIDTH), row):
                if color is not None:
                    pygame.draw.rect(screen, color,
                                     (j * GRID_WIDTH, i * GRID_WIDTH,
                                      GRID_WIDTH, GRID_WIDTH))
                    pygame.draw.rect(screen, WHITE,
                                     (j * GRID_WIDTH, i * GRID_WIDTH,
                                      GRID_WIDTH, GRID_WIDTH), 2)

    def remove_full_line(self):
        global screen_color_matrix
        global score
        global level
        new_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        index = GRID_NUM_HEIGHT - 1
        n_full_line = 0
        for i in range(GRID_NUM_HEIGHT - 1, -1, -1):
            is_full = True
            for j in range(GRID_NUM_WIDTH):
                if screen_color_matrix[i][j] is None:
                    is_full = False
                    continue
            if not is_full:
                new_matrix[index] = screen_color_matrix[i]
                index -= 1
            else:
                n_full_line += 1

        if n_full_line != 0:
            score += n_full_line*(n_full_line-1)+1  # 1 3 7 13

        level = score // 20 + 1
        screen_color_matrix = new_matrix

    def show_welcome(self):
        self.show_text( u'俄罗斯方块', 30, WIDTH / 2, HEIGHT / 2)
        self.show_text( u'按任意键开始游戏', 20, WIDTH / 2, HEIGHT / 2 + 50)
        self.show_text( u'按A进入/退出AI模式', 18, WIDTH / 2, HEIGHT / 2 + 90)

    def show_text(self, text, size, x, y, color=(0xff, 0xff, 0xff),bgColor = None):

        fontObj = pygame.font.Font('font/font.ttc', size)
        textSurfaceObj = fontObj.render(text, True, color,bgColor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (x, y)
        screen.blit(textSurfaceObj, textRectObj)


    def draw_score(self):
        global heightScore
        self.show_text( u'得分 : {}'.format(score), 18, WIDTH + SIDE_WIDTH // 2, 180)

        if heightScore is None:
            self.getHeightScore()

        if score>heightScore:
            heightScore = score

        self.show_text( u'level : {}  最高分 : {}'.format(level,heightScore), 15, WIDTH + SIDE_WIDTH // 2, 205)

    def showPause(self):
        GREEN = ( 0, 255, 0)
        BLUE = ( 0, 0, 128)
        self.show_text(u'暂停中...', 50, 250, 200, BLUE , GREEN)
        pygame.display.update()
    def drawAll(self):
        # 更新屏幕

        screen.fill(BLACK)
        self.draw_grids()
        self.draw_matrix()
        self.draw_score()
        self.drawNextBrick()


        self.show_text( u'AI模式：A',13, WIDTH+100,HEIGHT-100 , WHITE )
        self.show_text( u'再来一次：R',13, WIDTH+100,HEIGHT-80 , WHITE )
        self.show_text( u'我要暂停：P',13, WIDTH+100,HEIGHT-60 , WHITE )
        self.show_text( u'基本操作：↑↓← →',13, WIDTH+100,HEIGHT-40 , WHITE )
        self.show_text( u'Author：Charming(2018.4)',13, SCREEN_WIDTH-100,HEIGHT-10 , WHITE )

        if pause :
            self.showAD(u'突然暂停', u'害怕了吗')
        else:
            self.showAD()




        if live_cube is not None:
            live_cube.draw()

        if gameover:
            self.show_welcome()

    def drawNextBrick(self):
        global new_cube
        if new_cube is not None:
            new_cube.drawNext()

    def getHeightScore(self):
        global heightScore
        f = open('score.txt', 'r')
        heightScore = int( f.read() )
    def writeHeightScore(self):
        global heightScore
        f = open('score.txt', 'w')
        f.write( str(heightScore) )
        f.close()
    def showAD(self,text1 = None , text2 = None):
        global CUBE_COLORS
        global colorBool

        line1 = ['哇塞萌新', '运气好而已', '回去吧', '是不是快挂了', '年轻人不简单', '哇塞！！', '围观大佬']
        line2 = ['你会玩吗', '狗屎运而已', '后面太难了', '哈哈哈', '看走眼了', '这样都行？', '大佬请喝茶']
        if level > len(line1):
            num = len(line1)
        else:
            num = level
        if text1 is None and text2 is None:
            if gameover:
                text1 = u'广告位招租'
                text2 = u'非诚勿扰'
            else:
                text1 = line1[num - 1].decode('utf-8')
                text2 = line2[num - 1].decode('utf-8')

        GREEN = (0, 255, 0)
        pygame.draw.rect(screen, BLACK,
                         (WIDTH + 20, 240,
                          160, 80))
        pygame.draw.rect(screen, GREEN,
                         (WIDTH + 20, 240,
                          160, 80), 1)

        if colorBool :
            color = CUBE_COLORS[num]
        else :
            color =  CUBE_COLORS[random.randint(0, len(CUBE_COLORS) - 1)]

        self.show_text( text1,18, WIDTH+100,265 , color )
        self.show_text( text2,18, WIDTH+100,295 , color )




class Brick():
    SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    SHAPES_WITH_DIR = {
        'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
    }

    def __init__(self):
        self.shape = self.SHAPES[random.randint(0, len(self.SHAPES) - 1)]
        # 骨牌所在的行列
        self.center = (2, GRID_NUM_WIDTH // 2)
        self.dir = random.randint(0, len(self.SHAPES_WITH_DIR[self.shape]) - 1)
        self.color = CUBE_COLORS[random.randint(0, len(CUBE_COLORS) - 1)]

    def get_all_gridpos(self, center=None):
        curr_shape = self.SHAPES_WITH_DIR[self.shape][self.dir]
        if center is None:
            center = [self.center[0], self.center[1]]

        return [(cube[0] + center[0], cube[1] + center[1])
                for cube in curr_shape]

    def conflict(self, center):
        for cube in self.get_all_gridpos(center):
            # 超出屏幕之外，说明不合法
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= GRID_NUM_HEIGHT or  cube[1] >= GRID_NUM_WIDTH:
                return True

            # 不为None，说明之前已经有小方块存在了，也不合法
            if screen_color_matrix[cube[0]][cube[1]] is not None:
                return True

        return False

    def rotate(self):
        new_dir = self.dir + 1
        new_dir %= len(self.SHAPES_WITH_DIR[self.shape])
        old_dir = self.dir
        self.dir = new_dir
        if self.conflict(self.center):
            self.dir = old_dir
            return False

    def down(self):
        # import pdb; pdb.set_trace()
        center = (self.center[0] + 1, self.center[1])
        if self.conflict(center):
            return False

        self.center = center
        return True

    def left(self):
        center = (self.center[0], self.center[1] - 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def right(self):
        center = (self.center[0], self.center[1] + 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def draw(self):
        for cube in self.get_all_gridpos():
            pygame.draw.rect(screen, self.color,
                             (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
                              GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(screen, WHITE,
                             (cube[1] * GRID_WIDTH, cube[0] * GRID_WIDTH,
                              GRID_WIDTH, GRID_WIDTH),
                             1)
    def drawNext(self):
        for cube in self.get_all_gridpos((0,0)):
            pygame.draw.rect(screen, self.color,
                             (cube[1] * GRID_WIDTH+WIDTH+100, cube[0] * GRID_WIDTH+70,
                              GRID_WIDTH, GRID_WIDTH))
            pygame.draw.rect(screen, WHITE,
                             (cube[1] * GRID_WIDTH+WIDTH+100, cube[0] * GRID_WIDTH+70,
                              GRID_WIDTH, GRID_WIDTH),1)

# 显示框弹动速度
x, y = 10., 10.
speed_x, speed_y = 133., 170.
# ai对象
rw = None
# 是否ai模式
ai = False
# 玩家操作
class HouseWorker():
    # 开始游戏
    def start(self):
        global gameover
        global live_cube
        global new_cube
        global score
        global screen_color_matrix
        gameover = False
        live_cube = Brick()
        new_cube = Brick()
        score = 0
        screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        pass
    # 暂停操作
    def pause(self):
        global pause
        if pause:
            pause = False
        else :
            pause = True
    # 当暂停时
    def whenPause(self):
        # 暂停动画
        global pause_count
        global score
        global live_cube
        global level
        global screen_color_matrix
        global colorBool
        global dead
        pause_count += 1
        if pause_count % FPS > 10 and pause_count % FPS < 20:
            w.drawAll()
        else:
            w.showPause()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    hw.pause()
                elif event.key == pygame.K_ESCAPE:
                    hw.pause()
                    w.writeHeightScore()
                    # 退出pygame
                    pygame.quit()
                    # 退出系统
                    sys.exit()
                #   重新开始
                elif event.key == pygame.K_r:
                    w.writeHeightScore()
                    hw.pause()
                    score = 0
                    live_cube = Brick()
                    level = 1
                    dead = False
                    screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
                elif event.key == pygame.K_c:
                    if colorBool :
                        colorBool = False
                    else:
                        colorBool = True
                else:
                    pass

    # 当正常时
    def whenNormal(self):
        global score
        global live_cube
        global level
        global screen_color_matrix
        global gameover
        global running
        global counter
        global new_cube
        global colorBool
        global dead
        global ai
        global FPS
        # 正常运行时
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and pause == False:
                if gameover:
                    hw.start()
                    break
                if event.key == pygame.K_LEFT:
                    live_cube.left()
                elif event.key == pygame.K_RIGHT:
                    live_cube.right()
                elif event.key == pygame.K_DOWN:
                    live_cube.down()
                elif event.key == pygame.K_UP:
                    live_cube.rotate()
                elif event.key == pygame.K_SPACE:
                    while live_cube.down() == True:
                        pass
                elif event.key == pygame.K_ESCAPE:
                    w.writeHeightScore()
                    # 退出pygame
                    pygame.quit()
                    # 退出系统
                    sys.exit()
                #   重新开始
                elif event.key == pygame.K_r:
                    w.writeHeightScore()
                    score = 0
                    live_cube = Brick()
                    new_cube = Brick()
                    colorBool = True
                    dead = False
                    level = 1
                    screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
                elif event.key == pygame.K_c:
                    if colorBool :
                        colorBool = False
                    else:
                        colorBool = True
                elif event.key == pygame.K_p:
                    hw.pause()
                elif event.key == pygame.K_a:
                    if ai:
                        ai = False
                    else:
                        ai = True




        if live_cube and ai == True:
            rw = RobotWorker([2, 7], live_cube.shape, live_cube.dir, live_cube.color , screen_color_matrix)
            bestPoint =  rw.mainProcess()
            live_cube.dir = bestPoint['station']
            live_cube.center = bestPoint['center']
            w.drawAll()
            pygame.display.update()


        if ai is not True :
            flag = counter % (FPS // level) == 0
            FPS = 30
        else :
            flag = True
            FPS = 3000

        # 判断是否结束函数和执行down动作
        if gameover is False and flag :
            if live_cube.down() == False:
                for cube in live_cube.get_all_gridpos():
                    screen_color_matrix[cube[0]][cube[1]] = live_cube.color
                live_cube = new_cube
                new_cube = Brick()
                # 这里游戏结束
                if live_cube.conflict(live_cube.center):
                    w.writeHeightScore()
                    dead = True
                    gameover = True
                    colorBool = False

            # 消除满行
            w.remove_full_line()

        # 计时作用
        counter += 1

        if not dead:
            w.drawAll()
            pygame.display.update()

    # 当gameover时
    def whenGameOver(self):
        global score
        global live_cube
        global new_cube
        global level
        global screen_color_matrix
        global colorBool
        global dead
        global speed_x
        global speed_y
        global SCREEN_WIDTH
        global x
        global y

        # gameover时提示框的弹动功能
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 128)
        w.drawAll()
        w.showAD(u'挂了挂了', u'哈哈哈')
        w.show_text(u'Game Over', 50, x, y, BLUE, GREEN)
        w.show_text(u'按任意键重新开始', 25, x, y+38, BLUE, GREEN)

        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0

        x += speed_x * time_passed_seconds
        y += speed_y * time_passed_seconds

        # 到达边界则把速度反向
        if x > SCREEN_WIDTH - 150:
            speed_x = -speed_x
            x = SCREEN_WIDTH - 150
        elif x < 150:
            speed_x = -speed_x
            x = 150.

        if y > HEIGHT-38 - 25:
            speed_y = -speed_y
            y = HEIGHT-38 - 25
        elif y < 25:
            speed_y = -speed_y
            y = 25.


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if gameover and dead:
                    dead = False
                    colorBool = True
                    hw.start()
                    break
                if event.key == pygame.K_ESCAPE:
                    # 退出pygame
                    pygame.quit()
                    # 退出系统
                    sys.exit()
                #   重新开始
                elif event.key == pygame.K_r:
                    w.writeHeightScore()
                    score = 0
                    live_cube = Brick()
                    new_cube = Brick()
                    level = 1

                    colorBool = True
                    dead = False
                    screen_color_matrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
                elif event.key == pygame.K_c:
                    if colorBool:
                        colorBool = False
                    else:
                        colorBool = True
                else:
                    pass

# AI操作
# 基于Pierre Dellacherie算法
class RobotWorker():
    SHAPES = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]

    SHAPES_WITH_DIR = {
        'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
    }
    def __init__(self,center,shape,station,color,matrix):
        self.center = center
        self.shape = shape
        self.station = station
        self.color = color
        self.matrix = matrix

    def get_all_gridpos(self, center,shape,dir):
        curr_shape = self.SHAPES_WITH_DIR[shape][dir]

        return [(cube[0] + center[0], cube[1] + center[1])
                for cube in curr_shape]

    def conflict(self, center,matrix,shape,dir):
        for cube in self.get_all_gridpos(center,shape,dir):
            # 超出屏幕之外，说明不合法
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= GRID_NUM_HEIGHT or  cube[1] >= GRID_NUM_WIDTH:
                return True

            screen_color_matrix = self.copyTheMatrix( matrix )
            # 不为None，说明之前已经有小方块存在了，也不合法
            if screen_color_matrix[cube[0]][cube[1]] is not None:
                return True

        return False

    def copyTheMatrix(self,screen_color_matrix):
        newMatrix = [[None] * GRID_NUM_WIDTH for i in range(GRID_NUM_HEIGHT)]
        for i in range( len( screen_color_matrix ) ):
            for j in range( len( screen_color_matrix[i] ) ):
                newMatrix[i][j] = screen_color_matrix[i][j]

        return newMatrix

    def getAllPossiblePos(self,thisShape = 'Z'):
        theMatrix = self.matrix
        theStationNum = len(self.SHAPES_WITH_DIR[thisShape])
        theResult = []
        for k in range(theStationNum):
            for j in range(len(theMatrix[1])):
                for i in range(len(theMatrix) - 1):
                    if self.conflict([i + 1, j], theMatrix, thisShape, k) == True and self.conflict([i, j], theMatrix,
                                                                                                thisShape, k) == False:
                        if {"center": [i, j], "station": k} not in theResult:
                            theResult.append({"center": [i, j], "station": k})

        return theResult
    def getLandingHeight(self,center):
        return GRID_NUM_HEIGHT-1-center[0]

    def getErodedPieceCellsMetric(self,center,station):
        theNewMatrix = self.getNewMatrix(center,station)
        lines = 0
        usefulBlocks = 0
        theAllPos = self.get_all_gridpos(center,self.shape,station)
        for i in range(len(theNewMatrix)-1,0,-1):
            count = 0
            for j in range(len(theNewMatrix[1])):
                if theNewMatrix[i][j] is not None:
                    count += 1
            # 满一行
            if count == 15:
                lines +=1
                for k in range(len(theNewMatrix[1])):
                    if [i,k] in theAllPos:
                        usefulBlocks +=1
            # 整行未填充，则跳出循环
            if count == 0:
                break
        return lines*usefulBlocks
    def getNewMatrix(self,center,station):
        theNewMatrix = self.copyTheMatrix(self.matrix)
        theAllPos = self.get_all_gridpos(center,self.shape,station)
        for cube in theAllPos:
            theNewMatrix[cube[0]][cube[1]] = self.color
        return theNewMatrix


    def getBoardRowTransitions(self,theNewmatrix):
        transition = 0
        for i in range( len(theNewmatrix)-1 , 0 , -1 ):
            count = 0
            for j in range( len(theNewmatrix[1])-1 ):
                if theNewmatrix[i][j] is not None :
                    count += 1
                if theNewmatrix[i][j] == None and theNewmatrix[i][j+1] != None:
                    transition += 1
                if theNewmatrix[i][j] != None and theNewmatrix[i][j+1] == None:
                    transition += 1
        return transition

    def getBoardColTransitions(self,theNewmatrix):
        transition = 0
        for j in range( len(theNewmatrix[1]) ):
            for i in range( len(theNewmatrix)-1,1,-1 ):
                if theNewmatrix[i][j] == None and theNewmatrix[i-1][j] != None:
                    transition += 1
                if theNewmatrix[i][j] != None and theNewmatrix[i-1][j] == None:
                    transition += 1
        return transition

    def getBoardBuriedHoles(self,theNewmatrix):
        holes = 0
        for j in range(len( theNewmatrix[1] )):
            colHoles = None
            for i in range( len( theNewmatrix ) ):
                if colHoles == None and theNewmatrix[i][j] != None:
                    colHoles = 0

                if colHoles != None and theNewmatrix[i][j] == None:
                    colHoles += 1
            if colHoles is not None:
                holes += colHoles
        return holes

    def getBoardWells(self,theNewmatrix):
        sum_n = [0,1,3,6,10,15,21,28,36,45,55]
        wells = 0
        sum = 0

        for j in range( len(theNewmatrix[1]) ):
            for i in range( len(theNewmatrix) ):
                if theNewmatrix[i][j] == None:
                    if (j-1<0 or theNewmatrix[i][j-1] != None) and (j+1 >= 15 or theNewmatrix[i][j+1] != None):
                        wells += 1
                    else:
                        sum += sum_n[wells]
                        wells = 0
        return sum
    def mainProcess(self):
        pos = self.getAllPossiblePos(self.shape)
        bestScore = -999999
        bestPoint = None
        for point in pos:
            theScore = self.evaluateFunction( point)
            if theScore > bestScore:
                bestScore = theScore
                bestPoint = point
            elif theScore == bestScore:
                if self.getPrioritySelection( point ) < self.getPrioritySelection(bestPoint):
                    bestScore = theScore
                    bestPoint = point

        return bestPoint

    def getPrioritySelection(self,point):
        tarStation = point['station']
        nowStation = self.station
        #
        colNum = abs(7 - point['center'][1] )
        if tarStation >= nowStation:
            changeTimes = tarStation - nowStation
        else :
            changeTimes = len(self.SHAPES_WITH_DIR[self.shape]) - nowStation + tarStation

        result = colNum*100 + changeTimes
        if point['center'][1] <=7 :
            result += 10
        return result


    def evaluateFunction(self,point):
        newMatrix = self.getNewMatrix( point['center'],point['station'] )
        lh = self.getLandingHeight( point['center'] )
        epcm = self.getErodedPieceCellsMetric(point['center'],point['station'])
        brt = self.getBoardRowTransitions(newMatrix)
        bct = self.getBoardColTransitions(newMatrix)
        bbh = self.getBoardBuriedHoles(newMatrix)
        bw = self.getBoardWells(newMatrix)

        # 两个计算分数的式子，前者更优，后者是PD算法的原始设计
        score = -45*lh + 34*epcm - 32*brt - 98*bct - 79* bbh -34*bw
        # score = -1*lh + epcm - brt - bct - 4*bbh - bw
        return score




w =  Wall()
hw = HouseWorker()

while running:
    clock.tick(FPS)
    # 暂停时的事件循环
    if pause == True:
        hw.whenPause()
        continue
    if dead:
        hw.whenGameOver()
        continue
    # 正常时的事件循环
    hw.whenNormal()

























