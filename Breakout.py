import turtle
import random

# ------SCREEN SETUP--------
width = 770
screen = turtle.Screen()
screen.setup(width=width, height=600)
screen.bgcolor("black")
screen.title("BreakOut Game")
screen.tracer(0)
screen.mode("logo")


# ------PADDLE SETUP--------
class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("yellow")
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=4)
        self.move_right = False
        self.move_left = False

    def right_start(self):  # funzione che modifica lo stato dell'attributo move_right
        self.move_right = True

    def left_start(self):
        self.move_left = True

    def right_end(self):
        self.move_right = False

    def left_end(self):
        self.move_left = False

    def go_right(self):  # definisce il movimento del paddle
        x = self.xcor()
        if x < 340:  # se il paddle non è oltre la fine della finestra allora può andare a destra altrimenti noin fa nulla
            x += 7
            self.goto(x=x, y=-280)

    def go_left(self):
        x = self.xcor()
        if x > -345:
            x -= 7
            self.goto(x=x, y=-280)


paddle = Paddle()
paddle.setposition(0, -280)
paddle.setheading(90)

# ---------COMMANDS-----------

screen.listen()  # l'app riceverà i comandi da tastiera

screen.onkeypress(paddle.left_start, "Left")  # se tengo premuto Left si attiva paddle.left_start che rende True self.move_left = False di Paddle
screen.onkeypress(paddle.right_start, "Right")
screen.onkeyrelease(paddle.right_end, "Right")
screen.onkeyrelease(paddle.left_end, "Left")

# ------BRICKS SETUP--------

COLORS = ["red", "green", "blue"]


class Brick(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=1)

    def new_brick(self, loc):
        self.color(random.choice(COLORS))
        self.setposition(loc)

# Bricks positioning
interval = width / 2  # width è la larghezza della finestra
locations = []
xpos = int(0 - interval) + 20  # faccio partire il posizionamento dei brick da - interval ovvero da sinistra +20
ypos = 200  # riga di partenza

for _ in range(5):
    for _ in range(30):  # creo 30 bricks per riga
        loc = [xpos, ypos]
        locations.append(loc)
        xpos += 25  # a 25 di distanza ciascuno
    ypos -= 25  # e poi vado alla riga sopra e ripeto
    xpos = int(0 - interval) + 20  # resetto xpos partendo di nuovo da tutta sinistra

bricks = []
for x in locations:  # creo un brick per ogni loc creata sopra
    brick = Brick()
    brick.new_brick(x)
    bricks.append(brick)

# ------BALL SETUP--------
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.shapesize(stretch_wid=1, stretch_len=1)
ball.setheading(150)



def head_rel_to_hor(current_heading):
    new_head = current_heading + (90 - current_heading) * 2  # se per esempio la palla sale a 30°, per simulare un rimbalzo realistico la formula fa sì che : 30+(90-30)*2 = 150
    if new_head < 0:
        new_head += 360  # se il risultato viene negativo nel caso la palla viaggia per esempio in direzione 330
    return new_head

def head_rel_to_ver(current_heading):
    new_head = current_heading + (180 - current_heading)*2
    return new_head


# ------GAME--------
speed = 4
while True:
    if speed > 9:  # speed cap
        speed = 9

    if ball.ycor() < -279:  # se la palla tocca il fondo finisce il game
        break

    if ball.ycor() >= 290:  # se la palla tocca la parete superiore rimbalza verso sud
        heading = ball.heading()
        ball.setheading(head_rel_to_hor(heading))
        ball.forward(speed)
    elif ball.xcor() >= 370 or ball.xcor() <= -375:  # se la palla tocca le pareti laterali
        heading = ball.heading()
        ball.setheading(head_rel_to_ver(heading))
        ball.forward(speed)

    if paddle.distance(ball) < 45 and ball.ycor() < -265:  # se la palla tocca il paddle
        heading = ball.heading()
        random_heading = random.randint(315, 405)  # do una casualità al rimbalzo
        if random_heading >= 360:
            random_heading -= 360
        ball.setheading(random_heading)
        ball.forward(speed*2)

    for b in bricks:  # faccio il loop di tutti i bricks position per verificare un eventuale collisione con la palla
        if ball.distance(b) < 25:
            if ball.ycor() > (b.ycor()+10) or ball.ycor() < (b.ycor()-10):  # se la palla tocca il brick da sotto o da sopra
                heading = ball.heading()
                ball.setheading(head_rel_to_hor(heading))
                b.hideturtle()  # elimino il brick
                bricks.remove(b)
                speed *= 1.015
                ball.forward(speed)
            else:
                if ball.xcor() > (b.xcor()+10) or ball.xcor() < (b.xcor()-10):  # se la pappa tocca il brick da destra o da sinistra
                    heading = ball.heading()
                    ball.setheading(head_rel_to_ver(heading))
                    b.hideturtle()
                    bricks.remove(b)
                    speed *= 1.015
                    ball.forward(speed)

    if paddle.move_right:  # movimenti del paddle
        paddle.go_right()
    elif paddle.move_left:  # finchè è True la funzione sotto verrà eseguita
        paddle.go_left()
    ball.forward(speed)
    screen.update()

screen.exitonclick()
