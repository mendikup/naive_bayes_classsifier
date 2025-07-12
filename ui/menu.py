from random import choice


class Menu:
    @staticmethod
    def show_menu():
        print("what would you like to do")
        choise= input("1. select a local csv file to work with\n"
                      "2. copy URL for a csv file\n"
                      "3. Analyze by bayesian model statistics")
        return choise


    @staticmethod
    def suggest_options(options:list) -> str:
        choices = {}
        print("please select an option from the option below:")

        i = 1

        for option in options:
            choices[i] = option
            print(f"{i}. {option}")
            i+=1

        choice = input()

        if not choice.isdigit():
            print("enter numbers only")
            return Menu.suggest_options(options)

        int_choice=int(choice)

        if not (0 < int_choice < i):
            print(f"enter a number between 1 and {i-1}")
            return Menu.suggest_options(options)

        return choices[int_choice]


    @staticmethod
    def get_parmas(suggestions:dict) ->dict:

        """create  a dictionary to save each option(number the user choose) as a key and the
         parameters as values so we can store the options as a dictionary so we can send
         it to the bayes_model
        """
        selected_options = {}

        for suggestion in suggestions:
            print(f"for the parameter{suggestion}:")
            selected_choice=Menu.suggest_options(suggestion)
            selected_options[suggestions]=selected_choice

        return selected_options








