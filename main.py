import chess

# ==========================================
# PHẦN 1: ĐỊNH NGHĨA HẰNG SỐ VÀ HÀM
# Điểm số chuẩn theo hình ảnh: Chốt 1, Mã/Tượng 3, Xe 5, Hậu 9
# ==========================================
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000000 # Giá trị tượng trưng rất lớn cho Vua để chống bị ăn
}

def evaluate_board(board):
    """Hàm đánh giá điểm số CHỈ dựa trên số lượng quân cờ (Material)"""
    if board.is_checkmate():
        return -9999999 if board.turn == chess.WHITE else 9999999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    # Quét các ô đang có quân cờ và cộng/trừ điểm tuyệt đối
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        
        if piece.color == chess.WHITE:
            score += value
        else:
            score -= value
            
    return score

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if is_maximizing:
        best_score = -float('inf')
        for move in order_moves(board):
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break 
        return best_score
        
    else:
        best_score = float('inf')
        for move in order_moves(board):
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def get_best_move(board, depth):
    best_move = None
    best_score = -float('inf') if board.turn == chess.WHITE else float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    for move in order_moves(board):
        board.push(move)
        is_maximizing = (board.turn == chess.WHITE)
        score = minimax(board, depth - 1, alpha, beta, is_maximizing)
        board.pop()
        
        if board.turn == chess.WHITE:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
                
    return best_move

def order_moves(board):
    def score_move(move):
        if board.is_capture(move):
            if board.is_en_passant(move):
                return 10 
            victim = board.piece_type_at(move.to_square)
            attacker = board.piece_type_at(move.from_square)
            if victim and attacker:
                # Ưu tiên lấy quân nhỏ ăn quân lớn
                return 10 * PIECE_VALUES[victim] - PIECE_VALUES[attacker]
        return 0
    return sorted(board.legal_moves, key=score_move, reverse=True)