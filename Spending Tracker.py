# -*- coding: utf-8 -*-
import os
import datetime 
from collections import Counter

# Possible improvements: 
# 1. Over the break: use a JSON for file handling.
# 2. Create a proper login system instead of the makeshift version
# 3. Add more options in the dictionaries


'''
adding a mood and category dictionary because when I would try to print the most common category and mood, the program would print the corresponding 
letter rather than the word itself which I think makes the code less user friendly as it is added work for the user to go check what mood and category 
each letter corresponds to everytime they ask for a summary. 
'''

category_dict = {
    "a": "Clothes",
    "b": "Makeup",
    "c": "Entertainment",
    "d": "Food(lunch/dinner)",
    "e": "Coffee",
    "f": "Snacks",
    "g": "Other"
}

mood_dict =  {
    "a": "Happy",
    "b": "Sad",
    "c": "Frustrated",
    "d": "Stressed",
    "e": "Confused",
    "f": "Other"
}

def create_user_file(username): 
    if not os.path.exists(username + ".txt"):
        with open(username + ".txt", "w") as file: 
            file.write(f"{username}'s spending tracker\n") #files header line 
            file.write("Date, Amount, Category, Mood\n") #2nd header line, this is so that when the user calls to view all their enteries they know what order they are reading in
            # the if block above checks if the file exists for the user and if it doesn't it automatically makes one for a new username 

def spending_entry(username): 
    amount = float(input('please enter the amount you have spent since the last time you inputted your spending: $'))

    while True: 
        category = input('''what category does this transaction belong to from these options, please enter the categories corresponding letter: 
                             a) Clothes
                             b) Makeup
                             c) Entertainment
                             d) Food(lunch, dinner and brunch. Does NOT include coffee and snacks)
                             e) Coffee
                             f) snacks
                             g) Other 
                             ''').lower()
    
        '''
       making the user input the corresponding letter becuase sometimes people(me) struggle with spelling and its easier to just type one letter or number rather than the whole word on both the user side and programmer side 
       easier on the programmmers side as I do not need to check for misspellings and stuff and easier on the user side as they do not need to get stuck in a loop of having to repeatedly input a word becuase they got the 
       spelling wrong before
        '''
        
        if category in category_dict: #added this for a way to break out of the loop and move onto the next while block 
            break
        print('Invalid input, please try again\n')

    while True:
        mood = input('''What was your mood when making the following transaction, , please enter the categories corresponding letter
                     a) Happy
                     b) Sad
                     c) Frustrated
                     d) Stressed
                     e) Confused
                     f) Other 
                     ''').lower() #had to put .lower() as I realized if I accidentally type an uppercase letter I need to go through all the steps again which can be annoying to the user
        if mood in mood_dict:
            break
        print('Invalid input, please try again\n')
        
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") # %X was not working despite multiple attempts of deugging so I decided to just save date and time :)
    

    with open(username + '.txt', "a") as file: #appending above info to users file 
        file.write(f"{timestamp}, {amount}, {category_dict[category]}, {mood_dict[mood]}\n")

        

    print("")
        
#THINGS TO ADD: 
#1. add a way to delete all spending records or a spending record 
#2. ass a way to have all spending records printed for user to view

    
def calculate(username): #calculates the total spent for the month, since the file was made, most common mood to spend money, and most common category to spend money 

    total = 0
    total = 0 
    total_spending_pastWeek = 0 
    total_spending_30Days = 0 
    category_counter = Counter()
    mood_counter = Counter()
    
    now = datetime.datetime.now()
    
    try:
        with open(username+'.txt', 'r') as file:
            lines = file.readlines()[2:] # the program should be reading all lines except for the header as I want the header to be permanently there 
            for i in lines: 
                date_str, amount, category, mood = i.strip().split(",", maxsplit=3)

                amount = float(amount)
                date = datetime.datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S") 
                
                total = total + amount 
                
                if (now-date).days <= 7:
                    total_spending_pastWeek = total_spending_pastWeek + amount 
                if (now - date).days <= 30:
                    total_spending_30Days = total_spending_30Days + amount 
                    
                #fix category counter 
                category_counter[category] += 1
                mood_counter[mood] += 1
                
        #prints the counter of each category the user has entered
        print(f"Category counter: {category_counter}") 
        print(f"Mood counter: {mood_counter}")

         
        most_common_category = category_counter.most_common(1)
        most_common_mood = mood_counter.most_common(1)

        most_common_category = most_common_category[0][0] if most_common_category else "No inputted categories"
        most_common_mood = most_common_mood[0][0] if most_common_mood else "No inputted moods"



        

        return total, total_spending_pastWeek, total_spending_30Days, most_common_category, most_common_mood
    
    
    except FileNotFoundError:
        print("There is no spending data for you")
        return (0, 0, 0, "N/A", "N/A")
    print('')
    
    
