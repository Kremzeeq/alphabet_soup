import pprint

import statistics
import os

class ReportMaker():
    def __init__(self, answers_dict, decrypted_words_dict_collection, text_blob_params_dict,
                 word_decoder_max_epochs, time_taken_in_seconds, word_finder_name, no_of_random_letters):
        self.answers_dict = answers_dict
        self.decrypted_words_dict_collection = decrypted_words_dict_collection
        self.text_blob_params_dict = text_blob_params_dict
        self.word_decoder_max_epochs = word_decoder_max_epochs
        self.time_taken_in_seconds = time_taken_in_seconds
        self.word_finder_name = word_finder_name
        self.no_of_random_letters = no_of_random_letters

    def execute_report_maker(self):
        pp = pprint.PrettyPrinter(width=41, compact=True)
        pp.pprint(self.decrypted_words_dict_collection)
        result_dict_for_runs = self.get_result_dict_for_runs()
        list_of_percentage_of_words_correct_for_runs = result_dict_for_runs["list_of_percentage_of_words_correct_for_runs"]
        self.get_report_for_each_run(list_of_percentage_of_words_correct_for_runs)
        summary_report_dict_for_runs = self.get_summary_report_dict_for_runs(result_dict_for_runs)
        self.write_report_to_csv(summary_report_dict_for_runs)
        self.get_best_accuracy_report(summary_report_dict_for_runs)

    def get_summary_report_dict_for_runs(self, result_dict_for_runs):
        """
        mean_accuracy: The average of encrypted words correctly decrypted for runs as %.
        standard_deviation and median are in relation to list_of_percentage_of_words_correct_for_runs
        and are represents as %. Standard dev would represent % points.
        """
        list_of_percentage_of_words_correct_for_runs = \
            result_dict_for_runs["list_of_percentage_of_words_correct_for_runs"]
        mean_accuracy = statistics.mean(list_of_percentage_of_words_correct_for_runs)*100
        standard_dev = statistics.stdev(list_of_percentage_of_words_correct_for_runs)*100
        median = statistics.median(list_of_percentage_of_words_correct_for_runs)*100
        print("Overall mean accuracy: {}%".format(round(mean_accuracy,2)))
        print("Standard deviation: {}% pts".format(round(standard_dev,2)))
        print("Median: {}%".format(median))
        return {"mean_accuracy": mean_accuracy, "standard_dev": standard_dev, "median": median,
                "no_of_runs": len(list_of_percentage_of_words_correct_for_runs),
                "best_accuracy":result_dict_for_runs["best_accuracy"]*100,
                "best_decrypted_word_dict": result_dict_for_runs["best_decrypted_word_dict"]}

    def get_report_for_each_run(self, list_of_percentage_of_words_correct_for_runs):
        counter = 1
        print("Accuracy report: % of Correct words assigned in runs")
        for percentage in list_of_percentage_of_words_correct_for_runs:
            print("Run {}: {}%".format(counter, percentage * 100))
            counter += 1

    def get_result_dict_for_runs(self):
        list_of_percentage_of_words_correct_for_runs = []
        no_of_words = len(self.answers_dict)
        best_accuracy = 0
        best_decrypted_word_dict = None
        for decrypted_words_dict in self.decrypted_words_dict_collection:
            counter = 0
            for encrypted_word, correct_word in self.answers_dict.items():
                if decrypted_words_dict[encrypted_word] == correct_word:
                    counter += 1
            accuracy = counter / no_of_words
            if accuracy > best_accuracy:
                best_accuracy=accuracy
                best_decrypted_word_dict=decrypted_words_dict
            list_of_percentage_of_words_correct_for_runs.append(accuracy)
        return {"list_of_percentage_of_words_correct_for_runs":list_of_percentage_of_words_correct_for_runs,
                "best_accuracy":best_accuracy, "best_decrypted_word_dict":best_decrypted_word_dict}

    def write_report_to_csv(self, summary_report_dict_for_runs):
        file_path= '../reports/alphabet_soup_report.csv'
        metrics_line_for_csv = self.get_metrics_line_for_csv(summary_report_dict_for_runs)

        if os.path.exists(file_path):
            report_writer = open(file_path, 'a')
            report_writer.write(metrics_line_for_csv)
            report_writer.close()
        else:
            report_writer = open(file_path, 'w')
            first_line = "no_of_runs,mean_accuracy,standard_dev,median,word_decoder_max_epochs," \
                         "word_finder_min_iters_per_epoch,word_finder_min_potential_words,word_finder_max_epochs," \
                         "word_finder_max_attempts,no_of_random_letters,time_taken_in_seconds,word_finder_name," \
                         "best_accuracy,best_decrypted_word_dict"
            lines = first_line+metrics_line_for_csv
            report_writer.write(lines)
            report_writer.close()
        print("Written report to csv")

    def get_metrics_line_for_csv(self, summary_report_dict_for_runs):
        no_of_runs = summary_report_dict_for_runs['no_of_runs']
        mean_accuracy = summary_report_dict_for_runs['mean_accuracy']
        standard_dev = summary_report_dict_for_runs['standard_dev']
        median = summary_report_dict_for_runs['median']
        word_finder_min_iters_per_epoch = self.text_blob_params_dict["min_iters_per_epoch"]
        word_finder_min_potential_words = self.text_blob_params_dict["min_potential_words"]
        word_finder_max_epochs = self.text_blob_params_dict["max_epochs"]
        word_finder_max_attempts = self.text_blob_params_dict["max_attempts"]
        best_accuracy=summary_report_dict_for_runs["best_accuracy"]
        best_decrypted_word_dict=summary_report_dict_for_runs["best_decrypted_word_dict"]

        line_for_csv = "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(no_of_runs,
                                                                          mean_accuracy,
                                                                          standard_dev,
                                                                          median,
                                                                          self.word_decoder_max_epochs,
                                                                          word_finder_min_iters_per_epoch,
                                                                          word_finder_min_potential_words,
                                                                          word_finder_max_epochs,
                                                                          word_finder_max_attempts,
                                                                          self.no_of_random_letters,
                                                                          self.time_taken_in_seconds,
                                                                          self.word_finder_name,
                                                                          best_accuracy,
                                                                          best_decrypted_word_dict)
        return line_for_csv

    def get_best_accuracy_report(self, summary_report_dict_for_runs):
        no_of_runs = summary_report_dict_for_runs["no_of_runs"]
        best_accuracy = summary_report_dict_for_runs["best_accuracy"]
        best_decrypted_word_dict = summary_report_dict_for_runs["best_decrypted_word_dict"]
        print("No of Runs", no_of_runs)
        print("Best Accuracy for runs:", round(best_accuracy,1),"%")
        print("Best Decrypted Word Dictionary for runs:\n")
        print(best_decrypted_word_dict)
