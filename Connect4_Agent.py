import numpy as np
import time

class AIAgent(object):
    def __init__(self, player_id=1):
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.row_count = 6
        self.column_count = 7
        self.time_limit = 0.95
        self.start_time = None
        self.transposition_table = {}
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        self.win_score = 1000000
        self.lose_score = -1000000

    def make_move(self, state):
        self.start_time = time.time()
        self.transposition_table.clear()
        
        best_move = self.iterative_deepening(state)
        return best_move

    def iterative_deepening(self, state):
        best_move = self.get_valid_locations(state)[0]
        depth = 1
        while True:
            if time.time() - self.start_time > self.time_limit:
                break
            move = self.alpha_beta_search(state, depth)
            if time.time() - self.start_time > self.time_limit:
                break
            if move is not None:
                best_move = move
            depth += 1
        return best_move

    def alpha_beta_search(self, state, depth):
        alpha = float('-inf')
        beta = float('inf')
        best_score = float('-inf')
        best_move = None

        for move in self.order_moves(state):
            new_state = self.apply_move(state, move, self.player_id)
            score = self.min_value(new_state, depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
            if time.time() - self.start_time > self.time_limit:
                break

        return best_move

    def min_value(self, state, depth, alpha, beta):
        if self.is_terminal(state) or depth == 0 or time.time() - self.start_time > self.time_limit:
            return self.evaluate(state)

        value = float('inf')
        for move in self.order_moves(state):
            new_state = self.apply_move(state, move, self.opponent_id)
            value = min(value, self.max_value(new_state, depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(self, state, depth, alpha, beta):
        if self.is_terminal(state) or depth == 0 or time.time() - self.start_time > self.time_limit:
            return self.evaluate(state)

        value = float('-inf')
        for move in self.order_moves(state):
            new_state = self.apply_move(state, move, self.player_id)
            value = max(value, self.min_value(new_state, depth - 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def is_terminal(self, state):
        return self.check_winner(state, self.player_id) or self.check_winner(state, self.opponent_id) or len(self.get_valid_locations(state)) == 0

    def evaluate(self, state):
        if self.check_winner(state, self.player_id):
            return self.win_score
        elif self.check_winner(state, self.opponent_id):
            return self.lose_score
        else:
            return self.heuristic(state)

    def heuristic(self, state):
        score = 0
        
        center_array = [int(i) for i in list(state[:, self.column_count//2])]
        center_count = center_array.count(self.player_id)
        score += center_count * 3
        
        for r in range(self.row_count):
            for c in range(self.column_count):
                if c + 3 < self.column_count:
                    window = list(state[r, c:c+4])
                    score += self.evaluate_window(window)
                
                if r + 3 < self.row_count:
                    window = list(state[r:r+4, c])
                    score += self.evaluate_window(window)
                
                if r + 3 < self.row_count and c + 3 < self.column_count:
                    window = [state[r+i][c+i] for i in range(4)]
                    score += self.evaluate_window(window)
                
                if r + 3 < self.row_count and c - 3 >= 0:
                    window = [state[r+i][c-i] for i in range(4)]
                    score += self.evaluate_window(window)
        
        return score

    def evaluate_window(self, window):
        score = 0
        player_count = window.count(self.player_id)
        empty_count = window.count(0)
        opponent_count = window.count(self.opponent_id)

        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 5
        elif player_count == 2 and empty_count == 2:
            score += 2

        if opponent_count == 3 and empty_count == 1:
            score -= 4

        return score

    def order_moves(self, state):
        valid_locations = self.get_valid_locations(state)
        return sorted(valid_locations, key=lambda x: self.move_order.index(x))

    def get_valid_locations(self, state):
        return [col for col in range(self.column_count) if state[0][col] == 0]

    def apply_move(self, state, col, player):
        new_state = state.copy()
        for row in range(self.row_count-1, -1, -1):
            if new_state[row][col] == 0:
                new_state[row][col] = player
                break
        return new_state

    def check_winner(self, state, player):
        for c in range(self.column_count-3):
            for r in range(self.row_count):
                if state[r][c] == player and state[r][c+1] == player and state[r][c+2] == player and state[r][c+3] == player:
                    return True
        for c in range(self.column_count):
            for r in range(self.row_count-3):
                if state[r][c] == player and state[r+1][c] == player and state[r+2][c] == player and state[r+3][c] == player:
                    return True
        for c in range(self.column_count-3):
            for r in range(self.row_count-3):
                if state[r][c] == player and state[r+1][c+1] == player and state[r+2][c+2] == player and state[r+3][c+3] == player:
                    return True
        for c in range(self.column_count-3):
            for r in range(3, self.row_count):
                if state[r][c] == player and state[r-1][c+1] == player and state[r-2][c+2] == player and state[r-3][c+3] == player:
                    return True

        return False