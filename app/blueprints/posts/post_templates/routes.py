from . import posts
from flask import request, flash, redirect, url_for, render_template
from app.models import Post, db

@posts.route('/signup', methods=['GET', 'POST'])
def signup():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstName =form.firstName.data
        lastName=form.lastName.data
        email = form.email.data
        password= form.password.data

        # create an instance of User Class
        post = Post(firstName, lastName, email, password)

        db.session.add(post)
        db.session.commit()


        flash(f'Thank you for signing up {firstName}!', 'success')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)