def del_spending(username): #this is for deleting spendings for any reason such as accidentally inputting the wrong spending, decinding that you don't want a certain spending logged, etc.
    try:
        with open(username + ".txt", "r") as file:
            lines = file.readlines()
            
        if len(lines) <= 2:
            print("You do not have enough data on file to delete, consider inputting some data")
            
        else:
            print('Here are your spending records')
        
        #printing all records with line numbers 
        for i,line in enumerate(lines, start = 0): # I was going to start numbering the lines from 1 but then once I did I realized that I would have to write extra code as I would have to account for the program taking base 0 and user using base 1 
            print(f"{i}. {line.strip()}")
            
        del_line_num = (input('Enter the line number that you want to delete. To delete all inputs, type "delete all". If you do not wish to delete anything at the moment type "exit": '))
            
        if del_line_num.lower() == 'delete all': 
            lines = lines[:2]  
            with open(username + '.txt', 'w') as file:
                file.writelines(lines)
                
            print("All your records have been deleted.\n")
            
        elif del_line_num.lower() == 'exit': #added this because I realized that if I accdentally typed the option that corressponds to deletion, I had no way to getting out without deleting something first 
            print("Exiting back to main options")
            
        else:
            if int(del_line_num) == 0 or int(del_line_num) == 1:
                print("Cannot delete these lines")
        
            elif 1 <= int(del_line_num) <= len(lines):
                    del lines[int(del_line_num)]
                    with open(username + '.txt', 'w') as file:
                        file.writelines(lines)
                    print(f"input {del_line_num}, has been deleted successfully")
            
            else:
                print("please enter a valid option")
        
            
    except FileNotFoundError:
        print("No file found for this user.\n")
    
    print('')
        
def view_enteries(username):
    try:
        with open(username + ".txt", "r") as file:
            lines = file.readlines()
        
        if len(lines) <= 2:
            print("You have not recorded any spendings, please consider option 1 and record any recent spendings \n")
        else:
            print(f"Here are your spending records {username}")
            for i, line in enumerate(lines[2:], start=1):  # Skip the header
                print(f"{i}. {line.strip()}")
    
    except FileNotFoundError: #TALK to the debug room, try and expect may be redundant here becuase the file is automatically created for all useres 
        print(f"{username} you do not have a file")
      
    print('')
        
def main(): 
    '''I wanted to make a proper login system but that alone turned into nearly 100 lines of code and was
    getting too time consuming and I was having to debug a lot so I made this makeshift login system that only requires a 
    username and if the username does not exist then it makes a file for the new user
    '''
    username = input("Enter your username to pull up your file: ")
    create_user_file(username)
    
    while True:
        action = input('''What would you like to do today?(enter a number corresponding to one of the following options):
                       1) record new spendings
                       2) to get a summary of your spendings
                       3) Delete spendings 
                       4) View all your enteries
                       5) exit the program 
    
                       Enter number here: ''')
        print('')
        if action == "1":
            spending_entry(username)
        elif action == "2":
            total, total_spending_pastWeek, total_spending_30Days, most_common_category, most_common_mood = calculate(username)
            print(f"So far you have spent, ${total:.2f}, since you started keeping track of your spendings\n") #when printing I want to round to two decimal places hence the .2f
            print(f"Your total spending this past week was: ${total_spending_pastWeek:.2f}\n")
            print(f"Your total spending this past month was: ${total_spending_30Days:.2f}\n")
            print(f"your most common spending category was, {most_common_category}\n")
            print(f"Your most common mood while spending was, {most_common_mood}\n")  
        elif action == "3":
            del_spending(username)
        elif action == '4':
            view_enteries(username)
        elif action == "5": #put an option to exit the program becuase otherwise I was getting stuck in a loop of recording new spendings anf reviewing my spendings 
            print("Exited successfully\n")
            break # added the break statement to actually exit the program
        else:
            print("Please input a valid option\n")

if __name__ == "__main__":
    main()
        
