import math
import copy
import time

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board_state = self.create_initial_board_state()
        self.selected_cell = None
        self.player = 1

    def create_initial_board_state(self):
        """
        Cria o estado inicial do tabuleiro do jogo.

        Returns:
            list: O estado inicial do tabuleiro do jogo.
        """
        state = [[0 for _ in range(self.board_size + i)] for i in range(self.board_size)] + \
                [[0 for _ in range(self.board_size * 2 - 2 - i)] for i in range(self.board_size - 1)]

        for row in range(self.board_size * 2 - 1):
            if row != self.board_size - 1:
                state[row][0] = 1
                state[row][-1] = 2
            else:
                state[row][0] = 22
                state[row][1] = 1
                state[row][-2] = 2
                state[row][-1] = 11
        return state

    def update_selected_cell(self, cell):
        """
        Atualiza a célula selecionada no tabuleiro pelo jogador.

        Args:
            cell (tuple): A célula selecionada pelo jogador.
        """
        self.selected_cell = cell
    
    def update_player(self):
        """
        Atualiza o jogador ativo.
        """
        self.player = 3 - self.player
        
    
    def piece_playable(self, board_state, position, player):
        """
        Verifica se uma peça pode ser jogada.

        Args:
            board_state (list): O estado atual do tabuleiro.
            position (tuple): A posição da peça a ser verificada.
            player (int): O jogador que está tentando jogar a peça.

        Returns:
            bool: True se a peça for jogável, False caso contrário.
        """
        row,col = position
        opponent = 3 - player
        
        if row < self.board_size-1:
            if row == 0:
                if col == 0:
                    if (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True
                    
                elif col == len(board_state[row])-1:
                    if (board_state[row][col-1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True

                else:
                    if (board_state[row][col-1] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True
            
            else:
                if col == 0:
                    if (board_state[row-1][col] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True
                    
                elif col == len(board_state[row])-1:
                    if (board_state[row-1][col-1] != opponent) and (board_state[row][col-1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True
                    
                else:
                    if (board_state[row-1][col-1] != opponent) and (board_state[row-1][col] != opponent) and (board_state[row][col-1] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col+1] != opponent):
                        return True
                
                
                  
        elif row == self.board_size-1:
            if (board_state[row-1][col-1] != opponent) and (board_state[row-1][col] != opponent) and (board_state[row][col-1] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col-1] != opponent):
                return True
            
            
        else: 
            if row == len(board_state)-1:
                if col == 0:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row][col+1] != opponent):
                        return True
                    
                elif col == len(board_state[row])-1:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row][col-1] != opponent):
                        return True

                else:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row][col-1] != opponent) and (board_state[row][col+1] != opponent):
                        return True
            
            else:
                if col == 0:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row-1][col] != opponent):
                        return True
                    
                elif col == len(board_state[row])-1:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row+1][col-1] != opponent) and (board_state[row][col-1] != opponent):
                        return True
                    
                else:
                    if (board_state[row-1][col] != opponent) and (board_state[row-1][col+1] != opponent) and (board_state[row][col+1] != opponent) and (board_state[row+1][col] != opponent) and (board_state[row+1][col-1] != opponent) and (board_state[row][col-1] != opponent):
                        return True
            
        return False

    
    
    def find_pieces_playable(self, board_state, player):
        """
        Encontra as peças jogáveis para um determinado jogador no estado atual do tabuleiro.

        Args:
            board_state (list): O estado atual do tabuleiro.
            player (int): O jogador para o qual as peças jogáveis devem ser encontradas.

        Returns:
            list: Uma lista contendo as coordenadas das peças jogáveis.
        """
        pieces = []
        for row in range(len(board_state)):
            for col in range(len(board_state[row])):
                if board_state[row][col] == player and self.piece_playable(self.board_state, [row, col], player):
                    pieces.append([row,col]) 
        return pieces


    def valid_move(self, player, board_state, current_pos):
        """
        Verifica os movimentos válidos para uma peça em uma posição atual.

        Args:
            player (int): O jogador atual.
            board_state (list): O estado atual do tabuleiro.
            current_pos (list): As coordenadas da posição atual.

        Returns:
            list: Lista dos movimentos válidos.
        """
        # Na matriz os valid moves são para cima esquerda (ce), para cima (c), para a esquerda (e),
        # para a direita (d), para baixo (b) e para baixo direita (bd)
        valid_moves = []
        row, col = current_pos
        
        
        # Peça na parte de cima do tabuleiro
        if row < self.board_size-1:
            # Verifica se a celula de cima esquerda existe ... A peça não pode estar nem na primeira fila nem na primeira coluna
            if row != 0 and col != 0:
                if board_state[row-1][col-1] == 0:
                    valid_moves.append([row-1,col-1])
                elif board_state[row-1][col-1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col-1], "ce")
                
            # Verifica se a celula de cima existe ... A peça não pode estar na peimeira fila nem na ultima coluna se estiver na metade de cima do tabuleiro 
            if (row != 0) and (col != len(board_state[row])-1):
                if board_state[row-1][col] == 0:
                    valid_moves.append([row-1,col])
                elif board_state[row-1][col] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col], "c")
                        
            # Verifica se a celula da esquerda existe ... A peça não pode estar na primeira coluna
            if col != 0: 
                if board_state[row][col-1] == 0:
                    valid_moves.append([row,col-1])
                elif board_state[row][col-1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row,col-1], "e")
                    
            # Verifica se a celula da direta existe ... A peça não pode estar na última coluna
            if col != len(board_state[row])-1:
                if board_state[row][col+1] == 0:
                    valid_moves.append([row,col+1])
                elif board_state[row][col+1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row,col+1], "d")        
            
            # Existe sempre a celula de baixo
            if (board_state[row+1][col] == 22) and (player == 2):
                valid_moves.insert(0, [row+1,col])
            elif board_state[row+1][col] == 0:
                valid_moves.append([row+1,col])
            elif board_state[row+1][col] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col], "b")
            
            # Existe sempre a celula de baixo direita
            if ((board_state[row+1][col+1] == 11) and (player == 1)):
                valid_moves.insert(0, [row+1,col+1])
            elif board_state[row+1][col+1] == 0:
                valid_moves.append([row+1,col+1])
            elif board_state[row+1][col+1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col+1], "bd")
                  
                  
                                     
        # Peça na fila do meio
        elif row == self.board_size-1:
            # Existe sempre a celula de cima esquerda
            if board_state[row-1][col-1] == 0:
                valid_moves.append([row-1,col-1])
            elif board_state[row-1][col-1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col-1], "ce")
            
            # Existe sempre a celula de cima
            if board_state[row-1][col] == 0:
                valid_moves.append([row-1,col])
            elif board_state[row-1][col] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col], "c")
            
            # Existe sempre a celula da esquerda
            if ((board_state[row][col-1] == 22) and (player == 2)):
                valid_moves.insert(0, [row,col-1])
            elif board_state[row][col-1] == 0:
                valid_moves.append([row,col-1])
            elif board_state[row][col-1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row,col-1], "e")
                
            # Existe sempre a celula de baixo esquerda
            if board_state[row+1][col-1] == 0:
                valid_moves.append([row+1,col-1])
            elif board_state[row+1][col-1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col-1], "be")
            
            # Existe sempre a celula de baixo
            if board_state[row+1][col] == 0:
                valid_moves.append([row+1,col])
            elif board_state[row+1][col] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col], "b")
                
            # Existe sempre a celula da direita
            if ((board_state[row][col+1] == 11) and (player == 1)):
                valid_moves.insert(0, [row,col+1])
            elif board_state[row][col+1] == 0:
                valid_moves.append([row,col+1])
            elif board_state[row][col+1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row,col+1], "d")
            
        
        # Peça na parte de baixo do tabuleiro
        else:
            # Existe sempre a celula de cima
            if (board_state[row-1][col] == 22) and (player == 2):
                valid_moves.insert(0, [row-1,col])
            elif board_state[row-1][col] == 0:
                valid_moves.append([row-1,col])
            elif board_state[row-1][col] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col], "c")

            # Verifica se a celula da esquerda existe ... A peça não pode estar na primeira coluna
            if col != 0: 
                if board_state[row][col-1] == 0:
                    valid_moves.append([row,col-1])
                elif board_state[row][col-1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row,col-1], "e")
            
            # Verifica se a celula da direta existe ... A peça não pode estar na última coluna
            if col != len(board_state[row])-1:
                if board_state[row][col+1] == 0:
                    valid_moves.append([row,col+1])
                elif board_state[row][col+1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row,col+1], "d")
                    
            # Verifica se a celula de baixo existe ... A peça não pode estar na última fila nem na última coluna
            if row != len(board_state)-1 and col != len(board_state[row])-1:
                if board_state[row+1][col] == 0:
                    valid_moves.append([row+1,col])
                elif board_state[row+1][col] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col], "b")
                    
            # Existe sempre a celula de cima direita
            if ((board_state[row-1][col+1] == 11) and (player == 1)):
                valid_moves.insert(0, [row-1,col+1])
            elif board_state[row-1][col+1] == 0:
                valid_moves.append([row-1,col+1])
            elif board_state[row-1][col+1] == player:
                valid_moves = self.check_jump(board_state, player, valid_moves, [row-1,col+1], "cd")
                
            # Verifica se a celula de baixo da esquerda existe ... A peça não pode estar na última fila nem na primeira coluna
            if row != len(board_state)-1 and col != 0:
                if board_state[row+1][col-1] == 0:
                    valid_moves.append([row+1,col-1])
                elif board_state[row+1][col-1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col-1], "be")
        
        return valid_moves
    
    
    
    def check_jump(self, board_state, player, valid_moves, spot, direction):
        """
        Verifica a possibilidade de saltos de peças em uma determinada direção.

        Args:
            board_state (list): O estado atual do tabuleiro.
            player (int): O jogador atual.
            valid_moves (list): Lista de movimentos válidos.
            spot (list): As coordenadas da posição atual.
            direction (str): A direção do salto.

        Returns:
            list: Lista de movimentos válidos atualizada.
        """
        row,col = spot
        
        ## Verificar as diferentes direções de saltos
        
        # Parte de cima do tabuleiro
        if row < self.board_size-1:
            if direction == "ce":
                # Verifica se a celula de cima esquerda existe ... A peça não pode estar nem na primeira fila nem na primeira coluna
                if row != 0 and col != 0:
                    if board_state[row-1][col-1] == 0:
                        valid_moves.append([row-1,col-1])
                    elif ((board_state[row-1][col-1] == 2) and (player == 1)) or ((board_state[row-1][col-1] == 1) and (player == 2)):
                        valid_moves.append([row-1,col-1])
                    elif board_state[row-1][col-1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row-1,col-1], "ce")
                    
            elif direction == "c":
                # Verifica se a celula de cima existe ... A peça não pode estar na peimeira fila nem na ultima coluna 
                if row != 0 and col != len(board_state[row])-1:
                    if board_state[row-1][col] == 0:
                        valid_moves.append([row-1,col])
                    elif ((board_state[row-1][col] == 2) and (player == 1)) or ((board_state[row-1][col] == 1) and (player == 2)):
                        valid_moves.append([row-1,col])
                    elif board_state[row-1][col] == player:
                        return self.check_jump(board_state, player, valid_moves, [row-1,col], "c")
                    
            elif direction == "e":
                # Verifica se a celula da esquerda existe ... A peça não pode estar na primeira coluna
                if col != 0:
                    if board_state[row][col-1] == 0:
                        valid_moves.append([row,col-1])
                    elif ((board_state[row][col-1] == 2) and (player == 1)) or ((board_state[row][col-1] == 1) and (player == 2)):
                        valid_moves.append([row,col-1])
                    elif board_state[row][col-1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row,col-1], "e")
        
            elif direction == "d":
                # Verifica se a celula da direta existe ... A peça não pode estar na última coluna
                if col != len(board_state[row]) -1:
                    if board_state[row][col+1] == 0:
                        valid_moves.append([row,col+1])
                    elif ((board_state[row][col+1] == 2) and (player == 1)) or ((board_state[row][col+1] == 1) and (player == 2)):
                        valid_moves.append([row,col+1])
                    elif board_state[row][col+1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row,col+1], "d")
        
            elif direction == "b":
                # Existe sempre a celula de baixo
                if ((board_state[row+1][col] == 22) and (player == 2)):
                    valid_moves.insert(0, [row+1,col])
                elif board_state[row+1][col] == 0:
                    valid_moves.append([row+1,col])
                elif ((board_state[row+1][col] == 2) and (player == 1)) or ((board_state[row+1][col] == 1) and (player == 2)):
                    valid_moves.append([row+1,col])
                elif board_state[row+1][col] == player:
                    return self.check_jump(board_state, player, valid_moves, [row+1,col], "b")

            elif direction == "bd":
                # Existe sempre a celula de baixo direita
                if ((board_state[row+1][col+1] == 11) and (player == 1)):
                    valid_moves.insert(0, [row+1,col+1])
                elif board_state[row+1][col+1] == 0:
                    valid_moves.append([row+1,col+1])
                elif ((board_state[row+1][col+1] == 2) and (player == 1)) or ((board_state[row+1][col+1] == 1) and (player == 2)):
                    valid_moves.append([row+1,col+1])
                elif board_state[row+1][col+1] == player:
                    valid_moves = self.check_jump(board_state, player, valid_moves, [row+1,col+1], "bd")
                
                
        # Fila do meio    
        elif row == self.board_size-1:
            
            if direction == "c":
                if board_state[row-1][col-1] == 0:
                    valid_moves.append([row-1,col-1])
                elif ((board_state[row-1][col-1] == 2) and (player == 1)) or ((board_state[row-1][col-1] == 1) and (player == 2)):
                    valid_moves.append([row-1,col-1])
                elif board_state[row-1][col-1] == player:
                    return self.check_jump(board_state, player, valid_moves, [row-1,col-1], "ce")
                
            elif direction == "cd":
                if board_state[row-1][col] == 0:
                    valid_moves.append([row-1,col])
                elif ((board_state[row-1][col] == 2) and (player == 1)) or ((board_state[row-1][col] == 1) and (player == 2)):
                    valid_moves.append([row-1,col])
                elif board_state[row-1][col] == player:
                    return self.check_jump(board_state, player, valid_moves, [row-1,col-1], "c")
                    
            elif direction == "e":
                if ((board_state[row][col-1] == 22) and (player == 2)):
                    valid_moves.insert(0, [row,col-1])
                elif board_state[row][col-1] == 0:
                    valid_moves.append([row,col-1])
                elif ((board_state[row][col-1] == 2) and (player == 1)) or ((board_state[row][col-1] == 1) and (player == 2)):
                    valid_moves.append([row,col-1])
                elif board_state[row][col-1] == player:
                    return self.check_jump(board_state, player, valid_moves, [row,col-1], "e")
        
            elif direction == "d":
                if ((board_state[row][col+1] == 11) and (player == 1)):
                    valid_moves.insert(0, [row,col+1])
                elif board_state[row][col+1] == 0:
                    valid_moves.append([row,col+1])
                elif ((board_state[row][col+1] == 2) and (player == 1)) or ((board_state[row][col+1] == 1) and (player == 2)):
                    valid_moves.append([row,col+1])
                elif board_state[row][col+1] == player:
                    return self.check_jump(board_state, player, valid_moves, [row,col+1], "d")
        
            elif direction == "b":
                if board_state[row+1][col-1] == 0:
                    valid_moves.append([row+1,col-1])
                elif ((board_state[row+1][col-1] == 2) and (player == 1)) or ((board_state[row+1][col-1] == 1) and (player == 2)):
                    valid_moves.append([row+1,col-1])
                elif board_state[row+1][col-1] == player:
                    return self.check_jump(board_state, player, valid_moves, [row+1,col-1], "be")

            elif direction == "bd":
                if board_state[row+1][col] == 0:
                    valid_moves.append([row+1,col])
                elif ((board_state[row+1][col] == 2) and (player == 1)) or ((board_state[row+1][col] == 1) and (player == 2)):
                    valid_moves.append([row+1,col])
                elif board_state[row+1][col] == player:
                    return self.check_jump(board_state, player, valid_moves, [row+1,col], "b")
        
        
        # Parte de baixo do tabuleiro 
        else:
            if direction == "c":
                # Existe sempre a celula de cima
                if ((board_state[row-1][col] == 22) and (player == 2)):
                    valid_moves.insert(0, [row-1,col])
                elif board_state[row-1][col] == 0:
                    valid_moves.append([row-1,col])
                elif ((board_state[row-1][col] == 2) and (player == 1)) or ((board_state[row-1][col] == 1) and (player == 2)):
                    valid_moves.append([row-1,col])
                elif board_state[row-1][col] == player:
                    return self.check_jump(board_state, player, valid_moves, [row-1,col], "c")
        
            elif direction == "cd":
                # Existe sempre a celula de cima direita
                if ((board_state[row-1][col+1] == 11) and (player == 1)):
                    valid_moves.insert(0, [row-1,col+1])
                elif board_state[row-1][col+1] == 0:
                    valid_moves.append([row-1,col+1])
                elif ((board_state[row-1][col+1] == 2) and (player == 1)) or ((board_state[row-1][col+1] == 1) and (player == 2)):
                    valid_moves.append([row-1,col+1])
                elif board_state[row-1][col+1] == player:
                    return self.check_jump(board_state, player, valid_moves, [row-1,col+1], "cd")
        
            elif direction == "e":
                if col != 0: 
                    if board_state[row][col-1] == 0:
                        valid_moves.append([row,col-1])
                    elif ((board_state[row][col-1] == 2) and (player == 1)) or ((board_state[row][col-1] == 1) and (player == 2)):
                        valid_moves.append([row,col-1])
                    elif board_state[row][col-1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row,col-1], "e")

            elif direction == "d":
                if col != len(board_state[row]) -1: 
                    if board_state[row][col+1] == 0:
                        valid_moves.append([row,col+1])
                    elif ((board_state[row][col+1] == 2) and (player == 1)) or ((board_state[row][col+1] == 1) and (player == 2)):
                        valid_moves.append([row,col+1])
                    elif board_state[row][col+1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row,col+1], "e")
                        
            elif direction == "be":
                if row != len(board_state)-1 and col != 0:
                    if board_state[row+1][col-1] == 0:
                        valid_moves.append([row+1,col-1])
                    elif ((board_state[row+1][col-1] == 2) and (player == 1)) or ((board_state[row+1][col-1] == 1) and (player == 2)):
                        valid_moves.append([row+1,col-1])
                    elif board_state[row+1][col-1] == player:
                        return self.check_jump(board_state, player, valid_moves, [row+1,col-1], "be")

            elif direction == "b":
                # Verifica se a celula de baixo existe ... A peça não pode estar na última fila
                if row != len(board_state)-1 and col != len(board_state[row])-1:
                    if board_state[row+1][col] == 0:player
                    elif ((board_state[row+1][col] == 2) and (player == 1)) or ((board_state[row+1][col] == 1) and (player == 2)):
                        valid_moves.append([row+1,col])
                    elif board_state[row+1][col] == player:
                        return self.check_jump(board_state, player, valid_moves, [row+1,col], "b")
        
        
        return valid_moves
            
    def move_piece(self, board_state, current_pos, dest_pos, player): 
        """
        Move uma peça de uma posição para outra no tabuleiro.

        Args:
            board_state (list): O estado atual do tabuleiro.
            current_pos (list): As coordenadas da posição atual da peça.
            dest_pos (list): As coordenadas da posição de destino para a peça.
            player (int): O jogador que está realizando o movimento.

        Returns:
            bool: True se o movimento for bem-sucedido.
        """
        board_state[current_pos[0]][current_pos[1]] = 0
        board_state[dest_pos[0]][dest_pos[1]] = player
        return True
    

    def evaluate_state_2(self, board_state, player):
        """
        Avalia o estado atual do tabuleiro para um jogador específico.

        Args:
            board_state (list): O estado atual do tabuleiro.
            player (int): O jogador para o qual avaliar o estado.

        Returns:
            int: O valor da pontuação para o estado atual do tabuleiro para o jogador.
        """
        
        # Constants for scoring factors
        SCORE_PIECE_DIFFERENCE = 2
        SCORE_DISTANCE_TO_GOAL = -4  # Emphasize minimizing the distance to the respective goals
        SCORE_CENTER_CONTROL = 2     # Lesser emphasis on center control

        # For Player 1, the goal is the last column in the bottom row. For Player 2, it's the first column in the bottom row.
        if player == 1:
            goal_col = len(board_state[-1]) - 1  # Last column for Player 1
        else:  # Player 2
            goal_col = 0  # First column for Player 2

        num_pieces = sum(row.count(player) for row in board_state)
        num_opponent_pieces = sum(row.count(3 - player) for row in board_state)
        piece_difference = num_pieces - num_opponent_pieces

        total_distance_to_goal = 0
        for row_idx, row in enumerate(board_state):
            for col_idx, cell in enumerate(row):
                if cell == player:
                    if player == 1:
                        distance_to_goal = (len(board_state[-1]) - 1) - col_idx  # Distance to the rightmost column
                    else:  # Player 2
                        distance_to_goal = col_idx  # Distance from the leftmost column
                    total_distance_to_goal += distance_to_goal

        # Center control calculations
        center_rows_start = len(board_state) // 4
        center_rows_end = 3 * len(board_state) // 4
        center_control = sum(board_state[row][col] == player
                            for row in range(center_rows_start, center_rows_end + 1)
                            for col in range(len(board_state[row]) // 4, 3 * len(board_state[row]) // 4))

        score = (piece_difference * SCORE_PIECE_DIFFERENCE +
                total_distance_to_goal * SCORE_DISTANCE_TO_GOAL +
                center_control * SCORE_CENTER_CONTROL)
        return score
        
        
    

    def evaluate_state_1(self, board_state, player):
        """
        Avalia o estado atual do tabuleiro para um jogador específico.

        Args:
            board_state (list): O estado atual do tabuleiro.
            player (int): O jogador para o qual avaliar o estado.

        Returns:
            int: O valor da pontuação para o estado atual do tabuleiro para o jogador.
        """

        # Define goal positions for each player
        goal_row = self.board_size * 2 - 2  # Last row index for both players
        goal_col_player_1 = len(board_state[goal_row]) - 1  # Last column for Player 1
        goal_col_player_2 = 0  # First column for Player 2

        # Calculate the change in the number of pieces on the board
        num_pieces = sum(row.count(player) for row in board_state)
        num_opponent_pieces = sum(row.count(3 - player) for row in board_state)
        piece_difference = num_pieces - num_opponent_pieces
        winner_score = 0
        winner = self.check_winner(board_state)
        if winner == player:
            return 1000

        elif winner == 3-player:
            winner_score = -1000

        if num_pieces == 0:
            return float('-inf')  # Extremely bad situation for player

        # Calculate "distance" to goal for each piece
        total_distance = 0
        for row in range(len(board_state)):
            for col in range(len(board_state[row])):
                if board_state[row][col] == player:
                    if player == 1:
                        # Distance for player 1 is based on columns from the right
                        distance = goal_col_player_1 - col
                    else:
                        # Distance for player 2 is based on columns from the left
                        distance = col - goal_col_player_2
                    total_distance += distance

        # Score based on the change in number of pieces and total distance to goal
        score = piece_difference * 3 - total_distance + winner_score
        return score


    
    def minimax_medium(self, player, board, depth, maximizing_player):
        """
        Algoritmo Minimax para selecionar a melhor jogada num determinado estado do tabuleiro.

        Args:
            player (int): O jogador para o qual a jogada está sendo calculada.
            board (list): O estado atual do tabuleiro.
            depth (int): A profundidade máxima de busca na árvore de jogadas.
            maximizing_player (bool): Indica se é o jogador maximizador ou não.

        Returns:
            tuple: Um tuplo com a melhor jogada e sua pontuação associada.
        """
        if depth == 0 or self.check_winner(board):
            return None, self.evaluate_state_1(board, self.player)  ##chamada da primeira função de avaliação

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for piece in self.find_pieces_playable(board, player):
                for next_move in self.valid_move(player, board, piece):
                    board_copy = copy.deepcopy(board)
                    self.move_piece(board_copy, piece, next_move, player)  # Apply move to the board copy
                    _, eval = self.minimax_medium(3 - player, board_copy, depth - 1, False)  # Use unpacking to get the score
                    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, next_move)

            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for piece in self.find_pieces_playable(board, player):
                for next_move in self.valid_move(player, board, piece):
                    board_copy = copy.deepcopy(board)
                    self.move_piece(board_copy, piece, next_move, player)  # Correct placement inside loop
                    _, eval = self.minimax_medium(3 - player, board_copy, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, next_move)
            return best_move, min_eval
        
    def minimax_hard(self, player, board, depth, maximizing_player):
        '''
        Implementa o algoritmo Minimax, com a segunda função de avaliação, para escolher a melhor jogada para o jogador especificado.

        Parâmetros:
            player (int): O jogador atual para o qual a jogada está sendo avaliada.
            board (list): O estado atual do tabuleiro do jogo representado como uma lista 2D.
            depth (int): A profundidade máxima da árvore de busca.
            maximizing_player (bool): Indica se o jogador atual é o maximizador ou não.

        Retorna:
            tuple: Um tuplo com a melhor jogada e sua pontuação associada.
        '''
        if depth == 0 or self.check_winner(board):
            return None, self.evaluate_state_2(board, self.player)  ##chamada da segunda função de avaliação

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for piece in self.find_pieces_playable(board, player):
                for next_move in self.valid_move(player, board, piece):
                    board_copy = copy.deepcopy(board)
                    self.move_piece(board_copy, piece, next_move, player)  # Apply move to the board copy
                    _, eval = self.minimax_hard(3 - player, board_copy, depth - 1, False)  # Use unpacking to get the score
                    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, next_move)
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for piece in self.find_pieces_playable(board, player):
                for next_move in self.valid_move(player, board, piece):
                    board_copy = copy.deepcopy(board)
                    self.move_piece(board_copy, piece, next_move, player)  # Correct placement inside loop
                    _, eval = self.minimax_hard(3 - player, board_copy, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, next_move)
            return best_move, min_eval



    def check_winner(self, board_state):
        '''
        Avalia se o jogo já tem um vencedor.

        Parâmetros:
            board_state (list): O estado atual do tabuleiro do jogo representado como uma lista 2D.

        Retorna:
            int: O número do jogador que venceu o jogo. Retorna 0 se não houver vencedor ainda.
        '''
        if (board_state[self.board_size-1][0] == 2):
            return 2
        if (board_state[self.board_size-1][self.board_size * 2 - 2] == 1):
            return 1
        return 0
        


    def hill_climbing(self, player, board):
        '''
        Executa o algoritmo Hill Climbing para encontrar a melhor jogada para o jogador especificado no tabuleiro fornecido.

        Parâmetros:
            player (int): O jogador para quem a melhor jogada deve ser encontrada. O valor pode ser 1 ou 2, representando o Jogador 1 e o Jogador 2, respectivamente.
            board (list): O estado atual do tabuleiro do jogo representado como uma lista 2D.

        Retorna:
            tuple: Um tuplo com a melhor jogada encontrada pelo algoritmo Hill Climbing. O tuplp consiste em dois elementos:
               - A peça a ser movida (representada como um tuplo que contém as coordenadas da peça)
               - A célula de destino para mover a peça (representada como um tuplo que contém as coordenadas de destino)
        '''
        score = float('-inf')
        for piece in self.find_pieces_playable(board, player):
            for next_move in self.valid_move(player, board, piece):
                new_score = self.evaluate_state_2(board, player)
                if score < new_score:
                    score = new_score
                    best_move = (piece, next_move)
                    
        return best_move