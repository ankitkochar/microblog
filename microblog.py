from app import app, db
from app.models import User, Post, Postlike

@app.shell_context_processor
def make_shell_context():
	return {"db":db, "User":User, "Post":Post,"Postlike":Postlike}