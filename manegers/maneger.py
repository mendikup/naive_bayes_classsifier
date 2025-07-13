from sklearn.model_selection import train_test_split
from dal.dal import Dal
from ui.menu import Menu
from utils.cleaner import Cleaner
from utils.extract import Extract
from models.naive_bayes_trainer import Naive_bayesian_trainer
from models.classifier import Classifier
from tests.tester import Tester

class Maneger:

    def __init__(self):
        self.model = None
        self.params_and_values=None
        self.accuracy = None


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

                    # sends the "params_and_values" which contains the keys that represents the columns in the
                    # data and values represents unique values that where in each column in the data,to
                    # the function that asks the user what parmeters he wants to choose for checking
                    chosen_params = Menu.get_params(self.params_and_values)
                    print(f"the answer is:  {Classifier.ask_a_question(self.model, chosen_params)}")




    def raw_df_handler(self, raw_df):
        cleaned_df = Cleaner.clean_data(raw_df)
        self.params_and_values = Extract.extract_parameters_and_their_values(cleaned_df)
        print(self.params_and_values)
        train_df, test_df = train_test_split(cleaned_df, test_size=0.3)
        self.model = Naive_bayesian_trainer.train_model(train_df)
        self.accuracy = Tester.check_accuracy_percentage(self.model, test_df)
        print(f'The testing is over. {self.accuracy} %  Accuracy rate')






