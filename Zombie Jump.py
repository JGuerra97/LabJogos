from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.animation import *
from PPlay.sound import *
from random import randint

janela = Window(1024,700)
janela.set_title('Zombie Jump')
teclado = janela.get_keyboard()

# Menu
fundomenu = GameImage('FundoMenu.jpg')
fundojogo = GameImage('FundoJogo.jpg')
ZombieJump = Sprite('ZombieJump.png')
ZombieJump.set_position(janela.width/2 - ZombieJump.width/2, 0)
startbutton = Sprite('Jogar.png')
startbutton.set_position(janela.width/2 - startbutton.width/2, ZombieJump.y + ZombieJump.height + startbutton.height)
sairbutton = Sprite('Sair.png')
sairbutton.set_position(janela.width/2 - sairbutton.width/2, startbutton.y + startbutton.height + janela.height/100)
select = Sprite('ZJ.png')
select.set_position(startbutton.x - select.width, startbutton.y)
spritegameover = Sprite('Game Over.png')
spritegameover.set_position(janela.width/2 - spritegameover.width/2, janela.height/2 - spritegameover.height/2)
mascaraPausa = Sprite('Pausa.png')
mascaraPausa.set_position(0, 0)

# Chão (Plataforma 0)
ground = Sprite('ground.jpg')
ground.set_position(0, janela.height - ground.height)

# Rick (Player)
rick = Sprite('Rick.png', 20)
rick.set_position(0, janela.height - ground.height - rick.height)
marcador = Sprite('Marcador.jpg')
marcador.set_position(rick.x, rick.y + rick.height)

# Sons
somZumbi = Sound('Sons/ZumbiSom.ogg')
somZumbi.set_volume(80)
somZumbi.set_repeat(False)
somMorte = Sound('Sons/SomMorteRick.ogg')
somMorte.set_volume(100)
somMorte.set_repeat(False)
somMoeda = Sound('Sons/SomMoeda.ogg')
somMoeda.set_volume(60)
somMoeda.set_repeat(False)
somMenu = Sound('Sons/SomMenu.ogg')
somMenu.set_volume(60)
somMenu.set_repeat(True)
somJogo = Sound('Sons/SomDeFundo.ogg')
somJogo.set_volume(100)
somJogo.set_repeat(True)

jump = rick.y
j = 0
z = 0
c = 1
t = 1
t_pausa = 1
score = 0
velocidade_scrolling = 150 + score/5000

highscore = open('Highscore.txt', 'r')
hs = highscore.readlines()
hs = int(hs[0])
highscore.close()


def criar_plats():
    plats = []
    plat0 = Sprite('plataforma.jpg')
    pos = randint(0, 744)
    plat0.set_position(pos, ground.y - (rick.height + ground.height + plat0.height))
    plats.append(plat0)
    for i in range(1, 10):
        plat = Sprite('plataforma.jpg')
        while True:
            pos = randint(plats[i-1].x - plat.width - 50, plats[i-1].x + plats[i-1].width + 50)
            if plats[i-1].x - (3*(plat.width/4)) < pos < plats[i-1].x + (3*(plats[i-1].width/4)):
                continue
            if 0 <= pos <= 744:
                plat.set_position(pos, ground.y - ((i+1) * (rick.height + ground.height + plat.height)))
                break
        plats.append(plat)
    return plats


def desenhar_plats():
    for i in range(len(plataformas)):
        plataformas[i].draw()


def criar_moedas():
    coins = []
    for i in range(3):
        ocupado = True
        moeda = Sprite('Moeda.png')
        while ocupado:
            plat_moeda = randint(0, len(plataformas) - 1)
            moeda.set_position(plataformas[plat_moeda].x + plataformas[plat_moeda].width/2 - moeda.width/2,
                               plataformas[plat_moeda].y - moeda.height)
            ocupado = False
            for m in coins:
                if moeda.collided(m):
                    ocupado = True
        coins.append(moeda)
    return coins


