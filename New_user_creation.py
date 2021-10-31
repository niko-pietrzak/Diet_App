# Importing nessery python libraries
# Psycopg2 -> PostgreSQL adapter for python
# Datetime -> module supplies classes for manipulating dates and times.
import psycopg2 as pg2
from psycopg2 import Error
import datetime


# 1. Functions

# Below are the functions to convert and calculate basic measures for diet planning

# Measures converter to standardize the data in the database for people using Imperial type of measure
def weight_converter(weight_in_lbs):
    weight_in_kg = int(weight_in_lbs / 2.2046)
    return weight_in_kg

def height_converter(height_feets, height_inches):
    height_in_cm = int((30.48*height_feets)+(2.54*height_inches))
    return height_in_cm


# Function to calculate BMR -> Basal Metabolic rate
def BMR(sex, weight, height, age):
    if sex == 1:
        BMR = (10*weight)+(6.25*height)-(5*age) + 5
        return BMR
    elif sex == 2:
        BMR = (10*weight)+(6.25*height)-(5*age) - 161
        return BMR
    else:
        print("Your data is uncompletted!")


# Function to calculate TMR -> Total Metabolic rate based additionaly on our goals and activity 
def TMR(BMR, activity, goal):
    if activity == 1:
        TMR = BMR * 1.2
    elif activity == 2:
        TMR = BMR * 1.5   
    elif activity == 3:
        TMR = BMR * 1.75
    elif activity == 4:
        TMR = BMR * 2
    else:
        print("Your 'activity' data is uncompleted")
         
    if goal == 1:
        TMR = TMR - 400 
        return TMR
    elif goal == 2:
        TMR = TMR - 300
        return TMR
    elif goal == 3:
        TMR = TMR - 200
        return TMR
    elif goal == 4:
        return TMR
    elif goal == 5:
        TMR = TMR + 200
        return TMR
    elif goal == 6:
        TMR = TMR + 300
        return TMR
    elif goal == 7:
        TMR = TMR + 400
        return TMR
    else:
        print("Your 'goal' data is uncompleted")


# Funtion to calculate all neccesery nutritions to fill our daily calorie demand
def nutritions_calculation(TMR, weight, goal):
    if (goal == 1) or (goal == 2) or (goal==3):
        daily_fats_g = (TMR * 0.2)/9
        daily_proteins_g = 1.8 * weight
        daily_carbohydrates_g = (TMR - (TMR * 0.2) - (1.8 * weight * 4))/4  
    elif (goal == 4):
        daily_fats_g = (TMR * 0.225)/9
        daily_proteins_g = 1.8 * weight
        daily_carbohydrates_g = (TMR - (TMR * 0.225) - (1.8 * weight * 4))/4  
    elif (goal == 5) or (goal == 6) or (goal==7):
        daily_fats_g = (TMR * 0.225)/9
        daily_proteins_g = 2.2 * weight
        daily_carbohydrates_g = (TMR - (TMR * 0.225) - (2.2 * weight * 4))/4
        
    return (int(daily_fats_g), int(daily_proteins_g), int(daily_carbohydrates_g))  



# 2. New User Information Collecting

print("Hello. We are glad that you are willing to join us. Let's make a quick account for you...")
print("Just enter basic information about your account:")

#Basic information
username = input("Username: ")
password = input("Password: ")
first_name = input("First name: ")
last_name = input("Last name: ")
e_mail = input("E-mail: ")
age = float(input("Age: "))


#Units of measure, weight, height
temp_units = int(input("\nEnter units of measurments you want to use:\n1 for Imperial(pounds, feets); 2 for Metric(kg, cm): "))
if temp_units == 2:
    height = float(input("Height(cm): "))
    weight = float(input("Weight(kg): "))
    units = 2
elif temp_units == 1:
    units = 1
    weight_in_pounds = float(input("Weight(pounds): "))
    height_feets = float(input("Enter height(feets): "))
    height_inches = float(input("Inches:"))
    height = height_converter(height_feets, height_inches)
    weight = weight_converter(weight_in_pounds)

#Sex
temp_sex = input("\nEnter your sex (Male / Female): ")
if temp_sex == 'Male':
    sex = 1
elif temp_sex == "Female":
    sex = 2
else:
    print("Incorect sex!")


# Connecting to data base to import possible options to choose from for our goals, diets and activity
try:
    # connecting to an existing database
    connection = pg2.connect(database = 'Diet_app', user = 'postgres', password = 'Heisenberg05')
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    
    # Executing queries and assign them to new object
    cursor.execute("SELECT * FROM goals")
    goals_data = cursor.fetchall()

    cursor.execute("SELECT * FROM diets")
    diets_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM activity")
    activity_data = cursor.fetchall()
    
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()


#Goal
print ('\n')
for n in range(len(goals_data)):
    print(goals_data[n][0], ' - ', goals_data[n][1])
goal = int(input('What is your goal: '))

#Diet
print ('\n')
for n in range(len(diets_data)):
    print(diets_data[n][0], ' - ', diets_data[n][1])
diet = int(input('What is your diet: '))

#Activity
print ('\n')
for n in range(len(activity_data)):
    print(activity_data[n][0], ' - ', activity_data[n][1], ' - ', activity_data[n][2])
activity = int(input('What is your activity: '))
num_of_meals = int(input("How many meals a day would you like to eat: "))   



# 3. Calories and nutritions calculations 

user_BMR = BMR(sex, weight, height, age)
user_TMR = TMR(user_BMR, activity, goal)
daily_fats_g, daily_proteins_g, daily_carbohydrates_g = nutritions_calculation(user_TMR, weight, goal)

print("\nYour BMR(amount of calories you body needs to keep the body functioning at rest): ", user_BMR)
print("Your TMR(total calories you need based on your goals and activity): ", user_TMR)
print("Your daily carbohydrates intake grams: ", daily_carbohydrates_g)
print("Your daily proteins intake grams: ", daily_proteins_g)
print("Your daily fats intake grams: ", daily_fats_g, '\n')


# 4. Importing new user's data to database

try:
    connection = pg2.connect(database = 'Diet_app', user = 'postgres', password = 'Heisenberg05')
    cursor = connection.cursor()
    # Executing a SQL query to inssert data into the table
    insert_query = """INSERT INTO users(username, password, first_name, last_name, age, height_in_cm, weight_in_kg, e_mail, created_on, 
                    id_units_of_measure, id_sex, id_goal, id_diet, id_activity, caloric_demand, carbohydrates_daily, proteins_daily, fats_daily)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    account_creation_time = datetime.datetime.now()
    user_tuple = (username, password, first_name, last_name, age, height, weight, e_mail, account_creation_time, units, sex, goal, diet, activity, user_TMR, daily_carbohydrates_g, daily_proteins_g, daily_fats_g)
    cursor.execute(insert_query, user_tuple)
    connection.commit()
    print("1 user inserted successfully")
except (Exception, pg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")