import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# Personal and Business form directories and allowed extentions
Images = os.path.join("static", "images")
Extensions = {"png", "jpg", "jpeg"} 

# Dictionary to store posts
posts = {}

itineraries = [
    {'id': 1, 'name': 'Trip to Paris', 'destination': 'France', 'disembark_date': '2024-04-01'},
    {'id': 2, 'name': 'Beach vacation', 'destination': 'Maldives', 'disembark_date': '2024-07-15'}
]
days = 0
day_number = 1 

@app.get('/')
def index():
    return render_template('index.html')

# Business form submission
@app.route("/business_post_form", methods=["GET", "POST"])
def business_post_form():
    # Collects information from user's submitted form
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("business_post_form"))
        post = {
            "title": request.form.get("postTitle"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "description": request.form.get("postDescription"),
            "address_line_1": request.form.get("addressLine1"),
            "address_line_2": request.form.get("addressLine2"),
            "city": request.form.get("city"),
            "zip_code": request.form.get("zipCode"),  # Add ZIP code
            "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "state": request.form.get("state"),
            "website_link": request.form.get("websiteLink"),
            "phone_number": request.form.get("phoneNumber"),
            "email": request.form.get("email"),
            "hours_of_operation": request.form.get("hoursOfOperation"),
            "type": "business",
            "agreement_check": request.form.get("agreementCheck"),
            "comments": [],
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and file.filename:
            if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() in Extensions:
                filepath = os.path.join(Images, file.filename)
                file.save(filepath)
                post["image_filename"] = file.filename
        
        post_id = len(posts) + 1  # Assign unique ID to post
        post["id"] = post_id
        posts[post_id] = post  # Store post in dictionary

        return redirect(url_for("view_business_post", post_id=post_id))
    return render_template("business_post_form.html")


# Personal form submission
@app.route("/personal_post_form", methods=["GET", "POST"])
def personal_post_form():
    # Collects information from user's submitted form
    if request.method == "POST":
        if not request.form.get("agreementCheck"):
            return redirect(url_for("personal_post_form"))
        post = {
            "title": request.form.get("postTitle"),
            "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "country": request.form.get("countryVisited"),
            "category": request.form.get("eventCategory"),
            "description": request.form.get("postDescription"),
            "rating": request.form.get("inlineRadioOptions"),
            "trip_purpose": request.form.get("purposeOfTrip"),
            "time_of_visit": request.form.get("timeOfVisit"),
            "type": "personal",
            "agreement_check": request.form.get("agreementCheck"),
            "comments": [],
        }
        # Uploads image file
        file = request.files.get("addPictures")
        if file and file.filename:
            if "." in file.filename and file.filename.rsplit(".", 1)[1].lower() in Extensions:
                filepath = os.path.join(Images, file.filename)
                file.save(filepath)
                post["image_filename"] = file.filename

        post_id = len(posts) + 1  # Assign unique ID to post
        post["id"] = post_id
        posts[post_id] = post  # Store post in dictionary

        return redirect(url_for("view_personal_post", post_id=post_id))
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
    selected_country = request.args.get('country')
    if selected_country is None:
        selected_country = "None" 
    return render_template('discover_page_selected.html', selected_country=selected_country)

@app.route("/all_itineraries_page")
def all_itineraries():

    return render_template("all_itineraries_page.html", itineraries=itineraries)

@app.route("/edit_itinerary/<int:id>")
def edit_itinerary(id):
    
    return render_template("edit_itinerary.html")

@app.route("/delete_itinerary/<int:id>")
def delete_itinerary(id):

    return render_template("delete_itinerary.html")

@app.route('/itinerary_creation', methods=['GET', 'POST'])
def itinerary_creation():
    global days
    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        disembark_date = request.form['disembark_date']
        days = int(request.form['days'])

        day_number = 1 

        itinerary = {'id': len(itineraries) + 1, 'name': name, 'destination': destination, 'disembark_date': disembark_date}
        itineraries.append(itinerary)

        return redirect(url_for("itinerary_creation_step_2", day_number=day_number))

    return render_template('itinerary_creation_page.html', itineraries=itineraries)


@app.route('/itinerary_creation_step_2/<int:day_number>', methods=['GET', 'POST'])
def itinerary_creation_step_2(day_number):
    global days
    activities = []  # Initialize empty list for activities
    descriptions = []  # Initialize empty list for descriptions

    if day_number > days:
        #return "Error: Invalid day number"
        #Go to the all itineraries page.
        return redirect(url_for('all_itineraries'))
    
    if len(activities) != len(descriptions):
            return "Error: Number of activities and descriptions don't match"
    
    for activity, description in zip(activities, descriptions):
        #Process each activity and description here (temporary print statements for now)
        print("Activity: ", activity)
        print("Description: ", description)

    if request.method == 'POST':
        activities = request.form.getlist('activity')
        descriptions = request.form.getlist('description')

        if 'add_another' in request.form and len(activities) < 3:
            if day_number < days:

                return redirect(url_for('itinerary_creation_step_2', day_number=day_number + 1))
            else:
                return "It's the last day"
            
        else:
            return redirect(url_for('next_day', day_number=day_number))
    
    return render_template('itinerary_creation_step2.html', day_number=day_number)

@app.route('/next_day/<int:day_number>')
def next_day(day_number):
    next_day_number = day_number + 1
    return redirect(url_for("itinerary_creation_step_2", day_number=next_day_number))

if __name__ == '__main__':
    app.run(debug=True)