def coleta_moedas():
    global score
    recreate = 0
    captura_moeda = 0
    for m in moedas:
        if rick.collided(m):
            somMoeda.play()
            score = score + 1
            recreate = 1
            moedas.remove(m)
            break
    if recreate == 1:
        ocupado = True
        moeda = Sprite('Moeda.png')
        while ocupado:
            plat_moeda = randint(captura_moeda + 2, len(plataformas) - 1)
            if marcador.collided(plataformas[plat_moeda]):
                continue
            moeda.set_position(plataformas[plat_moeda].x + plataformas[plat_moeda].width/2 - moeda.width/2,
                               plataformas[plat_moeda].y - moeda.height)
            if marcador.collided(plataformas[plat_moeda]):
                continue
            ocupado = False
            for m in moedas:
                if moeda.collided(m):
                    ocupado = True
        moedas.append(moeda)


def recriar_moedas():
    recreate = 0
    for m in moedas:
        if m.y > janela.height:
            moedas.remove(m)
            recreate = 1
            break
    if recreate == 1:
        ocupado = True
        moeda = Sprite('Moeda.png')
        while ocupado:
            plat_moeda = randint(0, len(plataformas) - 1)
            if marcador.collided(plataformas[plat_moeda]):
                continue
            moeda.set_position(plataformas[plat_moeda].x + plataformas[plat_moeda].width / 2 - moeda.width / 2,
                               plataformas[plat_moeda].y - moeda.height)
            if marcador.collided(plataformas[plat_moeda]):
                continue
            ocupado = False
            for m in moedas:
                if moeda.collided(m):
                    ocupado = True
        moedas.append(moeda)


def desenhar_moedas():
    for i in range(len(moedas)):
        moedas[i].draw()


def criar_zumbi(plataform):
    zumbi1 = Sprite('Zumbi1_Walk.png', 12)
    zumbi1.set_position(plataformas[plataform].x, plataformas[plataform].y - zumbi1.height)
    return zumbi1


def gravity(sprite):
    colisao = False
    for i in plataformas:
        if sprite.collided(i):
            colisao = True
    if not sprite.collided(ground) and not colisao:
        rick.y = rick.y + 6


def scrolling(delta, vel):
    for p in plataformas:
        p.y = p.y + (vel * delta)
    for m in moedas:
        m.y = m.y + (vel * delta)
    zumbi.y = zumbi.y + (vel * delta)
    rick.y = rick.y + (vel * delta)
    marcador.y = marcador.y + (vel * delta)
    ground.y = ground.y + (vel * delta)


def pausa():
    somJogo.stop()
    while True:
        global t_pausa
        if teclado.key_pressed('p') and t_pausa >= 0.2:
            t_pausa = 0
            break
        fundojogo.draw()
        ground.draw()
        desenhar_plats()
        desenhar_moedas()
        zumbi.draw()
        rick.draw()
        janela.draw_text('Pontuação: ' + str(score), janela.width / 2, janela.height / 50, 100, (255, 0, 0), 'Chiller')
        mascaraPausa.draw()
        janela.draw_text('Aperte p para voltar para o jogo', 0, janela.height - 30, 30, (255, 255, 255), 'Chiller')
        t_pausa = t_pausa + janela.delta_time()
        janela.update()


