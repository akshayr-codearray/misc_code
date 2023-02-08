import os
import psycopg2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='mysecretpassword')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM emp;')
    emp = cur.fetchall()
    print(emp)
    print(type(emp))
    cur.close()
    conn.close()
    return jsonify({"emps":emp})


@app.route('/addEmp', methods=['POST', 'GET'])
def add_emp():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data['name']
            email = data['email']
            sal = data['sal']
            feed = data['feed']

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO emp (name, email, salary, feedback)'
                        'VALUES (%s, %s, %s, %s)',
                        (name, email, sal, feed)
                        )
            conn.commit()
            cur.close()
            conn.close()
    return "Emp added"


@app.route('/oneEmp/<int:e_id>')
def one_emp(e_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM emp WHERE id = %s', (e_id,))
    emp_details = cur.fetchall()
    cur.close()
    conn.close()
    return f"{emp_details}"


@app.route('/updateEmp/<int:e_id>', methods=["GET", "PUT"])
def update_emp(e_id):
    if request.method == 'PUT':
        if request.is_json:
            user = request.get_json()
            name = user['name']
            email = user['email']
            sal = user['sal']
            feed = user['feed']

            conn = get_db_connection()
            cur = conn.cursor()
            # cur.execute('SELECT * FROM emp WHERE id = %s', (e_id,))
            # emp_details = cur.fetchall()
            # print(emp_details)
            # print((emp_details[0][0]))
            query = "UPDATE emp SET name=%s , email=%s , salary=%s , feedback=%s WHERE id=%s "
            cur.execute(query, (name, email, sal, feed, e_id))
            conn.commit()

            cur.close()
            conn.close()
    return "emp updated"


@app.route('/deleteEmp/<int:e_id>', methods=["GET","DELETE"])
def del_emp(e_id):
    if request.method =="DELETE":
        conn = get_db_connection()
        cur = conn.cursor()
        del_query = "DELETE FROM emp WHERE id=%s "
        cur.execute(del_query,(e_id,))
        conn.commit()
        cur.close()
        conn.close()
    return "emp deleted"


if __name__ == '__main__':
    app.run(debug=True)
