from http.server import BaseHTTPRequestHandler, HTTPServer
import boto3
import json
import urllib.parse

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_segments = parsed_path.path.split('/')
        
        if len(path_segments) >= 3 and path_segments[1] == 'secrets':
            prefix = path_segments[2]
            secrets = self.get_secrets('/'+prefix)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(secrets).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def get_secrets(self, prefix):
        client = boto3.client('ssm')  # Create a Boto3 client for SSM
        secrets = {}

        # Retrieve all secret parameter values with the specified prefix
        response = client.get_parameters_by_path(Path=prefix, Recursive=True, WithDecryption=True)
        parameters = response['Parameters']
        
        # Add secret values to the 'secrets' dictionary
        for parameter in parameters:
            secrets[parameter['Name']] = parameter['Value']

        return secrets

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

