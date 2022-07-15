import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import (get_all_entries,
                    get_single_entry,
                    get_searched_entries,
                    delete_entry,
                    create_entry,
                    update_entry)
from views import get_all_moods
from views import get_all_tags

class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server
        """
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is None:
                    response = f"{get_all_moods()}"
            elif resource == "tags":
                if id is None:
                    response = f"{get_all_tags()}"
        #     elif resource == "locations":
        #         if id is not None:
        #             response = f"{get_single_location(id)}"
        #         else:
        #             response = f"{get_all_locations()}"
        #     elif resource == "employees":
        #         if id is not None:
        #             response = f"{get_single_employee(id)}"
        #         else:
        #             response = f"{get_all_employees()}"

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            # see if the query dictionary has an email key
            if query.get('q') and resource == 'entries':
                response = get_searched_entries(query['q'][0])

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        response = None

        # Add a new entry to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "entries":
            response = create_entry(post_body)

        # Encode the new entry and send in response
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "entries":
            success = update_entry(id, post_body)

        # if resource == "locations":
        #     update_location(id, post_body)

        # if resource == "employees":
        #     update_employee(id, post_body)

        # if resource == "customers":
        #     update_customer(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new data and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handles DELETE requests to the server
        """
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        # if resource == "locations":
        #     delete_location(id)

        # if resource == "employees":
        #     delete_employee(id)

        # if resource == "customers":
        #     delete_customer(id)

        # Encode the new entry and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
