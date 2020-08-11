import random
from textblob import Word as Textblob

class TextBlobWordFinder():
    """
    Class evaluates an encrypted_word using the Textblob library.
    When executed, the class provides a dictionary containing an index positions for where
    zeros represent letters in the word. It also provides a 'success' parameter, which
    provides a boolean value as to whether potential words have been found for the encrypted_word.
    A list of potential words is also provided in the dictionary in the final potential_words_dict
    for the encrypted_word.
    """
    def __init__(self, encrypted_word, alphabet, **kwargs):
        """
        :param kwargs:
        max_epochs: maximum number of epochs which are run with a minimum number of interations.
        min_iters_per_epoch: minimum number of iterations in an epoch. In each iteration,
        letters randomly substitute the zeros in the word to produce a test_word. The test_word
        is the passed to a nlp TextBlob object which will produce proxy words based
        on the spelling of the word. The proxy words are evaluated to check they are potential words.
        min_potential_words: If the threshold of providing a minimum number of potential words is not
        satisfied following epoching, then another attempt is made to derive proxy words for
        the encrypted words.
        max_attempts: limits the number of attempts
        """
        self.encrypted_word = encrypted_word
        self.min_iters_per_epoch = kwargs.get('min_iters_per_epoch')
        self.min_potential_words = kwargs.get('min_potential_words')
        self.max_epochs = kwargs.get('max_epochs')
        self.max_attempts = kwargs.get('max_attempts')
        self.alphabet = alphabet
        self.zeros_list = self.get_zeros_indexes()
        self.split_word = list(self.encrypted_word)

    def get_zeros_indexes(self):
        """
        Produces a list of indexes (self.zeros_list)
        where zeros represent letters in the encrypted_word
        :return e.g. '0ri0t' -> [0, 3]

        """
        # index the first zero
        zeros_list = []
        first_zero_index = self.encrypted_word.index('0')
        zeros_list.append(first_zero_index)
        for x in range(first_zero_index+1, len(self.encrypted_word)):
            if self.encrypted_word[x] == "0":
                zeros_list.append(x)
        return zeros_list

    def execute(self):
        success_dict = self.run_epochs_and_get_potential_words_dict(self.max_attempts)
        return success_dict

    def run_epochs_and_get_potential_words_dict(self, attempts_limit):
        """
        Epochs are run based on the attempts_limit and a potential_words_dict is provided
        :return: {self.encrypted_word: {"potential_words_list": potential_words_list,
                            "zeros_list": self.zeros_list, "success": success}}
        """
        print("Running epochs for", self.encrypted_word)
        potential_words_list = []
        attempts = 1
        success = True
        while bool(potential_words_list) == False:
            print("Attempt(s):", attempts)
            potential_words_list = self.get_minimal_potential_words_list()
            attempts += 1
            if attempts == attempts_limit+1:
                success = False
                print("No words found. results_dict['success']= False")
                break
        return {self.encrypted_word: {"potential_words_list": potential_words_list,
                            "zeros_list": self.zeros_list, "success": success}}

    def get_minimal_potential_words_list(self):
        """
        While the potential_word_list has fewer words than the required
        min_potential_words, epochs will be run to help build
        the potential_words_list. The epoch limit is determined
        by self.max_epochs
        :return:
        """
        potential_words_list = []
        epochs = 1
        while len(potential_words_list) < self.min_potential_words:
            print("Epoch {} of {}".format(epochs, self.max_epochs))
            potential_words_list.extend(self.get_potential_words_list_for_epoch(self.min_iters_per_epoch))
            potential_words_list = list(set(potential_words_list))
            epochs += 1
            if epochs == self.max_epochs + 1:
                break
        return potential_words_list

    def get_potential_words_list_for_epoch(self, min_iters_per_epoch):
        """
        A potential_words_list is build based on the minimum no. of iterations
        set for the epoch
        :param min_iters_per_epoch:
        :return:
        """
        potential_words_list = []
        for x in range(0, min_iters_per_epoch):
            test_word = self.get_test_word()
            proxy_words_list = self.get_proxy_words_dict(test_word)
            new_potential_words_list = self.get_potential_words_list(proxy_words_list)
            if new_potential_words_list:
                potential_words_list.extend(new_potential_words_list)
                potential_words_list = list(set(potential_words_list))
        return potential_words_list

    def get_test_word(self):
        """
        test_word created by substituting zeros from a split version of
        the encrypted_word (self.split_word) and with random letters. This
        references the self.zeros_list.
        :return: e.g. '0ri0t' -> drift

        """
        local_split_word = self.split_word.copy()
        random_letters = []
        for x in self.zeros_list:
            random_letter = None
            while random_letter not in random_letters:
                random_letter = random.choice(self.alphabet)
                local_split_word[x] = random_letter
                random_letters.append(random_letter)
        return "".join(local_split_word)

    def get_potential_words_list(self, proxy_words_dict):
        """
        Weightings are removed. A potential_words_list is built
        where words are the same length as the encrypted_word
        :param proxy_words_dict: e.g. {'wrist': 0.39, 'print': 0.29}
        :return: ['wrist', 'print']
        """
        potential_words_list = []
        for potential_word, v in proxy_words_dict.items():
            if v > 0 and len(potential_word) == len(self.encrypted_word):
                if self.check_if_potential_word(potential_word):
                    potential_words_list.append(potential_word)
        return potential_words_list

    def check_if_potential_word(self, potential_word):
        """
        letters (non zeros) from the split encrypted_word are
        checked against those at index positions in the potential_word.
        This is to deduce that it is truly a potential_word
        :param potential_word:
        :return: bool
        """
        split_potential_word = list(potential_word)
        for c, x in enumerate(self.split_word):
            if x.isalpha():
                if x != split_potential_word[c]:
                    return False
        return True

    def get_proxy_words_dict(self, test_word):
        """
        text_word e.g. 'rrixt', is passed to the NLP TextBlob object.
        This produces a list of tuples with proxy_words and a weighting e.g.
        [('wrist', 0.39), ('print', 0.29)]
        Basically, weightings >0 mean the proxy word is part of the English language.
        However, not clear on web if this corresponds to GB or US English.
        The list is transformed into a dictionary.
        Basically the spellcheck can be thought of as a fuzzy match to find actual words
        :param test_word: produce from self.get_test_word
        :return: e.g. {'wrist': 0.39, 'print': 0.29}
        """
        textblob = Textblob(test_word)
        proxy_words = textblob.spellcheck()

        proxy_words_dict = dict(proxy_words)
        return proxy_words_dict
















