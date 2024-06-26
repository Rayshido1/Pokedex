from flask.globals import request
from models.pokemon import Pokemon
from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods = ["GET","post"])
def buscar():
    pokemon = Pokemon(request.form["nome"].lower(),"", "","")

    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.nome}").text)
        result = res["sprites"]
        result = result["front_default"]
        pokemon.foto = result

        if len(res["types"]) == 2:
            pokemon.tipo1 = res["types"][0]["type"]["name"]
            pokemon.tipo2 = res["types"][1]["type"]["name"]
        else:
            pokemon.tipo1 = res["types"][0]["type"]["name"]

    except:
        return "Pokemon não encontrado!"
    return render_template("index.html",
    nome = pokemon.nome, 
    foto = pokemon.foto,
    tipo1 = pokemon.tipo1.upper(),
    tipo2 = pokemon.tipo2.upper(),


    )

if __name__=="__main__":
    app.run(debug=True)
