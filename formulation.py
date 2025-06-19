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
        cursor.execute("SELECT DATE_EXP FROM FORMULATION WHERE ID_FORMULATION = ?", (choice,))
        exp_date = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM PHASE WHERE ID_FORMULATION = ?", (choice,))
        phases_nb = cursor.fetchone()
        cursor.execute("SELECT TYPE_OPERATION, TEMPERATURE, DUREE, VITESSE FROM PHASE WHERE ID_FORMULATION = ?", (choice,))
        phase_info = cursor.fetchone()
        
        print(formulation_name,", created by ",creator_name, " on ",exp_date, ". This formulation contains ",phases_nb," phases :",phase_info)

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

def find_ID (cursor,id_personne):
    
    cursor.execute("SELECT NOM, PRENOM FROM PERSONNE WHERE ID_PERSONNE = ?", (id_personne,))
    user = cursor.fetchone()
    if user:
           return (f"{user[0]} {user[1]}")
    else:
           return "User ID not found"
       
def find_formualtion (cursor,ID_formulation):
    cursor.execute("SELECT * FROM FORMULATION WHERE ID_FORMULATION = ?", (ID_formulation,))
    selected_formul = cursor.fetchone()
    
    if selected_formul:                      
            return(f"{selected_formul[1]}")
    else:           
            return "Aucune formulation trouvée avec cet ID."

def db_research_resultat_test(cursor):
        cursor.execute("SELECT NOM_FORMULATION FROM FORMULATION WHERE ID_FORMULATION = ?", (choice,))
        formulation_name = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM RESULTAT_TEST WHERE ID_FORMULATION = ?", (choice,))
        tests_nb = cursor.fetchone() [0]
        cursor.execute("SELECT ASPECT, CONSISTANCE, HOMOGENEITE, ODEUR, TOUCHER, SENSATION, EMULSION, REMARQUES,TESTEUR, DATE_TEST FROM RESULTAT_TEST WHERE ID_FORMULATION = ?", (choice,))
        resultat_info = cursor.fetchall()  
        print(f"There is {tests_nb} test currently for the formulation {formulation_name[0]}")
        for i, test in enumerate(resultat_info, start=1):
            testeur_name=find_ID (cursor,test[8])
            print(f"""  Test {i} made by {testeur_name} on {test[9]}: 
                  - Aspect = {test[0]} 
                  - Consistency = {test[1]}
                  - Homogeneity = {test[2]} 
                  - Smell = {test[3]} 
                  - Touch = {test[4]} 
                  - Feel = {test[5]}  
                  - Emulsion = {test[6]} 
                  - Remarks = {test[7]}""")
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
        print("--- Formulations available ---")
        cursor.execute("SELECT ID_FORMULATION, NOM_FORMULATION FROM FORMULATION")
        formul_list = cursor.fetchall()
        for f in formul_list:
                print(f"ID: {f[0]}  Nom: {f[1]}  ")        
        choice_formulation = int(input("Write the ID of the formulation you want to try: "))
        name_formulation=find_formualtion(cursor,choice_formulation)
        id_personne = int(input("Enter your personnal user ID :"))
        ID_CREATEUR=find_ID (cursor,id_personne)
        print("Well",ID_CREATEUR,"you want to test", name_formulation)
        
        cursor.execute("SELECT COUNT (*) FROM RESULTAT_TEST",)
        nombre_resultat_test = cursor.fetchone()[0]
        ID_resultat=nombre_resultat_test + 1
        date_creation= str(input("Enter the date of the manipulation(YYYY-MM-DD) :"))
        aspect=input("What an aspect?")
        consistency=input("What consistency ?")
        homogenity=input("What homogenity ?")
        smell=input("What smell ?")
        sense_of_touch=input("What sense of touch ?")
        feeling_on_the_skin=input("What feeling on the skin ?")
        emultion=input("What emultion ?")
        remarks=input( "Remarks?")
        cursor.execute(""" INSERT INTO RESULTAT_TEST(ID_RESULTAT, DATE_TEST, ASPECT, CONSISTANCE, HOMOGENEITE, ODEUR, TOUCHER, SENSATION, EMULSION, REMARQUES, TESTEUR, ID_FORMULATION)VALUES (?, ?, ?, ?,?,?,?,?,?,?,?,?)""", (ID_resultat, date_creation, aspect, consistency, homogenity, smell, sense_of_touch, feeling_on_the_skin, emultion, remarks,  ID_CREATEUR, choice_formulation ))
        connection_db.commit()
        print(ID_CREATEUR,"your test as save in database for", name_formulation)

    #Show formulation
    if j == 3 :
        
        print("Formulations available in database :")
        
        #Show formulations saved in db
        cursor.execute("SELECT ID_FORMULATION, NOM_FORMULATION FROM FORMULATION ;")
        results = cursor.fetchall()
        for f in results:
                print(f"ID: {f[0]}  Nom: {f[1]}  ")
        
        
        
        #Select formu from db
        choice = int(input("Enter the ID from the desired formulaton : "))
        
        db_research_formulation(cursor)
        db_research_resultat_test(cursor)
        
        
    #Quit software
    if j == 4 :
        print("Program left.")
        j = False
       
connection_db.close()
