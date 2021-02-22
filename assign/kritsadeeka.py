import pymongo
from flask import Flask,jsonify,render_template,request
from flask_pymongo import PyMongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:HYBfhl68822@10.100.2.121:27017")  


db = client["kritsadeeka"] 

####### index ###############
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"
    return texts

########## GET ALL #################
@app.route("/football", methods=['GET'])
def get_ShowAll():
    char = db.football
    output = []
    for x in char.find():
        output.append({'clubname' : x['clubname'],
                        'coach' : x['coach'],
                        'squad' : x['squad'],})
    return jsonify(output)

############## GET ONE ############################
@app.route("/football/<name>", methods=['GET'])
def get_oneshow(name):
    char = db.football
    x = char.find_one({'clubname' : name})
    if x:
        output = {'clubname' : x['clubname'],
                        'coach' : x['coach'],
                        'squad' : x['squad'],}
    else:
        output = "No such name"
    return jsonify(output)

######################### INSERT ####################
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

##################### UPDATE ########################
@app.route('/football/<name>', methods=['PUT'])
def update_team(name):
    char = db.football
    x = char.find_one({'clubname' : name})
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

    char_id = char.update_one(myquery, newvalues)

    output = {'clubname' : clubname,
                        'coach' : coach,
                        'squad' : squad}

    return jsonify(output)

##################### DELETE ############################ 
@app.route('/football/<name>', methods=['DELETE'])
def delete(name):
    char = db.football
    x = char.find_one({'clubname' : name})

    char_id = char.delete_one(x)

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)