from app.blueprints.pokemon import pokemon
from flask import request, render_template,flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import requests
from app.blueprints.pokemon.forms import PokemonForm
from app.models import db,Pokemon, User

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
        pokemon = Pokemon.query.filter_by(name=pokemon_data).one_or_none()
        if pokemon:
            print(pokemon)
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
            flash(f'Great choice {current_user.name} you have added { poke.name } to your team!', 'success')
            return render_template('pokemonForm.html', form=form, pokemon_info=poke)
    return render_template('pokemonForm.html', form=form)

@pokemon.route('/team')
@login_required
def team():
    user = User.query.get(current_user.id)
    if user:
        all_members = user.caught_pokemon.all()
        print(all_members)
        return render_template('team.html', all_members=all_members, user=user)
    return "User not found"

@pokemon.route('/catch/<int:pokemon_id>', methods=['POST'])
@login_required
def catch_pokemon(pokemon_id):
    poke = Pokemon.query.get(pokemon_id)
    
    if not poke:
        return f"Pokémon {pokemon_id} does not exist."

    user_pokemons = current_user.caught_pokemon.all() 

    if len(user_pokemons) >= 5:
        flash(f'You can not add {poke.name}, your team is full!', 'danger')
        return redirect(url_for('pokemon.pokemon_form'))
    
    if poke in user_pokemons:
        flash(f'{poke.name} is already on your team!', 'success')
        return redirect(url_for('pokemon.pokemon_form'))

    current_user.caught_pokemon.append(poke)
    db.session.commit()
    flash(f'Great choice {current_user.firstName}! You have added {poke.name} to your team!', 'success')
    return redirect(url_for('pokemon.team'))

@pokemon.route('/release/<int:pokemon_id>', methods=['POST'])
@login_required
def release_pokemon(pokemon_id):
    poke = Pokemon.query.get(pokemon_id)
    
    if not poke:
        return f"Pokémon with ID {pokemon_id} does not exist."
    
    user_pokemons = current_user.caught_pokemon.all()  

    if poke in user_pokemons:
        current_user.caught_pokemon.remove(poke)
        db.session.commit()
        flash(f'{current_user.firstName}, you have released {poke.name} from your team!', 'info')
    return redirect(url_for('pokemon.team'))


@pokemon.route('/displayteams')
@login_required
def display_teams():
    users=User.query.filter(User.id != current_user.id, User.caught_pokemon).all()
    return render_template('displayUsers.html', users=users)


@pokemon.route('/displaytrainer/<int:user_id>')
@login_required
def display_trainer(user_id):
    user=User.query.get(user_id)
    if user.caught_pokemon:
        all_members=user.caught_pokemon
        return render_template('team.html', all_members=all_members, user=user)
    flash(f'{user.firstName} have not caught any pokemon yet!', 'warning')
    return redirect(url_for('pokemon.display_teams'))



@pokemon.route('/attack/<int:user_id>', methods=['GET'])
@login_required
def attack_user(user_id):
    if user_id == current_user.id:
        flash("You can't battle yourself!")
        return redirect(url_for('pokemon.team'))

    user_pokemons = current_user.caught_pokemon.all()
    defending_user = User.query.get(user_id)
    defending_pokemons = defending_user.caught_pokemon.all()

    if not user_pokemons or not defending_pokemons:
        flash("Invalid team! Both users must have valid Pokémon teams.")
        return redirect(url_for('pokemon.team'))

    return render_template('attack.html', 
                           user_pokemons=user_pokemons, 
                           defending_pokemons=defending_pokemons, 
                           defending_user=defending_user)


@pokemon.route('/battle_results', methods=['POST'])
@login_required
def battle_results():
    user_pokemons = current_user.caught_pokemon.all()
    defending_user_pokemons = User.query.get(request.form['defending_user_id']).caught_pokemon.all()

    if not user_pokemons or not defending_user_pokemons:
        return jsonify({"error": "Invalid team! Both users must have valid Pokémon teams."}), 400

   
    battle_results = simulate_battle(user_pokemons, defending_user_pokemons)

    outcomes = []
    for result in battle_results:
        if result[2] == 'fainted':
            outcomes.append(f"{result[0].name} attacked {result[1].name} and fainted")

   
    return render_template('battle_results.html', outcomes=outcomes)





#  battle between two teams 
def simulate_battle(team_a, team_b):
    battle_results = []


    for attacker in team_a:
        for defender in team_b:
            # damage calcs and outcomes
            damage = attacker.attack_base_stat - defender.defense_base_stat
            if damage < 0:
                damage = 0
            defender.hp_base_stat -= damage

            if defender.hp_base_stat <= 0:
                battle_results.append((attacker, defender, "fainted"))
    return battle_results

