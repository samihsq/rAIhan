import csv
import text2emotion as te

with open("OriginalCSVFiles/General.csv", "r", encoding='utf-8') as source:
    reader = csv.reader(source)

    with open("FilteredCSVFiles/Filtered.csv", "w", encoding='utf-8') as result:
        writer = csv.writer(result)
        for r in reader:
            
            if ("Rayhan25#0862" in r):
                emotion = te.get_emotion(r[3])
                print(emotion)
                writer.writerow((r[1],r[3]))

           


