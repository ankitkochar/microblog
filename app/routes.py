from app import app
# print(dir(app))

@app.route("/")
@app.route("/index")
def index():
	return "<h1>Hello Duniya</h1>"