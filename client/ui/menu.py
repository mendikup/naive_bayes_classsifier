from random import choice


class Menu:
    """
    Handles user interaction in a CLI-based menu system.
    """
    @staticmethod
    def show_menu():
        print("\nwhat would you like to do")
        choise= input("1. select a local csv file to work with\n"
                      "2. copy URL for a csv file\n"
                      "3. Analyze by bayesian model statistics")
        return choise

    @staticmethod
    def suggest_options(options: list) -> str:
        print("Please select an option:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit():
                index = int(choice)
                if 1 <= index <= len(options):
                    return options[index - 1]
            print("Invalid input. Try again.")

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








