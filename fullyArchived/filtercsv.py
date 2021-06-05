import csv
import text2emotion as te

with open("OriginalCSVFiles/General.csv", "r", encoding='utf-8') as source:
    reader = csv.reader(source)

    #with open("FilteredCSVFiles/Filtered.csv", "w", encoding='utf-8') as result:
        #writer = csv.writer(result)
    for r in reader:
            
        if ("Rayhan25#0862" in r):
            emotion = te.get_emotion(r[3])
            sum = emotion["Happy"] + emotion["Angry"] + emotion["Surprise"] + emotion["Sad"] + emotion["Fear"]
            filter = dict()
            for key, value in emotion.items():
                if value != 0:
                    filter[key] = value
            if sum > 0:
                writer = csv.writer(open("FilteredCSVFiles/"+str(list(filter)[0])+".csv", "a+", newline = '', encoding='utf-8'))
                writer.writerow((r[3],list(filter)[0],filter[list(filter)[0]]))
                print("printed in " + str(list(filter)[0]) + ".csv")
                #print(filter)
            else:
                pass
            #print(sum)
            #writer.writerow((r[3],emotion))

           


