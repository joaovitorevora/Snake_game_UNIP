import random
import pygame
from pygame import mixer
from copy import deepcopy

class Square(object): # Esta classe constrói um objeto quadrado, que é usado para exibir as partes da cobra e da comida.

    def __init__(self, posX, posY, color):

        self.width = 20  # Largura do quadrado (20).
        self.height = 20  # Altura do quadrado (20).
        self.color = color  # Define uma cor padrão.
        self.posX = posX  # Define a posição X para a posição indicada pelo parâmetro posX.
        self.posY = posY  # Define a posição Y para a posição indicada pelo parâmetro posY.
        self.dirRight = 1  # Define o quanto o quadrado está virado para direita.
        self.dirLeft = 0  # Define o quanto o quadrado está virado para esquerda.
        self.dirDown = 0  # Define o quanto o quadrado está virado para baixo.
        self.dirUp = 0  # Define o quanto o quadrado está virado para cima.

    def move(self, posX, posY, dirRight, dirLeft, dirUp, dirDown): # Função "move" para atualizar a posição do quadrado.

        self.posX = posX # Define a nova coordenada de X.
        self.posY = posY # Define a nova coordenada de Y.
        self.dirRight = dirRight # Define se está virado para a direita.
        self.dirLeft = dirLeft # Define se está virado para a esquerda.
        self.dirUp = dirUp # Define se está virado para cima.
        self.dirDown = dirDown # Define se está virado para baixo.

class Snake(object): # Esta classe constrói uma lista de quadrados, para representar a cobra.

    def __init__(self): # Contrução da cobra.

        self.body = []  # Define o corpo da cobra como uma lista vazia.
        self.head = Square(100, 300, (255, 255, 255))  # Cria a cabeça da cobra.
        self.body.append(self.head)  # Junta a cabeça ao corpo.

    def reset(self, posX, posY): # Reseta o tamanho da cobra para seu tamanho inicial.

        self.body = []
        self.head = Square(posX, posY, (255, 255, 255)) # Coordenada X e Y onde a cobra irá começar novamente.
        self.body.append(self.head) # Anexa a cabeça ao corpo.

    def move(self, vX, vY): # Função para mover a cobra através das teclas de setas. vX e vY são as velocidades da cobra em X e Y.

        keys = pygame.key.get_pressed()  # lê se uma tecla foi apertada.
        flag = False  # Mostra se a cobra "bateu" em sua cauda (quadrado logo após a cabeça).
        lastX = self.body[-1].posX  # Posição X inicial da cauda.
        lastY = self.body[-1].posY  # Posição Y inicial da cauda.
        self.reorganize()  # Reorganiza a cobra, deixando apenas a cabeça para ser alterada.

        if keys[pygame.K_w] or keys[pygame.K_UP]: # Se a tecla "W" ou "Seta para cima" forem apertados, move a cobra para cima.

            self.head.dirRight = 0
            self.head.dirLeft = 0
            self.head.dirDown = 0
            self.head.dirUp = 1
            vX = 0
            vY = -20

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: # Se a tecla "A" ou "Seta para esquerda" forem apertados, move a cobra para esquerda.

            self.head.dirRight = 0
            self.head.dirLeft = 1
            self.head.dirDown = 0
            self.head.dirUp = 20
            vX = -20
            vY = 0

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: # Se a tecla "S" ou "Seta para baixo" forem apertados, move a cobra para baixo.

            self.head.dirRight = 0
            self.head.dirLeft = 0
            self.head.dirDown = 1
            self.head.dirUp = 0
            vX = 0
            vY = 20

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: # Se a tecla "D" ou "Seta para direita" forem apertados, move a cobra para direita.

            self.head.dirRight = 1
            self.head.dirLeft = 0
            self.head.dirDown = 0
            self.head.dirUp = 0
            vX = 20
            vY = 0

        self.head.posX += vX  # Altera a velocidade de X quando a cobra se movimenta para esquerda ou direita.
        self.head.posY += vY  # Altera a velocidade de Y quando a cobra se movimenta para cima ou baixo.

        # Essas quatro instruções if/elif controlam os limites, para que a cobra não desapareça da tela.
        if self.head.posX >= 600:  # Se a posição da cabeça estiver muito à direita, ela reaparecerá no lado esquerdo.
            self.head.posX = 0
        elif self.head.posX < 0:  # Se a posição da cabeça estiver muito à esquerda, ela reaparecerá no lado direito.
            self.head.posX = 580
        elif self.head.posY >= 600:  # Se a posição da cabeça estiver muito para baixo, ela reaparecerá em cima.
            self.head.posY = 0
        elif self.head.posY < 0:  # Se a posição da cabeça estiver muito para cima, ela reaparecerá em baixo.
            self.head.posY = 580

        if self.head.posX == lastX and self.head.posY == lastY:  # Determina se a cobra voltou em sua própria cauda.
            flag = True

        return vX, vY, flag

    def reorganize(self): 
    # Reorganiza a cobra. Usando uma cópia da lista do corpo da cobra.
    # Cada quadrado é atualizado para os valores dos quadrados anteriores.

        newBody = deepcopy(self.body)  # Faz uma cópia "Superficial" do corpo.

        # Para cada quadrado no corpo da cobra, sua posição será atualizada para a posição do quadrado anterior.
        for index, square in enumerate(self.body):
            if square == self.body[0]:  # Pula a cabeça.
                continue
            else:
                self.body[index].move(newBody[index - 1].posX, newBody[index - 1].posY,
                                      newBody[index - 1].dirRight,
                                      newBody[index - 1].dirLeft, newBody[index - 1].dirUp,
                                      newBody[index - 1].dirDown)

    def addSquare(self): # Adiciona um quadrado à cauda da cobra.

        mixer.music.load("Arquivos do jogo/Som quando come.wav")  # Som da cobra quando come a comida.
        mixer.music.set_volume(0.05)  # Reduz o volume do som ao comer.
        mixer.music.play()  # Toca o som da cobra comendo.
        tail = self.body[-1]  # Cauda da cobra atual (último quadrado).

        if tail.dirDown == 1:  # Se a direção da cauda estiver voltada para baixo, adiciona um novo quadrado acima da cauda atual.
            newTail = Square(tail.posX, tail.posY - 20, (255, 255, 255))
            newTail.dirDown = 1
            newTail.dirRight = 0
            self.body.append(newTail)

        elif tail.dirUp == 1:  # Se a direção da cauda estiver voltada para baixo, adiciona um novo quadrado abaixo da cauda.
            newTail = Square(tail.posX, tail.posY + 20, (255, 255, 255))
            newTail.dirUp = 1
            newTail.dirRight = 0
            self.body.append(newTail)

        elif tail.dirRight == 1:  # Se a direção da cauda estiver voltada para baixo, adiciona um novo quadrado à esquerda da cauda.
            newTail = Square(tail.posX - 20, tail.posY, (255, 255, 255))
            self.body.append(newTail)

        elif tail.dirLeft == 1:  # Se a direção da cauda estiver voltada para baixo, adiciona um novo quadrado à direita da causa.
            newTail = Square(tail.posX + 20, tail.posY, (255, 255, 255))
            newTail.dirLeft = 1
            newTail.dirRight = 0
            self.body.append(newTail)

    def draw(self, window): # Desenha a cobra.

        for i, square in enumerate(self.body):
            pygame.draw.rect(window, square.color, (square.posX, square.posY, square.width, square.height))

