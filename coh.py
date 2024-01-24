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

    # Iterate over the profit and loss records in pairs
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

    # Write analysis results to the summary report text file
    with open("Summaryreport.txt", "a") as file:
            # Identify and write the day with the cash-on-hand increase
        if increasing:
            highest_increment = max(daily_differences, key=lambda x: x[1])
            file.write("[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST CASH SURPLUS] DAY: {highest_increment[0]}, AMOUNT: {highest_increment[1]}\n")
            # Identify and write the day with the highest cash-on-hand decrease
        elif decreasing:
            highest_decrement = min(daily_differences, key=lambda x: x[1])
            file.write("[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST CASH DEFICIT] DAY: {highest_decrement[0]}, AMOUNT: {abs(highest_decrement[1])}\n")
        else:
            # Sort and write deficits
            deficits = sorted([(day, -amount) for day, amount in daily_differences if amount < 0], key=lambda x: x[0])
            for deficit in deficits:
                file.write(f"[CASH DEFICIT] DAY: {deficit[0]}, AMOUNT: USD{deficit[1]}\n")

            # Extract and write the top 3 highest deficits
            top_deficits = sorted(deficits, key=lambda x: x[1], reverse=True)[:3]
            for i, deficit in enumerate(top_deficits, start=1):
                file.write(f"[{'HIGHEST' if i == 1 else '2ND HIGHEST' if i == 2 else '3RD HIGHEST'} CASH DEFICIT] DAY: {deficit[0]}, AMOUNT: USD{deficit[1]}\n")
