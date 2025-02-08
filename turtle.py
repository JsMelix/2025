import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Turtle Graphics Example")
screen.bgcolor("white")

# Create a turtle named "t"
t = turtle.Turtle()
t.shape("turtle")
t.color("blue")
t.speed(2)

# Draw a square
for _ in range(4):
    t.forward(100)  # Move forward by 100 units
    t.left(90)      # Turn left by 90 degrees

# Hide the turtle and display the window
t.hideturtle()
turtle.done()