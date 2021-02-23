import pymongo
from flask import Flask, jsonify, render_template, request

# from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb://admin:HYBfhl68822@10.100.2.121:27017"
)  # ทำการเชื่อม mongodb โดยใช้ user และ password ที่ได้รับ
# client = pymongo.MongoClient(
#     "mongodb://admin:HYBfhl68822@node9144-advweb-06.app.ruk-com.cloud:11168"
# )

db = client["Player"]  # ทำการเชื่อมต่อ mongodb ที่ได้สร้างไว้


@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"  # เป็นการทดสอบการเปิดหน้า page
    return texts


@app.route("/test")
def get_join():
    char = db.player  # ทำการเอา collection มาเก็บไว้ในตัวแปร
    getjoin = char.aggregate(  # ใช้ library ในการ join collection
        [
            {
                "$lookup": {  # คำสั่งในการ join table
                    "from": "manager",  # นำ collection ที่ต้องการจะ join มาใส่
                    "localField": "clubname",  # นำชื่อ คอลัมใน collection ของเราที่ต้องการจะ join มาใส่
                    "foreignField": "clubname",  # นำชื่อ คอลัมใน collection อื่นๆที่ต้องการจะ join มาใส่
                    "as": "club",  # ให้แสดงเป็น Title เป็นชื่ออะไร
                }
            },
            {
                "$unwind": "$club"
            },  # ทำการลบข้อมูลตัวต่างๆที่ ข้อมูลไม่แมตท์กันออกจพได้แค่ข้อมูลที่ตรงกัน
            {
                "$project": {  # เป็นการเลือกเฉพาะสิ่งที่เราต้องการจะดู
                    "_id": 0,  # ไม่ต้องการให้เลข _id ออกให้เป็น 0 แต่ถ้าต้องการให้ข้อมูลโชว์ให้ใส่เป็น 1
                    "name": 1,
                    "manager": 1,
                    "club": {
                        "clubname": "$club.clubname",  # เป็นการจัด field ให่ออกมาเฉพาะข้อมูล
                        "managername": "$club.name",
                    },
                }
            },
        ]
    )
    return json_util.dumps(getjoin)


@app.route("/football", methods=["GET"])  # ทำการ route ลิ้งและประกาศ medthod
def get_ShowAll():
    char = db.player  # ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    output = []
    for x in char.find():  # ทำการวนลูปเพิ่อหาข้อมูล
        output.append(
            {
                "name": x["name"],
                "clubname": x["clubname"],
                "age": x["age"],
            }
        )
    return jsonify(output)


@app.route("/football/<name>", methods=["GET"])  # ทำการ route ลิ้งและประกาศ medthod
def get_oneshow(name):
    char = db.player  # ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({"clubname": name})  # ทำการหาข้อมูลด้วยใช้ชื่อเป็นตัวค้นหา
    if x:
        output = {
            "name": x["name"],
            "clubname": x["clubname"],
            "age": x["age"],
        }
    else:
        output = "No such name"  # ถ้าไม่เจอจะขึ้นดังข้อความ
    return jsonify(output)


@app.route("/additem", methods=["POST"])
def add_team():
    char = db.player
    name = request.json["name"]
    clubname = request.json["clubname"]
    age = request.json["age"]

    char_id = char.insert({"name": name, "clubname": clubname, "age": age})

    new_char = char.find_one({"_id": char_id})
    output = {
        "name": new_char["name"],
        "clubname": new_char["clubname"],
        "age": new_char["age"],
    }
    return jsonify(output)


@app.route("/football/<name>", methods=["PUT"])  # ทำการ route ลิ้งและประกาศ medthod
def update_team(name):
    char = db.player  # ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({"clubname": name})  # ทำการหาข้อมูลด้วยใช้ชื่อเป็นตัวค้นหา
    if x:
        myquery = {"name": x["name"], "clubname": x["clubname"], "age": x["age"]}

    name = request.json["name"]
    clubname = request.json["clubname"]
    age = request.json["age"]

    newvalues = {
        "$set": {
            "name": name,
            "clubname": clubname,
            "age": age,
        }
    }

    char_id = char.update_one(myquery, newvalues)  # เป็นคำสั่งในการ update

    output = {"name": name, "clubname": clubname, "age": age}

    return jsonify(output)


@app.route("/football/<name>", methods=["DELETE"])  # ทำการ route ลิ้งและประกาศ medthod
def delete(name):
    char = db.player  # ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({"clubname": name})

    char_id = char.delete_one(x)  # ทำการลบจากค่า id ที่ได้รับ

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
