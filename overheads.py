import csv

def find_highest_overhead(csv_path):
    """
    This function reads the MonsoonSim overheads CSV file.
    It identifies the category with the highest overhead percentage from the records.

    Parameters:
    csv_path (str or Path): The file path of the CSV file to be analyzed.

    Returns:
    tuple: Containing the category with the highest overhead and the corresponding percentage.
    """
    # Open and read the CSV file
    with open(csv_path, mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader)
          
        # Initialize highest overhead and category
        highest_overhead = None
        highest_overhead_category = None

        for category, overhead in reader:
            # Convert overhead to float for comparison
            overhead_value = float(overhead)

            # Update highest overhead and category if necessary
            if highest_overhead is None or overhead_value > highest_overhead:
                highest_overhead = overhead_value
                highest_overhead_category = category

    # Write the result to the summary report text file
    with open("Summaryreport.txt", "w") as file:
        file.write(f"[HIGHEST OVERHEAD] {highest_overhead_category.upper()}: {highest_overhead}%\n")

