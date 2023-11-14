from app.blueprints.pokemon import pokemon
from flask import request, render_template
from flask_login import login_required
import requests



@pokemon.route('/')
@pokemon.route('/home')
def home():
    return render_template('home.html')

# pokemon form
@pokemon.route('/pokemonForm', methods=['GET','POST'])
@login_required
def pokemon_form():
    form = pokemonForm()
    if request.method =='POST':
        pokemon_data = form.name.data
        try:
            print(pokemon_data)
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
           
            return render_template('pokemonForm.html', pokemon_info=pokemon_dict, form=form)
        except:
            return render_template('pokemonForm.html',form=form)
    else:
        return render_template('pokemonForm.html', form=form)
    
# # REGISTERED_USERS={
# #     'heather@pokemon.com':{
# #         'name': 'Heather Smallwood',
# #         'password':'ocean7'
# #     }
# }
