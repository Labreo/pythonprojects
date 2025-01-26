#
import requests
def  get_data():
    print("Enter your username:")
    name=input('')

    url=f"https://api.github.com/users/{name}/events"
    response = requests.get(url)
    if response.status_code == 200:
        print("This username is valid!")
        return response.json()
    else:
        print("Invalid username")

def parse_events(git):
    if not git:
        print("No events found")
        return None

    else:
        for event in git:
            event_type = event['type']
            repo_name = event['repo']['name']
            Link = event['repo']['url']
            print(f"{event_type} on repository: {repo_name} {Link}")

github = get_data()
parse_events(github)


