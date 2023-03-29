# Import flask module
from flask import Flask
from flask import request
from pulp_optimization import get_itinerary
 
app = Flask(__name__)
 
@app.route('/')
def index():
    #day = request.args.get('day')
    #budget = request.args.get('budget')
    ids = request.args.get('stands')
    # Some params for personalization missing
    return get_itinerary(0, 0, ids)
 
# main driver function
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5902)
