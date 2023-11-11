
import pygame
import math
import numexpr as ne

from sympy import symbols, I,cos,sin,tan,cosh,sinh
# Define the complex variable z
z = symbols('z')
exp = input("f(z) = ")
expOg = exp.replace(str(exp),"("+str(exp)+")")
iter = int(input("Iterations :"))
for i in range(1,iter):
    exp = exp.replace("z",str(expOg))



exp += " + 0*z" # z must always be present
f_z = eval(exp)
x = f_z.as_real_imag()[0]
y = f_z.as_real_imag()[1]

ReTemp = str(format(x))
ImTemp = str(format(y))

# Change the values used in string
ReTemp = ReTemp.replace("re(z)","x")
ReTemp = ReTemp.replace("im(z)","y")
ImTemp = ImTemp.replace("re(z)","x")
ImTemp = ImTemp.replace("im(z)","y")

ReTemp += " + 0*x*y"
ImTemp += " + 0*y*x"

Re = ne.NumExpr(ReTemp)
Im = ne.NumExpr(ImTemp)
def checkInput():
    global running
    global screenRange
    global drawn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL and drawn:
                if event.y == 1:
                   screenRange /= 2
                elif event.y == -1:
                   screenRange *= 2

                screen.blit(textDrawing, (500,0))
                drawn = False

def drawFunction(w,h,pull):
        for i in range(0,w):
            x = screenRange*(i-qW/2)/(qW/2)
            screen.blit(screen,(0,0))
            if pull:
              pygame.display.flip()
            if not running:
                break
            for j in range(0,h):
                checkInput()
                y = screenRange*(qH/2-j)/(qH/2)
                try :
                 Real = Re(x,y)
                except:
                 Real = 50
                try :
                 Imaginary = Im(x,y)
                except:
                 Imaginary = 501
                Imaginary = Im(x,y)
                module = (Real**2 + Imaginary**2)**0.5
                module *= 1
                opacity = module/(1+module)
                if Real != 0:
                  if Real < 0:
                    argument = math.pi+math.atan((Imaginary/Real))
                  elif Real > 0:
                    if Imaginary < 0:
                       argument = 2*math.pi + math.atan((Imaginary/Real))
                    else:
                       argument = math.atan((Imaginary/Real))
                else:
                   argument = math.pi/2

                color = pygame.Color(0,0,0)
                color.hsva = (360*abs(argument)/(2*math.pi),100-90*opacity,90*opacity + 10)

                pygame.draw.rect(screen,color,(i*quality,j*quality,quality,quality))

screenRange = 2
quality = int(input("factor of quality = "))
# pygame setup
pygame.init()
pygame.display.set_caption('Complex Grapher')
screen = pygame.display.set_mode((800, 600))
qW = int(800/quality) + 1
qH = int(600/quality) + 1
fx = 0
fy = 0
running = True
drawn = False
clearedText = False
showCoor = False
font = pygame.font.Font('freesansbold.ttf', 18)
text = font.render('', True, "White")
textDrawing = font.render("Drawing",True,"White")
while running:
    checkInput()
    #SHOW COOR
    if not drawn:
        pygame.display.set_caption('Complex Grapher - Drawing')
        drawFunction(qW,qH,True)
        drawn = True
    else:
        pygame.display.set_caption('Complex Grapher')
    if pygame.mouse.get_pressed()[0]:
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        x = float("{:.2f}".format(screenRange*(mouseX-qW*quality/2)/(qW*quality/2)))
        y = float("{:.2f}".format(screenRange*(qH*quality/2-mouseY)/(qH*quality/2)))
        fx = "{:.2f}".format(float(Re(x,y)))
        fy = "{:.2f}".format(float(Im(x,y)))
        pygame.draw.rect(screen,"gray",(0,0,9*len('f('+str(x)+"+"+ str(y)+'i) = '+str(fx)+"+"+str(fy)+"i"),20))
        text = font.render('f('+str(x)+"+"+ str(y)+'i) = '+str(fx)+"+"+str(fy)+"i", True,"White")
        clearedText = False
        screen.blit(text, (0,0))
    elif not clearedText:
        drawFunction(9*len('f('+str(x)+"+"+ str(y)+'i) = '+str(fx)+"+"+str(fy)+"i") + 20,20,False)
        clearedText = True
    pygame.display.flip()
pygame.quit()