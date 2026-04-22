from flask import Flask, render_template, request, jsonify
import chess

from main import get_best_move, evaluate_board 

app = Flask(__name__)

# --- 1. ROUTE MỚI: TRANG MENU CHÍNH ---
@app.route('/')
def menu():
    return render_template('menu.html')

# --- 2. ROUTE: TRANG CHƠI CỜ ---
# Nhận các cấu hình từ Menu gửi sang qua URL (GET request)
@app.route('/game')
def game():
    time = int(request.args.get('time', 600))  # Mặc định 10 phút (600 giây)
    color = request.args.get('color', 'w')     # Mặc định Trắng
    depth = int(request.args.get('depth', 3))  # Mặc định Trung bình
    
    # Truyền biến sang giao diện HTML
    return render_template('index.html', time=time, color=color, depth=depth)

@app.route('/api/ai_move', methods=['POST'])
def ai_move():
    try:
        data = request.json
        if not data or 'fen' not in data:
            return jsonify({'error': 'Thiếu dữ liệu trạng thái bàn cờ (FEN)'}), 400

        fen = data.get('fen')
        
        try:
            depth = int(data.get('depth', 3))
        except ValueError:
            depth = 3 

        try:
            board = chess.Board(fen)
        except ValueError:
            return jsonify({'error': 'Chuỗi FEN không hợp lệ'}), 400

        if board.is_game_over():
            return jsonify({'move': None, 'status': 'game_over'})

        best_move = get_best_move(board, depth=depth)
        
        if best_move:
            return jsonify({'move': best_move.uci()})
        else:
            return jsonify({'error': 'AI không tìm được nước đi hợp lệ'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    try:
        fen = request.json.get('fen')
        board = chess.Board(fen)
        score = evaluate_board(board)
        return jsonify({'score': score})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Khởi động server thành công! Hãy mở trình duyệt ở địa chỉ http://127.0.0.1:5000")
    app.run(debug=True)