while True:

    score = 0
    velocidade_scrolling = 150 + score/5000
    new_plat = 1
    game_over = False
    ground.set_position(0, janela.height - ground.height)
    rick.set_position(0, janela.height - ground.height - rick.height)
    marcador.set_position(rick.x, rick.y + rick.height)
    plataformas = criar_plats()
    moedas = criar_moedas()
    plat_zombie = 0
    zumbi = criar_zumbi(plat_zombie)
    z = 0
    j = 0
    t_pausa = 1
    cronometro_zumbis = 1

    somMenu.play()

    if c >= 0.2:

        if teclado.key_pressed('down'):
            if select.y == startbutton.y:
                select.y = sairbutton.y
                select.x = sairbutton.x - select.width
                c = 0
                continue
            elif select.y == sairbutton.y:
                select.y = startbutton.y
                select.x = startbutton.x - select.width
                c = 0
                continue
        if teclado.key_pressed('up'):
            if select.y == sairbutton.y:
                select.y = startbutton.y
                select.x = startbutton.x - select.width
                c = 0
                continue
            elif select.y == startbutton.y:
                select.y = sairbutton.y
                select.x = sairbutton.x - select.width
                c = 0
                continue

        if teclado.key_pressed('enter'):
            if select.y == startbutton.y:
                somMenu.stop()

                while True:

                    if game_over:
                        if teclado.key_pressed('esc'):
                            if score > hs:
                                highscore = open('Highscore.txt', 'w')
                                highscore.write(str(score))
                                highscore.close()
                                highscore = open('Highscore.txt', 'r')
                                hs = highscore.readlines()
                                hs = int(hs[0])
                                highscore.close()
                            break
                        janela.set_background_color((0,0,0))
                        if score > hs:
                            janela.draw_text('Novo Recorde!', 20, 0, 100, (43, 43, 43), 'Chiller')
                            janela.draw_text('Novo Recorde!', 5, 10, 100, (255, 0, 0), 'Chiller')
                        janela.draw_text('Pontuação: ' + str(score), janela.width/2 + 15, 0, 100, (43, 43, 43), 'Chiller')
                        janela.draw_text('Pontuação: ' + str(score), janela.width/2, 10, 100, (255, 0, 0), 'Chiller')
                        janela.draw_text('Aperte Esc para voltar para o menu', 0, janela.height - 30, 30, (255, 255, 255), 'Chiller')
                        spritegameover.draw()
                        janela.update()
                        continue

                    if not somJogo.is_playing():
                        somJogo.play()

                    if teclado.key_pressed('p') and t_pausa >= 0.2:
                        t_pausa = 0
                        pausa()

                    if rick.y >= janela.height or rick.collided(zumbi):
                        somJogo.stop()
                        if somZumbi.is_playing():
                            somZumbi.stop()
                        somMorte.play()
                        game_over = True
                        continue

                    marcador.set_position(rick.x, rick.y + rick.height)
                    if teclado.key_pressed('esc'):
                        somJogo.stop()
                        if score > hs:
                            highscore = open('Highscore.txt', 'w')
                            highscore.write(str(score))
                            highscore.close()
                            highscore = open('Highscore.txt', 'r')
                            hs = highscore.readlines()
                            hs = int(hs[0])
                            highscore.close()
                        break

                    if teclado.key_pressed('left') and rick.x > 0:
                        rick.x = rick.x + (-300 * janela.delta_time())
                        if rick.get_curr_frame() < 10:
                            rick.set_curr_frame(10)
                        if t >= 0.375:
                            t = 0
                            rick.set_sequence_time(11, 19, 65, True)
                        rick.update()
                    elif teclado.key_pressed('right') and rick.x + rick.width < janela.width:
                        rick.x = rick.x + (300 * janela.delta_time())
                        if rick.get_curr_frame() > 8:
                            rick.set_curr_frame(0)
                        if t >= 0.375:
                            t = 0
                            rick.set_sequence_time(0, 8, 65, True)
                        rick.update()
                    else:
                        if rick.get_curr_frame() < 9:
                            rick.set_curr_frame(9)
                        elif rick.get_curr_frame() > 10:
                            rick.set_curr_frame(10)

                    for p in range(len(plataformas)):
                        if zumbi.collided(plataformas[p]):
                            plat_zombie = p
                            break

                    if marcador.collided(plataformas[plat_zombie]):
                        somZumbi.play()

                    if z == 0:
                        if zumbi.x + zumbi.width < plataformas[plat_zombie].x + plataformas[plat_zombie].width:
                            if (plataformas[plat_zombie].x + plataformas[plat_zombie].width) - (zumbi.x + zumbi.width) <= 2:
                                z = 1
                            if cronometro_zumbis >= 0.5:
                                if zumbi.get_curr_frame() > 5:
                                    zumbi.set_curr_frame(0)
                                    zumbi.update()
                                cronometro_zumbis = 0
                                zumbi.set_sequence_time(0, 5, 100, True)
                            zumbi.x = zumbi.x + (75 * janela.delta_time())
                    elif z == 1:
                        if zumbi.x > plataformas[plat_zombie].x:
                            if zumbi.x - plataformas[plat_zombie].x <= 2:
                                z = 0
                            if cronometro_zumbis >= 0.5:
                                if zumbi.get_curr_frame() < 6:
                                    zumbi.set_curr_frame(6)
                                    zumbi.update()
                                cronometro_zumbis = 0
                                zumbi.set_sequence_time(6, 11, 100, True)
                            zumbi.x = zumbi.x + (-75 * janela.delta_time())

                    collision = 0
                    for i in plataformas:
                        if marcador.collided(i):
                            collision = 1
                    if teclado.key_pressed('up') and j == 0 and (marcador.collided(ground) or collision == 1):
                        jump = rick.y
                        j = 55
                    if j > 0:
                        rick.y += -10
                        j += -1

                    for p in range(len(plataformas)):
                        if plataformas[p].y > janela.height + rick.height:
                            plat = Sprite('plataforma.jpg')
                            while True:
                                pos = randint(plataformas[len(plataformas)-1].x - plat.width - 50,
                                              plataformas[len(plataformas) - 1].x + plataformas[len(plataformas)-1].width + 50)
                                if plataformas[p-1].x - (3*(plataformas[p-1].width/4)) < pos < plataformas[p-1].x + (3*(plataformas[p-1].width/4)):
                                    continue
                                if 0 <= pos <= 744:
                                    plat.set_position(pos, plataformas[len(plataformas)-1].y - (rick.height + ground.height + plat.height))
                                    new_plat = new_plat + 1
                                    break
                            plataformas.append(plat)
                            plataformas.remove(plataformas[p])
                            if new_plat % 7 == 0 and zumbi.y > janela.height:
                                zumbi.set_position(plat.x + 2, plat.y - zumbi.height + 1)
                                z = 0
                                cronometro_zumbis = 1
                                zumbi.set_curr_frame(0)
                            break

                    coleta_moedas()
                    recriar_moedas()

                    cronometro_zumbis = cronometro_zumbis + janela.delta_time()
                    c = c + janela.delta_time()
                    t = t + janela.delta_time()
                    t_pausa = t_pausa + janela.delta_time()
                    gravity(marcador)
                    if not marcador.collided(ground):
                        scrolling(janela.delta_time(), velocidade_scrolling)
                    velocidade_scrolling += score/5000
                    fundojogo.draw()
                    ground.draw()
                    desenhar_plats()
                    desenhar_moedas()
                    zumbi.draw()
                    zumbi.update()
                    rick.draw()
                    janela.draw_text('Pontuação: ' + str(score), janela.width/2, janela.height/50, 100, (255, 0, 0), 'Chiller')
                    janela.draw_text('Aperte p para dar pausa', 0, janela.height - 30, 30, (255, 255, 255), 'Chiller')
                    janela.update()

            elif select.y == sairbutton.y:
                quit()

    c = c + janela.delta_time()
    fundomenu.draw()
    ZombieJump.draw()
    startbutton.draw()
    sairbutton.draw()
    select.draw()
    janela.draw_text('Criado por: Gabriel Brandão & João Matheus', 0, janela.height - 30, 30, (255, 255, 255), 'Chiller')
    janela.draw_text('Highscore: ' + str(hs), 0, 0, 35, (255, 0, 0), 'Chiller')
    janela.update()