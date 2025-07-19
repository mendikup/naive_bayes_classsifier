from random import choice


class Menu:
    """
    Handles user interaction in a CLI-based menu system.
    """
    @staticmethod
    def show_menu():
        print("\nwhat would you like to do")
        choise = input(
            "1. select a local csv file to work with\n"
            "2. copy URL for a csv file\n"
            "3. Analyze by bayesian model statistics\n"
            "4. Quit\n"
        )
        return choise.strip()


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
    def get_params(parameters:dict) ->dict:
        """
               Ask the user to choose a value for each parameter (feature).

               :param parameters: {column_name: [possible_values]}
               :return: {column_name: chosen_value}
               """
        selected_params_and_values = {}

        for parameter in parameters:
            print(f"for the parameter {parameter}:")
            selected_value=Menu.suggest_options(parameters[parameter])
            selected_params_and_values[parameter]=selected_value

        return selected_params_and_values








