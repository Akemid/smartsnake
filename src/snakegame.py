import pygame
import random
from pygame.surface import Surface
from constants import Colors

class Display:
    """
    Class that manage the display of the game
    """
    def __init__(self, dis_width:int, dis_height:int , caption_message:str):
        self.dis_width = dis_width
        self.dis_height = dis_height    
        self.set_display_message(caption_message)
        self.set_surface()
    
    def set_display_message(self,message:str):        
        pygame.display.set_caption(message)
    
    def set_surface(self):
        self.surface : Surface = pygame.display.set_mode(
            (self.dis_width, self.dis_height))
        
    def set_additional_surface(
        self, surface:Surface, position: list[float,float]):
        self.surface.blit(
            surface, position
        )
    
    def fill_background(self,color:list[int,int,int]):
        self.surface.fill(color)
    
    def update(self):
        pygame.display.update()
    
class GameStyle:
    """
    Class that represents all the style of
    our game
    """
    FONT_STYLE_DEFAULT = "bahnschrift"
    SCORE_FONT_DEFAULT = "comicsansms"
    FONT_STYLE_SIZE_DEFAULT = 25
    SCORE_FONT_SIZE_DEFAULT = 35
    
    def __init__(
        self,
        font_style:str=None,
        score_font:str=None,        
        font_size:int=None,
        score_size:int=None,) -> None:
        self.set_colors()
        self.set_fonts(
            font_style=font_style,
            score_font=score_font,
            font_size=font_size,
            score_size=score_size,
        )
    
    def set_colors(self):
        self.white = Colors.white.value
        self.yellow = Colors.yellow.value
        self.black = Colors.black.value
        self.red = Colors.red.value
        self.green = Colors.green.value
        self.blue = Colors.blue.value
    
    def set_fonts(
        self,
        font_style:str=None,
        score_font:str=None,
        font_size:int=None,
        score_size:int=None,
        ):
        self.font_style = pygame.font.SysFont(
            font_style if font_style else self.FONT_STYLE_DEFAULT,
            font_size if font_size else self.FONT_STYLE_SIZE_DEFAULT
            )
        self.score_font = pygame.font.SysFont(
            score_font if score_font else self.SCORE_FONT_DEFAULT,
            score_size if score_size else self.SCORE_FONT_SIZE_DEFAULT
            )

class Snake:
    """
    The snake that will move eating food
    """
    def __init__(
        self,
        snake_block:int,
        snake_speed:int,
        snake_color:tuple,
        surface: Surface,
        initial_position: list[int,int]
        ):
        self.initial_position = initial_position
        self.snake_block = snake_block
        self.snake_speed = snake_speed
        self.snake_color = snake_color
        self.position_list = [initial_position]
        self.head_position = initial_position.copy()
        self.surface = surface
        self.length = 1
        self.own_collision = False
    
    def reset_snake(self):
        self.position_list = [self.initial_position]
        self.head_position = self.initial_position.copy()
        self.own_collision = False
        self.length = 1
        print(f"position_list: {self.position_list}, head_position: {self.head_position}")
    
    def create_snake_block(self,position:tuple[float,float]):
        pygame.draw.rect(
            self.surface,
            self.snake_color,
            [
                position[0], position[1],
                self.snake_block,self.snake_block
            ]
        )
    
    def create_snake(self):
        for position in self.position_list:
            self.create_snake_block(position)
    
    def grow(self):
        self.length += 1
    
    def update_head(self, change: list[int,int]):
        self.head_position[0] += change[0]
        self.head_position[1] += change[1]
        self.position_list.append(self.head_position.copy())
        print(self.position_list)
        
    def handle_position_list_length(self):
        if len(self.position_list)> self.length:
            del self.position_list[0]
    
    def handle_own_collision(self):
        for position in self.position_list[:-1]:
            if position == self.head_position:
                self.own_collision = True
    
    def move(self, change: list[int,int]):
        self.update_head(change)
        self.handle_position_list_length()
        self.handle_own_collision()
        
