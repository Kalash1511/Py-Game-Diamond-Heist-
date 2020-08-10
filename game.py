import keyboard
from PIL import Image
import pygame
from pygame.locals import *
import time

pygame.init()
x = 1024
y = 768
pygame.display.set_caption('Diamond Heist')
screen = pygame.display.set_mode((x, y))


class GIFImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False

    def get_rect(self):
        return pygame.rect.Rect((0,0), self.image.size)

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0,0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()

        screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames)-1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)
    def fastforward(self):
        self.seek(self.length()-1)

    def get_height(self):
        return self.image.size[1]
    def get_width(self):
        return self.image.size[0]
    def get_size(self):
        return self.image.size
    def length(self):
        return len(self.frames)
    def reverse(self):
        self.reversed = not self.reversed
    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        return new



def load_image(name):
    image = pygame.image.load(name)
    return image

def success():
    dia = GIFImage("original.gif")
    run = True
    while run:
        if keyboard.is_pressed('s'):
            run = False
        screen.blit(load_image(r'back_success.jpg'), (0, 0))
        dia.render(screen, (262, 234))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()


def failure():
    run = True
    diamond = GIFImage("fail.gif")
    while run:
        if keyboard.is_pressed('s'):
            run = False
        screen.blit(load_image(r'fail_back.jpg'), (0, 0))
        diamond.render(screen, (185, 24))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()
    return run




class laser(object):
    def __init__(self, pos, color, orient, step):
        self.pos = pos
        self.color = color
        self.orient = orient
        self.step = step



def main() :

    images = []

    images.append(load_image('1.png'))
    images.append(load_image('2.png'))
    images.append(load_image('3.png'))
    images.append(load_image('4.png'))
    images.append(load_image('5.png'))
    images.append(load_image('6.png'))


    #creating GIFImage object

    diamond = GIFImage("diamond.gif")

    # creating list for laser object
    list = [
                laser(0, 3, 2, 10), laser(1024, 2, 2, -10),
                laser(200, 2, 1, 10), laser(568, 3, 1, -10),
                laser(400, 1, 1, 10), laser(368, 2, 1, -10),
                laser(200, 2, 2, 10), laser(824, 1, 2, -10)
           ]

    d_pos = 1024
    d_steps = 20
    restart = True

    while True:
        screen.blit(load_image(r'Background.jpg'), (0, 0))
        pygame.display.update()
        diamond.render(screen, (362, 284))
        pygame.display.update()

        pygame.draw.line(screen, (0, 255, 0), (0, 0), (1024- d_pos, 768), 3)
        pygame.display.update()
        pygame.draw.line(screen, (255, 0, 0), (0, 768), (1024 - d_pos, 0), 3)
        pygame.display.update()

        pygame.draw.line(screen, (0, 255, 0), (1024, 0), (d_pos, 768), 3)
        pygame.display.update()
        pygame.draw.line(screen, (255, 0, 0), (1024, 768), (d_pos, 0), 3)
        pygame.display.update()

        for obj in list:
            if keyboard.is_pressed('r'):
                for k in list:
                    if k.pos in range(284, 484) and k.orient == 1:
                        restart = failure()
                    elif k.pos in range(362, 662) and k.orient == 2:
                        restart = failure()

                if restart:
                    success()
                else :
                    restart = True

            if obj.orient == 1:
                screen.blit(images[obj.color-1], (0, obj.pos))
                pygame.display.update()
                obj.pos = obj.pos+obj.step
                if obj.pos > 760:
                    obj.pos = 0
                elif obj.pos < 0:
                    obj.pos = 768

            elif obj.orient == 2:
                screen.blit(images[obj.color + 2], (obj.pos, 0))
                pygame.display.update()
                obj.pos = obj.pos+obj.step
                if obj.pos > 1020:
                    obj.pos = 0
                elif obj.pos < 0:
                    obj.pos = 1024

        if d_pos < 10 or d_pos > 1030:
            d_steps = -1 * d_steps

        d_pos = d_pos - d_steps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()

if __name__ == '__main__':
    main()