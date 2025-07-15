from sklearn.model_selection import train_test_split
from client.ui.menu import Menu
from client.utils.cleaner import Cleaner
from client.utils.extract import Extract
from server.core.classifier import Classifier
from server.tests.test_accuracy import Tester
import requests
import pandas as pd

class Manager:

    def __init__(self):
        self.model = None
        self.params_and_values=None
        self.accuracy = None
        self.URL= "http://127.0.0.1:8000/"


    def run(self):
        running=True

        while running:
            user_selection=Menu.show_menu()

            if user_selection=="1":
                try:
                    list_of_files = requests.get(self.URL + "get_list_of_files").json()["list_of_files"]
                    chosen_file= Menu.suggest_options(list_of_files)
                    raw_data_as_list_of_dict=requests.get(f"{self.URL}/load_data/{chosen_file}").json()["data"]
                    raw_data=pd.DataFrame(raw_data_as_list_of_dict)
                    self.raw_df_handler(raw_data)
                except Exception as e:
                    print(f"Error: {e}")



            elif user_selection == "2":
                try:
                    url = input("Enter a link or URL")
                    raw_data_as_list_of_dict = requests.get(f"{url}/load_data/{chosen_file}").json()["data"]
                    raw_data = pd.DataFrame(raw_data_as_list_of_dict)
                    self.raw_df_handler(raw_data)

                except Exception as e:
                    print(f"Error: {e}")


            elif user_selection== "3":
                if self.model:
                    # Ask the user to choose values for specific parameters
                    chosen_params = Menu.get_params(self.params_and_values)
                    print(f"the answer is:  {Classifier.get_the_most_probability_predict(self.model, chosen_params)}")

                else:
                    print("choose a file to work first")

            else:
                print("invalid input,try again")




    def raw_df_handler(self, raw_df):
        raw_df= self.suggest_user_to_delete_columns(raw_df)

        cleaned_df = Cleaner.ensure_there_is_no_nan(raw_df)
        self.params_and_values= Extract.extract_parameters_and_their_values(cleaned_df)

        train_df, test_df = train_test_split(raw_df, test_size=0.3)


        try:
            response= requests.post(
                    f"{self.URL}train_model",
                            json=train_df.to_dict(orient="records"))

            if response.status_code != 200:
                print(f"Server error: {response.status_code}")
                print(f"Text response: {response.text}")

            elif response.ok:
                self.model = response.json()


                response = requests.post(
                    f"{self.URL}check_accuracy_rate"
                         ,     json= {"trained_model": self.model,
                                     "test_df":test_df.to_dict(orient = "records")
                                     }
                                )

                if response.status_code != 200:
                    print(f"Server error: {response.status_code}")
                    print(f"Text response: {response.text}")

                elif response.ok:
                    accuracy_data= response.json()
                    self.accuracy = accuracy_data["accuracy"]
                    print(f'The testing is over. {self.accuracy} %  Accuracy rate')




        except Exception as e:
         print(f"Error: {e}")









    def suggest_user_to_delete_columns(self, df):
        """
        Ask the user if they want to delete any columns before training.
        Allows multiple deletions until the user types 'done'.
        """

        choice = input("1. to delete any column of the table before training\n"
                       "2. to continue to training")
        if choice == "1":
            print("here are all the columns")
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
            df = Cleaner.drop_requested_columns(df, columns_to_delete)

        elif choice == "2":
            print("Here we go")

        else:
            print("invalid input")
            self.suggest_user_to_delete_columns(df)


        return df