"""
Result pre-applying brute force to first index position
Here's the potential_words_dict_collection
{'0ri0t': {'potential_words_list': ['grist', 'britt', 'print', 'gritt', 'drift', 'trist', 'wrist', 'pritt'], 'zeros_list': [0, 3], 'success': True}, '0ala00': {'zeros_list': [0, 4, 5], 'success': False}, '0e00est': {'zeros_list': [0, 2, 3], 'success': False}, '0e00ry': {'zeros_list': [0, 2, 3], 'success': False}, '0ra0e0': {'zeros_list': [0, 3, 5], 'success': False}, 's00r0': {'zeros_list': [1, 2, 4], 'success': False}, '00amy': {'potential_words_list': ['foamy', 'loamy', 'seamy'], 'zeros_list': [0, 1], 'success': True}, '0ebr0': {'potential_words_list': ['debra', 'gebre', 'debre', 'zebra'], 'zeros_list': [0, 4], 'success': True}, '0o0ey': {'potential_words_list': ['honey', 'foley', 'money', 'toney', 'covey', 'coney', 'howey', 'robey', 'gooey', 'boney', 'pokey', 'bogey', 'povey', 'cowey', 'jokey', 'nosey', 'corey', 'tovey', 'fogey', 'lovey', 'posey', 'mobey', 'fowey', 'josey', 'soley', 'bovey', 'pooey', 'coley', 'dokey', 'mosey', 'ropey', 'homey', 'holey', 'dopey', 'dovey', 'losey', 'morey'], 'zeros_list': [0, 2], 'success': True}, '0ro0ec0': {'zeros_list': [0, 3, 6], 'success': False}}
Key 0ri0t
Value {'potential_words_list': ['grist', 'britt', 'print', 'gritt', 'drift', 'trist', 'wrist', 'pritt'], 'zeros_list': [0, 3], 'success': True}
Key 0ala00
Value {'zeros_list': [0, 4, 5], 'success': False}
Key 0e00est
Value {'zeros_list': [0, 2, 3], 'success': False}
Key 0e00ry
Value {'zeros_list': [0, 2, 3], 'success': False}
Key 0ra0e0
Value {'zeros_list': [0, 3, 5], 'success': False}
Key s00r0
Value {'zeros_list': [1, 2, 4], 'success': False}
Key 00amy
Value {'potential_words_list': ['foamy', 'loamy', 'seamy'], 'zeros_list': [0, 1], 'success': True}
Key 0ebr0
Value {'potential_words_list': ['debra', 'gebre', 'debre', 'zebra'], 'zeros_list': [0, 4], 'success': True}
Key 0o0ey
Value {'potential_words_list': ['honey', 'foley', 'money', 'toney', 'covey', 'coney', 'howey', 'robey', 'gooey', 'boney', 'pokey', 'bogey', 'povey', 'cowey', 'jokey', 'nosey', 'corey', 'tovey', 'fogey', 'lovey', 'posey', 'mobey', 'fowey', 'josey', 'soley', 'bovey', 'pooey', 'coley', 'dokey', 'mosey', 'ropey', 'homey', 'holey', 'dopey', 'dovey', 'losey', 'morey'], 'zeros_list': [0, 2], 'success': True}
Key 0ro0ec0
Value {'zeros_list': [0, 3, 6], 'success': False}
"""