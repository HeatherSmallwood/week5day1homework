from flask import Flask, request, render_template
import requests
app = Flask(__name__)

@app.route('/')
def homePage():
    return 'Welcome to the Pokemon Card Selector!'


@app.route('/pokemonForm', methods=['GET','POST'])
def pokemon_form():
    if request.method =='POST':
        pokemon_data = request.form.get('pokemon_data').lower()
        try:
            pokemon_url= f"https://pokeapi.co/api/v2/pokemon/{pokemon_data}"
            response = requests.get(pokemon_url)
            extra_data = response.json()
            pokemon_dict = {
                'name' : extra_data['forms'][0]['name'],
                'ability_name' : extra_data['abilities'][0]['ability']['name'],
                'ability_name' : extra_data['abilities'][1]['ability']['name'],
                'base_experience' : extra_data['base_experience'],
                'attack_base_stat' : extra_data['stats'][1]['base_stat'],
                'defense_base_stat' : extra_data['stats'][2]['base_stat'],
                'hp_base_stat' : extra_data['stats'][0]['base_stat'],
                'sprites_image': extra_data['sprites']['front_shiny']
            }
            print(pokemon_dict)
            return render_template('pokemonForm.html', pokemon_info=pokemon_dict)
        except:
            return render_template('pokemonForm.html')
    else:
        return render_template('pokemonForm.html')



