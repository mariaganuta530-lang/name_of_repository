import turtle

house = turtle.Turtle()
house.speed(5)
house.pensize(3)
house.fillcolor("black")

house.begin_fill()
for _ in range(4):
    house.forward(100)
    house.left(90)
house.end_fill()
house.penup()
house.goto(0, 100) 
house.pendown()

house.begin_fill()
house.goto(50, 150)  
house.goto(100, 100)
house.goto(0, 100)   
house.end_fill()

house.penup()
house.goto(35, 0)    
house.pendown()
house.fillcolor("brown")
house.begin_fill()
house.goto(35, 50)   
house.goto(65, 50)   
house.goto(65, 0)  
house.goto(35, 0)    
house.end_fill()

house.penup()
house.goto(20, 60)   
house.pendown()
house.fillcolor("lightblue")
house.begin_fill()
for _ in range(4):
    house.forward(25)
    house.left(90)
house.end_fill()
house.hideturtle()