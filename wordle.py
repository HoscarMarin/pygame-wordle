
import random
import pygame, sys
import numpy as np

#-----------------CONSTANTS----------------
TAM_X = 360
TAM_Y = 640

TILE_SIZE = 50
TOP_MARGIN = 100
BORDER_SIZE = 5
KEY_BORDER_SIZE = 3
INNER_BORDER_SIZE = 1

FIVE = 5

BLUE = (33,133,213)
BOMB_CELL = (255, 0, 0)
HIDDEN_CELL = (153, 153, 153)
LIGHT_GREY = (128, 128, 128)
FLAGGED_CELL = (255, 100, 0)
BG_BLACK = (32,33,36)

top_keys = ['Q','W','E','R','T','Y','U','I','O','P']
mid_keys = ['A','S','D','F','G','H','J','K','L']
bot_keys = ['Z','X','C','V','B','N','M']

clues ={'Q': '-','W': '-','E': '-','R': '-','T': '-','Y': '-','U': '-','I': '-','O': '-','P': '-', 'A': '-','S': '-','D': '-','F': '-','G': '-','H': '-','J': '-','K': '-','L': '-','Z': '-','X': '-','C': '-','V': '-','B': '-','N': '-','M': '-'}

CELL_COLORS = {
    " ": (32,33,36),
    "-": LIGHT_GREY,
    "X": (58,58,60),
    "O": (181,159,59),
    "V": (83,141,78,255)
}

#-----------------------------------------

