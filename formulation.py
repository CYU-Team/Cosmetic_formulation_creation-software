import sqlite3
import matplotlib.pyplot as plt
import csv

def phase_creation():
    
    phase_type = str(input("Enter process type:"))
    speed = float(input("Enter mixing speed (RPM):"))
    temperature = float(input("Enter process temperature (°C):"))
    time = float(input("Enter process duration (min):"))
    
    cursor.execute("INSERT INTO PHASE WHERE ")

def ingredient_research(cursor):
    ingredient_property = str(input("Enter the researched property of your raw material : ")) 
    ingredient_property = f"%{ingredient_property}%" #f-string function to add % around ingredient_property
    cursor.execute("SELECT COSING, INCI FROM INGREDIENTS WHERE DESCRIPTION LIKE ? OR FONCTION LIKE ?", (ingredient_property, ingredient_property))
    line = cursor.fetchone()
    while line:
        print(line)
        line = cursor.fetchone()

    cosing = str(input("Enter the COSING number of the chosen raw material : "))
    return cosing

def db_research_formulation(cursor):
        cursor.execute("SELECT NOM_FORMULATION FROM FORMULATION WHERE ID_FORMULATION = ?", (choice,))
        formulation_name = cursor.fetchone()
        cursor.execute("SELECT ID_CREATEUR FROM FORMULATION WHERE ID_FORMULATION = ?", (choice,))
        result = cursor.fetchone()
        creator_id = result[0]
        cursor.execute("SELECT PRENOM, NOM FROM PERSONNE WHERE ID_PERSONNE = ?", (creator_id,))
        creator_name = cursor.fetchone()
        
        print(formulation_name,", created by ",creator_name)

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

def save_formulation_csv (formulation, cursor, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["COSING_Ref_No", "INCI_name", "Function", "Volume (mL)"])
        for ingredient in formulation:
            requete = 'SELECT INCI, FONCTION FROM INGREDIENTS WHERE COSING = ' + ingredient [0] ;
            cursor.execute(requete)
            elt = cursor.fetchone()
            if elt:
                writer.writerow([ingredient[0], elt[0], elt[1], ingredient[1]])
    print("Formulation saved into",filename)

connection_db = sqlite3.connect("laboratoire.db")
cursor = connection_db.cursor()

formulation = []

#main program loop
j = True
while j :

    print("1 - Create a formulation")
    print("2 - Enter results data from formulation test")
    print("3 - Show formulation")
    print("4 - Quit software")

    j = int(input("Enter your choice : "))

    #create a formulation
    if j == 1 :
        
        #new formulation
        formulation = []

        #user authentication
        id_personne = int(input("Enter your personnal user ID :"))
        cursor.execute("SELECT NOM, PRENOM FROM PERSONNE WHERE ID_PERSONNE = ?", (id_personne,))
        user = cursor.fetchone()
        print(user, "sucsessfully loged.")

        #formulation creation
        formulation_name = str(input("Enter the name of your new formulation : "))
        ##cursor.execute("INSERT INTO FORMULATION") à faire
        phases_quantity = int(input("How many phases will need " + formulation_name + "?"))

        for i in range(phases_quantity): #phases quantity loop

            phase_creation()

            #raw material research loop

            raw_materials = []
            i = True
            while i :
                cosing = ingredient_research(cursor)
                v = float(input("Enter the desired volume (mL) : "))
                raw_materials.append([cosing, v])
                i = str(input("Enter 'yes' if you want to enter a new raw materiel or 'no' if you doesn't want to add a new one : "))
                if i != "yes" :
                    i = False

            formulation.append([phase],[raw_materials])#marche pas

        print(formulation)#pour voir si ça marche pr l'instant

        #formulation saving in database
        db_save = str(input("Enter 'yes' if you want to save your formulation into database or 'no' if you doesn't want to save : "))
        if db_save == "yes":
            print("faire une def enregistrement ?")
        else:
            print("Formulation not saved in database.")

        #formulation saving (into csv file)
        csv_save = str(input("Enter 'yes' if you want to save your formulation into a csv file or 'no' if you doesn't want to save : "))
        if csv_save == "yes":
            user_file_name = str(input("Enter the name of your file :"))
            user_file_name += ".csv"
            save_formulation_csv (formulation, cursor, user_file_name)
        else:
            print("Formulation not saved. Back to main menu.")
    
    #Enter results data from formulation test
    if j == 2 :
        print("enter results")

    #Show formulation
    if j == 3 :
        
        print("Formulations available in database :")
        
        #Show formulations saved in db
        cursor.execute("SELECT ID_FORMULATION, NOM_FORMULATION FROM FORMULATION ;")
        results = cursor.fetchall()
        
        print(results)
        
        #Select formu from db
        choice = int(input("Enter the ID from the desired formulaton : "))
        
        db_research_formulation(cursor)
        
        
    #Quit software
    if j == 4 :
        print("Program left.")
        j = False
       
connection_db.close()
