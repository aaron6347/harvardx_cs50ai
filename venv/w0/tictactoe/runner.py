import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:
    # search event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # fill the screen with black colour
    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        # get rectangle
        titleRect = title.get_rect()
        # position the rectangle at center
        titleRect.center = ((width / 2), 50)
        # put title and rectangle on screen
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        # font play as X
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        # attach rectangle to the button
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        # put play as X and rectangle button on screen
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        # font play as O
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        # attach rectangle to the button
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        # put play as O and rectangle button on screen
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            # if player choose play as X, set user as X
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            # if player choose play as O, set user as O
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        # each loop find out the terminal of the game, check if the game is over or not
        game_over = ttt.terminal(board)
        # each loop find out who is the player that has to make a move
        player = ttt.player(board)

        # Show title
        # if game over is true based on terminal
        if game_over:
            winner = ttt.winner(board)
            # if no winner
            if winner is None:
                title = f"Game Over: Tie."
            # else display player X/O
            else:
                title = f"Game Over: {winner} wins."
        # else if game over is false and current player to make move is user
        elif user == player:
            title = f"Play as {user}"
        # else game over is false and current player to make move is computer
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            # if current player to make move is computer, do minimax analysis and make the action on the board
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            # else current player to make move is not computer, set this as true for computer as next player to make move
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            # get position of mouse
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        # action of player onto the board
                        board = ttt.result(board, (i, j))

        # if game over is true
        if game_over:
            # make play again button
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            # display play again button
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                # if the play again button get clicked then restart the game
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
