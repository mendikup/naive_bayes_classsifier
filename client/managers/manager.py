from ui.menu import Menu
import requests

class Manager:
    """
    Handles the main user interface and interaction with the server APIs.
    Offers options to train a model, drop columns, and classify input.
    """

    def __init__(self):
        # self.URL= "http://my_server:8000/"  # for Dockerfile
        # self.classify_URL = "http://my_classifier_server:8080/"  # for Dockerfile

        self.URL= "http://127.0.0.1:8000/"
        # Set base URLs for the main server and the classifier server
        self.URL = "http://127.0.0.1:8000/
        self.classify_URL = "http://127.0.0.1:8080/"

    def run(self):
        """
        Starts the main menu loop and responds to user input.
        """
        running = True
        while running:
            user_selection = Menu.show_menu()
            if user_selection == "1":
                self.handle_file_selection()
            elif user_selection == "2":
                self.handle_url_input()
            elif user_selection == "3":
                self.handle_prediction()
            elif user_selection == "4":
                running = False
            else:
                print("invalid input, try again")

    def handle_file_selection(self):
        """
        Guides the user to:
        - Choose a file
        - Optionally drop columns
        - Train the model
        - Sync the trained model to the classifier server
        """
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
                            print(f"There was a problem loading the model. Status code: {res.status_code}")
                    else:
                        print("Problem finishing data handling.")
                        print(f"Status code: {res.status_code}")
                else:
                    print("Problem loading file.")
                    print(f"Status code: {res.status_code}")
            else:
                print("Problem getting file list.")
                print(f"Status code: {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    def handle_url_input(self):
        """
        Placeholder for letting the user input a dataset URL.
        Currently not implemented.
        """
        url = input("Enter a link or URL: ")
        # Feature not implemented

    def handle_prediction(self):
        """
        Gets feature options from the classifier server,
        lets the user select values, and shows the prediction result.
        """
        res = requests.get(f"{self.classify_URL}get_features_and_unique_values")
        if res.ok:
            data = res.json()
            if data["exists"]:
                features_and_unique_values = data['features_and_unique_values']
                chosen_params = Menu.get_params(features_and_unique_values)
                res = requests.post(f"{self.classify_URL}classify", json=chosen_params)
                if res.ok:
                    print(f"Prediction: {res.json()['prediction']}")
                else:
                    print("Problem executing prediction.")
                    print(f"Status code: {res.status_code}")
            else:
                print("Please choose a file and train first.")
        else:
            print("Problem getting features.")
            print(f"Status code: {res.status_code}")

    def suggest_user_to_delete_columns(self):
        """
        Ask the user if they want to delete columns before training.
        Allows choosing multiple columns until 'done' is typed.
        """
        choice = input("1. delete column(s) before training\n2. continue to training\n")
        if choice == "1":
            print("Here are all the columns:")
            columns_to_delete = []
            res = requests.get(f"{self.URL}/get_list_of_columns")
            if res.ok:
                list_of_columns = res.json()["list_of_columns"]
                while len(list_of_columns) > 0:
                    chosen_column = Menu.suggest_options(list_of_columns)
                    columns_to_delete.append(chosen_column)
                    list_of_columns.remove(chosen_column)
                    done = input("Type 'done' to finish, any other key to continue: ")
                    if done == "done":
                        break
                print("Executing column removal...")
                res = requests.post(f"{self.URL}/drop_requested_columns",
                                    json={"columns_to_delete": columns_to_delete})
                if res.ok:
                    print("Columns removed successfully.")
                else:
                    print("Problem removing columns.")
                    print(f"Status code: {res.status_code}")
            else:
                print("Problem getting column list.")
                print(f"Status code: {res.status_code}")
        elif choice == "2":
            print("Proceeding to training...")
        else:
            print("Invalid input.")
            self.suggest_user_to_delete_columns()
