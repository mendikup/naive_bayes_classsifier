from sklearn.model_selection import train_test_split
from dal.dal import Dal
from ui.menu import Menu
from utils.cleaner import Cleaner
from utils.extract_keys import Extract_keys
from models.naive_bayes_trainer import Naive_bayesian_trainer
from models.classifier import Classifier

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

                # send the list above to the function in the UI that gets the list,
                # suggest the options to the user and return it's choice
                chosen_file= Menu.suggest_options(list_of_files)
                raw_data=Dal.load_data("data/" +chosen_file)
                self.raw_df_handler(raw_data)

            elif user_selection == "2":
                url = input("Enter a link or URL")
                raw_df = Dal.load_data(url)
                self.raw_df_handler(raw_df)

            elif user_selection== "3":
                if self.model:

                    # send the "suggestions" which contains the keys that represents the columns in the
                    # data and values represents unique values that where in each column in the data,to
                    # the function that asks the user what parmeters he wants to choose for checking
                    chosen_params = Menu.get_params(self.suggestions)
                    print(f"the answer is:  {Classifier.ask_a_question(self.model, chosen_params)}")




    def raw_df_handler(self, raw_df):
        # cleaned_df = Cleaner.clean_data(raw_df)
        self.suggestions = Extract_keys.extract(raw_df)
        print(self.suggestions)
        train_df, test_df = train_test_split(raw_df, test_size=0.3)
        self.model = Naive_bayesian_trainer.train_model(train_df)
        # self.accuracy = Tester.check_accuracy(self.model, test_df)






