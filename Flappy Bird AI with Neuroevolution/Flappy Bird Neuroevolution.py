import pygame
import numpy as np
import random
import math
random.seed(1)
pygame.init()
win = pygame.display.set_mode((900,500))
clock = pygame.time.Clock()
run = True
font = pygame.font.Font('freesansbold.ttf',32)
Gen = 0
i=0
birds = [pygame.image.load('bird1.png'),pygame.image.load('bird2.png')]
background = pygame.image.load('background.png')
pipes = [pygame.image.load('pipe1.png'),pygame.image.load('pipe2.png')]
pop=50
score = 0


#THE ACTIVATION FUNCTION
def tanh(x):
    if math.tan(math.pi/(180/x))<=0:
        return 0
    return 1
    



#inputs wil be = [y,,500-y,distancetouppipe,distancetodownpipe]

#####BIRDS CLASSS#####
class Birds:
    def __init__(self,y,fitness,dead,weights,weights2):
        self.y=y
        self.fitness=fitness
        self.dead=dead
        self.weights = weights
        self.weights2 = weights2
        
    def drawbird(self,a,b):
        #AI PART#
        i1 = math.sqrt((pipe[0].y-self.y)**2+(pipe[0].x-60)**2)
        i2 = math.sqrt((pipe[0].y-100-self.y)**2+(pipe[0].x-60)**2)
        train_X = np.array([[birds_array[0].y,500-birds_array[0].y]])
        out = tanh(np.dot(train_X,self.weights))
        train_X2 = np.array([[i1,i2]])
        out2 = tanh(np.dot(train_X2,self.weights2))

        if (out==1)|(out2==1):
            finalout = 1
        else:
            finalout = 0
        #MOVEMENTS#                           
        if finalout == 1:
            self.y-=15
        if self.dead == 0:
            if (self.y >= 450)|(self.y<=2):
                self.dead = 1
                print("Dead! ",self.fitness)
            else:
                self.b = win.blit(birds[a],(60,self.y))
                self.y+=5
                self.fitness+=1
            




        
#####PIPES CLASS#####
class Pipes:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def drawpipe(self):
        img1 = win.blit(pipes[0],(self.x,self.y))
        img2 = win.blit(pipes[1],(self.x,-360+self.y))
        self.x-=6
        for h in birds_array:
            if (h.dead==0)&((img1.colliderect(h.b))|(img2.colliderect(h.b))):
                h.dead = 1
                print("Dead! ",h.fitness)



#FIRST GENERATIONS OF BIRDS AND PIPES#
birds_array = [Birds(280,0,0,(2*np.random.random((2,1))-1),
                             (2*np.random.random((2,1))-1)) for z in range(pop)]
pipe = [Pipes(700+m,random.randint(240,360)) for m in range(0,5000,500)]
fittest_weights=[0 for i in range(5)]
fittest_weights2=[0 for i in range(5)]
fitnesses = [0 for i in range(pop)]






#CREATING A NEW GENERATION OF BIRDS#
def newgeneration(fw,fw2):
    global pipe
    pipe = [Pipes(700+m,random.randint(240,360)) for m in range(0,5000,500)]
    nba = []
    for i in range(5):
        nba.append(Birds(280,0,0,fw[i],fw2[i]))

    for t in range(pop-5):
        nw = np.random.random((2,1))
        nw2 = np.random.random((2,1))
        for w in range(2):
            nw[w][0]  = fw[random.randint(0,2)][0]  + ((random.random())-0.5)
            nw2[w][0] = fw2[random.randint(0,2)][0] + ((random.random())-0.5)
        nba.append(Birds(280,0,0,nw,nw2))
    return nba



 







#MAIN LOOP#
while run:
    #GENERAL SAME STUFF#
    win.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False




    a = False
    #Displaying the bird ** will change ofc
    for k in range(len(birds_array)):
        birds_array[k].drawbird(i,0)
        if birds_array[k].dead==0:
            a = True
            fitnesses[k] = birds_array[k].fitness
            
        
    i+=1
    i = i%2








    #Displaying the pipes ** will change ofc
    for p in pipe:
        p.drawpipe()
    if pipe[0].x<=0:
        del pipe[0]
        pipe.append(Pipes(5200,random.randint(240,360)))
        score += 1


    #CALLING THE NEWGENERATION FUNCTION
    if a == False:
        var = 0
        for _ in range(5):
            for g in range(pop):
                if var==5:
                    break
                if birds_array[g].fitness==max(fitnesses):
                    fittest_weights[var]=birds_array[g].weights
                    fittest_weights2[var]=birds_array[g].weights2
                    fitnesses[g]=0
                    var+=1
        if var<5:
            for h in range(var,5):
                max1=fitnesses.index(max(fitnesses))
                fitnesses[max1]=0
                fittest_weights[h] = (birds_array[max1].weights)
                fittest_weights2[h] = (birds_array[max1].weights2)
                
        birds_array = newgeneration(fittest_weights,fittest_weights2)
        Gen+=1
        score = 0






    #ENDINGS#
    text = font.render(("Gen : " + str(Gen)),True,(255,0,0))
    win.blit(text,(10,10))
    scoretext = font.render(("Score : " + str(score)),True,(255,0,0))
    win.blit(scoretext,(700,10))
    clock.tick(20)
    pygame.display.update()

pygame.quit()
