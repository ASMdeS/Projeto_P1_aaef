import pygame
from pygame.locals import *
from sys import exit
from Player import *
from Botao import *
from Obstaculo import *
from Coletaveis import *
import random

pygame.init()
# Icone do Jogo
icone_jogo = pygame.image.load('images/menu.png')
pygame.display.set_icon(icone_jogo)
# Iniciar Tela
screen = pygame.display.set_mode((600, 640))
menu = pygame.image.load('images/menu.png')
# Musica de Fundo
musica_de_fundo = pygame.mixer.music.load('sounds/CXR ATK - Dimensions.mp3')
pygame.mixer.music.play(-1)
# Fonte
fonte = pygame.font.SysFont('arial', 30, True, True)


# FUNÇÃO QUE MOSTRA O MENU PRINCIPAL
def menu_principal():
    while True:
        pygame.display.set_caption('Menu Principal')
        # CRIAÇÃO DOS BOTÕES
        botao_jogar = Botao('images/play_button.png', 195, 330)
        botao_sair = Botao('images/leave_button.png', 195, 455)
        botao_jogar.mostrar_botao(screen)
        botao_sair.mostrar_botao(screen)

        # FIM DE JOGO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if botao_jogar.apertado(mouse_x, mouse_y, 330, 415):
                    # RODAR O JOGO
                    print('jogar')
                    jogar()
                if botao_sair.apertado(mouse_x, mouse_y, 455, 540):
                    # FECHA A JANELA
                    print('sair')
                    pygame.quit()
                    exit()

        pygame.display.update()
        screen.blit(menu, (0, 0))


# Função para jogar o Space Battle
def jogar():
    pygame.display.set_caption('Space Battle')
    mapa_background = pygame.image.load('images/map_background.png')
    player1 = Player('images/nave_1.png', 260, 530, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_f)
    player2 = Player('images/nave_2.png', 260, 70, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_RCTRL)
    lista_obstaculos = gerar_lista_obstaculos()
    gerenciador_itens = GerenciadorItensColecionaveis()

    while True:
        # Clock
        pygame.time.Clock().tick(30)

        imagem_coracao = pygame.image.load("images/life.png")
        imagem_bala = pygame.image.load("images/bala.png")
        imagem_coracaoreduzido = pygame.transform.scale(imagem_coracao, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if random.random() < 0.009:  # Ajuste a probabilidade conforme necessário
            gerenciador_itens.gerar_item()

        player1.movimento(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, lista_obstaculos)
        player2.movimento(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, lista_obstaculos)

        player1.mostrar_player(screen)
        player2.mostrar_player(screen)

        for item in gerenciador_itens.itens:
            if pygame.sprite.collide_rect(player1, item):
                if item.name == "images/velocidade.png":
                    if player1.velocidade < 20:
                        player1.velocidade += 5
            if pygame.sprite.collide_rect(player2, item):
                if item.name == "images/velocidade.png":
                    if player2.velocidade < 20:
                        player2.velocidade += 5
            if pygame.sprite.collide_rect(player1, item):
                if item.name == "images/life.png":
                    if player1.vidas < 6:
                        player1.vidas += 1
            if pygame.sprite.collide_rect(player2, item):
                if item.name == "images/life.png":
                    if player2.vidas < 6:
                        player2.vidas += 1
            if pygame.sprite.collide_rect(player1, item):
                if item.name == "images/bala.png":
                    if player1.balas < 6:
                        player1.balas += 1
            if pygame.sprite.collide_rect(player2, item):
                if item.name == "images/bala.png":
                    if player2.balas < 6:
                        player2.balas += 1

        pygame.sprite.spritecollide(player1, gerenciador_itens.itens, True)
        pygame.sprite.spritecollide(player2, gerenciador_itens.itens, True)

        for obstaculo in lista_obstaculos:
            obstaculo.mostrar_obstaculo(screen)

        # Vidas dos Players
        for i in range(int(player1.vidas)):
            screen.blit(imagem_coracaoreduzido, (30 + (i * 20), 570))
        for i in range(int(player2.vidas)):
            screen.blit(imagem_coracaoreduzido, (30 + (i * 20), 40))

        # Balas dos Players
        for i in range(int(player1.balas)):
            screen.blit(imagem_bala, (570 - (i * 20), 570))
        for i in range(int(player2.balas)):
            screen.blit(imagem_bala, (570 - (i * 20), 40))

        gerenciador_itens.itens.update()
        gerenciador_itens.itens.draw(screen)

        pygame.display.update()
        screen.blit(mapa_background, (0, 0))


menu_principal()
