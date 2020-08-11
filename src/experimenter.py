
import string
import text_blob_word_finder
import pyspellchecker_word_finder
import encrypted_word_decoder
import report_maker
import copy
from timeit import default_timer as timer

def get_potential_words_dict_collection_report(potential_words_dict_collection):
    for k, v in potential_words_dict_collection.items():
        print("Key", k)
        print("Value", v)

class Experimenter():
    """
    The purpose of this class is to expand the alphabet_soup_report to help
    find optimal parameters for decrypting the encrypted_words provided
    in the answers_dict. Results are written to CSV using the ReportMaker class.
    Parameters passed to the Pyspellchecker and TextBlob word finders and
    EncryptedWordDecoders are logged, along with time taken and mean accuracy.
    Mean accuracy represents the % of words that were correctly decrypted according to
    various fixed parameters such as epochs. Epoching has been essential due to the
    randomisation used throughout the program.
    """
    def __init__(self):
        self.alphabet = list(string.ascii_lowercase)
        self.answers_dict = {'0ri0t':'wrist', '0ala00': 'galaxy', '0e00est':'request', '0e00ry': 'celery',
                '0ra0e0': 'braved', 's00r0':'shirk', '00amy':'foamy', '0ebr0': 'zebra', '0o0ey': 'money',
                '0ro0ec0': 'project'}
        self.encrypted_words = ['0ri0t', '0ala00', '0e00est', '0e00ry', '0ra0e0', 's00r0', '00amy', '0ebr0', '0o0ey',
                           '0ro0ec0']
        self.text_blob_params_dict = self.get_text_blob_params_dict(min_iters_per_epoch=50,
                                                                        min_potential_words=5,
                                                                        max_epochs=3,
                                                                        max_attempts=3)
        self.text_blob_word_finder = text_blob_word_finder.TextBlobWordFinder
        self.word_decoder_max_epochs = 75
        self.pyspellchecker_no_of_random_letters = 0
        self.pyspellchecker_word_finder = pyspellchecker_word_finder.PyspellcheckerWordFinder

    def get_text_blob_params_dict(self, min_iters_per_epoch, min_potential_words, max_epochs, max_attempts):
        return {"min_iters_per_epoch": min_iters_per_epoch,
                "min_potential_words": min_potential_words,
                "max_epochs": max_epochs,
                "max_attempts": max_attempts}

    def execute_experimenter(self):
        self.get_results_for_text_blob_word_finder()
        self.pyspellchecker_no_of_random_letters = 10
        self.text_blob_params_dict = {k:0 for (k,v) in self.text_blob_params_dict.items()}
        self.get_results_for_pyspellchecker_word_finder()

    def get_results_for_text_blob_word_finder(self):

        self.get_results_for_control(self.text_blob_word_finder)
        self.get_results_for_changing_text_blob_params_dict("min_iters_per_epoch", [50, 75, 100, 125, 150])
        self.get_results_for_changing_text_blob_params_dict("min_potential_words", [3, 4, 5, 6, 7])
        self.get_results_for_changing_text_blob_params_dict("max_epochs", [3, 4, 5, 6, 7, 8])
        self.get_results_for_changing_text_blob_params_dict("max_attempts", [3, 4, 5])
        self.get_results_for_changing_word_decoder_max_epochs([5, 10, 25, 50, 75, 100, 125, 150], self.text_blob_word_finder)

    def get_results_for_pyspellchecker_word_finder(self):
        self.get_results_for_control(self.pyspellchecker_word_finder)
        self.get_results_for_changing_word_decoder_max_epochs([5, 10, 25, 50, 75, 100, 125, 150], self.pyspellchecker_word_finder)
        self.get_results_for_changing_no_of_random_letters([5, 10, 15, 20, 25, 26])

    def get_results_for_control(self, word_finder):
        print("Getting control results for", word_finder.__name__)
        self.get_results_for_params(self.text_blob_params_dict, self.word_decoder_max_epochs, word_finder)

    def get_results_for_params(self, text_blob_params_dict, word_decoder_max_epochs, word_finder):
        start = timer()
        potential_words_dict_collection = self.get_potential_words_dict_collection_for_word_finder(word_finder,
                                                                                                   text_blob_params_dict)

        get_potential_words_dict_collection_report(potential_words_dict_collection)

        encrypted_word_decoder_cls = encrypted_word_decoder.EncryptedWordDecoder(self.alphabet,
                                                                             self.encrypted_words,
                                                                             potential_words_dict_collection,
                                                                             max_epochs=word_decoder_max_epochs)
        decrypted_words_dict_collection = encrypted_word_decoder_cls.execute_encrypted_word_decoder()
        print(decrypted_words_dict_collection)
        end = timer()
        time_taken_in_seconds = end-start
        word_finder_name = word_finder.__name__
        report_maker_cls = report_maker.ReportMaker(self.answers_dict, decrypted_words_dict_collection,
                                                text_blob_params_dict, word_decoder_max_epochs,
                                                time_taken_in_seconds, word_finder_name,
                                                self.pyspellchecker_no_of_random_letters)

        report_maker_cls.execute_report_maker()

    def get_results_for_changing_text_blob_params_dict(self, field, test_list):
        print("Getting results for {}, with test_list {}".format(field, test_list))
        for x in test_list:
            word_finder_params_dict_copy = copy.deepcopy(self.text_blob_params_dict)
            word_finder_params_dict_copy[field] = x
            self.get_results_for_params(word_finder_params_dict_copy, self.word_decoder_max_epochs, self.text_blob_word_finder)
        print("Completed test for", field)

    def get_results_for_changing_word_decoder_max_epochs(self, test_list, word_finder):
        print("Getting results for word_decoder_max_epochs, with test_list {}".format(test_list))
        for x in test_list:
            self.get_results_for_params(self.text_blob_params_dict, x, word_finder)
        print("Completed test for word_decoder_max_epochs")

    def get_results_for_changing_no_of_random_letters(self, test_list):
        print("Getting results for changing pyspellchecker_no_of_random_letters, with test_list {}".format(test_list))
        for x in test_list:
            self.pyspellchecker_no_of_random_letters = x
            self.get_results_for_params(self.text_blob_params_dict, self.word_decoder_max_epochs,
                                        self.pyspellchecker_word_finder)
        print("Completed test for changing pyspellchecker_no_of_random_letters")

    def get_potential_words_dict_collection(self, word_finder, **kwargs):
        """
        :return: {self.encrypted_word:"potential_words_list": potential_words_list,
                                    "zeros_list": self.zeros_list, "success": success}}
        e.g. {'0ri0t': {'potential_words_list': ['drift', 'grist', 'wrist', 'print'],
                'zeros_list': [0, 3], 'success': True}
        """
        potential_words_dict_collection = {}

        for encrypted_word in self.encrypted_words:
            word_finder_instance = word_finder(encrypted_word, self.alphabet, **kwargs)

            potential_words_dict = word_finder_instance.execute()
            potential_words_dict_collection.update(potential_words_dict)
        return potential_words_dict_collection

    def get_potential_words_dict_collection_for_word_finder(self, word_finder_meta_class, text_blob_params_dict):
        potential_words_dict_collection = {}
        word_finder_name = word_finder_meta_class.__name__
        if word_finder_name == "TextBlobWordFinder":
            print("Getting TextBlobWordFinder word_dict_collection")
            potential_words_dict_collection = self.get_potential_words_dict_collection(word_finder_meta_class,
                                                                                       **text_blob_params_dict)
        elif word_finder_name== "PyspellcheckerWordFinder":
            print("Getting PyspellcheckerWordFinder word_dict_collection")
            potential_words_dict_collection = self.get_potential_words_dict_collection(
                                            word_finder_meta_class, no_of_random_letters=self.pyspellchecker_no_of_random_letters)
        if potential_words_dict_collection:
            return potential_words_dict_collection
        else:
            raise ValueError("No potential_words_dict_collection. Check word_finder string names")

