from flask import Flask, redirect, url_for, render_template, request, Response
import requests
import pokebase as pb


app = Flask(__name__)

# flask backend 

# render template
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def link():
    return render_template("link.html")
    
@app.route("/<name>")
def name(name):
    return render_template("hello.html", content=name)

weaknessdict = {
    'normal': 'grey',
    'water': '#699ccf',
    'fire': '#f5804e',
    'electric': '#db922c',
    'grass': '#38c955',
    'ice': '#7ebecf',
    'fighting': 'brown',
    'poison': 'darkmagenta',
    'ground': '#ab694d',
    'flying': '#8c82e0',
    'psychic': '#de54c0',
    'bug': '#6fa66f',
    'rock': '#a38c24',
    'ghost': 'darkorchid',
    'dragon': '#406ab8',
    'dark': '#231c70',
    'steel': '#7691a6',
    'fairy': '#dd7e6b'
}

# returns string of pokemon type(s)
def type_string(pokemon):
    pokemon_type = str(pokemon.types[0].type)
    if len(pokemon.types) == 2:
        pokemon_type += f'/{pokemon.types[1].type}'
    return pokemon_type

@app.route("/weakness", methods=['GET', 'POST'])
def weakness():
    if request.method == 'POST' and request.form.get('pokemon'):
        poke = request.form.get('pokemon')
        try: 
            # 2 API calls due to pokemon with different forms
            poke = str(poke).lower()
            userSpecies = pb.pokemon_species(poke)
            userPokemon = pb.pokemon(userSpecies.id)
        except: 
            return render_template("weakness.html", error=True) 
        immunities = {}
        double_damage = {}
        quad_damage = {}
        collection = []
        # calculations for immunities, weaknesses, and resistances
        for slot in userPokemon.types:
            for weaknessobj in slot.type.damage_relations.double_damage_from:
                weakness = weaknessobj.get('name')
                if weakness in double_damage:
                    double_damage.pop(weakness)
                    quad_damage[weakness] = (weaknessdict.get(weakness))
                else:
                    double_damage[weakness] = (weaknessdict.get(weakness))
        for slot in userPokemon.types:        
            for resistanceobj in slot.type.damage_relations.half_damage_from:
                resistance = resistanceobj.get('name')
                while resistance in double_damage:
                    double_damage.pop(resistance)
            for immunityobj in slot.type.damage_relations.no_damage_from:
                immunity = immunityobj.get('name')
                while immunity in double_damage:
                    double_damage.pop(immunity)
                immunities[immunity] = weaknessdict.get(immunity)

        collection.append(immunities)
        collection.append(double_damage)
        collection.append(quad_damage)
        usrTypes = type_string(userPokemon)
        imgLink = f'https://pokeres.bastionbot.org/images/pokemon/{userPokemon.id}.png'

        return render_template("weakness.html", content=userPokemon, collection=collection, pic=imgLink, usrTypes=usrTypes)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug = True)
