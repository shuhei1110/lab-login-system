"""log file ctl
"""

from typing import Union

def read_last_two_logs(filename:str) -> Union[bool, list]:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            line_count = len(lines)
            if line_count < 2:
                return False
            else:
                last_two_logs = lines[-2:]
                return last_two_logs
    except FileNotFoundError:
        return None

def extract_addresses(log_entry:str) -> set:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    scaned_date, scaned_time, *addresses = log_entry.split(', ')
    return set(addresses)

def compare_addresses(previous_addresses, current_addresses) -> set:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    added_addresses = current_addresses - previous_addresses
    removed_addresses = previous_addresses - current_addresses
    return added_addresses, removed_addresses

def analyze_log(log_file:str) -> list:
    """

        Args:
            ():

        Responses
            (): 

        Notes:

    """
    last_two_logs = read_last_two_logs(log_file)

    if last_two_logs:
        previous_log_entry = last_two_logs[0].strip()
        current_log_entry = last_two_logs[1].strip()

        previous_addresses = extract_addresses(previous_log_entry)
        current_addresses = extract_addresses(current_log_entry)

        added, removed = compare_addresses(previous_addresses, current_addresses)

        if added:
            result_added = added
        else:
            result_added = None
        if removed:
            result_removed = removed
        else:
            result_removed = None
        
        return [True, result_added, result_removed]
        
    else:
        return [None]



