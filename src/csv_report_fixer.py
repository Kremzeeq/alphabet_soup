import pandas as pd

class CSVReportFixer:
    def __init__(self, csv_report, fixed_csv_report):
        """
        This module follows steps in the alphabet_soup_pandas_problem
        It deals with a certain use case where columns have particular labels
        csv_report: This is the path for the CSV report which need to be fixed
        fixed_csv_report: This is the path for the fixed CSV report
        """
        self.csv_report = csv_report
        self.fixed_csv_report = fixed_csv_report

    def execute(self):
        results_df = self.read_report_csv_as_df()
        columns = self.get_df_columns(results_df)
        results_df = self.convert_columns_to_string(results_df)
        results_df = self.fix_best_decrypted_word_dict_column(results_df)
        results_df = self.drop_columns_not_needed_and_reset_index(results_df)
        self.rename_columns_and_write_to_csv(results_df, columns)

    def read_report_csv_as_df(self):
        """
        Step 1: Read the dataframe
        """
        print("Executing CSVReportFixer")
        return pd.read_csv(self.csv_report)

    def get_df_columns(self, results_df):
        """
        Step 2: Get df columns
        """
        return results_df.columns


    def convert_columns_to_string(self, results_df):
        """
        Step 3: Converts 'object' columns to 'string'

        """
        results_df[["word_decoder_max_epochs", "word_finder_min_iters_per_epoch",
                    "word_finder_min_potential_words", "word_finder_max_epochs",
                    "word_finder_max_attempts", "no_of_random_letters", "time_taken_in_seconds",
                    "word_finder_name", "best_accuracy", "best_decrypted_word_dict"]] =\
                    results_df[["word_decoder_max_epochs", "word_finder_min_iters_per_epoch",
                    "word_finder_min_potential_words", "word_finder_max_epochs",
                    "word_finder_max_attempts", "no_of_random_letters", "time_taken_in_seconds",
                    "word_finder_name", "best_accuracy", "best_decrypted_word_dict"]].astype('string')

        return results_df

    def fix_best_decrypted_word_dict_column(self, results_df):
        """
        Step 4: Concatenate the respective string columns under
        the 'best_decrypted_word_dict' column.
        Set the data type for the column as string.
        """
        results_df['best_decrypted_word_dict'] =\
            results_df[["word_decoder_max_epochs", "word_finder_min_iters_per_epoch",
                        "word_finder_min_potential_words", "word_finder_max_epochs",
                        "word_finder_max_attempts", "no_of_random_letters", "time_taken_in_seconds",
                        "word_finder_name", "best_accuracy", "best_decrypted_word_dict"]].agg(','.join, axis=1)
        results_df["best_decrypted_word_dict"].astype('string')
        return results_df

    def drop_columns_not_needed_and_reset_index(self, results_df):
        """
        Step 5: Drop the columns which are no longer needed and reset the column index
        """
        results_df.drop(["word_decoder_max_epochs", "word_finder_min_iters_per_epoch",
                         "word_finder_min_potential_words", "word_finder_max_epochs",
                         "word_finder_max_attempts", "no_of_random_letters", "time_taken_in_seconds",
                         "word_finder_name", "best_accuracy"], axis=1, inplace=True)

        results_df.reset_index(inplace=True)
        return results_df

    def rename_columns_and_write_to_csv(self, results_df, columns):
        """
        Step 6: Rename columns and write the dataframe to self.fixed_csv_report
        :param columns:
        :return:
        """
        results_df.columns = columns
        results_df.to_csv(self.fixed_csv_report, index=False)
        print(self.csv_report, "has been fixed so it can be read as a dataframe for analysis")
        print("Fixed file is available here:", self.fixed_csv_report)