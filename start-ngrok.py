import argparse
import json
from pyngrok import ngrok, conf
import os
import psutil
import signal
import socket
import sys
import subprocess

def get_saved_data():
    # Attempt to read saved data from 'data.json'
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Return None if the file doesn't exist or is not properly formatted
        return None

def save_data(data):
    # Save the provided data to 'data.json'
    with open('data.json', 'w') as file:
        json.dump(data, file)

def signal_handler(sig, frame):
    # Handle Ctrl+C signal, print a message, and exit the script
    print('You pressed Ctrl+C!')
    sys.exit(0)

def is_port_in_use(port):
    # Check if a specified port is in use on localhost
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_and_terminate_process(port):
    # Find and terminate a process using a specified port
    for process in psutil.process_iter(['pid', 'name', 'connections']):
        for conn in process.info.get('connections', []):
            if conn.laddr.port == port:
                print(f"Port {port} is in use by process {process.info['name']} (PID {process.info['pid']})")
                try:
                    # Attempt to terminate the process
                    process.terminate()
                    print(f"Terminated process with PID {process.info['pid']}")
                except psutil.NoSuchProcess:
                    print(f"Process with PID {process.info['pid']} not found")

def main():
    # Default port for the application
    target_port = 7865
    
    # Check if the target port is in use, terminate the process if it is
    if is_port_in_use(target_port):
        find_and_terminate_process(target_port)
    else:
        print(f"Port {target_port} is free.")

    # Argument parsing for token, domain, and reset
    parser = argparse.ArgumentParser(description='Console app with token and domain arguments')
    parser.add_argument('--token', help='Specify the token')
    parser.add_argument('--domain', help='Specify the domain')
    parser.add_argument('--reset', action='store_true', help='Reset saved data')

    args = parser.parse_args()

    # Retrieve saved data from 'data.json'
    saved_data = get_saved_data()

    # Check if the reset flag is provided, reset saved data if true
    if args.reset:
        if saved_data is not None:
            saved_data = {'token': '', 'domain': ''}
    else:
        # If not resetting, update saved data based on provided token and domain arguments
        if saved_data is not None:
            if args.token:
                saved_data['token'] = args.token
            if args.domain:
                saved_data['domain'] = args.domain
        else:
            saved_data = {'token': '', 'domain': ''}

    # If token is not provided, prompt the user for input
    if args.token is None:
        if saved_data and saved_data['token']:
            args.token = saved_data['token']
        else:
            args.token = input('Enter the token: ')
            if args.token == '':
                args.token = input('Enter the token: ')
            saved_data['token'] = args.token

    # If domain is not provided, prompt the user for input
    if args.domain is None:
        args.domain = ''
        if saved_data and saved_data['domain']:
            args.domain = saved_data['domain']
        else:
            args.domain = input('Enter the domain: ')
            saved_data['domain'] = args.domain

    # Save the updated data to 'data.json'
    save_data(saved_data)

    # Print the token and domain
    print(f'Token: {args.token}')
    print(f'Domain: {args.domain}')
    
    # If a token is provided, set up ngrok, start the main application, and wait for Ctrl+C to exit
    if args.token != '':
        ngrok.kill()
        srv = ngrok.connect(target_port, pyngrok_config=conf.PyngrokConfig(auth_token=args.token),
                            bind_tls=True, domain=args.domain).public_url
        print(srv)

        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        # Start the main application using a subprocess
        cmd = 'python Fooocus/entry_with_update.py --always-high-vram'
        env = os.environ.copy()
        subprocess.run(cmd, shell=True, env=env)
        
        # Wait for Ctrl+C to exit
        signal.pause()
    else:
        print('An ngrok token is required. You can get one on https://ngrok.com')

if __name__ == '__main__':
    main()
