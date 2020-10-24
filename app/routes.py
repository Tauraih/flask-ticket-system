from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, send_file
from io import  BytesIO
from app import db
from app import app, images
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, CreateTicketForm, Status, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm    # SearchForm,
from app.models import User, Ticket, Post
from app.email import send_password_reset_email, send_ticket_details


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes has been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.passord.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
#         g.search_form = SearchForm()
#     g.locale = str(get_locale())


# @app.route('/search')
# @login_required
# def search():
#     if not g.search_form.validate():
#         return redirect(url_for('index'))
#     page = request.args.get('page', 1, type=int)
#     posts, total = Ticket.search(g.search_form.q.data, page, current_app.config['ITEMS_PER_PAGE'])
#     next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
#         if total > page * current_app.config['ITEMS_PER_PAGE'] else None
#     prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
#         if page > 1 else None
#     return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = CreateTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, content=form.content.data, department=form.department.data,
                        file=form.file.data, priority=form.priority.data, email=form.email.data, name=form.name.data)
        db.session.add(ticket)
        db.session.commit()
        user = Ticket.query.filter_by(email=form.email.data).first()
        if user:
            send_ticket_details(user)
        flash('Ticket submitted successfully')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)


thirty_days = datetime.today() - timedelta(days=30)
sixty_days = datetime.today() - timedelta(days=60)
ninety_days = datetime.today() - timedelta(days=90)
@app.route('/dashboard')
@login_required
def dashboard():
    small = Ticket.query.filter(Ticket.timestamp >= thirty_days).count()
    medium = Ticket.query.filter(Ticket.timestamp > thirty_days, Ticket.timestamp <= sixty_days).count()
    large = Ticket.query.filter(Ticket.timestamp > sixty_days, Ticket.timestamp <= ninety_days).count()
    open = Ticket.query.filter_by(status='Open').count()
    closed = Ticket.query.filter_by(status='Closed').count()
    resolved = Ticket.query.filter_by(status='Resolved').count()
    return render_template('dashboard.html', small=small, medium=medium,
                           large=large, open=open, closed=closed, resolved=resolved)


@app.route('/each/<id>', methods=['GET', 'POST'])
@login_required
def each(id):
    point = Ticket.query.filter_by(id=id).first_or_404()
    form = Status()
    if form.validate_on_submit():
        point.status = form.status.data
        db.session.commit()
        flash('Ticket updated successfully')
        return redirect(url_for('stats'))
    return render_template('each.html', point=point, form=form)


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    single = Ticket.query.first_or_404()
    # form = Status()
    # if request.method == 'POST' and form.validate_on_submit():
    #     updates = Ticket(status=form.status.data)
    #     db.session.add(updates)
    #     # record = Ticket.query.get(request.form.get('id', type=int))
    #     # record.status = request.form.get('status')
    #     db.session.commit()
    #     flash('Ticket updated successfully')
    #     return redirect(url_for('stats'))
    return render_template('updatestatus.html', single=single)


# shows tickets which are less than thirty days
@app.route('/entry')
def thirty():
    point = Ticket.query.filter(Ticket.timestamp >= thirty_days).all()
#     # medium = Ticket.query.filter(Ticket.timestamp > thirty_days, Ticket.timestamp <= sixty_days).all()
#     # large = Ticket.query.filter(Ticket.timestamp > sixty_days, Ticket.timestamp <= ninety_days).all()
    return render_template('thirty.html', point=point)


# shows tickets which are between 30 and 60 days
@app.route('/sixty')
def sixty():
    point = Ticket.query.filter(Ticket.timestamp > thirty_days, Ticket.timestamp <= sixty_days).all()
    return render_template('thirty.html', point=point)


# shows tickets which are between 60 and 90 days
@app.route('/ninety')
def ninety():
    point = Ticket.query.filter(Ticket.timestamp > sixty_days, Ticket.timestamp <= ninety_days).all()
    return render_template('thirty.html', point=point)


# for showing statistics of all tickets
@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    # form = EachTicket(), Item()
    items = Ticket.query.all()
    # page = request.args.get('page', 1, type=int)
    # item = Ticket.query.order_by(Ticket.timestamp.desc()).paginate(page, app.config['TICKETS_PER_PAGE'], False)
    # next_url = url_for('stats', page=items.next_num) if items.has_next else None
    # prev_url = url_for('stats', page=items.prev_num) if items.has_prev else None
    # table = Stats(items)
    # page = request.args.get('page', 1, type=int)
    # stat = Ticket.query.order_by(Ticket.timestamp.desc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    return render_template('stats.html', items=items)   # , next_url=next_url, prev_url=prev_url, item=item


# for creating tickets
@app.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = CreateTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, content=form.content.data, department=form.department.data,
                        file=form.file.data, priority=form.priority.data, email=form.email.data, name=form.name.data)
        db.session.add(ticket)
        db.session.commit()
        user = Ticket.query.filter_by(email=form.email.data).first()
        if user:
            send_ticket_details(user)
        flash('Ticket submitted successfully')
        return redirect(url_for('index'))
    return render_template('ticket.html', title='Tickets', form=form)


@app.route('/check_ticket_progress/<token>')
def check_ticket_progress(token):
    # progress = Ticket.query.filter_by(id=id).first_or_404()
    user = Ticket.verify_send_ticket_details_token(token)
    if not user:
        return redirect(url_for('index'))
    return render_template('check_ticket_progress.html')


@app.route('/search')
def search():
    posts = Ticket.query.whoosh_search(request.args.get('query')).all()

    return render_template('index.html', posts=posts)


@app.route('/kb', methods=['GET', 'POST'])
def kb():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully')
        return redirect(url_for('index'))
    post = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('kb.html', title='Knowledge Base', post=post, form=form)

# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['inputfile']
#     newfile = File(name=file.name, data=file.read())
#     db.session.add(newfile)
#     db.session.commit()
#     return 'saved' + file.filename + 'to the database'
#
#
# @app.route('/download')
# def download():
#     file_data = File.query.filter_by(id=2).first()
#     return send_file(BytesIO(file_data.data), as_attachment=True)
