import time
from datetime import datetime
from .message_detector import detect_messages

CHECK_INTERVAL = 60

if __name__ == "__main__":
    print("Sathyabama Placement Monitor Started!")
    print("Checking Google Groups every 60 seconds...")

    while True:
        try:
            print(
                f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking..."
            )
            detect_messages()

        except KeyboardInterrupt:
            print("\nMonitor stopped.")
            break

        except Exception as error:
            print("Monitoring error:", error)

        time.sleep(CHECK_INTERVAL)