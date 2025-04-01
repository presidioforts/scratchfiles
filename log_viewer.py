import argparse
import os

LOG_FILE = "agentic_training.log"

def show_logs(lines: int = 20):
    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    with open(LOG_FILE, "r") as f:
        all_lines = f.readlines()
        for line in all_lines[-lines:]:
            print(line.strip())

def clear_logs():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
        print("Log file cleared.")
    else:
        print("No log file to clear.")

def main():
    parser = argparse.ArgumentParser(description="Agentic Log Viewer CLI")
    parser.add_argument("--tail", type=int, default=20, help="Number of log lines to show")
    parser.add_argument("--clear", action="store_true", help="Clear the log file")

    args = parser.parse_args()

    if args.clear:
        clear_logs()
    else:
        show_logs(args.tail)

if __name__ == "__main__":
    main()