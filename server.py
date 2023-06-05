from flask_app import app
from flask_app.controllers import users, shows

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
	
if __name__=="__main__":
	app.run(debug=True)