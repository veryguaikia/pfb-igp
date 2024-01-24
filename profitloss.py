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

    # Write analysis results to the summary report text file
    with open("Summaryreport.txt", "a") as file:
            # Identify and write the day with the highest profit increase
        if increasing:
            highest_increment = max(daily_differences, key=lambda x: x[1])
            file.write("[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST PROFIT SURPLUS] DAY: {highest_increment[0]}, AMOUNT: {highest_increment[1]}\n")
            # Identify and write the day with the highest profit decrease
        elif decreasing:
            highest_decrement = max(daily_differences, key=lambda x: x[1])
            file.write("[NET PROFIT DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST PROFIT DEFICIT] DAY: {highest_decrement[0]}, AMOUNT: {abs(highest_decrement[1])}\n")
        else:
            # Initialize an empty list for deficits
            deficits = []

            # Iterate through each record in daily_differences
            for day, amount in daily_differences:
                # Include only the records where the amount is less than zero
                if amount < 0:
                    # Append the day and the negated amount to the deficits list
                    deficits.append((day, -amount))

            # Sort the deficits list by the day
            deficits = sorted(deficits, key=lambda x: x[0])
            for deficit in deficits:
                file.write(f"[PROFIT DEFICIT] DAY: {deficit[0]}, AMOUNT: USD{deficit[1]}\n")

            # Extract and write the top 3 highest deficits
            top_deficits = sorted(deficits, key=lambda x: x[1], reverse=True)[:3]
            for i, deficit in enumerate(top_deficits, start=1):
                file.write(f"[{'HIGHEST' if i == 1 else '2ND HIGHEST' if i == 2 else '3RD HIGHEST'} PROFIT DEFICIT] DAY: {deficit[0]}, AMOUNT: USD{deficit[1]}\n")