class Button: # Classe "Button" para criar os botões do menu inicial.

    def __init__(self, x, y, width, height, text):

        self.color = (107, 199, 107) # Cor do botão.
        self.x = x # Coordenada X do botão.
        self.y = y # Coordenada Y do botão.
        self.width = width # Largura do botão.
        self.height = height # Altura do botão.
        self.text = text # Texto do botão.

    def draw(self, window): # Função que desenha o botão.

        pygame.draw.rect(window, (25, 79, 41),
                         (round(self.x - 3), round(self.y - 3), round(self.width + 6), round(self.height + 6)), 0)
        pygame.draw.rect(window, self.color, (round(self.x), round(self.y), round(self.width), round(self.height)), 0)
        font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 20)
        buttonText = font.render(self.text, False, (255, 255, 255))
        blitX = int(self.x + (self.width / 2 - buttonText.get_width() / 2))
        blitY = int(self.y + (self.height / 2 - buttonText.get_height() / 2))
        window.blit(buttonText, (blitX, blitY))

    def hover(self, pos): # Verifica se a posição da seta do mouse está em cima do botão ("true" se sim e "false" se não).

        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

def redraw(window, snake, snack, score): # Função para redesenhar a janela (e os demais componentes) de jogo após cada movimento.

    window.fill((47, 48, 47))  # Preenche o fundo com a cor cinza.
    font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 20)  # Fonte usada no display da pontuação.
    scoreText = font.render(str(score), True, (255, 255, 255))  # Renderiza o texto da pontuação.
    if score > 99:
        window.blit(scoreText, [535, 10])
    elif score > 9:
        window.blit(scoreText, [550, 10])
    else:
        window.blit(scoreText, [565, 10])

    snake.draw(window)  # Chama a função "draw" da cobra.
    drawSnack(window, snack, snack.color)  # Desenha a comida.
    pygame.display.update()

