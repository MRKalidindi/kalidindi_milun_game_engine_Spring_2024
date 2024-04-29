import pygame as pg

clock = pg.time.Clock()
FPS = 30

frames = ["frame1", "frame2", "frame3", "frame4"]


# while True:
#     x = x%len(frames)
#     print(frames[x])
#     x+=1




# print(frames[x])
# firstFrame = x%len(frames)
# print(frames[firstFrame])
x = 0
then = 0
current_frame = 0

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 10:
        print([current_frame])
        current_frame = (current_frame + 1) % 4
        # print(now)
        # then = now
    # print(pg.time.get_ticks())
    