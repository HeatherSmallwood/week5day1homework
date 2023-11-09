from flask import request, render_template
import requests
from app import app
from app.forms import pokemonFormForm
from app.forms import LoginForm
from app.forms import SignupForm


# Home
@app.route('/')
def homePage():
    return render_template('home.html')

# pokemon form
@app.route('/pokemonForm', methods=['GET','POST'])
def pokemon_form():
    form = pokemonFormForm()
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
    
REGISTERED_USERS={
    'heather@pokemon.com':{
        'name': 'Heather Smallwood',
        'password':'ocean7'
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return f'Hello, {REGISTERED_USERS[email]['name']}'
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = f'{form.firstName.data} {form.lastName.data}'
        email = form.email.data
        password= form.password.data
        REGISTERED_USERS[email] ={
            'name':full_name,
            'password':password
        }
        return f'Thank you for singing up {full_name}!'
    else:
        return render_template('signup.html', form=form)


