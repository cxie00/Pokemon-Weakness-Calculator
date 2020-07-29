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
    url = "https://pokeapi.co/api/v2/pokemon/phione"
    data, error = fetch_data_from_url(url)
    print(data)
    print(error)
    """user_input = input("Enter a Pokemon whose weakness you would like to calculate: ")
    userPokemon = pb.pokemon(str(user_input))
    print(userPokemon)
    immunities = []
    double_damage = []
    quad_damage = []
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

    if len(immunities) > 0:
        result0 = f'{userPokemon} is immune to: \n'
        for i in immunities:
            result0 += f'{i} \n'
        print(result0)
    if len(double_damage) > 0:
        result1 = f'{userPokemon} is 1x weak to: \n'
        for w1 in double_damage:
            result1 += f'{w1} \n'
        print(result1)
    if len(quad_damage) > 0:
        result2 = f'{userPokemon} is 2x weak to: \n'
        for w2 in quad_damage:
            result2 += f'{w2} \n'
        print(result2)"""

weaknesscalc()