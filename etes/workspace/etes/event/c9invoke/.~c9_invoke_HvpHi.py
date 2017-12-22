from etes import app #dir = etes directory

@app.route('/')
@app.route('/index')
def index():
    return ("Hello World!")
    






























