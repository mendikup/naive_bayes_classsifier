from dal.dal import Dal
from ui.menu import Menu
from utils.cleaner import Cleaner
from utils.extract_keys import Extract_keys

class Maneger:

    def __init__(self):
        self.model = None
        self.suggestions=None


    def run(self):
        running=True

        while running:
            user_selection=Menu.show_menu()

            if user_selection=="1":
                list_of_files=Dal.get_list_of_files()

                # send the list above to the function in the ui that gets the list
                # and suggest the options to the user and return it's choice
                chosen_file= Menu.suggest_options(list_of_files)
                raw_data=Dal.load_data("data/"+chosen_file)
                self.raw_df_handler(raw_data)

            elif user_selection == "2":
                url = input("Enter a link or URL")
                raw_df = Dal.load_data(url)
                self.raw_df_handler(raw_df)
            elif user_selection== "3":
                if self.model:
                    chosen_params = Menu.get_params(self.suggestions)


    def raw_df_handler(self, raw_df):
        cleaned_df = Cleaner.clean_data(raw_df)
        self.suggestions = Extract_keys.extract(cleaned_df)
        self.model = Naive_bayes.train_model(train_df)
        self.accuracy = Tester.check_accuracy(self.model, test_df)






)