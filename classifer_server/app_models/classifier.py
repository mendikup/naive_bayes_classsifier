import  numpy as np

class Classifier:

    @staticmethod
    def get_the_most_probability_predict(trained_model, params_and_values):
        """
        Predicts the most probable classification using the Naive Bayes model.

        :param trained_model: Nested dictionary of conditional probabilities.
        :param params_and_values: Dictionary of chosen attribute values {column_name: value}.
        :return: Most probable class label.
        """

        # calculate  probability for each label using conditional probabilities
        final_result = {}
        for label in trained_model["sum"]: # "sum"  key is referenced to amount of total cases/rows ,amount of each
                                           # cases for specific label in the the table
            if label == "total_cases":
                continue
            likelihoods = []
            for feature ,value in params_and_values.items():
                try:
                    prob = trained_model[label][feature][value]
                except KeyError:
                    prob = 1e-10  #if the specific value is missing we add min value

                likelihoods.append(prob)

            likelihoods.append(trained_model['sum'][label] / trained_model['sum']['total_cases'])
            likelihoods = np.array(likelihoods)
            result = np.prod(likelihoods)
            final_result[label] = result

        # Select the class label with the highest calculated probability
        most_prob = max(final_result, key=final_result.get)

        return most_prob


