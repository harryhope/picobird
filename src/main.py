from machine import Pin,PWM
import time
import random
import display
import sprites
from battery import Battery

BL = 13

MODE_MENU = "menu"
MODE_PLAYING = "playing"
MODE_END = "end"

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 134

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 22

BUTTON_A = Pin(15,Pin.IN,Pin.PULL_UP)
BUTTON_B = Pin(17,Pin.IN,Pin.PULL_UP)

mode = MODE_MENU

def clear_screen(lcd):
    lcd.fill(lcd.white)

def draw_sprite(sprite, lcd, offset_x = 0, offset_y = 0):
    for y, row in enumerate(sprite):
        if (row != "x"):
            for pair in row:
                lcd.fill_rect(pair[0] + offset_x, y + offset_y,
                              pair[1] - pair[0], 1, lcd.black)

def draw_battery(battery, lcd):
    level = round(battery.percentage() / 10)
    lcd.fill_rect(205, 11, 10, 6,lcd.white)
    lcd.fill_rect(205, 11, level, 6,lcd.black)
    
def get_high_score():
    try:
        f = open("score.txt")
        score = f.read()
        f.close()
        return score
    except:
        return "0"

def set_high_score(score):
    f = open("score.txt", "w")
    f.write(str(score))
    f.close()
    
class Bird():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 2.0
        
    def draw(self, lcd):
        bird_sprite = sprites.bird_up
        if (BUTTON_A.value() == 0):
            bird_sprite = sprites.bird_down       
        draw_sprite(bird_sprite, lcd, 2, self.y)
        
    def flap(self):
        self.velocity = -4.0
        
    def apply_gravity(self):
        if (self.velocity < 6.0):
            self.velocity = self.velocity + 0.6
        self.y = self.y + int(self.velocity)
        self.x = self.x + 4
        if (self.y < 0):
            self.y = 0

class Wall():
    def __init__(self, x, score):
        self.x = x
        self.gap = random.randint(10, SCREEN_HEIGHT - 10)
        self.size = max(PLAYER_HEIGHT + 8, 80 - score)
    
    def draw(self, player_x, lcd):
        screen_x = self.x - player_x
        half = int(self.size / 2)
        lcd.fill_rect(screen_x, 0, 4, self.gap - half,lcd.black)
        lcd.fill_rect(screen_x, self.gap + half, 4,
                      SCREEN_HEIGHT - half,lcd.black)
    
    def is_colliding_with(self, player):
        half = int(self.size / 2)
        x_overlap = player.x + PLAYER_WIDTH >= self.x and player.x + PLAYER_WIDTH <= self.x + 4
        player_above_gap = player.y < self.gap - half
        player_below_gap = player.y + PLAYER_HEIGHT > self.gap + half
        return x_overlap and (player_above_gap or player_below_gap)
        
class State():
    def __init__(self):
        self.player = Bird(5, 25)
        self.obstacle = Wall(SCREEN_WIDTH,0)
        self.mode = MODE_MENU
        self.score = 0
        self.did_draw_menu = False
        self.did_draw_game_over = False
        self.battery = Battery(addr=0x43)
       
    def main_menu(self, lcd):
        draw_battery(self.battery, lcd)
        if (not self.did_draw_menu):
            clear_screen(lcd)
            draw_sprite(sprites.main_menu, lcd, 6 , 0)
            self.did_draw_menu = True
            lcd.text(get_high_score(),21,16,lcd.black)
        
        if(BUTTON_A.value() == 0):
            self.restart()

    def play(self, lcd):
        clear_screen(lcd)
        
        self.player.apply_gravity()
        
        if (BUTTON_A.value() == 0):
            self.player.flap()
        
        if (self.obstacle.x + 4 < self.player.x):
            self.score = self.score + 1
            self.obstacle = Wall(self.player.x + SCREEN_WIDTH, self.score)
            
        self.obstacle.draw(self.player.x, lcd)
        
        self.player.draw(lcd)
        lcd.text("Score: " + str(self.score),4,4,lcd.black)
        
        if (self.player.y + PLAYER_HEIGHT > SCREEN_HEIGHT or self.obstacle.is_colliding_with(self.player)):
            self.mode = MODE_END
    
    def game_over(self, lcd):
        if (not self.did_draw_game_over):
            clear_screen(lcd)
            draw_sprite(sprites.game_over, lcd, 6 , 0)
            self.did_draw_game_over = True
            high_score = get_high_score()
            lcd.text(str(self.score),150,38,lcd.black)
            lcd.text(high_score,150,72,lcd.black)
            if (int(high_score) < self.score):
                set_high_score(self.score)
                lcd.text("NEW HIGH SCORE!",62,84,lcd.black)
                
        if (BUTTON_B.value() == 0):
            self.mode = MODE_MENU
            
    def restart(self):
        self.did_draw_game_over = False
        self.did_draw_menu = False
        self.player = Bird(5, 25)
        self.obstacle = Wall(SCREEN_WIDTH,0)
        self.mode = MODE_PLAYING
        self.score = 0
        
    def tick(self, lcd):
        if (self.mode == MODE_MENU):
            self.main_menu(lcd)
        elif (self.mode == MODE_PLAYING):
            self.play(lcd)
        else: # mode == MODE_END
            self.game_over(lcd)    

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768) # max 65535

    lcd = display.LCD()
    clear_screen(lcd)
    lcd.show()
    
    state = State()
    
    while(1):     
        state.tick(lcd)         
        lcd.show()
        
    time.sleep(1)
    clear_screen()

