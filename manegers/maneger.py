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

                else:
                    print("choose a file to work first")

            else:
                print("invalid input,try again")





    def raw_df_handler(self, raw_df):
        self.suggest_deleting_columns(raw_df)
        cleaned_df = Cleaner.ensure_there_is_no_nan(raw_df)
        self.params_and_values = Extract.extract_parameters_and_their_values(cleaned_df)


        train_df, test_df = train_test_split(raw_df, test_size=0.3)
        self.model = Naive_bayesian_trainer.train_model(train_df)
        print(self.model)
        self.accuracy = Tester.check_accuracy_percentage(self.model, test_df)
        print(f'The testing is over. {self.accuracy} %  Accuracy rate')



    def suggest_deleting_columns(self, df):
        choice = input("1. to delete any column of the table before training\n"
                       "2. to continue to training")
        if choice == "1":
            columns_to_delete = []
            list_of_columns = Extract.extract_columns_list(df)[:-1]
            while len(list_of_columns) > 0:
                chosen_column = Menu.suggest_options(list_of_columns)
                columns_to_delete.append(chosen_column)
                list_of_columns.remove(chosen_column)
                done = input("write 'done' to execute, any other key to continue inserting")
                if done == "done":
                    break
            print("executing..")
            Cleaner.drop_requested_columns(df, columns_to_delete)
        elif choice == "2":
            print("Here we go")
        else:
            print("invalid input")
            self.suggest_deleting_columns(df)