def draw_centered(screen, row, number, color, height):
    long = number*(TILE_SIZE + 2*BORDER_SIZE)
    x_axis = TAM_X
    margin = int((x_axis-long)/2)
    for i in range(number):
        pygame.draw.rect(screen, color, pygame.Rect(i*(TILE_SIZE+BORDER_SIZE*2) + margin, height, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, CELL_COLORS[results[row, i]], pygame.Rect(i*(TILE_SIZE+BORDER_SIZE*2) + margin + INNER_BORDER_SIZE, height + INNER_BORDER_SIZE, TILE_SIZE-2*INNER_BORDER_SIZE, TILE_SIZE-2*INNER_BORDER_SIZE))
        number_surface = boxes_font.render(boxes[row][i],True,(255,255,255))
        number_rect = number_surface.get_rect(center = (int(i*(TILE_SIZE+BORDER_SIZE*2) + margin + TILE_SIZE/2), int(height + TILE_SIZE/2)))
        screen.blit(number_surface,number_rect)

def draw_keys():
    key_size = int(TAM_X/len(top_keys))
    height = int(TAM_Y-(4*TAM_X/len(top_keys)))
    for i in range(len(top_keys)):
        pygame.draw.rect(screen, CELL_COLORS[clues[top_keys[i]]], pygame.Rect(i*key_size + KEY_BORDER_SIZE, height, key_size-2*KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE))
        number_surface = keys_font.render(top_keys[i],True,(255,255,255))
        number_rect = number_surface.get_rect(center = (int(i*key_size + KEY_BORDER_SIZE + key_size/4), int(height + key_size/4)))
        screen.blit(number_surface,number_rect)
    
    key_size = int(TAM_X/len(mid_keys))
    height = int(TAM_Y-(3*TAM_X/len(top_keys)))
    for i in range(len(mid_keys)):
        pygame.draw.rect(screen, CELL_COLORS[clues[mid_keys[i]]], pygame.Rect(i*key_size + KEY_BORDER_SIZE, height, key_size-2*KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE))
        number_surface = keys_font.render(mid_keys[i],True,(255,255,255))
        number_rect = number_surface.get_rect(center = (int(i*key_size + KEY_BORDER_SIZE + key_size/4), int(height + key_size/4)))
        screen.blit(number_surface,number_rect)
    
    height = int(TAM_Y-(2*TAM_X/len(top_keys)))
    #pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(KEY_BORDER_SIZE, height + KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE))
    #screen.blit(enter_img,(KEY_BORDER_SIZE, height + KEY_BORDER_SIZE))
    
    for i in range(len(bot_keys)):
        pygame.draw.rect(screen, CELL_COLORS[clues[bot_keys[i]]], pygame.Rect((i+1)*key_size + KEY_BORDER_SIZE, height + KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE))
        number_surface = keys_font.render(bot_keys[i],True,(255,255,255))
        number_rect = number_surface.get_rect(center = (int((i+1)*key_size + KEY_BORDER_SIZE + key_size/4), int(height + key_size/4)))
        screen.blit(number_surface,number_rect)
    
    #pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect((i+2)*key_size + KEY_BORDER_SIZE, height + KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE, key_size-2*KEY_BORDER_SIZE))
    #screen.blit(del_img,((i+2)*key_size + KEY_BORDER_SIZE, height + KEY_BORDER_SIZE))

def check_word(i):
    global gameover
    is_sol = True
    player_word = ''.join(boxes[i])
    if player_word in accepted_words:
        for pos, letter in enumerate(boxes[i]):
            results[i, pos] = 'X'
            clues[letter] = 'X'
            if(letter in pc_word):
                results[i, pos] = 'O'
                clues[letter] = 'O'
                if (pc_word[pos] == letter):
                    results[i, pos] = 'V'
                    clues[letter] = 'V'
                else:
                    is_sol = False
            else:
                is_sol = False
        gameover = is_sol
        return True
    else:
        print("That's not a word")
        return False

            

#Read accepted words (User input must be one of these)
f = open("AllWordle.txt", "r")
words_with_newline = f.readlines()
accepted_words = [word[:-1] for word in words_with_newline] #erase the last \n
#print(len(accepted_words))

#Read guessing words (Words to guess will be picked from these)
f = open("CommonWordle.txt", "r")
words_with_newline = f.readlines()
guessing_words = [word[:-1] for word in words_with_newline] #erase the last \n
#print(len(guessing_words))

pc_word = random.choice(guessing_words)
print(pc_word)
print(pc_word in accepted_words)

gameover = False

pygame.init()
screen = pygame.display.set_mode((TAM_X,TAM_Y))
clock = pygame.time.Clock()
keys_font = pygame.font.Font('fonts/Mockup-Regular.otf',15)
boxes_font = pygame.font.Font('fonts/Mockup-Regular.otf',30)
title_font = pygame.font.Font('fonts/Mockup-Regular.otf',70)
enter_surface = pygame.image.load('imgs/enter1.png').convert_alpha()
enter_img = pygame.transform.scale(enter_surface, (15,15))
del_surface = pygame.image.load('imgs/arrowback1.png').convert_alpha()
del_img = pygame.transform.scale(del_surface, (20,20))

boxes = np.full((6, FIVE), ' ')
results = np.full((6, FIVE), ' ')
cursor = [0,0]

while True:
    for event in pygame.event.get():
        if cursor[0]>5:
            gameover = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not gameover:
            if(event.key == pygame.K_BACKSPACE):
                if(cursor[1]>0):
                    boxes[cursor[0], cursor[1]-1] = ' '
                    cursor[1] -= 1
            elif(event.key == pygame.K_RETURN):
                if(cursor[1]==FIVE):
                    if(check_word(cursor[0])):
                        cursor[0] += 1
                        cursor[1] = 0
            elif(cursor[1]<FIVE and ((event.key>=pygame.K_a and event.key<=pygame.K_z) or event.key ==241)):
                boxes[cursor[0], cursor[1]] = pygame.key.name(event.key).upper()
                cursor[1] += 1

    
    pygame.draw.rect(screen, BG_BLACK, pygame.Rect(0,0,TAM_X,TAM_Y))
    title_surface = title_font.render('WORDLE',True,(255,255,255))
    title_rect = title_surface.get_rect(center = (int(TAM_X/2), 50))
    screen.blit(title_surface,title_rect)

    for i in range(6):
        draw_centered(screen, i,  FIVE, HIDDEN_CELL, TOP_MARGIN + i*(TILE_SIZE+2*BORDER_SIZE))
    
    draw_keys()

    pygame.display.update()
    clock.tick(60)