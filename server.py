from http.server import BaseHTTPRequestHandler, HTTPServer
import boto3
import json
import urllib.parse
import os

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path_segments = parsed_path.path.split('/')
        
        if len(path_segments) >= 3 and path_segments[1] == 'secrets':
            prefix = path_segments[2]
            try:
                secrets = self.get_secrets('/'+prefix)
                env_vars = self.get_environment_variables()
                response_data = {"secrets": secrets, "environment_variables": env_vars}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error retrieving secrets: {str(e)}'.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def get_secrets(self, prefix):
        client = boto3.client('ssm')  # Create a Boto3 client for SSM
        secrets = {}

        try:
            # Retrieve all secret parameter values with the specified prefix using pagination
            paginator = client.get_paginator('get_parameters_by_path')
            response_iterator = paginator.paginate(Path=prefix, Recursive=True, WithDecryption=True)
        except Exception as e:
            raise Exception(f'Error retrieving secrets: {str(e)}')
           
        # Iterate through the paginated responses and add secret values to the 'secrets' dictionary
        for response in response_iterator:
            try:
                parameters = response['Parameters']
                for parameter in parameters:
                    secrets[parameter['Name']] = parameter['Value']
            except Exception as e:
                pass

        return secrets

    def get_environment_variables(self):
        env_vars = {}

        # Retrieve all environment variables
        for key, value in os.environ.items():
            env_vars[key] = value

        return env_vars

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