def goodSnackPos(snake, pX, pY): # Verifica se as coordenadas geradas para a comida não estão no mesmo local que a cobra.

    for index, square in enumerate(snake.body):
        if square.posX == pX and square.posY == pY:
            return False

    return True

def newSnack(): # Gera aleatoriamente novas coordenadas para a comida aparecer.

    posX = random.randint(1, 28)  # Gera um número para X, sem incluir as bordas.
    posY = random.randint(1, 28)  # Gera um número para Y, sem incluir as bordas.
    posX = posX * 20  # Multiplica X pela largura do quadrado que compõem a cobra.
    posY = posY * 20  # Multiplica Y pela largura do quadrado que compõem a cobra.

    return [posX, posY]

def drawSnack(window, snack, snackColor): # Desenha a comida na tela.

    pygame.draw.rect(window, snackColor, (snack.posX, snack.posY, 20, 20))

def snakeHit(snake): # Função que verifica se a cabeça da cobra bateu em seu corpo.

    for index, square in enumerate(snake.body):
        if index == 0:
            continue
        elif snake.head.posX == square.posX and snake.head.posY == square.posY:
            return True

    return False

def helpWindow(window): # Exibe uma nova tela que contém os controles, instruções e objetivo para os jogadores verem.

    run = True
    font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 18)  # Fonte usada para exibir a pontuação.
    controls = font.render("Use \"WASD\" para mover a cobra!", True, (255, 255, 255))
    controls2 = font.render("Ou utilize as setas!", True, (255, 255, 255))
    objective = font.render("Coma a comida para cobra crescer!", True, (255, 255, 255))
    objective2 = font.render("Mas nao coma a si mesmo!", True, (255, 255, 255))
    back = Button(150, 400, 300, 75, "Voltar")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    run = False

        mousePos = pygame.mouse.get_pos()
        window.fill((47, 48, 47))  # Preenche o fundo com uma cor cinza.
        window.blit(controls, (60, 150))
        window.blit(controls2, (150, 190))
        window.blit(objective, (30, 270))
        window.blit(objective2, (120, 310))
        back.draw(window)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)

        pygame.display.update()

    mainMenu()


def highScoreWin(window): # Tela onde é exibida as melhores pontuações do jogador.

    run = True
    back = Button(150, 462, 300, 75, "Voltar")
    resetEasy = Button(400, 200, 40, 40, "")  # Botão para resetar o modo fácil.
    resetNormal = Button(400, 275, 40, 40, "")  # Botão para resetar o modo normal.
    resetHard = Button(400, 350, 40, 40, "")  # Botão para resetar o modo difícil.
    titleFont = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 36)
    font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 24)
    resetFont = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 14)
    HSTitle = titleFont.render("High Score:", True, (255, 255, 255))
    resetText = resetFont.render("Reset", True, (255, 255, 255))
    resetIcon = pygame.image.load("Arquivos do jogo/icone_reset.png")
    resetIcon = pygame.transform.scale(resetIcon, (35, 35))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    run = False
                elif resetEasy.hover(mousePos):
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt")
                    lines = file.readlines()
                    lines[0] = "0\n"
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt", "w")
                    file.writelines(lines)
                    file.close()
                elif resetNormal.hover(mousePos):
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt")
                    lines = file.readlines()
                    lines[1] = "0\n"
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt", "w")
                    file.writelines(lines)
                    file.close()
                elif resetHard.hover(mousePos):
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt")
                    lines = file.readlines()
                    lines[2] = "0"
                    file = open("Arquivos do jogo/Maiores pontuacoes.txt", "w")
                    file.writelines(lines)
                    file.close()

        window.fill((47, 48, 47))
        HSFile = open("Arquivos do jogo/Maiores pontuacoes.txt")
        lines = HSFile.readlines()
        HSFile.close()
        easy = font.render("Easy: " + lines[0].strip(), True, (255, 255, 255))
        normal = font.render("Normal: " + lines[1].strip(), True, (255, 255, 255))
        hard = font.render("Hard: " + lines[2].strip(), True, (255, 255, 255))
        mousePos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        back.draw(window)
        resetEasy.draw(window)
        resetNormal.draw(window)
        resetHard.draw(window)
        window.blit(HSTitle, (100, 75))
        window.blit(easy, (130, 200))
        window.blit(normal, (130, 275))
        window.blit(hard, (130, 350))
        window.blit(resetText, (385, 165))
        window.blit(resetIcon, (402, 202))
        window.blit(resetIcon, (402, 277))
        window.blit(resetIcon, (402, 352))

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            elif resetEasy.hover(mousePos):
                resetEasy.color = (124, 230, 124)
            elif resetNormal.hover(mousePos):
                resetNormal.color = (124, 230, 124)
            elif resetHard.hover(mousePos):
                resetHard.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)
                resetEasy.color = (107, 199, 107)
                resetNormal.color = (107, 199, 107)
                resetHard.color = (107, 199, 107)

        pygame.display.update()

    mainMenu()

