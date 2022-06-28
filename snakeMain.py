# GUI Project #1 - Snake Game
# David Daniliuc & 05/05/2021
# Simple snake game. Hitting yourself or the border will end the game. 
# Collect snacks to increase your score and the length of your snake.
# All postions go from 0, 0 to 19, 19 then get multipled to pygame coordinates.
import pygame, time, random

# Initialise pygame and the display
pygame.init()
width, height, rows = 600, 600, 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font('pixelFont.ttf', 24)
FPS = 10

# Colors
lightBlack = (30, 30, 30)
darkBlack = (20, 20, 20)
gridColor = (210, 210, 210)
bodyColor = (120, 120, 255)

#custom eyes data
xEyes = [[(0, 0), (6, 6)], [(6, 0), (0, 6)]]
triEyes = [(0, 4), (3, 1), (6, 4)]

# class to independently set and control position and direction of each part of the snake.
class Cube():
    def __init__(self, startPos, dirnX=1, dirnY=0, color=(255,0,0)):
        self.pos = startPos
        self.dirnX = dirnX
        self.dirnY = dirnY
        self.color = color

    def move(self, velX, velY): #single function to set direction to new values then alter self.pos to itself + new direction.
        self.dirnX = velX
        self.dirnY = velY
        self.pos = [self.pos[0] + self.dirnX, self.pos[1] + self.dirnY]