class Food:
    
    def __init__(
        self,
        width:int,
        height:int,
        surface:Surface,
        color:list[int,int,int],
        x_size: int,
        y_size: int,
        ) -> None:
        self.width = width
        self.height = height
        self.surface = surface
        self.color = color
        self.x_size = x_size
        self.y_size = y_size
    
    def create_random_position(self, max_position:int, block_size:int):
        return round(
            random.randrange(0,max_position - block_size) / 10.0
            ) * 10.0
    
    def generate_food_position(self):
        self.foodx = self.create_random_position(self.width,self.x_size)
        self.foody = self.create_random_position(self.height,self.y_size)
    
    def create_food(self):
        pygame.draw.rect(
            self.surface, self.color,
            [
                self.foodx,
                self.foody,
                self.x_size,
                self.y_size,
            ]
        ) 
    
    
class SnakeGame:
    
    def __init__(self,window_height:int,window_width:int) -> None:
        pygame.init()
        self.display = Display(
            dis_height=window_height,
            dis_width=window_width,
            caption_message="Snake Game but smarter"
        )
        
        self.set_initial_position()
        self.game_style = GameStyle()
        self.snake = Snake(
            snake_block=10,
            snake_speed=15,
            initial_position=[self.x1_initial,self.y1_initial],
            snake_color=self.game_style.black,
            surface=self.display.surface
        )
        self.food = Food(
            width=window_height,
            height=window_height,
            color=self.game_style.green,
            surface=self.display.surface,
            x_size=self.snake.snake_block,
            y_size=self.snake.snake_block
        )
        self.game_over = False
        self.game_close = False
        self.clock =pygame.time.Clock()        
        self.food.generate_food_position()
    
    def set_initial_position(self):
        self.x1_initial = self.display.dis_width / 2
        self.y1_initial = self.display.dis_height / 2
        self.x1_change = 0
        self.y1_change = 0
    
    def reset_game(self):
        self.x1_change = 0
        self.y1_change = 0
        self.snake.reset_snake()
        self.food.generate_food_position()        
        self.game_close = False
        self.game_over = False
    
    def set_score_message(self,score):        
        value =  self.game_style.score_font.render(
            f"Your score is {score}",
            True,
            self.game_style.yellow
        )
        self.display.set_additional_surface(value, [0,0])
    
    def set_message(self,msg_text:str,color:tuple[int,int,int]):
        mesg = self.game_style.font_style.render(msg_text, True, color)
        self.display.set_additional_surface(
            mesg, [self.display.dis_width / 6, self.display.dis_height / 3]
            )
        
    def handle_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_close = True
                    self.game_over = False
                if event.key == pygame.K_c:                    
                    self.reset_game()
                    self.game_loop()
    
    def handle_key_movement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x1_change = -self.snake.snake_block
                    self.y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    self.x1_change = self.snake.snake_block
                    self.y1_change = 0
                elif event.key == pygame.K_UP:
                    self.y1_change = -self.snake.snake_block
                    self.x1_change = 0
                elif event.key == pygame.K_DOWN:
                    self.y1_change = self.snake.snake_block
                    self.x1_change = 0
    
    def check_limits(self):
        if self.snake.head_position[0] >= self.display.dis_width \
            or self.snake.head_position[0] < 0 \
            or self.snake.head_position[1] >= self.display.dis_height \
            or self.snake.head_position[1] < 0:
            self.game_over = True
    
    def score(self):
        if self.snake.head_position[0] == self.food.foodx \
            and self.snake.head_position[1] == self.food.foody:
            self.food.generate_food_position()
            self.snake.grow()
    
    def game_loop(self):
        while not self.game_close:
            while self.game_over == True:
                self.display.fill_background(self.game_style.blue)
                self.set_message(
                    "You Lost! Press C-Play Again or Q-Quit",
                    self.game_style.red
                )
                self.set_score_message(self.snake.length - 1)
                self.display.update()
                self.handle_exit()
            self.handle_key_movement()
            self.check_limits()
            self.display.fill_background(self.game_style.blue)
            self.food.create_food()
            self.snake.move([self.x1_change, self.y1_change])
            if self.snake.own_collision:
                self.game_over = True
            self.snake.create_snake()
            self.set_score_message(self.snake.length - 1)
            self.display.update()
            self.score()
            self.clock.tick(self.snake.snake_speed)
        pygame.quit()
        quit()
        

if __name__ == "__main__":
    snake_game = SnakeGame(
        window_height=400,
        window_width=600,
    )
    snake_game.game_loop()