def mainMenu():

    pygame.init()  # Inicializa o Pygame.
    window = pygame.display.set_mode((600, 600))  # Cria a tela inicial.
    pygame.display.set_caption("Snake — Feito por Mateus, Letícia, João e Diego")  # Mostra os autores do game.
    icon = pygame.image.load("Arquivos do jogo\icone.png")
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
    easy = Button(200, 250, 200, 75, "Easy")
    normal = Button(200, 362.5, 200, 75, "Normal")
    hard = Button(200, 475, 200, 75, "Hard")
    helpButton = Button(540, 20, 40, 40, "")
    hsButton = Button(485, 20, 40, 40, "")
    helpCalled = False
    hsCalled = False

    # Lê as maiores pontuações.
    HSFile = open("Arquivos do jogo/Maiores pontuacoes.txt", "r+")
    HSFileLines = HSFile.readlines()
    highScores = []

    for i in range(0, 3):
        highScores.append(HSFileLines[i])

    HSFile.close()

    run = True

    while run: # Se o jogador pressionar a tecla de sair (X), então o jogo é fechado.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.hover(mousePos):
                    diff = 125
                    high = highScores[0]
                    run = False
                elif normal.hover(mousePos):
                    diff = 100
                    high = highScores[1]
                    run = False
                elif hard.hover(mousePos):
                    diff = 75
                    high = highScores[2]
                    run = False
                elif helpButton.hover(mousePos):
                    helpCalled = True
                    run = False
                elif hsButton.hover(mousePos):
                    hsCalled = True
                    run = False

        window.fill((47, 48, 47))  # Preenche o fundo com uma cor cinza.
        font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 60)  # Fonte usada na tela de pontuação.
        font2 = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 16)  # Fonte usada na tela de pontuação.
        titleText = font.render("Snake", True, (255, 255, 255))  # Renderiza o texto da pontuação.
        author = font2.render("by  M. L. J. D.", False, (255, 255, 255))
        window.blit(titleText, (110, 80)) 
        window.blit(author, (275, 180))
        easy.draw(window)
        normal.draw(window)
        hard.draw(window)
        helpButton.draw(window)
        hsButton.draw(window)
        qMark = pygame.image.load("Arquivos do jogo/icone de interrogacao.png")
        qMark = pygame.transform.scale(qMark, (32, 32))
        trophy = pygame.image.load("Arquivos do jogo/icone de trofeu.png")
        trophy = pygame.transform.scale(trophy, (35, 35))
        window.blit(qMark, (543, 23))
        window.blit(trophy, (487, 22))
        mousePos = pygame.mouse.get_pos()

        if pygame.MOUSEMOTION:
            if easy.hover(mousePos):
                easy.color = (124, 230, 124)
            elif normal.hover(mousePos):
                normal.color = (124, 230, 124)
            elif hard.hover(mousePos):
                hard.color = (124, 230, 124)
            elif helpButton.hover(mousePos):
                helpButton.color = (124, 230, 124)
            elif hsButton.hover(mousePos):
                hsButton.color = (124, 230, 124)
            else:
                easy.color = (107, 199, 107)
                normal.color = (107, 199, 107)
                hard.color = (107, 199, 107)
                helpButton.color = (107, 199, 107)
                hsButton.color = (107, 199, 107)

        pygame.display.update()

    if helpCalled:
        helpWindow(window)
    elif hsCalled:
        highScoreWin(window)
    else:
        main(window, diff, high)


