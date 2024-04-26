import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt



from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:karam@localhost:5432/finalproject14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from src.models.itinerary import Itinerary
from src.repositories.itinerary_repository import get_itinerary_repo
from src.repositories.post_repository import PostRepository
from src.models.post import Post, Comment
#from src.repositories.user_repository import user_repository



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
    return render_template('index.html')

@app.route('/sign-in', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    return redirect(url_for('index'))



@app.post('/join')
def join():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400)
   # if user_repository.does_email_exist(email):
       # abort(400, "Email already exists")
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    #user_repository.create_user(email, hashed_password)
   # user_info = user_repository.create_user(email, password)
    
   # if isinstance(user_info, Exception):
    #    abort(500, "Failed to create user")
    #return redirect('/')

    
   
# @app.route('/join', methods=['POST'])
# def join():
#     account_type = request.form.get('account_type') 
#     if account_type == 'individual':
#         first_name = request.form['firstName']
#         last_name = request.form['lastName']
#     elif account_type == 'business':
#         company_name = request.form['companyName']
#         ein_number = request.form['einNumber']
    
#     return redirect(url_for('index'))



# View all posts
@app.route('/all_posts')
def all_posts():
    posts = post_repository.get_all_posts()
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
                post["image_filename"] = file.filename
        
        
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

        post = post_repository.create_post(**post_data)
        return redirect(url_for("view_personal_post", post_id=post.id))
    return render_template("personal_post_form.html")


# INCOMPLETE
@app.route("/edit_business_post/<int:post_id>", methods=["GET", "POST"])
def edit_business_post(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    if request.method == "POST":
        post["title"] = request.form.get("postTitle")
        post["country"] = request.form.get("countryVisited")
        post["category"] = request.form.get("eventCategory")
        post["description"] = request.form.get("postDescription")
        post["zip_code"] = request.form.get("zipCode")
        # ---undone
        posts[post_id] = post
        return redirect(url_for("view_business_post", post_id=post_id))
    return render_template("edit_business_post.html", post=post)

# INCOMPLETE
@app.route("/delete_business_post/<int:post_id>")
def delete_business_post(post_id):
    if post_id in posts:
        del posts[post_id]
    return redirect(url_for("view_all_posts"))

# INCOMPLETE
@app.route("/edit_personal_post/<int:post_id>", methods=["GET", "POST"])
def edit_personal_post(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    if request.method == "POST":
        post["title"] = request.form.get("postTitle")
        post["country"] = request.form.get("countryVisited")
        post["category"] = request.form.get("eventCategory")
        post["description"] = request.form.get("postDescription")
        post["rating"] = request.form.get("inlineRadioOptions")
        post["trip_purpose"] = request.form.get("purposeOfTrip")
        post["time_of_visit"] = request.form.get("timeOfVisit")
        # ---undone
        posts[post_id] = post
        return redirect(url_for("view_personal_post", post_id=post_id))
    return render_template("edit_personal_post.html", post=post)

# INCOMPLETE
@app.route("/delete_personal_post/<int:post_id>")
def delete_personal_post(post_id):
    if post_id in posts:
        del posts[post_id]
    return redirect(url_for("view_all_posts"))


# Comment on a post section
@app.route("/add_comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    username = request.form.get("username")
    content = request.form.get("content")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = {
        "username": username,
        "content": content,
        "timestamp": timestamp,
        "edited": False,
    }
    post["comments"].append(comment)
    if post["type"] == "business":
        return redirect(url_for("view_business_post", post_id=post_id))
    else:
        return redirect(url_for("view_personal_post", post_id=post_id))

# INCOMPLETE
@app.route("/edit_comment/<int:post_id>/<int:comment_index>", methods=["POST"])
def edit_comment(post_id, comment_index):
    post = posts.get(post_id)
    if not post or comment_index >= len(post["comments"]):
        return "Comment not found", 404
    post["comments"][comment_index]["content"] = request.form.get("content")
    post["comments"][comment_index]["edited"] = True
    if post["type"] == "business":
        return redirect(url_for("view_business_post", post_id=post_id))
    else:
        return redirect(url_for("view_personal_post", post_id=post_id))


@app.route("/delete_comment/<int:post_id>/<int:comment_index>")
def delete_comment(post_id, comment_index):
    post = posts.get(post_id)
    if not post or comment_index >= len(post["comments"]):
        return "Comment not found", 404
    del post["comments"][comment_index]
    if post["type"] == "business":
        return redirect(url_for("view_business_post", post_id=post_id))
    else:
        return redirect(url_for("view_personal_post", post_id=post_id))


# View a business post by ID
@app.route("/view_business_post/<int:post_id>")
def view_business_post(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    return render_template("view_business_post.html", post=post)


# View a personal post by ID 
@app.route("/view_personal_post/<int:post_id>")
def view_personal_post(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404
    return render_template("view_personal_post.html", post=post)

# Delete a post by ID INCOMPLETE
@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    if post_id in posts:
        del posts[post_id]
    return redirect(url_for("index"))

#Discover Page
@app.get('/DiscoverPage')
def discover_page():
    return render_template('discover_page.html')

@app.get('/discover_page_selected')
def discover_page_selected():
    #posts = Post.query.limit(2).all()
    
    selected_country = request.args.get('country')
    if selected_country is None:
        selected_country = "None" 
    return render_template('discover_page_selected.html', selected_country=selected_country)

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


#End user session
@app.post('/logout')
def logout():
    del session['user_id']
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
