import pygame
pygame.init()
#screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Chess Showdown')
#fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)
#FPS and clock
FPS = 30
clock = pygame.time.Clock()
#game state variables
player_turn = 0
selected_piece_index = None
possible_moves = []
captured_white_pieces = []
captured_black_pieces = []
game_ended = False
game_winner = ''
#piece setup
piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
white_pieces = [
    'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
black_pieces = [
    'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
white_positions = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)
]
black_positions = [
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)
]
#load and scale images
piece_images = {
    'white': {
        'pawn': pygame.transform.scale(pygame.image.load('white pawn.png'), (64, 64)),
        'rook': pygame.transform.scale(pygame.image.load('white rook.png'), (64, 64)),
        'knight': pygame.transform.scale(pygame.image.load('white knight.png'), (64, 64)),
        'bishop': pygame.transform.scale(pygame.image.load('white bishop.png'), (64, 64)),
        'queen': pygame.transform.scale(pygame.image.load('white queen.png'), (64, 64)),
        'king': pygame.transform.scale(pygame.image.load('white king.png'), (64, 64)),
    },
    'black': {
        'pawn': pygame.transform.scale(pygame.image.load('black pawn.png'), (64, 64)),
        'rook': pygame.transform.scale(pygame.image.load('black rook.png'), (64, 64)),
        'knight': pygame.transform.scale(pygame.image.load('black knight.png'), (64, 64)),
        'bishop': pygame.transform.scale(pygame.image.load('black bishop.png'), (64, 64)),
        'queen': pygame.transform.scale(pygame.image.load('black queen.png'), (64, 64)),
        'king': pygame.transform.scale(pygame.image.load('black king.png'), (64, 64)),
    }
}
def draw_board():
    colors = [(255, 255, 255), (0, 0, 0)]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * 100, row * 100, 100, 100))
def draw_pieces():
    for index, pos in enumerate(white_positions):
        piece = white_pieces[index]
        image = piece_images['white'][piece]
        screen.blit(image, (pos[0] * 100, pos[1] * 100))
    for index, pos in enumerate(black_positions):
        piece = black_pieces[index]
        image = piece_images['black'][piece]
        screen.blit(image, (pos[0] * 100, pos[1] * 100))
def draw_valid_moves(moves):
    for move in moves:
        pygame.draw.circle(screen, (0, 255, 0), (move[0] * 100 + 50, move[1] * 100 + 50), 15)
def check_moves(piece, pos, color):
    moves = []
    if piece == 'pawn':
        moves = check_pawn_moves(pos, color)
    elif piece == 'rook':
        moves = check_rook_moves(pos, color)
    elif piece == 'knight':
        moves = check_knight_moves(pos, color)
    elif piece == 'bishop':
        moves = check_bishop_moves(pos, color)
    elif piece == 'queen':
        moves = check_queen_moves(pos, color)
    elif piece == 'king':
        moves = check_king_moves(pos, color)
    return moves
def check_pawn_moves(pos, color):
    moves = []
    direction = 1 if color == 'white' else -1
    start_row = 1 if color == 'white' else 6
    one_step = (pos[0], pos[1] + direction)
    two_steps = (pos[0], pos[1] + 2 * direction)
    if 0 <= one_step[1] < 8 and one_step not in white_positions and one_step not in black_positions:
        moves.append(one_step)
    if pos[1] == start_row and 0 <= two_steps[1] < 8 and two_steps not in white_positions and two_steps not in black_positions:
        moves.append(two_steps)
    return moves
def check_rook_moves(pos, color):
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for direction in directions:
        for i in range(1, 8):
            target = (pos[0] + i * direction[0], pos[1] + i * direction[1])
            if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                if target in white_positions if color == 'white' else black_positions:
                    break
                moves.append(target)
                if target in black_positions if color == 'white' else white_positions:
                    break
            else:
                break
    return moves
def check_knight_moves(pos, color):
    moves = []
    offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for offset in offsets:
        target = (pos[0] + offset[0], pos[1] + offset[1])
        if 0 <= target[0] < 8 and 0 <= target[1] < 8:
            if target not in white_positions if color == 'white' else black_positions:
                moves.append(target)
    return moves
def check_bishop_moves(pos, color):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in directions:
        for i in range(1, 8):
            target = (pos[0] + i * direction[0], pos[1] + i * direction[1])
            if 0 <= target[0] < 8 and 0 <= target[1] < 8:
                if target in white_positions if color == 'white' else black_positions:
                    break
                moves.append(target)
                if target in black_positions if color == 'white' else white_positions:
                    break
            else:
                break
    return moves
def check_queen_moves(pos, color):
    return check_rook_moves(pos, color) + check_bishop_moves(pos, color)

def check_king_moves(pos, color):
    moves = []
    offsets = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]
    for offset in offsets:
        target = (pos[0] + offset[0], pos[1] + offset[1])
        if 0 <= target[0] < 8 and 0 <= target[1] < 8:
            if target not in white_positions if color == 'white' else black_positions:
                moves.append(target)
    return moves
def draw_winner():
    message = f'{game_winner} wins!'
    text = font_large.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_ended:
            pos = pygame.mouse.get_pos()
            col = pos[0] // 100
            row = pos[1] // 100
            clicked_pos = (col, row)
            if player_turn == 0:
                if selected_piece_index is None:
                    if clicked_pos in white_positions:
                        selected_piece_index = white_positions.index(clicked_pos)
                        selected_piece = white_pieces[selected_piece_index]
                        possible_moves = check_moves(selected_piece, clicked_pos, 'white')
                else:
                    if clicked_pos in possible_moves:
                        white_positions[selected_piece_index] = clicked_pos
                        player_turn = 1
                    selected_piece_index = None
                    possible_moves = []
            else:
                if selected_piece_index is None:
                    if clicked_pos in black_positions:
                        selected_piece_index = black_positions.index(clicked_pos)
                        selected_piece = black_pieces[selected_piece_index]
                        possible_moves = check_moves(selected_piece, clicked_pos, 'black')
                else:
                    if clicked_pos in possible_moves:
                        black_positions[selected_piece_index] = clicked_pos
                        player_turn = 0
                    selected_piece_index = None
                    possible_moves = []
    screen.fill((0, 0, 0))
    draw_board()
    draw_pieces()
    draw_valid_moves(possible_moves)
    if game_ended:
        draw_winner()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()