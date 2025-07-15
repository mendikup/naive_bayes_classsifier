import  numpy as np

class Classifier:

    @staticmethod
    def ask_a_question(trained_model, dict_test):
        """
        Predicts the most probable classification using the Naive Bayes model.

        :param trained_model: Nested dictionary of conditional probabilities.
        :param dict_test: Dictionary of chosen attribute values {column_name: value}.
        :return: Most probable class label.
        """

        # Compute  probability for each label using conditional probabilities
        final_result = {}
        for label in trained_model["sum"]:
            likelihoods = []
            if label == "total_cases":
                continue

            for feature ,value in dict_test.items():
                try:
                    conditional_prob = trained_model[label][feature][value]
                except KeyError:
                    conditional_prob = 1e-10  #if the specific value is missing we add min value

                likelihoods.append(conditional_prob)

            likelihoods.append(trained_model['sum'][label] / trained_model['sum']['total_cases'])
            likelihoods = np.array(likelihoods)
            result = np.prod(likelihoods)
            final_result[label] = result

        # Select the class label with the highest calculated probability
        most_prob = max(final_result, key=final_result.get)

        return most_prob


