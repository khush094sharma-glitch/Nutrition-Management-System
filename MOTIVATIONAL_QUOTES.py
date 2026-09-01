import csv
quotes=[
        ["YOUR BODY DESERVES BETTER FUEL"],
        ["EAT GOOD,FEEL GOOD"],
        ["YOU'RE WHAT YOU EAT"]]

with open("MOTIVATIONAL_QUOTES.csv", "w", newline="") as file:
    writer= csv.writer(file)
    writer.writerows(quotes)  

print("done")