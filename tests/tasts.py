import pandas as pd
import numpy as np
import pprint

model = pd.read_csv("../data/basic.csv")
copy_model = model.copy()

trained_by = model.columns[-1]

model.sort_values(trained_by, inplace=True)

column_trained_by = model[trained_by]
# we drop the last column
model.drop(inplace=True, columns=[trained_by])

# initialize the dictionary model with a nested  dictionary called sum to save the calculations to use theme in the end
statistics = {"sum": {"total_cases": len(copy_model.index)}}

# start loop through  the list that contains the unique options in the class column
for unique_posiability in column_trained_by.unique():
    #  for each option count the number of times it appears in the class column (we will need it for calculations in the end
    statistics['sum'][unique_posiability] = (copy_model[trained_by] == unique_posiability).sum()

    statistics[unique_posiability] = {}
    for column in model.columns:
        statistics[unique_posiability][column] = {}
        for unique_key in model[column].unique():
            statistics[unique_posiability][column][unique_key] = ((copy_model[column] == unique_key) & (copy_model[trained_by] == unique_posiability)).sum() / statistics['sum'][unique_posiability]



pprint.pprint(statistics, width=120)

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
            # ensure there is no value 0 in the list because if so the final calculation by
            if 0 in list_of_nums:
                list_of_nums += 1
            result = np.prod(list_of_nums)
            result %= 1
            final_result[option] = result

    for key, val in final_result.items():
        print(f"{key} has {val}")
    strong = max(final_result, key=final_result.get)
    print(f"it is obviously {strong} :-)")

    return final_result

print()



mendies_dict=sample_candidate = {
    "degree": "Master",
    "experience_years": 5,
    "certification": "yes",
    "english_level": "high",
    "location": "Tel Aviv",
    "willing_to_travel": "yes",
    "worked_remotely_before": "yes"
}

dicti={"weather":"sunny",
       "day":"weekend"}


print(ask_a_question(statistics, dicti))