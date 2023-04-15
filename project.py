from flask import render_template, jsonify, request
from explain import CompareQueries
from interface import app


@ app.route('/')
def home():
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()

    query1 = data['query1']
    query2 = data['query2']

    qep1diff, qep2diff, diff, qep1, qep2, error = [], [], [], [], [], ''

    try:
        qep1diff, qep2diff, diff, qep1, qep2, error = CompareQueries(
            query1, query2)
    except:
        error = 'Error generating the results, please check your input.'

    return jsonify(qep1diff=qep1diff, qep2diff=qep2diff, diff=diff, qep1=qep1, qep2=qep2, error=error)


if __name__ == '__main__':
    app.run()
