import schedule
import time
from plyer import notification

def send_reminder(message):
    notification.notify(
        title='Reminder!',
        message=message,
        app_name='Python Reminder',
        timeout=10
    )
    print(f"Reminder sent: '{message}'")


print("What would you like to be reminded of?")
reminder_message = input()

print("In how many minutes would you like to be reminded?")
interval = float(input())

schedule.every(interval).minutes.do(send_reminder, message= f"It's time to {reminder_message}")

print(f"Great! I will remind you to '{reminder_message}' every {interval} minutes. You can now minimize this window but DO NOT CLOSE IT")

while True:
    schedule.run_pending()
    time.sleep(1)