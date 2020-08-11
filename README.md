# Alphabet Soup
## A problem of decrypting encrypted words using Python


![alphabet_soup](assets/alphabet_soup.jpg "alphabet_soup")

## Here's the Alphabet Soup problem:

A list contains 10 common English words. However, they are incomplete.
Zeros in each word represent where letters of the alphabet should substitute these.
There are at least 26 zeros and each letter of the alphabet should be used exactly once to substitute the zeros and arrive at decrypted_words.

The answers should be provided in a dictionary where encrypted words correspond to decrypted words. 

Here's the encrypted list of words:

encrypted_words = ['0ri0t', '0ala00', '0e00est', '0e00ry', '0ra0e0', 's00r0', '00amy', '0ebr0', '0o0ey','0ro0ec0']

Here's the desired outcome as a dictionary: 

answers_dict = {'0ri0t':'wrist', '0ala00': 'galaxy', '0e00est':'request', '0e00ry': 'celery',
                '0ra0e0': 'braved', 's00r0':'shirk', '00amy':'foamy', '0ebr0': 'zebra', 
                '0o0ey': 'money', '0ro0ec0': 'project'}

## Webpage Reports

There are two in-depth webpage reports viewable here:

a) [Alphabet Soup Project](https://htmlpreview.github.io/?https://github.com/Kremzeeq/alphabet_soup/blob/master/alphabet_soup_project.html)

This provides in-depth analysis on this project with further information.
A report is produced using data from [reports/alphabet_soup_report_fixed.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report_fixed.csv)

b) [Alphabet Soup Pandas Problem](https://htmlpreview.github.io/?https://github.com/Kremzeeq/alphabet_soup/blob/master/alphabet_soup_pandas_problem.html)

This provides a separate side project involving pandas to fix the formatting problem
with the [reports/alphabet_soup_sample_report.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_sample_report.csv) file.
This helps produce the fixed version of the file which is analysed for the Alphabet Soup project.
This is a copy of [reports/alphabet_soup_sample_report.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report.csv) just in case it is overwritten by the user.

## Running the code

* Ensure [requirements.txt](https://github.com/Kremzeeq/alphabet_soup/blob/master/requirements.txt) is installed

* Please consider that [src/main.py](https://github.com/Kremzeeq/alphabet_soup/blob/master/src/main.py) is split into three sections.

* Comment or uncomment code as seen fit for the three code sections prior to running the code.

### Here's an overview of the three main code sections:

1. This to to help identify optimal parameters for solving the alphabet soup problem.
Results are written to [reports/alphabet_soup_sample_report.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report.csv)

2. Allows user to run [src.experimenter.py](https://github.com/Kremzeeq/alphabet_soup/blob/master/src/experimenter.py) with optimal parameters as seen fit. Results for the
test run would be appended to [reports/alphabet_soup_sample_report.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report.csv)

3. This provides a **fixed** version of [reports/alphabet_soup_sample_report.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report.csv) which may be updated by the user.
This results in producing [reports/alphabet_soup_sample_report_fixed.csv](https://github.com/Kremzeeq/alphabet_soup/blob/master/reports/alphabet_soup_report_fixed.csv) using
 [src/csv_report_fixer.py](https://github.com/Kremzeeq/alphabet_soup/blob/master/src/csv_report_fixer.py).
 This follows steps presented in the Alphabet Soup Pandas Problem webpage report. 