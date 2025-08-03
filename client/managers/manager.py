from ui.menu import Menu
import requests

class Manager:
    """
    Handles user interaction and communication with the server and classifier APIs.
    Provides options to load data, train models, and make predictions.
    """

    def __init__(self):
        """Initializes the Manager with base URLs for both servers."""
        self.URL = "http://127.0.0.1:8000/"
        self.classify_URL = "http://127.0.0.1:8080/"

    def run(self):
        """Starts the main menu loop and executes user-selected actions."""
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
        """Allows user to select a file, optionally drop columns, train the model, and sync it."""
        try:
            res = requests.get(self.URL + "get_list_of_files", timeout=5)
            if res.ok:
                list_of_files = res.json()["list_of_files"]
                chosen_file = Menu.suggest_options(list_of_files)
                res = requests.get(f"{self.URL}/load_data/{chosen_file}", timeout=5)
                if res.ok:
                    self.suggest_user_to_delete_columns()
                    res = requests.get(f"{self.URL}/clean_df_and_train_model", timeout=10)
                    if res.ok:
                        accuracy = res.json()["accuracy"]
                        print(f"The testing is over. {accuracy}% Accuracy rate")
                        res = requests.get(f"{self.classify_URL}sync_model_from_remote", timeout=5)
                        if not res.ok:
                            print(f"Problem syncing model. {res.status_code}: {res.text}")
                    else:
                        print(f"Problem finishing training. {res.status_code}: {res.text}")
                else:
                    print(f"Problem loading file. {res.status_code}: {res.text}")
            else:
                print(f"Problem getting file list. {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")

    def handle_url_input(self):
        """Placeholder for URL input feature (currently not implemented)."""
        url = input("Enter a link or URL: ")
        print("Feature not implemented yet.")

    def handle_prediction(self):
        """Allows the user to input features and receive a class prediction."""
        try:
            res = requests.get(f"{self.classify_URL}get_features_and_unique_values", timeout=5)
            if res.ok:
                data = res.json()
                if data["exists"]:
                    features_and_unique_values = data['features_and_unique_values']
                    chosen_params = Menu.get_params(features_and_unique_values)
                    res = requests.post(f"{self.classify_URL}predict", json=chosen_params, timeout=5)
                    if res.ok:
                        print(f"Prediction: {res.json()['prediction']}")
                    else:
                        print(f"Prediction failed. {res.status_code}: {res.text}")
                else:
                    print("Please choose a file and train first.")
            else:
                print(f"Failed to fetch features. {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")

    def suggest_user_to_delete_columns(self):
        """Guides the user through optional column removal before training."""
        choice = input("1. delete column(s) before training\n2. continue to training\n")
        if choice == "1":
            columns_to_delete = []
            try:
                res = requests.get(f"{self.URL}/get_list_of_columns", timeout=5)
                if res.ok:
                    list_of_columns = res.json()["list_of_columns"]
                    while list_of_columns:
                        chosen = Menu.suggest_options(list_of_columns)
                        columns_to_delete.append(chosen)
                        list_of_columns.remove(chosen)
                        done = input("Type 'done' to finish, any other key to continue: ")
                        if done == "done":
                            break
                    res = requests.post(f"{self.URL}/drop_requested_columns",
                                        json={"columns_to_delete": columns_to_delete}, timeout=5)
                    if res.ok:
                        print("Columns removed successfully.")
                    else:
                        print(f"Failed to remove columns. {res.status_code}: {res.text}")
                else:
                    print(f"Failed to get columns. {res.status_code}: {res.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error during column deletion: {e}")
        elif choice == "2":
            print("Proceeding to training...")
        else:
            print("Invalid input.")
            self.suggest_user_to_delete_columns()
