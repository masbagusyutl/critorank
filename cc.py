import time
import requests

def read_authorization_data(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def post_request(url, auth_token):
    headers = {"Authorization": auth_token}
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed with status code: {response.status_code}")
        return None

def get_request(url, auth_token):
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed with status code: {response.status_code}")
        return None

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

def process_tasks(auth_token):
    tasks = get_request("https://api.cryptorank.io/v0/tma/account/tasks", auth_token)
    if tasks:
        for task in tasks:
            task_name = task['name']
            if not task['isDone']:
                print(f"Processing task: {task_name}")
                task_id = task['id']
                task_claim_url = f"https://api.cryptorank.io/v0/tma/account/claim/task/{task_id}"
                response = post_request(task_claim_url, auth_token)
                if response:
                    balance = response.get('balance', 'Unknown')
                    print(f"Task {task_name} completed. Balance: {balance}")
                time.sleep(2)  # Wait 2 seconds between each task
            else:
                print(f"Task {task_name} is already completed.")

def process_accounts():
    auth_tokens = read_authorization_data('data.txt')
    total_accounts = len(auth_tokens)
    print(f"Total accounts: {total_accounts}")

    for idx, auth_token in enumerate(auth_tokens, start=1):
        print(f"Processing account {idx}/{total_accounts}")

        # End farming
        print("Ending farming...")
        end_response = post_request("https://api.cryptorank.io/v0/tma/account/end-farming", auth_token)
        if end_response:
            balance = end_response.get('balance', 'Unknown')
            print(f"Balance after ending farming: {balance}")
        
        time.sleep(5)  # Wait 5 seconds before starting farming

        # Start farming
        print("Starting farming...")
        post_request("https://api.cryptorank.io/v0/tma/account/start-farming", auth_token)

        # Get account info
        account_info = get_request("https://api.cryptorank.io/v0/tma/account", auth_token)
        if account_info:
            balance = account_info.get('balance', 'Unknown')
            print(f"Account balance: {balance}")

        # Process tasks
        process_tasks(auth_token)
        
        if idx < total_accounts:
            print("Waiting 5 seconds before switching accounts...")
            time.sleep(5)
    
    print("All accounts processed. Starting 6-hour countdown...")
    countdown_timer(6)

if __name__ == "__main__":
    while True:
        process_accounts()
