from app.blueprints.pokemon import pokemon
from flask import request, render_template,flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from app.blueprints.pokemon.forms import PokemonForm
from app.models import db,  Pokemon


@pokemon.route('/')
@pokemon.route('/home')
def home():
    return render_template('home.html')

# pokemon form
@pokemon.route('/pokemonForm', methods=['GET','POST'])
@login_required
def pokemon_form():
    form = PokemonForm()
    if request.method =='POST':
        pokemon_data = form.name.data.lower()
        pokemon = Pokemon.query.get(pokemon_data)
        if pokemon:
             return render_template('pokemonForm.html',pokemon_info=pokemon, form=form)
        else:
            print(pokemon_data)
            pokemon_url= f"https://pokeapi.co/api/v2/pokemon/{pokemon_data}"
            response = requests.get(pokemon_url)
            extra_data = response.json()
            pokemon_dict = {
                'name' : extra_data['forms'][0]['name'],
                'ability_name' : extra_data['abilities'][0]['ability']['name'],
                'base_experience' : extra_data['base_experience'],
                'attack_base_stat' : extra_data['stats'][1]['base_stat'],
                'defense_base_stat' : extra_data['stats'][2]['base_stat'],
                'hp_base_stat' : extra_data['stats'][0]['base_stat'],
                'sprites_image': extra_data['sprites']['front_shiny']
            }
            poke=Pokemon(name=pokemon_dict['name'],ability_name=pokemon_dict['ability_name'],
                         base_experience=pokemon_dict['base_experience'], attack_base_stat=pokemon_dict['attack_base_stat'],
                         defense_base_stat=pokemon_dict['defense_base_stat'],hp_base_stat=pokemon_dict['hp_base_stat'],
                         sprites_image=pokemon_dict['sprites_image'])
            db.session.add(poke)
            db.session.commit()
            flash(f'Great choice {current_user.id} you have added { poke.name }to your team!', 'success')
    return render_template('pokemonForm.html', form=form)
        


@pokemon.route('/team')
@login_required
def team():
    all_members = pokemon.query.all()
    return render_template('team.html', all_members=all_members)



@pokemon.route('/catch/<int:name>', methods=['POST'])
@login_required
def catch_pokemon(name):
    poke = Pokemon.query.get(name)

    for poke in pokemon:
        if len(current_user.team) >= 6:
            return f'Your team is full'
        elif user.id.pokemon_id == pokemon_id:
             return f'{name} is already on your team!'

        else:
            current_user.team.append(poke)
            db.session.commit()
            flash(f'Great choice {user.id} you have added { name }to your team!', 'success')
            return redirect(url_for(pokemon.team))
        


# add restriction for no duplicates

@pokemon.route('/release/<int:user_pokemon_id>', methods=['POST'])
def release_pokemon(name):
    poke = Pokemon.query.get(name)
    if poke and poke in current_user.release:
        current_user.team.remove(poke)
        db.session.commit()
        flash(f'{user.id}, you have released{ name }from your team!', 'info')
    return redirect(url_for(pokemon.team))
