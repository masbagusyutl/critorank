import time
import requests

def read_authorization_data(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def post_request(url, auth_token):
    headers = {"Authorization": auth_token}
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        print("Request successful.")
    else:
        print(f"Request failed with status code: {response.status_code}")

def countdown_timer(hours):
    total_seconds = hours * 3600
    while total_seconds:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_format = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
        print(f"Restarting in: {time_format}", end='\r')
        time.sleep(1)
        total_seconds -= 1
    print("\nCountdown finished. Restarting process...")

def process_accounts():
    auth_tokens = read_authorization_data('data.txt')
    total_accounts = len(auth_tokens)
    print(f"Total accounts: {total_accounts}")

    for idx, auth_token in enumerate(auth_tokens, start=1):
        print(f"Processing account {idx}/{total_accounts}")
        # End farming
        print("Ending farming...")
        post_request("https://api.cryptorank.io/v0/tma/account/end-farming", auth_token)
        time.sleep(5)  # Wait 5 seconds before starting farming
        # Start farming
        print("Starting farming...")
        post_request("https://api.cryptorank.io/v0/tma/account/start-farming", auth_token)
        if idx < total_accounts:
            print("Waiting 5 seconds before switching accounts...")
            time.sleep(5)
    
    print("All accounts processed. Starting 6-hour countdown...")
    countdown_timer(6)

if __name__ == "__main__":
    while True:
        process_accounts()
