from home import Home
from utils.notifications import start_notification_loop

if __name__ == "__main__":
    start_notification_loop()
    Home().run()
