# Source File Name: Bacterium_07.py
# Author's Name: Jacob Meikle
# Last Modified By: Jacob Meikle
# Date Last Modified: July 31, 2013
""" 
  Program Description:  This is a side-scroller game where the player controls a single bacteria in the blood
      stream and must infect as many red blood cells as possible while avoiding white blood cells.
    
  Version: 0.7 -  *Clicking the closing X now closes the whole game.
                  *Added "final boss" Heart. 
                  *Fixed some bugs
      
  Version: 0.6 -  *Added white cell behaviors based on level
                  *Added random bonus t cell events with sound   
      
  Version: 0.5 -  *Added level progression with game ending.
                  *White blood cells now die on collision.                 
      
  Version: 0.4 -  *Added sound.
                  *Added a game-end screen.
                  
  Version: 0.3 -  *Added White blood cells.
                  *Implemented pixel-perfect collisions for white blood cells.              
                  *You can now lose the game.  
      
      
  Version: 0.2 -  *Changed movement style of bacteria.
                  *Added a cursor.               
                  *Added Red Blood cells.                      

  Version: 0.1 -  *Start screen.
                  *Bacteria object that follows the mouse.               
                  *Scrolling background implemented.
"""
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 600))

""" The Cursor class creates a small red dot wich provides a visual cusor for the player. """
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/cursor.gif")
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255)) 

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex,mousey)
      
""" The Bacteria class creates an avatar for the player. """
class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bacterium.gif")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.image.set_colorkey((255, 255, 255)) 
        self.rect.center = (200, 320)
        self.rect.inflate(-50,-50)
        
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndInfect = pygame.mixer.Sound("assets/infect.wav")
            self.sndDie = pygame.mixer.Sound("assets/die.wav")
            self.sndBonus = pygame.mixer.Sound("assets/bonus.wav")
            self.sndMusic = pygame.mixer.Sound("assets/music.wav")
            self.sndMusic.play(-1)

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        
        #buffer of 10 px to stop up or down movement
        if mousey > self.rect.centery + 5 or mousey < self.rect.centery - 5:
            if mousey > self.rect.centery:
                #moving down
                self.rect.centery += 2
                pygame.transform.rotate(self.image,10)
            else:
                #moving up
                self.rect.centery += -2
                pygame.transform.rotate(self.image,20)
     
""" The RedCell class creates red blood cells which must be infected. """              
class RedCell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/blood_cell.gif")
        self.rect = self.image.get_rect()
        self.reset()
        self.infected = False
        self.dy = -2
    
    def update(self):
        self.rect.centerx += self.dy
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.rect.centery = random.randrange(0, screen.get_height())
        self.rect.centerx = random.randrange(screen.get_width(), screen.get_width()*3)
        self.infected = False
        self.image = pygame.image.load("assets/blood_cell.gif")
        
    def infect(self):
        self.image = pygame.image.load("assets/infected_blood_cell.gif")
        self.infected = True
        
""" random score bonus t cells"""
class TCell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/T_Cell.gif")
        self.image.set_colorkey((255, 255, 255)) 
        self.rect = self.image.get_rect()
        self.reset()
        self.dy = -2
    
    def update(self):
        self.rect.centerx += self.dy
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.rect.centery = random.randrange(0, screen.get_height())
        self.rect.centerx = random.randrange(screen.get_width(), screen.get_width()*5)

                
        
""" The final heart. """              
class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/heart.gif")
        self.image.set_colorkey((255, 255, 255)) 
        self.rect = self.image.get_rect()
        self.dy = -2
        self.rect.centerx = screen.get_width() * 5
        self.rect.centery = 300
    
    def update(self):
        self.rect.centerx += self.dy
        if self.rect.right < 0:
            self.reset()
            
        
