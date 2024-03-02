"""
"""

def read_last_two_logs(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            last_two_logs = lines[-2:]
            return last_two_logs
    except FileNotFoundError:
        return None

def extract_addresses(log_entry):
    scaned_date, scaned_time, *addresses = log_entry.split(', ')
    return set(addresses)

def compare_addresses(previous_addresses, current_addresses):
    added_addresses = current_addresses - previous_addresses
    removed_addresses = previous_addresses - current_addresses
    return added_addresses, removed_addresses

def main():
    log_file = 'log.txt'

    last_two_logs = read_last_two_logs(log_file)

    if last_two_logs and len(last_two_logs) == 2:
        previous_log_entry = last_two_logs[0].strip()
        current_log_entry = last_two_logs[1].strip()

        previous_addresses = extract_addresses(previous_log_entry)
        current_addresses = extract_addresses(current_log_entry)

        added, removed = compare_addresses(previous_addresses, current_addresses)

        if added:
            print(f"新しく現れたアドレス: {', '.join(added)}")
        if removed:
            print(f"削除されたアドレス: {', '.join(removed)}")
    else:
        print("前回のログエントリが不足しています。")

if __name__ == "__main__":
    main()

