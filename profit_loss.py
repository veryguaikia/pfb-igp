import csv

def analyze_netprofit(csv_path):
    """
    Reads the MonsoonSim profit-and-loss CSV file and:
    - Specifically analyzes the net profit column.
    - Calculates daily differences in net profit.
    - Identifies trends such as increasing, decreasing, or fluctuating patterns.

    Parameters:
    csv_path (str): The file path of the CSV file to be analyzed.

    Returns:
    str: A description of the net profit trend along with specific details.
        - For an increasing trend, it returns the day with the highest increment.
        - For a decreasing trend, it returns the day with the highest decrement.
        - For a fluctuating trend, it prints all deficit days and returns the top 3 highest deficits.
    """
    # Open and read the CSV file
    with open(csv_path, mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)  

        # Initialize an empty list for the profit-and-loss records
        profitloss_records = []
        for row in reader:
            # Convert the first (day) and fifth (net profit) elements of each row to integers
            record = [int(row[0]), int(row[4])]  
            # Append the converted record to the list
            profitloss_records.append(record)  

    # Initialize an empty list for the daily differences
    daily_differences = []

    # Iterate over the profit and loss records in pairs
    for previous_record, current_record in zip(profitloss_records, profitloss_records[1:]):
        # Extract the day and value from each record
        previous_day, previous_value = previous_record
        current_day, current_value = current_record

        # Calculate the difference in values between the current and previous record
        difference = current_value - previous_value

        # Append the day and the calculated difference to the daily differences list
        daily_differences.append((current_day, difference))

    # Determine the overall trend of the profit/loss
    increasing = all(diff > 0 for _, diff in daily_differences)
    decreasing = all(diff < 0 for _, diff in daily_differences)

    # Analysis based on trend
    if increasing:
        # Initialise the highest increment in profit with the first value in daily_differences.
        highest_increment = daily_differences[0]
        
        # Loop through each entry in daily_differences, which contains pairs of day and profit difference.
        for diff in daily_differences:
            # Check if the current day's profit difference is greater than the highest recorded so far.
            if diff[1] > highest_increment[1]:
                # Update the highest increment with the current day's data.
                highest_increment = diff

        # Open the file "summary_report.txt" in append mode to add new content without overwriting existing data.
        with open("summary_report.txt", "a") as file:
            # Write a summary line indicating a consistent profit surplus trend.
            file.write("[PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            # Write the details of the day with the highest profit surplus and the amount.
            file.write(f"[HIGHEST PROFIT SURPLUS] DAY: {highest_increment[0]}, AMOUNT: SGD{highest_increment[1]}\n")

    elif decreasing:
        # Initialise the highest decrement in profit with the first value in daily_differences.
        highest_decrement = daily_differences[0]

        # Loop through each entry in daily_differences.
        for diff in daily_differences:
            # Check if the current day's profit difference is less than the highest recorded so far.
            if diff[1] < highest_decrement[1]:
                # Update the highest decrement with the current day's data.
                highest_decrement = diff
                
        # Open the file "summary_report.txt" in append mode.
        with open("summary_report.txt", "a") as file:
            # Write a summary line indicating a consistent profit deficit trend.
            file.write("[PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            # Write the details of the day with the highest profit deficit and the amount,
            # using the absolute value to ensure a positive number is displayed.
            file.write(f"[HIGHEST PROFIT DEFICIT] DAY: {highest_decrement[0]}, AMOUNT: SGD{abs(highest_decrement[1])}\n")

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
                profitloss = f"[PROFIT DEFICIT] DAY: {deficit[0]}, AMOUNT: SGD{deficit[1]}\n"
                file.write(profitloss)

            # Recording the top 3 highest deficit days
            if highest_deficit:
                highest = f"[HIGHEST PROFIT DEFICIT] DAY: {highest_deficit[0]}, AMOUNT: SGD{highest_deficit[1]}\n"
            if second_highest_deficit:
                second_highest = f"[2ND HIGHEST PROFIT DEFICIT] DAY: {second_highest_deficit[0]}, AMOUNT: SGD{second_highest_deficit[1]}\n"
            if third_highest_deficit:
                third_highest = f"[3RD HIGHEST PROFIT DEFICIT] DAY: {third_highest_deficit[0]}, AMOUNT: SGD{third_highest_deficit[1]}\n"
                file.write(highest + second_highest + third_highest)
