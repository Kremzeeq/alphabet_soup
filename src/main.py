"""
Alphabet soup

Please refer to ../README.md for more information on this code

In depth explaination, with analysis of reports/alphabet_soup_report.csv is available
in ../alphabet_soup_report.pdf


"""

import experimenter
import csv_report_fixer
import datetime
from timeit import default_timer as timer
import pyspellchecker_word_finder

start = timer()

experimenter_cls = experimenter.Experimenter()

"""
Main Code Section 1

This to to help identify optimal parameters

PLEASE NOTE: This code section takes approx 4 hours to run as it takes time to 
obtain proxy words for encrypted words using spell checking libraries;
 Textblob and Pyspellchecker.

Finding words using the text_blob_Word_finder is particularly time intensive. 

Results from running this section of code are written to: ../reports/alphabet_soup_report.csv

This can be analyzed e.g. through using pandas along with graphical libraries/ 


"""
#experimenter_cls.execute_experimenter()

"""
Main Code Section 2

Allows user to run experimenter with optimal parameters as seen fit.
This is to try and obtain a decrypted word dictionary, closest to achieving the desired outcome.

Desired outcome: {'0ri0t':'wrist', '0ala00': 'galaxy', '0e00est':'request', '0e00ry': 'celery',
                  '0ra0e0': 'braved', 's00r0':'shirk', '00amy':'foamy', '0ebr0': 'zebra', 
                  '0o0ey': 'money', '0ro0ec0': 'project'}
                
Example outcome: {'0ala00': 'galaxy', '0ro0ec0': 'project', '0ra0e0': 'brazen', '0e00est': 'request', 
                  '0o0ey': 'dovey', 's00r0': 'swarm', '0ri0t': 'lriet', '00amy': 'foamy', 
                  '0ebr0': 'cebri', '0e00ry': 'heskry'}
                  
The best outcome from running the parameters will be logged in the shell and also will be appended to 
the file: reports/alphabet_soup_report.csv. Thus it will be found at the base of the file,
in the right-most column: best_decrypted_word_dict.

Uncomment the code below to run Main Code Section 2.             

PLEASE NOTE: the pyspellchecker is provided as the default word finder for the use case below.      
"""

"""
text_blob_params_dict = experimenter_cls.get_text_blob_params_dict(min_iters_per_epoch=0,
                                                               min_potential_words=0,
                                                               max_epochs=0,
                                                               max_attempts=0)
word_decoder_max_epochs=75
word_finder=pyspellchecker_word_finder.PyspellcheckerWordFinder
experimenter_cls.pyspellchecker_no_of_random_letters = 10
experimenter_cls.get_results_for_params(text_blob_params_dict, word_decoder_max_epochs, word_finder)

end = timer()
seconds = end-start
time_taken = str(datetime.timedelta(seconds=seconds))
print("Time taken", time_taken)

"""

"""
Main Code Section 3

This executes the CSVReportFixer instance so that a 'fixed' version of the alphabet_soup_report.csv
is produced which can be read into a pandas dataframe for analysis. 

alphabet_soup_pandas_problem.html provides more information on this

"""


csv_report_fixer_cls = csv_report_fixer.CSVReportFixer('../reports/alphabet_soup_report.csv',
                                                       '../reports/alphabet_soup_report_fixed.csv')

csv_report_fixer_cls.execute()