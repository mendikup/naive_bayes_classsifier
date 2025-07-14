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

        # Compute posterior probability for each label using conditional probabilities
        final_result = {}
        for label in model["sum"]:
            likelihoods = []
            if label == "total_cases":
                continue


            for feature ,value in dict_test.items():
                try:
                    conditional_prob = model[label][feature][dict_test[value]]
                except KeyError:
                    conditional_prob = 1e-10  #if the specific value is missing we add min value

                likelihoods.append(conditional_prob)
            likelihoods.append(model['sum'][label] / model['sum']['total_cases'])
            likelihoods = np.array(likelihoods)
            result = np.prod(likelihoods)
            final_result[label] = result


        most_prob = max(final_result, key=final_result.get)

        return most_prob


