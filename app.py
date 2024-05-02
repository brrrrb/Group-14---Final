import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt



load_dotenv()
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))



app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')
bcrypt = Bcrypt(app)

# Database configuration Co-Pilot Assistance
app.secret_key = os.getenv('APP_SECRET_KEY', 'default_fallback_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONNECTION_STRING', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from src.models.itinerary import Itinerary
from src.repositories.itinerary_repository import get_itinerary_repo
from src.repositories.post_repository import PostRepository
from src.models.post import Post, Comment


from src.repositories.user_repository import does_username_exist, create_user, get_user_by_username, get_user_by_id, create_business_user



itinerary_repository = get_itinerary_repo()
post_repository = PostRepository()

# Personal and Business form directories and allowed extentions
Images = os.path.join("static", "images")
Extensions = {"png", "jpg", "jpeg"} 

# Dictionary to store posts
posts = {}

days = 0
day_number = 1 


#HOME PAGE 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/secret')
    return render_template('index.html')

@app.route('/secret')
def secret_page():
    if 'user_id' not in session:
        return redirect('/')

    user = get_user_by_id(session['user_id'])
    if not user:
        flash('User not found. Please log in again.', 'error')
        return redirect('/login')

    # Check what data is available and create a display name accordingly
    if 'company_name' in user and user['company_name']:
        display_name = user['company_name']
    elif 'first_name' in user and 'last_name' in user and user['first_name'] and user['last_name']:
        display_name = f"{user['first_name']} {user['last_name']}"
    else:
        display_name = "Anonymous"  # Default name if no name details are available

    return render_template('secret.html', user=user, display_name=display_name)





@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    if not username or not password or not first_name or not last_name:
        abort(400, "All fields are required")
    if does_username_exist(username):
        abort(400, 'Username already exists')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = create_user(first_name, last_name, username, hashed_password)
    session['user_id'] = user['user_id']  # Stores user ID in session immediately after signup
    session['username'] = user['username']  # Stores username in session
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']
    return redirect('/secret')




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = get_user_by_username(username)
    if user and bcrypt.check_password_hash(user['hashed_password'], password):
        session['user_id'] = user['user_id']
        session['username'] = username
        if user.get('company_name'):
            session['company_name'] = user['company_name']
            session.pop('first_name', None)
            session.pop('last_name', None)
        else:
            session['first_name'] = user.get('first_name')
            session['last_name'] = user.get('last_name')
            session.pop('company_name', None)
        return redirect('/secret')
    else:
        return abort(401, 'Invalid credentials')



@app.route('/signup_business', methods=['POST'])
def signup_business():
    company_name = request.form.get('companyName')
    ein_number = request.form.get('einNumber')
    username = request.form.get('businessUsername')
    password = request.form.get('businessPassword')

    if not company_name or not ein_number or not username or not password:
        abort(400, "All fields are required")
    
    if len(ein_number) != 9 or not ein_number.isdigit():
        abort(400, "EIN must be exactly 9 digits")
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        user = create_business_user(company_name, ein_number, username, hashed_password)
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['company_name'] = user['company_name']
        return redirect('/secret')
    except Exception as e:
        return abort(400, str(e))





@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('company_name', None)
    session.clear()
    return redirect('/')






# View all posts
@app.route('/all_posts')
def all_posts():
    posts = Post.query.all()
    return render_template('all_posts.html', posts=posts)

@app.route('/view_post_details/<int:post_id>')
def view_post_details(post_id):
    post = post_repository.get_post_by_id(post_id)
    if post.type == 'business':
        return render_template('view_business_post.html', post=post)
    else:
        return render_template('view_personal_post.html', post=post)

# Business form submission
@app.route("/business_post_form", methods=["GET", "POST"])
def business_post_form():
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("business_post_form"))
        post_data = {
            "title": request.form.get("postTitle"),
            "description": request.form.get("postDescription"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "posted_at": datetime.now(),
            "type": "business",
            # Business fields
            "address_line_1": request.form.get("addressLine1"),
            "city": request.form.get("city"),
            "zip_code": request.form.get("zipCode"),
            "state": request.form.get("state"),
            "website_link": request.form.get("websiteLink"),
            "phone_number": request.form.get("phoneNumber"),
            "email": request.form.get("email"),
            "hours_of_operation": request.form.get("hoursOfOperation"),
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and file.filename:
            if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() in Extensions:
                filepath = os.path.join(Images, file.filename)
                file.save(filepath)
                post_data["image_filename"] = file.filename
        
        
        post = post_repository.create_post(**post_data)
        return redirect(url_for("view_business_post", post_id=post.id))
    return render_template("business_post_form.html")


# Personal form submission
@app.route("/personal_post_form", methods=["GET", "POST"])
def personal_post_form():
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("personal_post_form"))
        post_data = {
            "title": request.form.get("postTitle"),
            "description": request.form.get("postDescription"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "posted_at": datetime.now(),
            "type": "personal",
            # Personal fields
            "trip_purpose": request.form.get("purposeOfTrip"),
            "time_of_visit": request.form.get("timeOfVisit"),
            "rating": request.form.get("inlineRadioOptions"),
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and file.filename:
            if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() in Extensions:
                filepath = os.path.join(Images, file.filename)
                file.save(filepath)
                post_data["image_filename"] = file.filename

        post = post_repository.create_post(**post_data)
        return redirect(url_for("view_personal_post", post_id=post.id))
    return render_template("personal_post_form.html")

@app.route("/edit_business_post/<int:post_id>", methods=["GET", "POST"])
def edit_business_post(post_id):
    post = post_repository.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    if request.method == "POST":
        post_data = {
            "title": request.form.get("postTitle"),
            "description": request.form.get("postDescription"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "posted_at": datetime.now(),
            "type": "business",
            # Business fields
            "address_line_1": request.form.get("addressLine1"),
            "city": request.form.get("city"),
            "zip_code": request.form.get("zipCode"),
            "state": request.form.get("state"),
            "website_link": request.form.get("websiteLink"),
            "phone_number": request.form.get("phoneNumber"),
            "email": request.form.get("email"),
            "hours_of_operation": request.form.get("hoursOfOperation"),
        }
        updated_post = post_repository.update_post(post_id, **post_data)
        if updated_post:
            return redirect(url_for("view_business_post", post_id=post_id))
        else:
            return "Error updating post", 500
    return render_template("edit_business_post.html", post=post)

@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    success = post_repository.delete_post(post_id)
    if success:
        return redirect(url_for("all_posts"))
    else:
        return "Error deleting post", 500
    
@app.route("/edit_personal_post/<int:post_id>", methods=["GET", "POST"])
def edit_personal_post(post_id):
    post = post_repository.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    if request.method == "POST":
        # Collect data from form and update post
        post_data = {
            "title": request.form.get("postTitle"),
            "description": request.form.get("postDescription"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "posted_at": datetime.now(),
            "type": "personal",
            "trip_purpose": request.form.get("purposeOfTrip"),
            "time_of_visit": request.form.get("timeOfVisit"),
            "rating": request.form.get("inlineRadioOptions"),

            # Include other fields as necessary
        }
        updated_post = post_repository.update_post(post_id, **post_data)
        if updated_post:
            return redirect(url_for("view_personal_post", post_id=post_id))
        else:
            return "Error updating post", 500
    return render_template("edit_personal_post.html", post=post)

@app.route("/delete_personal_post/<int:post_id>", methods=["POST"])
def delete_personal_post(post_id):
    success = post_repository.delete_post(post_id)
    if success:
        return redirect(url_for("all_posts"))
    else:
        return "Error deleting post", 500

# Comment on a post section
@app.route("/add_comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('all_posts'))

    username = request.form.get("username")
    content = request.form.get("content")
    if not username or not content:
        flash('Username and content are required.', 'error')
        return redirect(url_for('view_personal_post' if post.type == 'personal' else 'view_business_post', post_id=post_id))

    new_comment = Comment(username=username, content=content, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('view_personal_post' if post.type == 'personal' else 'view_business_post', post_id=post_id))

@app.route("/edit_comment/<int:post_id>/<int:comment_id>", methods=["POST"])
def edit_comment(post_id, comment_id):
    edited_content = request.form.get('edited_content')
    if not edited_content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('show_edit_comment_form', post_id=post_id, comment_id=comment_id))
    
    comment = Comment.query.get(comment_id)
    if comment:
        comment.content = edited_content
        comment.edited = True
        db.session.commit()
        return redirect(url_for('view_post_details', post_id=post_id))
    else:
        flash('Comment not found.', 'error')
        return redirect(url_for('all_posts'))

@app.route("/edit_comment/<int:post_id>/<int:comment_id>")
def show_edit_comment_form(post_id, comment_id):
    post = post_repository.get_post_by_id(post_id)
    comment = Comment.query.get(comment_id)
    if not post or not comment:
        flash("Post or Comment not found", "error")
        return redirect(url_for('all_posts'))
    return render_template("edit_comment.html", post_id=post_id, comment=comment)


@app.route("/delete_comment/<int:post_id>/<int:comment_id>", methods=["POST"])
def delete_comment(post_id, comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    else:
        return "Comment not found", 404

    post = Post.query.get(post_id)
    if post:
        if post.type == 'business':
            return redirect(url_for('view_business_post', post_id=post_id))
        else:
            return redirect(url_for('view_personal_post', post_id=post_id))
    return redirect(url_for('all_posts'))


# View a business post by ID
@app.route("/view_business_post/<int:post_id>")
def view_business_post(post_id):
    post = post_repository.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    return render_template("view_business_post.html", post=post)

# View a personal post by ID 
@app.route("/view_personal_post/<int:post_id>")
def view_personal_post(post_id):
    post = post_repository.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    return render_template("view_personal_post.html", post=post)

#Discover Page
@app.get('/DiscoverPage')
def discover_page():
    return render_template('discover_page.html')

@app.get('/discover_page_selected')
def discover_page_selected():
    selected_country = request.args.get('country')
    if selected_country is None:
        selected_country = "None"
    if selected_country != "None":
        posts = Post.query.filter_by(country=selected_country).all()
    else:
        posts = Post.query.all()
    return render_template('discover_page_selected.html', selected_country=selected_country, posts=posts)


@app.get("/all_itineraries_page")
def all_itineraries():
    itineraries = itinerary_repository.get_all_itineraries().values()
    return render_template("all_itineraries_page.html", itineraries=itineraries)

@app.get('/itinerary_creation')
def itinerary_creation():
    return render_template('itinerary_creation_page.html')


@app.post('/itinerary_creation_step_2')
def itinerary_creation_step_2():
    global days, day_number

    name = request.form['name']
    destination = request.form['destination']
    disembark_date = request.form['disembark_date']
    days = int(request.form['days'])
    day_number = 1 

   
    user_itinerary=itinerary_repository.create_itinerary(name, destination, disembark_date, days)
    print(user_itinerary.itinerary_id)
    print(user_itinerary.name)
    print(user_itinerary.destination)

    itinerary_id = user_itinerary.itinerary_id

    return redirect(url_for('add_activities', itinerary_id=itinerary_id, day_number=day_number))


@app.get('/add_activities/<int:itinerary_id>/<int:day_number>')
def add_activities(itinerary_id, day_number):
    
    itinerary=itinerary_repository.get_itinerary_by_id(itinerary_id)
    if not itinerary:
        return abort(400)
    
    print(itinerary.days)

    if day_number > itinerary.days:
        #redirct to the page they were just on
        return abort(400)

    return render_template('itinerary_creation_step2.html', itinerary_id=itinerary_id, day_number=day_number, itinerary=itinerary, day=itinerary.days)

@app.post('/add_activities/<int:itinerary_id>/<int:day_number>')
def add_activities_post(itinerary_id, day_number):
    global days

    activity = request.form['activity']
    description = request.form['description']
    
    itinerary=itinerary_repository.get_itinerary_by_id(itinerary_id)
    if not itinerary:
        return abort(400)
    
    if day_number > itinerary.days:
        return abort(400)
    
        
    itinerary.add_activity(day_number, activity, description)
    itinerary_repository.update_itinerary(itinerary_id, itinerary.activities)

    print(itinerary.activities)
    print(description)

    if day_number < itinerary.days:
        return redirect(url_for('add_activities', itinerary_id=itinerary_id, day_number=day_number+1))
    else:
        #return redirect(url_for('view_itinerary', itinerary_id=itinerary_id, days=itinerary.days))
        return redirect(url_for('all_itineraries'))
    

    #return redirect(url_for('view_itinerary', itinerary_id=itinerary_id, days=itinerary.days))
    
@app.get('/view_itinerary/<int:itinerary_id>')
def view_itinerary(itinerary_id):

    itinerary=itinerary_repository.get_itinerary_by_id(itinerary_id)

    if itinerary:
        return render_template('view_itinerary.html', itinerary=itinerary)
        #return render_template('view_itinerary.html', itinerary=itinerary, zip=zip)
    else:
        return "Itinerary not found"
    
@app.get('/delete_itinerary/<int:itinerary_id>')
def delete_itinerary(itinerary_id):
    itinerary_repository.delete_itinerary(itinerary_id)
    return redirect(url_for('all_itineraries'))

@app.get('/edit_itinerary/<int:itinerary_id>')
def edit_itinerary(itinerary_id):
    itinerary=itinerary_repository.get_itinerary_by_id(itinerary_id)

    if not itinerary:
        return abort(400)
    
    countries = ["Puerto Rico", "Italy", "Greece", "Hawaii","Jamaica", "Brazil", "Sweeden",  "Australia"]
    return render_template('edit_itinerary.html', itinerary=itinerary, countries=countries)

@app.post('/edit_itinerary/<int:itinerary_id>')
def edit_itinerary_post(itinerary_id):
    global days

    name = request.form['name']
    destination = request.form['destination']
    disembark_date = request.form['disembark_date']
    days = int(request.form['days'])

    itinerary=itinerary_repository.get_itinerary_by_id(itinerary_id)
    

    if not itinerary:
        return abort(400)
    
    itinerary.name = name
    itinerary.destination = destination
    itinerary.disembark_date = disembark_date

    print(itinerary)
    print(itinerary.name)
    print(itinerary.destination)
    print(itinerary.itinerary_id) 

    activities = {}


    for day in range(1, days + 1):
        activities[day] = []
        index = 0
        while f'activities[{day}][{index}][activity]' in request.form:
            activity = request.form[f'activities[{day}][{index}][activity]']
            description = request.form[f'activities[{day}][{index}][description]']
            activities[day].append({"activity": activity, "description": description})
            index += 1

    itinerary.activities = activities

    # Update the itinerary in the repository
    #updated_itinerary = itinerary_repository.update_itinerary(itinerary_id, itinerary)
    # if updated_itinerary is None:
    #     return abort(500, "Failed to update itinerary")

    return redirect(url_for('view_itinerary', itinerary_id=itinerary_id))

if __name__ == '__main__':
    app.run(debug=True)
