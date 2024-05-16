from app import SimpleFrame

app = SimpleFrame()

@app.route('/')
def root(request, response):
    response.text = "THis is root page"

@app.route('/home')
def home(request, response):
    response.text = "THis is home page"

@app.route('/news')
def news(request, response):
    response.text = "THis is news page"

@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f"Hello {name}"

@app.route('/students')
class Students:
    def get(self, request, response):
        response.text = "Students page"

    def post(self, request, response):
        response.text = "Endpoint to create a student"


def new_handler(request, response):
    response.text = "From new handler"

app.add_route("/new-handler", new_handler)