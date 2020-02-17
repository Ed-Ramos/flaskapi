from flask import Flask, jsonify, request

from pymongo import MongoClient

app = Flask(__name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]

client = MongoClient('mongodb://db-demo:PMchGczDLHWIQcN1wKnYJp2Jg9Ay3EqHdttn6CQ1uDZvTlB4osTusAFwjIzJzy18o34SHFXVqKg6CovNoYmcDg==@db-demo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')

db = client.db2 # create or refer to db2 as db

posts = db.posts #create a collection named posts


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'})


# @app.route('/lang', methods=['GET'])
# def returnAll():
#     return jsonify({'languages': languages})


@app.route('/org', methods=['GET'])
def returnAll():
    org = []
    for x in posts.find({}, {"_id": 0}):
        org.append(x)
    return jsonify({'organization': org})


# @app.route('/lang/<string:name>', methods=['GET'])
# def returnOne(name):
#     langs = [language for language in languages if language['name'] == name]
#     return jsonify({'language': langs[0]})

@app.route('/org/<string:person>', methods=['GET'])
def returnOne(person):
    org = []
    for x in posts.find({"name": person}, {"_id": 0}):
        org.append(x)
    if not org:
        return "Looks like that person is not in organization"
    else:
        return jsonify({'organization': org})


# @app.route('/lang', methods=['POST'])
# def addOne():
#     language = {'name': request.json['name']}
#
#     languages.append(language)
#     return jsonify({'languages': languages})


@app.route('/org', methods=['POST'])
def addOne():
    newEntry = {'name': request.json['name'], 'city': request.json['city'], 'team': request.json['team']}
    posts.insert(newEntry)

    org = []
    for x in posts.find({}, {"_id": 0}):
        org.append(x)
    return jsonify({'organization': org})


# @app.route('/lang/<string:name>', methods=['PUT'])
# def editOne(name):
#     langs = [language for language in languages if language['name'] == name]
#     langs[0]['name'] = request.json['name']
#     return jsonify({'language': langs[0]})


@app.route('/org/<string:person>', methods=['PUT'])
def editOne(person):
    posts.update(
        {'name': person}, {"name":request.json['name'], 'city': request.json['city'], 'team': request.json['team']})

    org = []
    for x in posts.find({}, {"_id": 0}):
        org.append(x)
    return jsonify({'organization': org})


# @app.route('/lang/<string:name>', methods=['DELETE'])
# def removeOne(name):
#     lang = [language for language in languages if language['name'] == name]
#     languages.remove(lang[0])
#     return jsonify({'language': languages})


@app.route('/org/<string:person>', methods=['DELETE'])
def removeOne(person):
    posts.remove({'name': person})

    org = []
    for x in posts.find({}, {"_id": 0}):
        org.append(x)
    return jsonify({'organization': org})

if __name__ == '__main__':
    app.run(debug=True)
