from flask import Flask, redirect, url_for, render_template, request, Response
import requests
import pokebase as pb

from collections import namedtuple
POKEMON_COLOR_API = "https://pokeapi.co/api/v2/pokemon-color/"
POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"
Pokemon = namedtuple('Pokemon', "name habitat growth_rate shape") 
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

def fetch_data_from_url(url):
    response = requests.get(url)
    data = {}
    error = {}

    if response.status_code != 200:
        error = {"error": "No data"}
    else:
        try:
            data = response.json()
        except ValueError:
            error = {"error": "JSON could not be decoded"}

    return data, error


def get_pokemon_data(poke_data):
    for pokemon in poke_data.get("pokemon_species"):
        name = pokemon.get("name")
        url = pokemon.get("url")
        details, error = fetch_data_from_url(url)
        if error:
            continue # We are not rendering this pokemon
        habitat, growth_rate, shape = [
        details.get(feature).get("name") 
            if details.get(feature) else "UNKNOWN"
            for feature in ["habitat", "growth_rate", "shape"]
        ]
        yield Pokemon(name=name, habitat=habitat, growth_rate=growth_rate, shape=shape)

# For streaming large data
# Reference: http://flask.pocoo.org/docs/1.0/patterns/streaming/
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv
@app.route("/pokemon", methods=['GET', 'POST'])
def pokemon():
    pokemons = []
    color = ""

    if request.method == 'POST' and request.form.get('color'):
        print("pokemon in if")
        color = request.form.get('color')
        url = f"{POKEMON_COLOR_API}{color}"
        data, error = fetch_data_from_url(url)
        print(data)
        print(error)
        if error:
            return render_template("pokemon.html", error=error, color=color) 
        else:
            pokemons = get_pokemon_data(data)
            return Response(stream_template('pokemon.html', pokemons=pokemons, color=color))

    print("pokemon out of if")
    return render_template("pokemon.html", pokemons=pokemons, color=color)



if __name__ == "__main__":
    app.run(debug = True)
"""
todo:
when calculate is clicked, do a get request to search page with search parameter
can make it submit to 
look up form submit
action is the site -- so /pokemon 
you can send information TO a URL
    so, to the pokemon page, im gonna give this page: charmander.
    so i need to figure it out with this route page
"""