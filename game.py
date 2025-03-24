import pygame
import sys

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        self.player_turn = True
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.font = pygame.font.Font(None, 36)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for i in range(1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 100, 0), (i * 100, 300), 2)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 100), (300, i * 100), 2)
        for i in range(3):
            for j in range(3):
                text = self.font.render(self.board[i][j], True, (0, 0, 0))
                self.screen.blit(text, (j * 100 + 40, i * 100 + 30))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.player_turn:
                x, y = pygame.mouse.get_pos()
                row = y // 100
                col = x // 100
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'X'
                    if not self.check_winner(self.board) and not self.is_draw():
                        self.player_turn = False
                        self.computer_turn()
                        self.player_turn = True

    def computer_turn(self):
        best_move, _ = self.minimax(self.board, 0, -float('inf'), float('inf'), True)
        if best_move:
            self.board[best_move[0]][best_move[1]] = 'O'

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        winner = self.check_winner(board)
        if winner:
            if winner == 'X':
                return None, -10 + depth
            elif winner == 'O':
                return None, 10 - depth
        if self.is_draw(board):
            return None, 0

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        _, score = self.minimax(board, depth + 1, alpha, beta, False)
                        board[i][j] = ' '
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_move, best_score
        else:
            best_score = float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        _, score = self.minimax(board, depth + 1, alpha, beta, True)
                        board[i][j] = ' '
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_move, best_score

    def check_winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        return None

    def is_draw(self, board=None):
        if board is None:
            board = self.board
        for row in board:
            if ' ' in row:
                return False
        return self.check_winner(board) is None

    def run(self):
        while True:
            self.draw_board()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
