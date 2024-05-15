from datetime import datetime

# Define a global variable to store the array
global_notification_array = []


def check_due_matches():
    from .models import Match
    data = Match.objects.all()
    # Your task logic goes here
    print('Scheduled task executed to check matches for the day!')
    currentDate = datetime.now().date()
    formattedDate = currentDate.strftime('%Y-%m-%d')

    print(f"{formattedDate}")
    for item in data:
        # print(f"{item.date} and {item.time}")
        date_object1 = datetime.strptime(str(item.date), "%Y-%m-%d")
        date_object2 = datetime.strptime(formattedDate, "%Y-%m-%d")
        if date_object1 == date_object2:
            print(
                f"There is a match for {item.date} by {item.time}, send an email to")
            for player in item.registeredPlayers:
                print(f"email address : {str(player['email'])}")

    return None
