import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 使用する色のリスト
colors = ['赤', '青', '黄色']

# 色覚検査の問題数
num_tests = 5

# 色覚検査の問題と正解
color_tests = [{'question': color, 'options': colors, 'answer': color} for color in random.choices(colors, k=num_tests)]

# 現在の問題インデックス
current_question_index = 0

# 正解数を格納するリスト
correct_answers_list = [0] * num_tests

# ホームページ
@app.route('/')
def home():
    global current_question_index, correct_answers_list
    current_question_index = 0
    correct_answers_list = [0] * num_tests
    return render_template('home.html')

# 問題を開始するページ
@app.route('/index')
def index():
    global current_question_index, correct_answers_list
    current_question_index = 0
    correct_answers_list = [0] * num_tests
    return render_template('index.html', question=color_tests[current_question_index])


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global current_question_index, correct_answers_list
    user_answer = request.form['user_answer']

    # インデックスが範囲内かどうかを確認
    if current_question_index < num_tests:
        current_question = color_tests[current_question_index]

        if user_answer == current_question['answer']:
            correct_answers_list[current_question_index] = 1

        current_question_index += 1

    if current_question_index < num_tests:
        return render_template('index.html', question=color_tests[current_question_index])
    else:
        return redirect(url_for('result'))

@app.route('/result')
def result():
    global correct_answers_list
    correct_answers = sum(correct_answers_list)
    current_question_index = 0  # リセット
    return render_template('result.html', correct_answers=correct_answers, num_tests=num_tests)

if __name__ == '__main__':
    app.run(debug=True)
