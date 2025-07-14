import  numpy as np

class Classifier:

    @staticmethod
    def ask_a_question(model, dict_test):
        """
        Predicts the most probable classification using the Naive Bayes model.

        :param trained_model: Nested dictionary of conditional probabilities.
        :param dict_test: Dictionary of chosen attribute values {column_name: value}.
        :return: Most probable class label.
        """

        # Compute posterior probability for each class using conditional probabilities
        final_result = {}
        for option in model["sum"]:
            list_of_nums = []
            if not option == "total_cases":
                for column in dict_test:
                    try:
                        conditional_prob = model[option][column][dict_test[column]]
                    except KeyError:
                        conditional_prob = 1e-10  #if the specific value is

                    list_of_nums.append(conditional_prob)
                list_of_nums.append(model['sum'][option] / model['sum']['total_cases'])
                list_of_nums = np.array(list_of_nums)



                # multiply the
                result = np.prod(list_of_nums)

                final_result[option] = result


        most_prob = max(final_result, key=final_result.get)
        # print(f" according to the model the answer to your question in the  highest probability is {strong} ")

        return most_prob


