from app.blueprints.pokemon import pokemon
from flask import request, render_template,flash, redirect, url_for
from flask_login import login_required, current_user, db
import requests



@pokemonForm.route('/')
@pokemonForm.route('/home')
def home():
    return render_template('home.html')

# pokemon form
@pokemonForm.route('/pokemonForm', methods=['GET','POST'])
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


@pokemon.route('/capture_pokemon', methods=['GET', 'POST'])
@login_required
def Pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        name =form.name.data
        img_url = form.img_url.data
        user_id = current_user.id
      

        # create an instance of capture pokemon Class
        pokemon = Pokemon(name, img_url, user_id)

        db.session.add(pokemon)
        db.session.commit()


        flash(f'Great choice {user_id} you have added { name }to your team!', 'success')
        return redirect(url_for('pokemon.team'))
    else:
        return render_template('create_team.html', form=form)
    
@pokemon.route('/team')
@login_required
def team():
    all_members = pokemon.query.all()
    return render_template('team.html', all_members=all_members)



# @captured.route('/catch/<int:pokemon_id>', methods=['POST'])
# def catch_pokemon(pokemon_id):
#     pass

# @captured.route('/release/<int:user_pokemon_id>', methods=['POST'])
# def release_pokemon(user_pokemon_id):
#     pass
