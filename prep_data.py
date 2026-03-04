import csv

input_files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

with open("data/pink_morsels.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Sales", "Date", "Region"])
    for file in input_files:
        with open(file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["product"] == "pink morsel":
                    price = float(row["price"].replace("$", ""))
                    sales = int(row["quantity"]) * price
                    writer.writerow([
                        sales,
                        row["date"],
                        row["region"]
                    ])