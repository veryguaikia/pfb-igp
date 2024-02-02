import csv

def analyze_cash_on_hand(csv_path):
    """
    Reads the MonsoonSim cash-on-hand CSV file and:
    - Specifically analyzes the cash-on-hand column.
    - Calculates daily differences in cash-on-hand.
    - Identifies trends such as increasing, decreasing, or fluctuating patterns.

    Parameters:
    csv_path (str): The file path of the CSV file to be analyzed.

    Returns:
    str: A description of the cash-on-hand trend along with specific details.
        - For an increasing trend, it returns the day with the highest increment.
        - For a decreasing trend, it returns the day with the highest decrement.
        - For a fluctuating trend, it prints all deficit days and returns the top 3 highest deficits.
    """
    # Read the CSV file
    with open(csv_path, mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader) 

        # Initialize an empty list for the cash-on-hand records
        coh_records = []
        for row in reader:
            # Convert the first two elements of each row to integers
            record = [int(row[0]), int(row[1])]  
            # Append the converted record to the list
            coh_records.append(record)  

    # Initialize an empty list for the daily differences
    daily_differences = []

    # Iterate over the cash-on-hand record in pairs
    for previous_record, current_record in zip(coh_records, coh_records[1:]):
        # Extract the day and value from each record
        previous_day, previous_value = previous_record
        current_day, current_value = current_record

        # Calculate the difference in values between the current and previous record
        difference = current_value - previous_value

        # Append the day and the calculated difference to the daily differences list
        daily_differences.append((current_day, difference))

    # Determine the trend based on daily differences
    increasing = all(diff[1] > 0 for diff in daily_differences)
    decreasing = all(diff[1] < 0 for diff in daily_differences)

# Analysis based on trend
    if increasing:
        # Initialise the highest increment with the first value in daily_differences
        highest_increment = daily_differences[0]

        # Iterate through each daily difference
        for diff in daily_differences:
            # If the current difference is greater than the highest recorded increment,
            # update the highest increment
            if diff[1] > highest_increment[1]:
                highest_increment = diff

        # Open the file "summary_report.txt" in append mode
        with open("summary_report.txt", "a") as file:
            # Write a line indicating a general cash surplus trend
            file.write("[CASH SURPLUS] CASH-ON-HAND ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            # Write details of the day with the highest cash surplus and its amount
            file.write(f"[HIGHEST CASH SURPLUS] DAY: {highest_increment[0]}, AMOUNT: SGD{highest_increment[1]}\n")
    
    elif decreasing:
    # Initialise the highest decrement with the first value in daily_differences
        highest_decrement = daily_differences[0]

        # Iterate through each daily difference
        for diff in daily_differences:
        # If the current difference is less than the highest recorded decrement,
        # update the highest decrement
            if diff[1] < highest_decrement[1]:
                highest_decrement = diff
                
        # Open the file "summary_report.txt" in append mode
        with open("summary_report.txt", "a") as file:
            # Write a line indicating a general cash deficit trend
            file.write("[CASH DEFICIT] CASH-ON-HAND ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            # Write details of the day with the highest cash deficit and its amount,
            # ensuring the deficit amount is positive by taking its absolute value
            file.write(f"[HIGHEST CASH DEFICIT] DAY: {highest_decrement[0]}, AMOUNT: SGD{abs(highest_decrement[1])}\n")

    else:
        # Initialize a list to store deficits
        deficits = []

        # Iterate over daily differences and directly add deficits to the list
        for diff in daily_differences:
            if diff[1] < 0:
                # Store the day and the positive value of the deficit
                deficits.append((diff[0], -diff[1]))  # Convert deficit to positive

        # Function to return the second element of the list
        def sort_by_amount(item):
            """
            - Returns the second element of a list.
            - Function has one parameter, item.
            """
            return item[1]

        # Sort the deficits in descending order based on the amount to find the top 3 highest deficits
        deficits.sort(key=sort_by_amount, reverse=True)

        # Extract the top 3 highest deficits
        highest_deficit = deficits[0] if deficits else None
        second_highest_deficit = deficits[1] if len(deficits) > 1 else None
        third_highest_deficit = deficits[2] if len(deficits) > 2 else None

        # Sort the deficits by day for the summary report
        deficits.sort()

        with open("summary_report.txt", "a") as file:
            # Recording all deficit days, ordered by day
            for deficit in deficits:
                coh = f"[CASH DEFICIT] DAY: {deficit[0]}, AMOUNT: SGD{deficit[1]}\n"
                file.write(coh)

            # Recording the top 3 highest deficit days
            if highest_deficit:
                highest = f"[HIGHEST CASH DEFICIT] DAY: {highest_deficit[0]}, AMOUNT: SGD{highest_deficit[1]}\n"
            if second_highest_deficit:
                second_highest = f"[2ND HIGHEST CASH DEFICIT] DAY: {second_highest_deficit[0]}, AMOUNT: SGD{second_highest_deficit[1]}\n"
            if third_highest_deficit:
                third_highest = f"[3RD HIGHEST CASH DEFICIT] DAY: {third_highest_deficit[0]}, AMOUNT: SGD{third_highest_deficit[1]}\n"
                file.write(highest + second_highest + third_highest)