"""
Time taken for previous runs
4H36M11S
3H:57M:55S

FOR TESTING
potential_words_dict_collection = { '0ri0t': {'potential_words_list': ['drift', 'grist', 'wrist', 'print'], 'zeros_list': [0, 3], 'success': True},
'0ala00': {'potential_words_list': ['balaga', 'galaxy', 'palate', 'palace', 'galant', 'falaba', 'salary', 'malady'], 'zeros_list': [0, 4, 5], 'success': True},
'0e00est': {'potential_words_list': ['tempest', 'keenest', 'nearest', 'meekest', 'deepest', 'request', 'bequest', 'dearest', 'veriest', 'meanest'], 'zeros_list': [0, 2, 3], 'success': True},
'0e00ry': {'potential_words_list': ['sentry', 'gentry', 'belfry', 'memory', 'vestry', 'descry'], 'zeros_list': [0, 2, 3], 'success': True},
'0ra0e0': {'potential_words_list': ['grades', 'draped', 'erased', 'traced', 'grazed', 'crater', 'grated', 'urates', 'brazen', 'trades', 'prayed', 'traded', 'graven', 'gravel', 'erases', 'framed', 'frayed', 'crates', 'braved', 'fraser', 'graves', 'graver', 'travel', 'trader', 'traces', 'braced', 'prayer', 'frames', 'graces', 'drawer', 'prater', 'braver', 'grapes', 'braces'], 'zeros_list': [0, 3, 5], 'success': True},
's00r0': {'potential_words_list': ['sworn', 'sacro', 'snort', 'store', 'stark', 'scars', 'sport', 'scurf', 'spore', 'smart', 'snare', 'swore', 'snore', 'scare', 'shorn', 'skirt', 'spurs', 'shirt', 'sorry', 'share', 'spark', 'start', 'spire', 'short', 'scarf', 'score', 'story', 'swarm', 'shore', 'snarl', 'sacre', 'sears', 'sharp', 'seers', 'sabre', 'storm', 'stirs', 'sword', 'scorn', 'supra', 'stern', 'stars', 'spare', 'stare'], 'zeros_list': [1, 2, 4], 'success': True},
'00amy': {'potential_words_list': [], 'zeros_list': [0, 1], 'success': False},
'0ebr0': {'potential_words_list': [], 'zeros_list': [0, 4], 'success': False},
'0o0ey': {'potential_words_list': ['coley', 'dovey', 'money', 'honey'], 'zeros_list': [0, 2], 'success': True},
'0ro0ec0': {'potential_words_list': ['protect', 'project'], 'zeros_list': [0, 3, 6], 'success': True}}


"""
