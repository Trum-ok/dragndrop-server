import os
import pyperclip

from toast import balloon_tip
from flask import Flask, request, jsonify

app = Flask(__name__)

SUCCESS = "./_assets/check.ico"
ERROR = "./_assets/error.ico"


@app.route('/')
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "success", 'msg': "Сервер работает! Ваш IP: " + request.remote_addr}), 200


@app.route('/send_code', methods=['POST'])
def receive_code():
    code = request.json.get('code', '')
    
    if code:
        pyperclip.copy(code)
        balloon_tip("success", 'Code copied to clipboard!', icon_path=SUCCESS)
        return jsonify({"status": "success", "message": "Code copied to clipboard!"}), 200
    else:
        balloon_tip("Ошибка", 'No code provided.', icon_path=ERROR)
        return jsonify({"status": "error", "message": "No code provided."}), 400


@app.route('/send_files', methods=['POST'])
def send_files():
    if not request.files:
        print('В запросе нет файлов')
        balloon_tip("Ошибка", 'В запросе нет файлов!', icon_path=ERROR)
        return jsonify({"status": "error", "message": "No file part in the request"}), 400
    
    saved_files = []

    for key, file in request.files.items():
        print(key, file.filename)
        downloads_path = "D:\\OKBOOMER\\3агрузки"
        file.save(os.path.join(downloads_path, file.filename))

    return jsonify({
        "status": "success",
        "message": f"Successfully uploaded {len(saved_files)} file(s).",
        "files": saved_files
    }), 200


def run_server(pc_port: int, debug: bool = False):
    app.run(host='0.0.0.0', port=pc_port, debug=debug)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#     run_server(True)
