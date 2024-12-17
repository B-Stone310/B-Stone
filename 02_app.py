from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import random
import os

app = Flask(__name__)
CORS(app)  # CORS 허용

# 퀴즈 데이터 로드 (엑셀 파일 경로)
file_path = os.path.join(os.path.dirname(__file__), 'vocabulary.xlsx')  # 파일 경로를 동적으로 설정

# 데이터 로딩 함수
def load_data():
    try:
        data = pd.read_excel(file_path)
        korean_words = data.iloc[:, 0].tolist()  # 첫 번째 열에 한국어 단어
        japanese_meanings = data.iloc[:, 1].tolist()  # 두 번째 열에 일본어 뜻
        return korean_words, japanese_meanings
    except Exception as e:
        print(f"Error loading file: {e}")
        return [], []  # 예외 처리 시 빈 리스트 반환

# 정답을 저장할 전역 변수
correct_answer = ""
korean_words, japanese_meanings = load_data()

# 퀴즈 질문 생성 함수
def generate_question():
    global correct_answer
    if not korean_words or not japanese_meanings:  # 데이터가 로드되지 않으면 빈 질문 반환
        return "No data available", []
    
    # 랜덤으로 질문 인덱스 선택
    question_idx = random.randint(0, len(korean_words) - 1)
    question_word = korean_words[question_idx]
    correct_answer = japanese_meanings[question_idx]

    # 정답을 제외한 임의의 오답 3개 선택
    incorrect_answers = random.sample([meaning for meaning in japanese_meanings if meaning != correct_answer], 3)
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)  # 오답과 정답을 섞음

    return question_word, options

@app.route("/")
def index():
    # 퀴즈 질문과 옵션을 랜덤으로 생성
    question_word, options = generate_question()
    return render_template('index.html', question_word=question_word, options=options)

@app.route("/check_answer/<selected_option>")
def check_answer(selected_option):
    # 선택한 옵션이 정답인지 확인
    if selected_option == correct_answer:
        return jsonify({"result": "Correct!", "color": "green"})
    else:
        return jsonify({"result": f"Wrong! The correct answer is {correct_answer}", "color": "red"})

@app.route("/get_question", methods=["GET"])
def get_question():
    question_word, options = generate_question()  # 랜덤 질문과 선택지 생성
    if question_word == "No data available":  # 데이터가 없는 경우 처리
        return jsonify({"error": "No quiz data available."})
    
    return jsonify({
        "word": question_word,
        "options": options,
        "correct": correct_answer
    })

if __name__ == "__main__":
    app.run(debug=True)
