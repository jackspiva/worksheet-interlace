import statistics
from collections import Counter
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]

student_answer = [line.split(', ', 1) for line in open(inFile)]

for idx, sublist in enumerate(student_answer):
     student_answer[idx] = [
         int(el) if el.isdigit() else el.strip('\n')
         for el in sublist
    ]

sorted_student_answer = sorted(student_answer, key=lambda x: x[0])
print (sorted_student_answer)

def new_input():
    Type_of_Analysis = input('What would you like done? Select Mean, Median, Mode, Student, Max, Min, Standard Deviation, Pie Chart, Bar Graph or Exit: ')

    Type_of_Analysis = Type_of_Analysis.lower()
    answers = [item[0] for item in sorted_student_answer]

    #print("answers", answers)

    if (Type_of_Analysis == 'student'):
        person = input('Give a student name to see their answer: ')
        for sublist in sorted_student_answer:
            if sublist[1] == person:
                print ("Found it!", person,"'s answer was", sublist[0])
                new_input()

    if (Type_of_Analysis == 'median'):
        actual_median = statistics.median(answers)
        print (actual_median)

    if (Type_of_Analysis == 'mode'):
        print("not implemented")

    if Type_of_Analysis == 'mean':
        L = [float(n) for n in answers if n]
        avg = sum(L)/len(L) if L else '-'
        print(avg)

    if (Type_of_Analysis == "max"):
        print("not implemented")

    if (Type_of_Analysis == "min"):
        print("not implemented")

    if (Type_of_Analysis == "standard deviation"):
        print("not implemented")

   # if (Type_of_Analysis == "pie chart"):
   #     print(answers)
   #     modelist = Counter(answers)
   #     print(modelist)

   #    test = []
   #    test2 = []

    #   for x in range(min(answers),(max(answers)+ 1)):
    #       if (x in modelist):
    #            test.append(x)
    #            test2.append(modelist[x])

    #    print (test)
    #    print (test2)

    #    labels = test
    #    sizes = test2
    #    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']
    #    explode = (0.1, 0, 0, 0, 0)  # explode 1st slice
 
        # Plot
    #    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    #        autopct='%1.1f%%', shadow=True, startangle=140)
    #    plt.axis('equal')
    #    plt.show()   

    if (Type_of_Analysis == "bar graph"):
        print("not implemented")

    if (Type_of_Analysis != "exit"):
        new_input()
new_input()

