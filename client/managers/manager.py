from ui.menu import Menu
import requests

class Manager:

    def __init__(self):
        # self.URL= "http://my_server:8000/"  # for Dockerfile
        # self.classify_URL = "http://my_classifier_server:8080/"  # for Dockerfile

        self.URL= "http://127.0.0.1:8000/"
        self.classify_URL = "http://127.0.0.1:8080/"

    def run(self):
        running=True
        while running:
            user_selection=Menu.show_menu()
            if user_selection=="1":
                 self.handle_file_selection()
            elif user_selection == "2":
                self.handle_url_input()
            elif user_selection== "3":
                self.handle_prediction()
            elif user_selection == "4":
                running = False

            else:
                print("invalid input,try again")


    def handle_file_selection(self):
        try:
            res = requests.get(self.URL + "get_list_of_files")
            if res.ok:
                list_of_files = res.json()["list_of_files"]
                chosen_file = Menu.suggest_options(list_of_files)
                res = requests.get(f"{self.URL}/load_data/{chosen_file}")
                if res.ok:
                    self.suggest_user_to_delete_columns()
                    res = requests.get(f"{self.URL}/clean_df_and_train_model")
                    if res.ok:
                        accuracy = res.json()["accuracy"]
                        print(f"The testing is over. {accuracy} % Accuracy rate")
                        res = requests.get(f"{self.classify_URL}sync_model_from_remote")
                        if not res.ok:
                            print(f"there was a problem to load the model , status code: {res.status_code}")
                    else:
                        print("There was a problem finish the process of handling the data ")
                        print(f"status code: {res.status_code}")
                else:
                    print("There was a problem loading the file.")
                    print(f"Status code: {res.status_code}")
            else:
                print("there was a problem getting list of files")
                print(f"Status code: {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")


    def  handle_url_input(self):
        # try:
        url = input("Enter a link or URL")
        # raw_data_as_list_of_dict = requests.get(f"{url}/load_data/{chosen_file}").json()["data"]
        # raw_data = pd.DataFrame(raw_data_as_list_of_dict)
        #
        # except Exception as e:
        #     print(f"Error: {e}"


    def handle_prediction(self):
        res = requests.get(f"{self.classify_URL}get_features_and_unique_values")
        if res.ok:
            data = res.json()
            if data["exists"]:
                features_and_unique_values = data['features_and_unique_values']
                chosen_params = Menu.get_params(features_and_unique_values)
                res = requests.post(
                    f"{self.classify_URL}classify",
                    json=chosen_params
                )
                if res.ok:
                    print(f"according to the prediction the answer is {res.json()['prediction']}")
                else:
                    print("the was a problem execute the prediction")
                    print(f"status code: {res.status_code}")
            else:
                print("choose a file to work first")
        else:
            print("the was a problem to to get features and unique_values")
            print(f"status code: {res.status_code}")



    def suggest_user_to_delete_columns(self):
        """
        Ask the user if he wants to delete any columns before training.
        Allows multiple deletions until the user types 'done'.
        """

        choice = input("1.  delete any column of the table before training\n"
                       "2.  continue to training")
        if choice == "1":
            print("here are all the columns")
            columns_to_delete = []
            # list_of_columns = Extract.extract_columns_list(df)[:-1]
            res = requests.get(f"{self.URL}/get_list_of_columns")
            if res.ok:
                list_of_columns = res.json()["list_of_columns"]

                while len(list_of_columns) > 0:
                    chosen_column = Menu.suggest_options(list_of_columns)
                    columns_to_delete.append(chosen_column)
                    list_of_columns.remove(chosen_column)
                    done = input("write 'done' to execute, any other key to continue inserting")
                    if done == "done":
                        break
                print("executing..")

                res = requests.post(f"{self.URL}/drop_requested_columns",
                                         json={"columns_to_delete": columns_to_delete})
                if res.ok:
                    print("The requested columns has been dropped")
                else:
                    print("there was a problem dropping the columns you wanted")
                    print(f"status code: {res.status_code}")

            else:
                print("There was a problem to get the list of columns")
                print(f"status code: {res.status_code}")

        elif choice == "2":
            print("Here we go")

        else:
            print("invalid input")
            self.suggest_user_to_delete_columns()