from flask import Flask,render_template,url_for

app=Flask(__name__)
@app.route("/about")
def about():
	return render_template("about.html")
	
@app.route("/index")
def index():
	return render_template("index.html")
	
@app.route("/post")
def post():
	return render_template("blog-post.html")
	
@app.route("/profile")
def profile():
	return render_template("profile.html")
@app.route("/")
def home():
	return render_template("layout.html")
	
if __name__=="__main__":
	app.run(debug=True)
	
