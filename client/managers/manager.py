from ui.menu import Menu
import requests

class Manager:

    def __init__(self):
        # self.URL= "http://0.0.0.0:8000/"  for dockerfile
        self.URL= "http://127.0.0.1:8000/"

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
            response = requests.get(self.URL + "get_list_of_files")
            if response.ok:
                list_of_files = response.json()["list_of_files"]
                chosen_file = Menu.suggest_options(list_of_files)
                response = requests.get(f"{self.URL}/load_data/{chosen_file}")
                if response.ok:
                    self.suggest_user_to_delete_columns()
                    response = requests.get(f"{self.URL}/raw_df_handler")
                    if response.ok:
                        accuracy = response.json()["accuracy"]
                        print(f"The testing is over. {accuracy} % Accuracy rate")
                    else:
                        print("There was a problem finish the process of handling the data ")
                        print(f"status code: {response.status_code}")
                else:
                    print("There was a problem loading the file.")
                    print(f"Status code: {response.status_code}")
            else:
                print("there was a problem getting list of files")
                print(f"Status code: {response.status_code}")
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
        response = requests.get(f"{self.URL}/get_features_and_unique_values")
        if response.ok:
            data = response.json()
            if data["exists"]:
                features_and_unique_values = data['features_and_unique_values']
                chosen_params = Menu.get_params(features_and_unique_values)
                response = requests.post(
                    f"{self.URL}predict",
                    json=chosen_params
                )
                if response.ok:
                    print(f"according to the prediction the answer is {response.json()['predict']}")
                else:
                    print("the was a problem execute the prediction")
                    print(f"status code: {response.status_code}")
            else:
                print("choose a file to work first")
        else:
            print("the was a problem to to get features and unique_values")
            print(f"status code: {response.status_code}")



    def suggest_user_to_delete_columns(self):
        """
        Ask the user if they want to delete any columns before training.
        Allows multiple deletions until the user types 'done'.
        """

        choice = input("1.  delete any column of the table before training\n"
                       "2.  continue to training")
        if choice == "1":
            print("here are all the columns")
            columns_to_delete = []
            # list_of_columns = Extract.extract_columns_list(df)[:-1]
            response = requests.get(f"{self.URL}/get_list_of_columns")
            if response.ok:
                list_of_columns = response.json()["list_of_columns"]

                while len(list_of_columns) > 0:
                    chosen_column = Menu.suggest_options(list_of_columns)
                    columns_to_delete.append(chosen_column)
                    list_of_columns.remove(chosen_column)
                    done = input("write 'done' to execute, any other key to continue inserting")
                    if done == "done":
                        break
                print("executing..")

                response = requests.post(f"{self.URL}/drop_requested_columns",
                                         json={"columns_to_delete": columns_to_delete})
                if response.ok:
                    print("The requested columns has been dropped")
                else:
                    print("there was a problem dropping the columns you wanted")
                    print(f"status code: {response.status_code}")

            else:
                print("There was a problem to get the list of columns")
                print(f"status code: {response.status_code}")

        elif choice == "2":
            print("Here we go")

        else:
            print("invalid input")
            self.suggest_user_to_delete_columns()