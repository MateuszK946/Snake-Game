import pygame
import random
import tkinter as tka
from tkinter import messagebox
import sys

class Cube(object):
    rows = 20
    def __init__(self, start_position, direx = 1, direy = 0, color = (0, 255, 0)):
        self.start_position = start_position
        self.direx = direx
        self.direy = direy
        self.color = color

    def move(self, direx, direy):
        self.direx = direx
        self.direy = direy
        self.start_position = (self.start_position[0] + self.direx, self.start_position[1] + self.direy)

    def draw(self, surface):
        cube_size = size // rows
        row = self.start_position[0]
        column = self.start_position[1]
        pygame.draw.rect(surface, s.color, (row * cube_size + 2, column * cube_size + 2, cube_size - 3, cube_size - 3))    # rysowanie kostki, +1 i -2 są dodane po to aby kostka nie pokrywała się z krawędziami siatki

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, start_position):
        self.color = color
        self.head = Cube(start_position)
        self.body.append(self.head)
        self.direy = 1
        self.direx= 0

    def move(self):    # ruch węża
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # zamyka grę jeśli zostanie naciśnięty przycisk wyjścia (X)
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:    # wąż porusza się w lewo
                self.direx = -1
                self.direy = 0
                self.turns[self.head.start_position[:]] = [self.direx, self.direy]    # zapisanie pozycji głowy węża w momencie naciśnięcia klawisza, reszta ciała węża musi przejść przez ten punkt i skręcić w kierunku tam gdzie skręciła głowa
            elif keys[pygame.K_RIGHT]:    # wąż porusza się w prawo
                self.direx = 1
                self.direy = 0
                self.turns[self.head.start_position[:]] = [self.direx, self.direy]
            elif keys[pygame.K_UP]:    # wąż porusza się w górę
                self.direx = 0
                self.direy = -1
                self.turns[self.head.start_position[:]] = [self.direx, self.direy]
            elif keys[pygame.K_DOWN]:    # wąż porusza się w dół
                self.direx = 0
                self.direy = 1
                self.turns[self.head.start_position[:]] = [self.direx, self.direy]

        for i, c in enumerate(self.body):
            p = c.start_position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:    # przechodzenie węża na drugą stronę ekranu if i elify w sytuacji gdy wąż dotknie ściany przenoszą głowę na przeciwną strone planszy
                if c.direx == -1 and c.start_position[0] <= 0:
                    c.start_position = (c.rows - 1, c.start_position[1])
                elif c.direx == 1 and c.start_position[0] >= c.rows - 1:
                    c.start_position = (0, c.start_position[1])
                elif c.direy == -1 and c.start_position[1] <= 0:
                    c.start_position = (c.start_position[0], c.rows - 1)
                elif c.direy == 1 and c.start_position[1] >= c.rows - 1:
                    c.start_position = (c.start_position[0], 0)
                else:    # jeśli wąż nie dotyka krawędzi ruch jest wykonywany jak w założeniu
                    c.move(c.direx, c.direy)

    def death(self, start_position):    # śmierć węża
        self.head = Cube(start_position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direx = 0
        self.direy = 1

    def add_cube_to_tail(self):    # dodanie klocka do ogona węża
        tail = self.body[-1]
        dx = tail.direx
        dy = tail.direy

        if dx == 1 and dy == 0:    # jesli ostatnia kostka w ciele węża porusza się w prawo klocek zostanie dodany w pozycji -1 za ostanią pozycją
            self.body.append(Cube((tail.start_position[0] - 1, tail.start_position[1])))
        elif dx == -1 and dy == 0:    # jesli ostatnia kostka w ciele węża porusza się w lewo klocek zostanie dodany w pozycji +1 za ostanią pozycją
            self.body.append(Cube((tail.start_position[0] + 1, tail.start_position[1])))
        elif dx == 0 and dy == 1:    # jesli ostatnia kostka w ciele węża porusza się w dół klocek zostanie dodany w pozycji -1 za ostanią pozycją
            self.body.append(Cube((tail.start_position[0], tail.start_position[1] - 1)))
        elif dx == 0 and dy == -1:    # jesli ostatnia kostka w ciele węża porusza się w górę klocek zostanie dodany w pozycji +1 za ostanią pozycją
            self.body.append(Cube((tail.start_position[0] , tail.start_position[1] + 1)))

        # nadanie kierunku poruszania starego ostatniego klocka się dla nowego ostatniego klocka
        self.body[-1].direx = dx
        self.body[-1].direy = dy

    def draw_snake(self, surface):    # narysowanie węża
        for i, c in enumerate(self.body):
            c.draw(surface)


def draw_grid(width, rows, surface):    # rysowanie siatki planszy do gry
    between_rows = width // rows    # odstęp pomiędzy liniami siatki
    x = 0
    y = 0
    for i in range(rows):    # tworzenie siatki na planszy do gry
        x = x + between_rows
        y = y + between_rows
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x,width))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (width, y))

def draw_window(surface):    # rysowanie okna (planszy) gry
    surface.fill((255, 255, 255))    # nadanie powierzchni okna koloru
    s.draw_snake(surface)    # rysowanie węża w oknie
    new_apple.draw(surface)    # rysowanie jabłka
    draw_grid(size, rows, surface)    # rysowanie siatki
    pygame.display.update()

def apple(snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.start_position ==(x, y), positions))) >0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tka.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global size, rows, s, new_apple, flag
    size = 500    # wielkośc okna dialogowego gry
    rows = 20    # ilość wierszy

    window = pygame.display.set_mode((size, size))

    s = Snake((0, 255, 0), (10, 10))
    new_apple = Cube(apple(s), color=(255, 0, 0))
    flag = True   # jeżeli True to gra będzie działać

    while flag:
        pygame.time.delay(50)    # spowolnienie gry o podaną liczbę milisekund
        pygame.time.Clock().tick(10)    # ilość klatek na sekundę jaką pokonuje wąż
        s.move()
        if s.body[0].start_position == new_apple.start_position:
            s.add_cube_to_tail()
            new_apple = Cube(apple(s), color=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].start_position in list(map(lambda z: z.start_position, s.body[x+1:])):
                print('Wynik: ', len(s.body))
                message_box('Game over!', 'YOU LOSE!')
                s.death((10, 10))
                break

        draw_window(window)

main()
