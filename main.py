import nyan
import random
import math

block_size = 25
last_key_pressed = "RIGHT"
leader_board = []
snake_parts = []
counter = 0
growth = 1
score_text = nyan.new_text(text=str(counter), x=360, y=260, z=1)
nyan.set_backdrop("lightblue")
game_state = "Menu"
print(game_state)
food = nyan.new_rect(width=10, height=10, x=0, y=0, color="yellow")
game_over = nyan.new_text(text = "G A M E  O V E R", x=0, y=0, color="red", is_hidden=True)
highscore_text = nyan.new_text(text = "" ,is_hidden = True)
Leader = nyan.new_image(image = "Leader.png", x = 100, y = -200)
Snake = nyan.new_image(image = "Snake.png", x = 10, y = 75, size = 1000 , z = 1)
Play = nyan.new_image(image = "Play.png", x = -100, y = -200)
Back = nyan.new_image(image = "Back.png", x = 0, y = -200)
title = nyan.new_text(text = "Snake", color = "dark blue", x = 0, y = -100, font_size = 200)
animation_timer = nyan.new_timer()

@nyan.repeat_forever
async def menu():
    global game_state
    if game_state != "Menu": return
    Back.hide()
    if nyan.mouse.is_touching(Leader):
        Leader.size += (600 - Leader.size)/3
    else:
        Leader.size = 500
    if nyan.mouse.is_touching(Leader) and nyan.mouse.is_clicked:
        Leader.transparency = 80
    else:
        Leader.transparency = 100

    if nyan.mouse.is_touching(Play):
        Play.size += (600 - Play.size)/3
    else:
        Play.size = 500

    if nyan.mouse.is_touching(Play) and nyan.mouse.is_clicked:
        Play.transparency = 80
        game_state = "Alive"
        print(game_state)
        Play.hide()
        Snake.hide()
        Leader.hide()
        title.hide()
    else:
        Play.transparency = 100

@Leader.when_clicked
async def leaderboard():
    global game_state
    game_state = "Leaderboard"
    print(game_state)
    Play.hide()
    Snake.hide()
    Leader.hide()
    title.hide()
    score_text.hide()
    food.hide()
    head.hide()
    Back.show()
    fh = open("leaderboard.txt", "r")
    scores = []
    for line in fh:
        scores.append(int(line))
    scores.sort(reverse=True)
    highscore_text.show()
    highscore_text.text = scores[0]
    
@nyan.repeat_forever
async def backbutton():
    global game_state
    if nyan.mouse.is_touching(Back):
        Back.size += (600 - Back.size)/3
    else:
        Back.size = 500

    if nyan.mouse.is_touching(Back) and nyan.mouse.is_clicked:
        Back.transparency = 80
        game_state = "Menu"
        print(game_state)
        Back.show()
        Snake.show()
        Leader.show()
        title.show()
        Play.show()
    else:
        Back.transparency = 100
    highscore_text.text.hide()
for i in range(growth):
    part = nyan.new_rect(width=block_size, height=block_size, x=(block_size * i), y=0, color="gainsboro", border_width=2, border_color="grey")
    snake_parts.append(part)


head = snake_parts[0]
head.direction = 'right'

def food_spawn():
    food_x = random.randrange(-350,350,block_size)
    food_y = random.randrange(-250,250,block_size)
    food.go_to(food_x, food_y)

@nyan.repeat_forever
async def death():
    global game_state
    if game_state != "Alive": return
    tail = snake_parts[1:]
    for p in tail:
        if head.is_touching(p):
            game_over.show()
            game_state = "Dead"
            print(game_state)
            await nyan.sleep(3)
            game_over.hide()
            leaderboard = open("leaderboard.txt", "a")
            leaderboard.write(str(counter) + "\n")
            leaderboard.close()
            game_state == "Menu"
            print(game_state)


@nyan.repeat_forever
async def eat():
    if game_state != "Alive": return
    global counter
    global growth
    if head.is_touching(food):
        counter = counter + 1
        score_text.text=str(counter)
        growth = growth + 1
        food_spawn()
        snake_parts.append(nyan.new_rect(width=block_size, height=block_size, x=1000, y=1000, color="gainsboro", border_width=2, border_color="grey"))
        
@nyan.repeat_forever
async def move():
    if game_state != "Alive": return

    if last_key_pressed == 'up':
        if head.direction != 'down':
            head.direction="up"
    elif last_key_pressed == "down":
        if head.direction != "up":
            head.direction="down"
    elif last_key_pressed == "right":
        if head.direction != "left":
            head.direction="right"
    elif last_key_pressed == "left":
        if head.direction != "right":
            head.direction="left"

    for i in range(len(snake_parts) - 2, -1, -1):
        snake_parts[i+1].go_to(snake_parts[i])
    
    if head.direction == 'up':
        head.y += block_size
    elif head.direction == 'down':
        head.y -= block_size
    elif head.direction == "right":
        head.x += block_size
    elif head.direction ==  "left":
        head.x -= block_size

    await nyan.sleep(.1)


@nyan.when_key_pressed('up', 'down', 'right', 'left')
async def store_last_key(key):
    global last_key_pressed
    last_key_pressed = key



@nyan.repeat_forever
async def wrap_around():
    if game_state != "Alive": return
    global head
    if head.x < nyan.screen.left:
        head.x = nyan.screen.right
    elif head.x > nyan.screen.right:
        head.x = nyan.screen.left
    if head.y < nyan.screen.bottom: 
        head.y = nyan.screen.top
    elif head.y > nyan.screen.top:
        head.y = nyan.screen.bottom

nyan.start_program() 