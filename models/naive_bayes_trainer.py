import pandas as pd
import numpy as np
import pprint

class Naive_bayesian_trainer:


    @staticmethod
    def train_model(df):
        copy_model = df.copy()
        trained_by = df.columns[-1]
        df.sort_values(trained_by, inplace=True)

        column_trained_by = df[trained_by]
        # Remove the target column from the model DataFrame to ensure it's not mistakenly used as a feature during training
        df.drop(inplace=True, columns=[trained_by])
        # initialize the dictionary model with a nested  dictionary called sum to save the calculations to use theme in the end
        statistics = {"sum": {"total_cases": len(copy_model.index)}}

        # start loop through  the list that contains the unique target labels in the class column
        for target_value in column_trained_by.unique():
            #  for each option count the number of times it appears in the class column (we will need it for calculations in the end
            statistics['sum'][target_value] = (copy_model[trained_by] == target_value).sum()

            statistics[target_value] = {}
            for column in df.columns:
                statistics[target_value][column] = {}
                for unique_key in df[column].unique():
                    statistics[target_value][column][unique_key] = (((copy_model[column] == unique_key) & (copy_model[trained_by] == target_value)).sum() + 1) / statistics['sum'][target_value]

        return statistics





def ask_a_question(model, dict_test):
    final_result = {}
    for option in model["sum"]:
        list_of_nums = []
        if not option == "total_cases":
            for column in dict_test:
                num = model[option][column][dict_test[column]]
                list_of_nums.append(num)
            list_of_nums.append(model['sum'][option] / model['sum']['total_cases'])
            list_of_nums = np.array(list_of_nums)
            # Make sure the list contains no zero, because multiplying by 0 would zero out the final probability
            if 0 in list_of_nums:
                list_of_nums += 1

            # multiply the
            result = np.prod(list_of_nums)
            result %= 1
            final_result[option] = result

    for key, val in final_result.items():
        print(f"{key} has {val}")
    strong = max(final_result, key=final_result.get)
    print(f"it is obviously {strong} :-)")

    return final_result



