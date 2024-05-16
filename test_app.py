import pytest

def test_basics_route_add(app):
    @app.route('/')
    def root(request, response):
        response.text = "THis is root page"

def test_duplicate_route_add(app):
    @app.route('/')
    def root(request, response):
        response.text = "THis is root page"
    
    with pytest.raises(AssertionError):
        @app.route('/')
        def root2(request, response):
            response.text = "THis is root page"

def test_request_can_sent_by_client(app, test_client):
    @app.route('/')
    def root(request, response):
        response.text = "THis is root page"
    
    assert test_client.get("http://testserver").text == "THis is root page"

@pytest.mark.parametrize("name, expected_response", [
    ("ali", "Hello ali"),
    ("olim", "Hello olim"),
])

def parametrized_test(app, test_client, name, expected_response):
    @app.route('/hello/{name}')
    def greeting(request, response, name):
        response.text = f"Hello {name}"

    assert test_client.get("http://testserver/hello/{name}").text == expected_response
    

def test_class_based(app, test_client):
    @app.route('/books')
    class Books:
        def get(self, request, response):
            response.text = "Books page"

        def post(self, request, response):
            response.status_code = 201
            response.text = "Endpoint to create a book"

    resp = test_client.get("http://testserver/books")
    assert resp.status_code == 200 and resp.text == "Books page"

    resp_post = test_client.post("http://testserver/books")
    assert resp_post.status_code == 201 and resp_post.text == "Endpoint to create a book"

    resp_put = test_client.put("http://testserver/books")
    assert resp_put.status_code == 405 and resp_put.text == "Method Not Allowed"

def test_default_response(app, test_client):
    @app.route('/')
    def root(request, response):
        response.text = "THis is news page"

    resp = test_client.get("http://testserver/news")
    assert resp.status_code == 404 and resp.text == "Page not found"

def test_alternative_handler(app, test_client):
    def new_handler(request, response):
        response.text = "From new handler"

    app.add_route('/new-handler', new_handler)

    resp = test_client.get("http://testserver/new-handler").text == "From new handler"
