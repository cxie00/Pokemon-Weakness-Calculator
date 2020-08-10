import pokebase as pb

import requests
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
def weaknesscalc():
    poke = pb.pokemon("charizard")
    print(poke.types[0].type)

weaknesscalc()
"""
weaknessdict = {
    'normal': 'grey',
    'water': 'blue',
    'fire': 'red',
    'grass': 'green',
    'ice': 'aliceblue',
    'fighting': 'red',
    'poison': 'purple',
    'ground': 'brown',
    'flying': 'blue',
    'psychic': 'pink',
    'bug': 'green',
    'rock': 'green',
    'ghost': 'purple',
    'dragon': 'blue',
    'dark': 'black',
    'steel': 'black',
    'fairy': 'pink'
}

dict = {}
string = 'flying'
dict[string] = weaknessdict.get(string)
print(dict)"""