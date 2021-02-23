import pymongo
from flask import Flask,jsonify,render_template,request
from flask_pymongo import PyMongo

app = Flask(__name__)

#client = pymongo.MongoClient("mongodb://admin:HYBfhl68822@10.100.2.121:27017")  #ทำการเชื่อม mongodb โดยใช้ user และ password ที่ได้รับ
client = pymongo.MongoClient("mongodb://admin:HYBfhl68822@node9144-advweb-06.app.ruk-com.cloud:11168")

db = client["kritsadeeka"] #ทำการเชื่อมต่อ mongodb ที่ได้สร้างไว้

@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"  #เป็นการทดสอบการเปิดหน้า page
    return texts


@app.route("/football", methods=['GET']) #ทำการ route ลิ้งและประกาศ medthod 
def get_ShowAll():
    char = db.football #ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    output = [] 
    for x in char.find(): #ทำการวนลูปเพิ่อหาข้อมูล
        output.append({'clubname' : x['clubname'],
                        'coach' : x['coach'],
                        'squad' : x['squad'],})
    return jsonify(output)


@app.route("/football/<name>", methods=['GET']) #ทำการ route ลิ้งและประกาศ medthod 
def get_oneshow(name):
    char = db.football #ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({'clubname' : name}) #ทำการหาข้อมูลด้วยใช้ชื่อเป็นตัวค้นหา
    if x:
        output = {'clubname' : x['clubname'],
                        'coach' : x['coach'],
                        'squad' : x['squad'],}
    else:
        output = "No such name" #ถ้าไม่เจอจะขึ้นดังข้อความ
    return jsonify(output)


@app.route('/football', methods=['POST'])
def add_team():
  char = db.football
  clubname = request.json['clubname']
  coach = request.json['coach']
  squad = request.json['squad']

  char_id = char.insert({'clubname': clubname, 
                         'coach': coach,
                        'squad': squad})

  new_char = char.find_one({'_id': char_id })
  output = {'clubname' : new_char['clubname'], 
                        'coach' : new_char['coach'],
                        'squad' : new_char['squad'],}
  return jsonify(output)


@app.route('/football/<name>', methods=['PUT']) #ทำการ route ลิ้งและประกาศ medthod 
def update_team(name):
    char = db.football #ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({'clubname' : name}) #ทำการหาข้อมูลด้วยใช้ชื่อเป็นตัวค้นหา
    if x:
        myquery = {'clubname' : x['clubname'], 
                        'coach' : x['coach'],
                        'squad' : x['squad']}

    clubname = request.json['clubname']
    coach = request.json['coach']
    squad = request.json['squad']

    
    newvalues = {"$set" : {'clubname' : clubname,
                        'coach' : coach,
                        'squad' : squad,}}

    char_id = char.update_one(myquery, newvalues) #เป็นคำสั่งในการ update

    output = {'clubname' : clubname,
                        'coach' : coach,
                        'squad' : squad}

    return jsonify(output)


@app.route('/football/<name>', methods=['DELETE']) #ทำการ route ลิ้งและประกาศ medthod 
def delete(name):
    char = db.football #ทำการดึงข้อมูลจาก database มาเก็บใส่ตัวแปร
    x = char.find_one({'clubname' : name})

    char_id = char.delete_one(x) #ทำการลบจากค่า id ที่ได้รับ

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000)