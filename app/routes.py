from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import pokemonFormForm
from app.forms import LoginForm
from app.forms import SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user


# Home
@app.route('/')
@app.route('/home')
def home():
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

        queried_user = User.qurt.filter(User.email ==email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.firstName}!', 'success')
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstName =form.firstName.data
        lastName=form.lastName.data
        email = form.email.data
        password= form.password.data

        # create an instance of User Class
        user = User(firstName, lastName, email, password)

        db.session.add(user)
        db.session.commit()


        flash(f'Thank you for signing up {firstName}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route('/logout')

def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('login'))


