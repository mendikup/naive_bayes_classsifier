
class Menu:
    @staticmethod
    def show_menu():
        print("what would you like to do")
        choise= input("1. select a local csv file to work with\n"
                      "2. copy URL for a csv file\n"
                      "3. Analyze by bayesian model statistics")
        return choise



