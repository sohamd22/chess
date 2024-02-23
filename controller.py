import pygame, sys
from chessBoard import ChessBoard

SIZE = 8

chessBoard = ChessBoard()

pygame.init()
TILE_SIZE = 80
WIDTH, HEIGHT = TILE_SIZE * 8, TILE_SIZE * 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))

LIGHT_GREEN = (233, 236, 209)
DARK_GREEN = (127, 153, 92)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (243,246,145)
LIME = (191,205,93)
font = pygame.font.Font("OpenSans-Regular.ttf", 60)

selection = None

game_over = ""

curr_player = 1

while True:    
    if(not(game_over)):
        game_over = chessBoard.terminal()
        if(game_over):
            winner = chessBoard.winner()
            if(winner):
                game_over = "Black Wins" if winner == -1 else "White Wins"
            else:
                game_over = "Draw"
                
        tiles = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                rect = pygame.Rect(j * TILE_SIZE, (SIZE - 1 - i) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if((i, (SIZE - 1 - j)) == selection):
                    pygame.draw.rect(screen, YELLOW if (i + j) % 2 else LIME, rect)
                else:
                    pygame.draw.rect(screen, LIGHT_GREEN if (i + j) % 2 else DARK_GREEN, rect)
                row.append(rect)

                if chessBoard.board[i][SIZE - 1 - j] != None:
                    piece_image = pygame.transform.scale(pygame.image.load(f"./images/{chessBoard.board[i][SIZE - 1 - j].notation + str(chessBoard.board[i][SIZE - 1 - j].color)}.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))
                    screen.blit(piece_image, (j * TILE_SIZE, (SIZE - 1 - i) * TILE_SIZE))
            tiles.append(row)

        pygame.display.flip()

        if(chessBoard.player == -curr_player and not(game_over)):
            move = chessBoard.minimax()
            chessBoard = chessBoard.result(move[0], move[1])

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and chessBoard.player == curr_player:
                mouse = pygame.mouse.get_pos()
                if(not(selection)):
                    selection = ((SIZE - 1 - mouse[1] // TILE_SIZE), (SIZE - 1 - mouse[0] // TILE_SIZE))
                    if(min(selection) < 0 or max(selection) >= SIZE):
                        selection = None
                else:
                    placement = ((SIZE - 1 - mouse[1] // TILE_SIZE), (SIZE - 1 - mouse[0] // TILE_SIZE))
                    result_board = chessBoard.result(selection, placement)
                    if(result_board):
                        chessBoard = result_board
                    selection = None   
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        text = font.render(game_over, True, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, text_rect)

    pygame.display.flip()