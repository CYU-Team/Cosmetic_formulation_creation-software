import sqlite3
import matplotlib.pyplot as plt
import csv


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
            return "No wording found with this ID."
        

def find_name_ingredient (cosing,cursor):
    
    cursor.execute("SELECT INCI FROM INGREDIENTS WHERE COSING=?", (cosing,))
    name=cursor.fetchone()
    return (f"{name[0]}")


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
        
        cursor.execute("SELECT ID_PHASE, TYPE_OPERATION, TEMPERATURE, DUREE, VITESSE FROM PHASE WHERE ID_FORMULATION = ?", (choice,))
        phase_info = cursor.fetchall() 
        
       
        print(f"{formulation_name[0]}, created by {creator_name[0]} {creator_name[1]} on {exp_date[0]}.")
        print(f"This formulation contains {phases_nb} phases:")
        for i, phase in enumerate(phase_info, start=1):
            ID_PHASE = phase[0]
            print(f"  Phase {i}: Operation={phase[1]}, Temp={phase[2]}°C, Duration={phase[3]}min, Speed={phase[4]} RPM")        
            cursor.execute("SELECT ID_INGREDIENT, MASSE FROM COMPOS_PHASE_INGREDIENT WHERE ID_PHASE = ?", (ID_PHASE,))
            ingredient_info = cursor.fetchall()           
            
            if ingredient_info:
               print("    Ingredients:")
               for ing in ingredient_info:
                   inci_name = find_name_ingredient(ing[0], cursor)
                   print(f"      - {ing[1]} g of {inci_name} (COSING {ing[0]})")
            else:
               print("    No ingredients in this phase.")
        
       
            
            
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
        

       

connection_db = sqlite3.connect("laboratoire.db")
cursor = connection_db.cursor()



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
        
        
        
        
        #user authentication
        id_personne = int(input("Enter your personnal user ID :"))
        ID=find_ID(cursor,id_personne)
        print("Hi",ID)
        #formulation creation
        formulation_name = str(input("Enter the name of your new formulation : "))
        phases_quantity = int(input("How many phases will need " + formulation_name + "?"))
        
        cursor.execute("SELECT COUNT(*) FROM FORMULATION")
        nombre_formulation = cursor.fetchone()[0]
        ID_Formulation = nombre_formulation + 1
        cursor.execute("SELECT MAX(ID_PHASE) FROM PHASE")
        last_id_phase = cursor.fetchone()[0]
        last_id_phase = last_id_phase + 10
       

        for i in range(phases_quantity):
            ID_PHASE = last_id_phase + 1
            last_id_phase = ID_PHASE   
            
           
            phase_type = input("Enter process type: ")
            speed = float(input("Enter mixing speed (RPM): "))
            temperature = float(input("Enter process temperature (°C): "))
            time = float(input("Enter process duration (min): "))
            NUM_PHASE = i
            cursor.execute(""" INSERT INTO PHASE (ID_PHASE, TYPE_OPERATION, TEMPERATURE, DUREE, VITESSE, NUM_PHASE, ID_FORMULATION) VALUES (?, ?, ?, ?, ?, ?, ?)""", (ID_PHASE, phase_type, temperature, time, speed, NUM_PHASE, ID_Formulation))
            connection_db.commit()
            print("Phase created.")
            
            i = True
            while i :
                cosing = ingredient_research(cursor)
                v = float(input("Enter the desired masse (g) : "))
                cursor.execute(""" INSERT INTO COMPOS_PHASE_INGREDIENT(ID_PHASE, ID_INGREDIENT, MASSE)VALUES (?, ?, ?)""", (ID_PHASE, cosing, v))
                connection_db.commit()
                i = str(input("Enter 'yes' if you want to enter a new raw materiel or 'no' if you doesn't want to add a new one : "))
                if i != "yes" :
                    i = False

        #formulation saving in database
        db_save = str(input("Enter 'yes' if you want to save your formulation into database or 'no' if you doesn't want to save : "))
        if db_save == "yes":
            
           
            user_file_name = str(input("Enter the name of your file :"))
            date_creation= str(input("Enter the date of the manipulation(YYYY-MM-DD) :"))
            ID_manipilator= int (input ("Enter your ID :"))
            cursor.execute(""" INSERT INTO FORMULATION(ID_FORMULATION, NOM_FORMULATION, DATE_EXP, ID_CREATEUR)VALUES (?, ?, ?, ?)""", (ID_Formulation, user_file_name, date_creation, ID_manipilator))
            connection_db.commit()
            print("Formulation saved in the database.")
            
            
        else:
            print("Formulation not saved in database.")
        
       

        
    
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
        print("--- Formulations available ---")
        cursor.execute("SELECT ID_FORMULATION, NOM_FORMULATION FROM FORMULATION")
        formul_list = cursor.fetchall()
        for f in formul_list:
                print(f"ID: {f[0]}  Nom: {f[1]}  ")
        choice = int(input("Enter the ID from the desired formulaton : "))
        db_research_formulation(cursor)
        db_research_resultat_test(cursor)
    #Quit software
    if j == 4 :
        print("Program left.")
        j = False
       
connection_db.close()
