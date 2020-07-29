from flask import Flask, redirect, url_for, render_template, request, Response
import requests
import pokebase as pb

POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"
app = Flask(__name__)

# flask backend 

# render template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def link():
    return render_template("link.html")
    
@app.route("/<name>")
def name(name):
    return render_template("hello.html", content=name)

@app.route("/weakness", methods=['GET', 'POST'])
def weakness():
    if request.method == 'POST' and request.form.get('pokemon'):
        poke = request.form.get('pokemon')
        try: 
            userPokemon = pb.pokemon(str(poke).lower())
        except: 
            return render_template("weakness.html", error=True) 
        immunities = []
        double_damage = []
        quad_damage = []
        
        # calculations
        for slot in userPokemon.types:
            for weaknessobj in slot.type.damage_relations.double_damage_from:
                weakness = weaknessobj.get('name')
                if weakness in double_damage:
                    double_damage.remove(weakness)
                    quad_damage.append(weakness)
                else:
                    double_damage.append(weakness)
        for slot in userPokemon.types:        
            for resistanceobj in slot.type.damage_relations.half_damage_from:
                resistance = resistanceobj.get('name')
                while resistance in double_damage:
                    double_damage.remove(resistance)
            for immunityobj in slot.type.damage_relations.no_damage_from:
                immunity = immunityobj.get('name')
                while immunity in double_damage:
                    double_damage.remove(immunity)
                immunities.append(immunity)
        imglink = f'https://pokeres.bastionbot.org/images/pokemon/{userPokemon.id}.png'
        return render_template("weakness.html", content=userPokemon, immunities=immunities, double_damage=double_damage, quad_damage= quad_damage, pic=imglink )
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)