""" The WhiteCell class creates a white blood cells that kill the player. """
class WhiteCell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/white_blood_cell.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()
        self.dy = 1
        self.dx = -1
        self.dead = False
        self.level = 1

    def update(self):
        
        self.rect.centerx += self.dx
        #white cell begins to move up and down.
        if self.level > 2:
            self.rect.centery += self.dy
        #off screen horizontal
        if self.rect.right < 0:
            self.reset()
            
        #off vertical
        if self.rect.top < 0:
            self.dy = 1
        elif self.rect.bottom > screen.get_height():
            self.dy = -1
    def reset(self):
        self.rect.left = random.randrange(screen.get_width(), screen.get_width()*3) 
        self.rect.centery = random.randrange(0, screen.get_height())
        self.image = pygame.image.load("assets/white_blood_cell.gif")
        self.image = self.image.convert()
        self.dead = False


    def die(self):
        self.image = pygame.image.load("assets/dead_white_blood_cell.gif")
        self.image = self.image.convert()
        self.dead = True

""" The BloodStream class creates the scrolling background. """    
class BloodStream(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bg.jpg")
        self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.dx = 1
        self.reset()
        
    def update(self):
        self.rect.left -= self.dx
        if self.rect.left <= -3200:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0

""" The Scoreboard class creates the score labels in the top left. """
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
        
    def update(self):
        self.text = "lives: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        
""" This class manages the progression of levels """        
class levelChanger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.level = 0
        self.font = pygame.font.SysFont("None", 50)
        self.text = "Level: %d" % (self.level)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width()-75 
        self.tick = 0
        self.oneSecond = 68
        self.rect.centery = 20
        self.levelFinished = False
       
        
    def update(self):
        self.rect.centerx = screen.get_width()-75
        self.rect.centery = 20
        self.text = "Level: %d" % (self.level)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.tick += 1
        
        #no conditions here for level 1
        if self.tick > self.oneSecond * 30 and self.tick < self.oneSecond * 34 :

            #Display level complete label
            self.text = "Level: %d Complete!" % (self.level)
            self.image = self.font.render(self.text, 1, (255, 255, 255))
            self.rect.centerx = screen.get_width() / 2 - 75
            self.rect.centery = screen.get_height() / 2 - 50
        elif self.tick > self.oneSecond * 34 :
            self.levelFinished = True
          
        
        

""" The game function is called when entering the main playing state."""    
def game(level, score, lives):
    pygame.display.set_caption("~~Bacterium~~")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    bacteria = Bacteria()
    donePlaying = False
  
    cursor = Cursor()
    
    if level == 1:
        #spawning enemies
        redCells = [ RedCell() for i in range(8)]
        whiteCells = [ WhiteCell() for i in range(12)]

    elif level == 2:
        #spawning enemies
        redCells = [ RedCell() for i in range(11)]
        whiteCells = [ WhiteCell() for i in range(10)]
    elif level == 3:
        #spawning enemies
        redCells = [ RedCell() for i in range(16)]
        whiteCells = [ WhiteCell() for i in range(14)]
    else:
        #spawning enemies
        redCells = [ RedCell() for i in range(25)]
        whiteCells = [ WhiteCell() for i in range(0)]
    
    if level > 1:  
        #upgrade white cell ai    
        for thiscell in whiteCells:
            thiscell.level = level
            thiscell.dx = random.randrange(2,4) * -1
       

    Tcell = TCell()
    
    bloodStream = BloodStream()
    
    scoreboard = Scoreboard()
    scoreboard.score = score
    scoreboard.lives = lives
    
    levelShow = levelChanger()
    levelShow.level = level
    levelShow.levelFinished = False

    if level == 4:
        heart = Heart()
        friendSprites = pygame.sprite.OrderedUpdates(bloodStream,heart,Tcell, redCells, bacteria, cursor)
        enemySprites = pygame.sprite.Group()
        scoreSprite = pygame.sprite.Group(scoreboard)
        levelSprite = pygame.sprite.Group()       
    else:
        friendSprites = pygame.sprite.OrderedUpdates(bloodStream, redCells,Tcell,  bacteria, cursor)
        enemySprites = pygame.sprite.Group(whiteCells)
        scoreSprite = pygame.sprite.Group(scoreboard)
        levelSprite = pygame.sprite.Group(levelShow)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(68)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
                
        #check is the level is over
        if levelShow.levelFinished:
            keepGoing = False
        
        #check collisions
        
        if level == 4:
            #check for heart collision
            if bacteria.rect.colliderect(heart.rect):
                keepGoing = False
         
        #bacteria
        for cell in redCells:
        
            if bacteria.rect.colliderect(cell.rect):
                if cell.infected == False:
                    bacteria.sndInfect.play()
                    scoreboard.score += 100
                    cell.infect()
            
        # T cell Bonus
        if bacteria.rect.colliderect(Tcell.rect):
            bacteria.sndBonus.play();
            scoreboard.score += 1000
            Tcell.reset()

        #white blood cell collision
        #check if sprites collide
        if pygame.sprite.spritecollide(bacteria, enemySprites, False):
            #if major sprite collide intiate pixel perfect collision detection       
            hitWhites = pygame.sprite.spritecollide(bacteria, enemySprites, False, pygame.sprite.collide_mask)
            if hitWhites:       
                if scoreboard.lives <= 0:
                    keepGoing = False
                for theCell in hitWhites:
                    #check if the enemy cell is alive
                    if theCell.dead == False:
                        bacteria.sndDie.play()
                        scoreboard.lives -= 1
                        theCell.die()
        
        friendSprites.update()
        enemySprites.update()
        scoreSprite.update()
        levelSprite.update()
        
        friendSprites.draw(screen)
        enemySprites.draw(screen)
        scoreSprite.draw(screen)
        levelSprite.draw(screen)
        
        
        pygame.display.flip()

    bacteria.sndMusic.stop()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return donePlaying, scoreboard.score, scoreboard.lives

""" The gameReport function is called when leaving the playing state and shows your score."""    
def gameReport(score, alive):
    pygame.display.set_caption("~~Bacterium~~")

    bacteria = Bacteria()
    bloodStream = BloodStream()
    
    allSprites = pygame.sprite.Group(bloodStream, bacteria)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    
    if alive:
        instructions = (
        "Your Score Is: %d" % score ,
        "Good Job!",
        "Click to replay, or Esc to exit."
    
        )
    else:
        instructions = (
        "Your Score Is: %d" % score ,
        "Better luck next time.",
        "Click to replay, or Esc to exit."
    
        )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(66)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    #end music
    bacteria.sndMusic.stop()

    pygame.mouse.set_visible(True)
    return donePlaying

""" The instructions function is called at the very beginning ."""    
#Instructions Screen    
def instructions():
    pygame.display.set_caption("~~Bacterium~~")

    bacteria = Bacteria()
    bloodStream = BloodStream()
    
    allSprites = pygame.sprite.Group(bloodStream, bacteria)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Bacterium.",
    "",
    "Instructions:  You are a single bacterium,",
    "infecting the blood stream.",
    "",
    "Touch red blood cells to infect them.",
    "Beware of the white blood cells,",  
    "",  
    "Tiny Green T-Cells are worth bonus points.",
    "",
    "Steer with the mouse.",
    "",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(66)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    #stop music
    bacteria.sndMusic.stop()

    pygame.mouse.set_visible(True)
    return donePlaying

""" The main method that intiates the game states."""            
def main():
    donePlaying = False
    while not donePlaying:
        Finalscore = 0
        Lives = 10
        alive = False
        donePlaying = instructions()
        if not donePlaying:
            donePlaying, Finalscore, Lives = game(1, Finalscore, Lives)
            if Lives > 0 and not donePlaying:
                donePlaying, Finalscore, Lives = game(2, Finalscore, Lives)
                if Lives > 0 and not donePlaying:
                    donePlaying, Finalscore, Lives = game(3, Finalscore, Lives)
                    if Lives > 0 and  not donePlaying:
                        donePlaying, Finalscore, Lives = game(4, Finalscore, Lives)
        if not donePlaying:
            if Lives > 0:
                alive = True
            donePlaying = gameReport(Finalscore, alive)


if __name__ == "__main__":
    main()
    
    