def main(window, diff, high): # Loop principal do jogo.

    snake = Snake()  # Cria a cobra.
    snackColor = (111, 201, 129)  # Define a cor da cobra (verde).
    snackPos = newSnack()  # Gera coordenadas possíveis para a comida aparecer.

    while not goodSnackPos(snake, snackPos[0], snackPos[1]): # Verifica se a comida tem as mesmas coordenadas da cobra, e gera uma nova comida em caso positivo.
        snackPos = newSnack()

    snack = Square(snackPos[0], snackPos[1], snackColor)  # Cria a comida.

    score = 0
    velX = 20  # Velocidade inicial de X.
    velY = 0  # Velocidade inicial de Y.
    run = True
    redraw(window, snake, snack, score)

    while run: # Loop principal.
        pygame.time.delay(diff)  # Atraso entre os loops deixa o jogo mais lento.

        for event in pygame.event.get(): # Se o jogador pressionar a tecla "X", então o jogo fecha.
            if event.type == pygame.QUIT:
                pygame.quit()

        velX, velY, secondSquare = snake.move(velX, velY)  # Invoca a função de movimento da cobra.

        if secondSquare or snakeHit(snake):  # Verifica se a cobra colidiu com si mesma.
            mixer.music.load("Arquivos do jogo/Som quando morre.wav")  # Efeito de sonoro de quando a cobra bate em si mesma.
            mixer.music.play()
            run = False

        if snake.head.posX == snack.posX and snake.head.posY == snack.posY:  # Se a cabeça da cobra colidir com a comida.
            snake.addSquare()  # Adiciona um quadrado à cobra (aumenta seu corpo).
            score += 1  # Adiciona 1 para a pontuação.
            snackPos = newSnack()  # Cria coordenadas para uma nova comida.

            while not goodSnackPos(snake, snackPos[0], snackPos[1]): # Verifica se as coordenadas não são as da cobra.
                snackPos = newSnack()

            snack = Square(snackPos[0], snackPos[1], snackColor)  # Adiciona uma comida na tela.

        redraw(window, snake, snack, score)  # Redesenha a tela.

    gameOver(window, score, diff, high)


def gameOver(window, score, diff, high):
    high = int(high)
    newHS = False
    run = True
    menu = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.hover(mousePos):
                    menu = True
                    run = False

        if score > high:
            newHS = True
            high = score  # Defini a nova pontuação como a mais alta.
            HSFile = open("Arquivos do jogo/Maiores pontuacoes.txt", "r")
            lines = HSFile.readlines()

            if diff == 125:
                lines[0] = str(score) + "\n"
            elif diff == 100:
                lines[1] = str(score) + "\n"
            elif diff == 75:
                lines[2] = str(score) 

            HSFile = open("Arquivos do jogo/Maiores pontuacoes.txt", "w")
            HSFile.writelines(lines)
            HSFile.close()

        window.fill((47, 48, 47))  # Preenche o fundo com uma cor cinza.
        mousePos = pygame.mouse.get_pos()
        font = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 40)  # Fonte usada na tela de pontuação.
        font2 = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 21)  # Fonte usada na tela de pontuação.
        font3 = pygame.font.Font("Arquivos do jogo/Modelo de fonte - 8 bit.ttf", 18)  # Fonte usada na tela de pontuação.
        gameOverText = font.render("Game Over", True, (255, 255, 255))  # Renderiza o texto da pontuação.
        scoreText = font2.render("Score: " + str(score), True, (255, 255, 255))
        back = Button(20, 20, 40, 40, "")
        back.draw(window)
        arrow = pygame.image.load("Arquivos do jogo/icone de seta.png")
        arrow = pygame.transform.scale(arrow, (25, 25))
        window.blit(arrow, (26, 27))
        keys = pygame.key.get_pressed()
        HSFile = open("Arquivos do jogo/Maiores pontuacoes.txt")
        lines = HSFile.readlines()

        if diff == 125:
            highScoreNum = lines[0].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))
        elif diff == 100:
            highScoreNum = lines[1].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))
        elif diff == 75:
            highScoreNum = lines[2].strip()
            highScoreText = font2.render("High Score: " + highScoreNum, True, (255, 255, 255))

        restart = font3.render("Press \"SPACE\" to play again", True, (255, 255, 255))
        window.blit(gameOverText, [120, 240])
        window.blit(restart, [75, 500])

        # Exibe a pontuação na tela.
        if score > 99:
            window.blit(scoreText, [205, 310])
        elif score > 9:
            window.blit(scoreText, [215, 310])
        else:
            window.blit(scoreText, [225, 310])

        # Exibe a maior pontuação na tela.
        if int(highScoreNum) > 99:
            window.blit(highScoreText, [150, 350])
        elif int(highScoreNum) > 9:
            window.blit(highScoreText, [160, 350])
        else:
            window.blit(highScoreText, [170, 350])

        if newHS:
            newHSText = font2.render("New High Score!", True, (255, 255, 255))
            window.blit(newHSText, [150, 100])

        if keys[pygame.K_SPACE]:
            run = False

        if pygame.MOUSEMOTION:
            if back.hover(mousePos):
                back.color = (124, 230, 124)
            else:
                back.color = (107, 199, 107)

        pygame.display.update()

    if menu:
        mainMenu()
    else:
        main(window, diff, high)

mainMenu()