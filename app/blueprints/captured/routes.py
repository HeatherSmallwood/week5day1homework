from .captured_templates import captured
from flask import request, flash, redirect, url_for, render_template
from app.models import Captured, db
from flask_login import current_user, login_required

@captured.route('/capture_pokemon', methods=['GET', 'POST'])
@login_required
def Capture_pokemon():
    form = CapturedForm()
    if request.method == 'POST' and form.validate_on_submit():
        name =form.name.data
        caption=form.caption.data
        img_url = form.img_url.data
        user_id = current_user.id
      

        # create an instance of capture pokemon Class
        capture = Captured(name, caption, img_url, user_id)

        db.session.add(capture)
        db.session.commit()


        flash(f'Great choice {user_id} you have added { name }to your team!', 'success')
        return redirect(url_for('captured.team'))
    else:
        return render_template('create_team.html', form=form)