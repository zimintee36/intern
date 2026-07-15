from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )


# 读取全部注册
@app.route("/register", methods=["GET"])
def get_register():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM register")

    result = cursor.fetchall()

    print(result)   # 看 Flask terminal 输出

    cursor.close()
    db.close()

    return jsonify(result)


# 新增注册
@app.route("/register", methods=["POST"])
def add_register():

    data = request.json

    db = get_db()
    cursor = db.cursor()

    sql = """
    INSERT INTO register(student_id, studentname, coursename)
    VALUES(%s,%s,%s)
    """

    cursor.execute(sql, (
        data["student_id"],
        data["studentname"],
        data["coursename"]
    ))

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message":"Register successfully"
    })

# 修改注册
@app.route("/register/<student_id>", methods=["PUT"])
def update_register(student_id):

    data = request.json

    db = get_db()
    cursor = db.cursor()

    sql = """
    UPDATE register
    SET student_id=%s,
        studentname=%s,
        coursename=%s
    WHERE student_id=%s
    """
    cursor.execute(sql,(
        data["student_id"],
        data["studentname"],
        data["coursename"],
        student_id
    ))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message":"Updated successfully"})

# 删除注册
@app.route("/register/<student_id>", methods=["DELETE"])
def delete_register(student_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM register WHERE student_id=%s",
        (student_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message":"Deleted"
    })

# 获取课程列表
@app.route("/course", methods=["GET"])
def get_course():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM course")

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)

# 课程学生查询
@app.route("/course/<coursename>/students", methods=["GET"])
def get_course_students(coursename):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT student_id, studentname, coursename
        FROM register
        WHERE coursename=%s
    """, (coursename,))

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)









if __name__ == "__main__":
    app.run(port=5000, debug=True)