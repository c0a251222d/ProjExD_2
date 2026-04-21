import os
import sys
import pygame as pg
import random 


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > 1100:
        yoko = False
    if rct.top < 0 or rct.bottom > 650:
        tate = False
    return (yoko, tate)


def gameover(screen: pg.Surface) -> None:
    """
    画面をブラックアウトし，
    泣いているこうかとん画像と
    「Game Over」の文字列を
    5秒間表示させる
    """
    go_screen = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_screen, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_screen.set_alpha(150)

    go_font = pg.font.Font(None, 50)
    go_txt = go_font.render("Game Over", True, (255, 255, 255))
    go_txt_rct = go_txt.get_rect()
    go_txt_rct.center = 550, 325

    kktn1_img = pg.image.load("fig/8.png")
    kktn1_img_rct = kktn1_img.get_rect()
    kktn1_img_rct.center = 400, 325
    kktn2_img = pg.image.load("fig/8.png")
    kktn2_img_rct = kktn2_img.get_rect()
    kktn2_img_rct.center = 700, 325

    go_screen.blit(go_txt, go_txt_rct)
    screen.blit(go_screen, [0, 0])
    screen.blit(kktn1_img, kktn1_img_rct)
    screen.blit(kktn2_img, kktn2_img_rct)
    pg.display.update()
    pg.time.wait(5000)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return (bb_imgs, bb_accs)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0, WIDTH)), (random.randint(0, HEIGHT))
    bb_vx = 5
    bb_vy = 5

    clock = pg.time.Clock()
    tmr = 0
    # bb_imgs = 
    # bb_accs = init_bb_imgs()[1]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(+5, 0)}
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bb_rct.move_ip(bb_vx, bb_vy)
        if check_bound(bb_rct)[0] == (False):
            bb_vx = bb_vx*-1
            bb_rct.move_ip(bb_vx, bb_vy)
        if check_bound(bb_rct)[1] == (False):
            bb_vy = bb_vy*-1
            bb_rct.move_ip(bb_vx, bb_vy)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