#player: snake object starting with a head(cube object), body list starting with head, score(increased by snack eaten), overall velocity, is dead(variable for drawing head face),
# is dead(variable for drawing head face), is left(variable for drawing head face), turnPoints store the position and current velocity when the head turns direction. 
# This works by checking if a body piece is at the position then moving(cube.move) it by the turnPoints velocity not their own velocity. Then after the entire body travels 
# throught the point it is delete from the dictonary, keeping it dynamic and preventing bugs.
class Snake(object):
    def __init__(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.score = 0
        self.velX = 1
        self.velY = 0
        self.dead = False
        self.isLeft = False
        self.turnPoints = {}

    def move(self):
        keys = pygame.key.get_pressed()

        for key in keys: # loop throught the values of keys checking for the arrow keys and space bar.
            if keys[pygame.K_LEFT]:
                if not self.velX == 1 or len(self.body) < 3:#preventing the snake from going back into itself.
                    self.isLeft = True
                    self.velX = -1
                    self.velY = 0
                    self.turnPoints[tuple(self.head.pos)] = [self.velX, self.velY]#save head position as key and value to velocity after left key pressed

            elif keys[pygame.K_RIGHT]:
                if not self.velX == -1 or len(self.body) < 3:#preventing the snake from going back into itself.
                    self.isLeft = False
                    self.velX = 1
                    self.velY = 0
                    self.turnPoints[tuple(self.head.pos)] = [self.velX, self.velY]#save head position as key and value to velocity after right key pressed

            elif keys[pygame.K_UP]:
                if not self.velY == 1 or len(self.body) < 3:#preventing the snake from going back into itself.
                    self.velX = 0
                    self.velY = -1
                    self.turnPoints[tuple(self.head.pos)] = [self.velX, self.velY]#save head position as key and value to velocity after up key pressed

            elif keys[pygame.K_DOWN]:
                if not self.velY == -1 or len(self.body) < 3:#preventing the snake from going back into itself.
                    self.velX = 0
                    self.velY = 1
                    self.turnPoints[tuple(self.head.pos)] = [self.velX, self.velY]#save head position as key and value to velocity after down key pressed

            #dev tool to increase length quickly. Does not change score
            elif keys[pygame.K_SPACE] or keys[pygame.K_SPACE]:
                self.increaseLength()
                break

        for i, cube in enumerate(self.body):
            #save cube.pos to a varible for checking
            cubePos = tuple(cube.pos)
            # print(cube.pos, cube.dirnX, cube.dirnY, 'pos dirn'+str(i)) #DEBUG
            # print(self.turnPoints, 'before') #DEBUG

            # check direction and if position on that axis is outside the border
            if cube.dirnX == -1 and cube.pos[0] <= 0:
                gameEnd('You hit the border!')#function that resets the game and prints the text given
                break#break to prevent multiple resets and other bugs
            elif cube.dirnX == 1 and cube.pos[0] >= rows-1:
                gameEnd('You hit the border!')
                break
            elif cube.dirnY == 1 and cube.pos[1] >= rows-1:
                gameEnd('You hit the border!')
                break
            elif cube.dirnY == -1 and cube.pos[1] <= 0:
                gameEnd('You hit the border!')
                break

            elif cubePos in self.turnPoints:#check if cubePos is inside one of the turnPoints
                turnDirection = self.turnPoints[cubePos]#assign direction of turn point to a variable.
                # print(turnDirection, 'turn') #DEBUG
                cube.move(turnDirection[0], turnDirection[1])#move(cube.move) by turn point direction instead of cube's own velocity.
                # print(len(self.body), 'len') #DEBUG
                if i == len(self.body) - 1:#if this is the last time the function loops throught, the current 
                    self.turnPoints.pop(cubePos)
                    # print(self.turnPoints, 'after') #DEBUG
            else:# if cube isn't outside the grid and isn't turning direction
                cube.move(cube.dirnX, cube.dirnY) #move(cube.move) by the cube's own velocity.

    def increaseLength(self):#function to increase length of body by adding a cube to the end of the list
        tail = self.body[-1]#get last cube in body list

        #check direction of tail then add cube. 
        if tail.dirnX == 1 and tail.dirnY == 0: #moving right
            self.body.append(Cube([tail.pos[0] - 1, tail.pos[1]], dirnX=tail.dirnX, dirnY=tail.dirnY))
        elif tail.dirnX == -1 and tail.dirnY == 0: #moving left
            self.body.append(Cube([tail.pos[0] + 1, tail.pos[1]], dirnX=tail.dirnX, dirnY=tail.dirnY))
        elif tail.dirnX == 0 and tail.dirnY == 1: #moving down
            self.body.append(Cube([tail.pos[0], tail.pos[1] - 1], dirnX=tail.dirnX, dirnY=tail.dirnY))
        elif tail.dirnX == 0 and tail.dirnY == -1: #moving up
            self.body.append(Cube([tail.pos[0], tail.pos[1] + 1], dirnX=tail.dirnX, dirnY=tail.dirnY))

    def draw(self):
        #dimension of the grid squares
        gridSize = width // rows
        print(gridSize)

        #loop through the list and draw backwards to create overlap of head when gameEnd() is called 
        for i, cube in enumerate(self.body[::-1]):
            if cube == self.head: #if the cube is the head of the snake, draw rect border then body.
                pygame.draw.rect(screen, gridColor, (cube.pos[0]*gridSize, cube.pos[1]*gridSize, gridSize+1, gridSize+1))
                pygame.draw.rect(screen, bodyColor, (cube.pos[0]*gridSize+1, cube.pos[1]*gridSize+1, gridSize-1, gridSize-1))
                if self.dead: #if the snake is dead, superimpose and offset xEyes data over eye position. 
                    for i in range(2): #loop twice to draw both eyes.
                        for line in xEyes:
                            pygame.draw.line(screen, lightBlack, (line[0][0] + cube.pos[0]*gridSize + int(gridSize/3*(i+1)) - (line[1][1]/2), (line[0][1] + cube.pos[1]*gridSize + int(gridSize/3)) - (line[1][1]/2)), (line[1][0] + cube.pos[0]*gridSize + int(gridSize/3*(i+1)) - (line[1][1]/2), (line[1][1] + cube.pos[1]*gridSize + int(gridSize/3)) - (line[1][1]/2)), 2)
                elif self.velY == -1: #if the snake is going upward, draw triangle with point facing up over eye position.
                    for i in range(2): #loop twice to draw both eyes.
                        #isolate position into a variable to simplicity
                        eyePos = [(point[0] + cube.pos[0]*gridSize + int(gridSize/3*(i+1)) - (triEyes[2][0]/2), point[1] + cube.pos[1]*gridSize + int(gridSize/3) - (triEyes[2][1]/2)) for point in triEyes]
                        pygame.draw.polygon(screen, lightBlack, eyePos)
                elif self.velY == 1: #if the snake is going downward, draw triangle with point facing down over eye position.
                    for i in range(2):
                        #same position except invert y position by subtracting y by 4 then absolutizing the value to prevent negative values.
                        eyePos = [(point[0] + cube.pos[0]*gridSize + int(gridSize/3*(i+1)) - (triEyes[2][0]/2), abs(point[1]-4) + cube.pos[1]*gridSize + int(gridSize/3) - (triEyes[2][1]/2)) for point in triEyes]
                        pygame.draw.polygon(screen, lightBlack, eyePos)
                else:
                    #draws mouth and eye and uses isLeft as a int to offset the eye and mouth position depending on it's value. For example if isLeft = True, then the 
                    # eyes will be offset by 2 as int(isLeft) = 1 then 1*2 = 2. And the mouth gets offset by a third of gridSize if True. 
                    # Draw the mouth goes outside the else statement as it is independent from the eyes
                    pygame.draw.circle(screen, lightBlack, (cube.pos[0]*gridSize + int(gridSize/3) - 2 + 1 - int(self.isLeft)*2, cube.pos[1]*gridSize + int(gridSize/3) + 1), 2)
                    pygame.draw.circle(screen, lightBlack, (cube.pos[0]*gridSize + int(gridSize/3*2) + 2 + 1 - int(self.isLeft)*2, cube.pos[1]*gridSize + int(gridSize/3) + 1), 2)
                pygame.draw.circle(screen, lightBlack, (cube.pos[0]*gridSize + int(gridSize/3*2) + 1 - int(self.isLeft)*(int(gridSize/3)), cube.pos[1]*gridSize + int(gridSize/3*2) + 1), 5)

            else: #else means that the cube isn't the head thus only draw a rect. 
                pygame.draw.rect(screen, bodyColor, (cube.pos[0]*gridSize+1, cube.pos[1]*gridSize+1, gridSize-1, gridSize-1))

        #DEBUG
        # for point in self.turnPoints: #show turn points on grid 
        #     pygame.draw.rect(screen, (210, 210, 210, 130), (point[0]*gridSize+1, point[1]*gridSize+1, gridSize-1, gridSize-1))

#object for snack, position, and random color.
class Snack(object):
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.color = color

    def draw(self):#simple draw function
        gridSize = width // rows

        pygame.draw.rect(screen, self.color, (self.pos[0]*gridSize+1, self.pos[1]*gridSize+1, gridSize-1, gridSize-1))

def createSnack():
    # create a random position for the snack
    # if the position overlap with the snake then the loop repeats until it creates a number that doesn't(return ends the loop and function).
    while True:
        snackPos = [random.randint(1, rows-2), random.randint(1, rows-2)]

        for cube in snake.body:
            if not cube.pos == snackPos:#check overlap
                return Snack(snackPos[0], snackPos[1], tuple(int(random.randint(70, 255)) for i in range(3))) #return Snack object with randomize position and random RBG color

#initialize player and snack
snake = Snake([2, 2])
snack = createSnack()

def reset(newPos):
    global snack, FPS #to let reset() know to change the global variables
    # snake reset
    snake.head = Cube(newPos)
    snake.body = [snake.head]
    snake.score = 0
    snake.velX = 1
    snake.velY = 0
    snake.dead = False
    snake.isLeft = False
    snake.turnPoints = {}
    # snack reset
    snack = createSnack()
    # reset fps
    FPS = 10

def gameEnd(message):
    print(message)
    print('Score:', snake.score)
    snake.dead = True #change to True to draw X eyes.
    redrawWindow()
    reset((10,10)) #change snake.dead back to False
    pygame.time.delay(1000)

def drawGrid(): #create a grid starting at 1, 1
    gridSize = width // rows

    for i in range(1, rows, 1):
        pygame.draw.line(screen, gridColor, (i*gridSize, gridSize), (i*gridSize, width-gridSize))
        pygame.draw.line(screen, gridColor, (gridSize, i*gridSize), (width-gridSize, i*gridSize))

#redraw function
def redrawWindow():
    screen.fill(darkBlack)

    # draw grid/background
    pygame.draw.rect(screen, lightBlack, (30, 30, width-60, height-60))
    drawGrid()

    # draw snake and snack
    snake.draw()
    snack.draw()

    # create text font and draw score
    scoreText = font.render('Score: '+str(snake.score), False, (255, 255, 255))
    screen.blit(scoreText, (0, 0))

    # draw the four possible face to test them, values are absolute
    # pygame.draw.rect(screen, bodyColor, (0*30+1, 0*30+1, 30-1, 30-1))
    # pygame.draw.circle(screen, lightBlack, (0*30 + int(30/3*2) + 1, 0*30 + int(30/3*2) + 1), 5)
    # pygame.draw.circle(screen, lightBlack, (0*30 + int(30/3) - 2 + 1, 0*30 + int(30/3) + 1), 2)
    # pygame.draw.circle(screen, lightBlack, (0*30 + int(30/3*2) + 2 + 1, 0*30 + int(30/3) + 1), 2)

    # pygame.draw.rect(screen, bodyColor, (1*30+1, 0*30+1, 30-1, 30-1))
    # pygame.draw.circle(screen, lightBlack, (1*30 + int(30/3) + 1, 0*30 + int(30/3*2) + 1), 5)
    # pygame.draw.circle(screen, lightBlack, (1*30 + int(30/3) - 2 + 1 - int(1)*2, 0*30 + int(30/3) + 1), 2)
    # pygame.draw.circle(screen, lightBlack, (1*30 + int(30/3*2) + 2 + 1 - int(1)*2, 0*30 + int(30/3) + 1), 2)

    # pygame.draw.rect(screen, bodyColor, (2*30+1, 0*30+1, 30-1, 30-1))
    # pygame.draw.circle(screen, lightBlack, (2*30 + int(30/2) + 1, 0*30 + int(30/3*2) + 1), 5)
    # for i in range(2):
    #     for line in xEyes:
    #         pygame.draw.line(screen, lightBlack, (line[0][0] + 2*30 + int(30/3*(i+1)) - (line[1][1]/2), (line[0][1] + 0*30 + int(30/3)) - (line[1][1]/2)), (line[1][0] + 2*30 + int(30/3*(i+1)) - (line[1][1]/2), (line[1][1] + 0*30 + int(30/3)) - (line[1][1]/2)), 2)

    # pygame.draw.rect(screen, bodyColor, (3*30+1, 0*30+1, 30-1, 30-1))
    # pygame.draw.circle(screen, lightBlack, (3*30 + int(30/2) + 1, 0*30 + int(30/3*2) + 1), 5)
    # for i in range(2):
    #     eyePos = [(point[0] + 3*30 + int(30/3*(i+1)) - (triEyes[2][0]/2), point[1] + 0*30 + int(30/3) - (triEyes[2][1]/2)) for point in triEyes] #upward
    #     eyePos = [(point[0] + 3*30 + int(30/3*(i+1)) - (triEyes[2][0]/2), abs(point[1]-4) + 0*30 + int(30/3) - (triEyes[2][1]/2)) for point in triEyes] #downward
    #     pygame.draw.polygon(screen, lightBlack, eyePos)

    pygame.display.flip()

running = True
while running:
    # the more apples eaten, the higher the frame rate the game runs at thus increasing the snake's speed.
    clock.tick(FPS)
    FPS = 10 + snake.score//2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    snake.move()
    if snake.head.pos == snack.pos: #check if player head is in snack grid position then create new snack and add cube to body
        print('Yum!')
        snake.score += 1
        snake.increaseLength()
        snack = createSnack()

    for x in range(len(snake.body)):#check snake self collision
        if snake.head.pos in [cube.pos for cube in snake.body[1:]]:
            gameEnd('You hit yourself!')
            break

    #Draw the scene
    redrawWindow()
pygame.quit()