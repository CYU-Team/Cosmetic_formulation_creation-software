import sqlite3
import matplotlib.pyplot as plt
import csv

def ingredient_research(cursor):
    ingredient_property = str(input("Enter the researched property of your raw material : ")) 
    ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
    cursor.execute("SELECT COSING, INCI FROM INGREDIENTS WHERE DESCRIPTION OR FONCTION LIKE ?", (ingredient_property,))
    line = cursor.fetchone()
    while line:
        print(line)
        line = cursor.fetchone()
    cosing = str(input("Enter the COSING number of the chosen raw material : "))
    return cosing

def show_formulation (formulation, cursor) :
    nom_tranches = []
    taille_tranches = []
    for ingredient in formulation :
        requete = 'SELECT INCI, FONCTION FROM INGREDIENTS WHERE COSING = ' + ingredient [0] ;
        cursor.execute(requete)
        elt = cursor.fetchone()
        nom_tranches.append (elt [0] + " (" + ingredient [0] + ")")
        taille_tranches.append (ingredient [1])
        print ("- ", ingredient [1], "ml de ", elt [0], "(",elt [1], ") [", ingredient [0], "]")
        plt.pie(taille_tranches, labels = nom_tranches, autopct = "%1.1f%%")
        plt.title("Composition of the formulation")
        plt.show()

def save_formulation (formulation, cursor, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["COSING_Ref_No", "INCI_name", "Function", "Volume (mL)"])
        for ingredient in formulation:
            requete = 'SELECT INCI, FONCTION FROM INGREDIENTS WHERE COSING = ' + ingredient [0] ;
            cursor.execute(requete)
            elt = cursor.fetchone()
            if elt:
                writer.writerow([ingredient[0], elt[0], elt[1], ingredient[1]])
    print("Formulation saved into",filename,".")

connection_db = sqlite3.connect("laboratoire.db")
cursor = connection_db.cursor()

formulation = []

#program loop
j = True
while j :

    print("1 - Create a formulation")
    print("2 - Enter results data from formulation test")
    print("3 - Show formulation")
    print("4 - Quit software")

    j = int(input("Enter your choice : "))

    if j == 1 :
        
        #new formulation
        formulation = [] 

        #raw material research loop
        i = True
        while i :
            cosing = ingredient_research(cursor)
            v = float(input("Enter the desired volume (mL) : "))
            formulation.append([cosing, v])
            i = str(input("Enter 'yes' if you want to enter a new raw materiel or 'no' if you doesn't want to add a new one : "))
            if i != "yes" :
                i = False
        
        #formulation saving (into csv file)
        save = str(input("Enter 'yes' if you want to save your formulation into a csv file or 'no' if you doesn't want to save : "))
        if save == "yes":
            save_formulation (formulation, cursor, "formulation.csv")
        else:
            print("Formulation not saved. Back to main menu.")
    
    if j == 2 :
        print("enter results")

    if j == 3 :
        show_formulation (formulation, cursor)

    if j == 4 :
        print("Program left.")
        j = False
       
connection_db.close()
