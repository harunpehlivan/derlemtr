from flask_api import FlaskAPI
import random

app = FlaskAPI(__name__)

kelimeler =[]
with open('static/kelimeler.txt',encoding='utf-8') as fd:
    for kelime in fd:
        kelimeler.append(kelime.strip())

def get_random_kelime(say):
    n = 1 if say is None else say
    if n<1: n = 1
    elif n>10: n = 10

    sayilar = [random.randrange(len(kelimeler)) for _ in range(n)]
    return [kelimeler[sayilar[m]] for m in range(n)]
        
def kelime_yolla():
    return {
	'sayı': 0,
        'text': get_random_kelime(1)[0]
    }

@app.route("/", methods=['GET'])
def bos_kelime_listesi():
    return {'0':'Lütfen doğru parametre girin'}

@app.route("/<int:key>/", methods=['GET'])
def kelime_listesi(key):
    kelimelist = get_random_kelime(key)
    return {i: kelimelist[i] for i in range(len(kelimelist))}

@app.route("/kelime/", methods=['GET'])
def tek_kelime():
    return kelime_yolla()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11713,debug=True)

