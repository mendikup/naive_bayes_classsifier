from core.classifier import Classifier

class Tester:
    """
    Utility class to test model accuracy on labeled test data.
    """
    @staticmethod
    def check_accuracy_percentage(trained_model, test_df):
        """
        Calculates how many predictions match the true labels in the test set.

        :param trained_model: trained Naive Bayes model.
        :param test_df: DataFrame with same structure as training set.
        :return: Accuracy percentage (0–100).
        """
        if test_df.empty:
            return 0.0

        correct_guesses = 0
        # Iterate over each row, predict its class, compare with actual label
        for i in range(len(test_df.index)):
            params_and_values = {}
            expected = test_df.iloc[i, -1]
            row_values = test_df.iloc[i, :-1]
            for inx_row in row_values.index:
                params_and_values[inx_row] = row_values[inx_row]
            predicted = Classifier.get_the_most_probability_predict(trained_model, params_and_values)
            if predicted == expected:
                correct_guesses += 1

        return (correct_guesses / len(test_df.index)) * 100