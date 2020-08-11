import random
from spellchecker import SpellChecker

class PyspellcheckerWordFinder():
    """
    Class evaluates an encrypted_word using the pyspellchecker library.
    When executed, the class provides a dictionary containing an index positions for where
    zeros represent letters in the word. It also provides a 'success' parameter, which
    provides a boolean value as to whether potential words have been found for the encrypted_word.
    A list of potential words is also provided in the dictionary in the final potential_words_dict
    for the encrypted_word.
    """
    def __init__(self, encrypted_word, alphabet, **kwargs):
        """

        :param encrypted_word: The original word which contains zeros which need to be decoded to
        arrive at a word
        :param alphabet: a list with alphabetical letters A-Z
        :param no_of_random_letters: Represents no. of random letters
        which would be substituted into encrypted words at the first zero index position to produce test words
        """
        self.encrypted_word = encrypted_word
        self.alphabet = alphabet
        self.zeros_list = self.get_zeros_indexes()
        self.split_word = list(self.encrypted_word)
        self.spell_checker = SpellChecker()
        self.no_of_random_letters = kwargs.get('no_of_random_letters')

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
        print("Executing word_finder for,", self.encrypted_word)
        if self.check_random_letters_valid():
            proxy_words_list = self.get_proxy_words_list()
            potential_words_list = self.get_potential_words_list(proxy_words_list)
            potential_words_dict = self.get_potential_words_dict(potential_words_list)
            return potential_words_dict

    def check_random_letters_valid(self):
        """
        Checks self.no_of_random_letters kwarg to see if it is a valid
        number of alphabetical letters which can be evaluated

        """
        if self.no_of_random_letters in range(1, 27):
            return True
        else:
            raise ValueError("Please ensure no_of_random_letters is inclusively between 1 and 26")



    def get_proxy_words_list(self):
        """
        self.spell_checker.candidates is very good at sourcing multiple proxy_words for
        half of the encrypted_words: '0ri0t','00amy','0ebr0', '0o0ey','0ro0ec0'.
        Further to this a proxy_word_list can be extended to include further results
        based on creating test_words based on substituting zeros in the encrypted_word
        """
        proxy_word_list = []
        proxy_word_list.extend(self.spell_checker.candidates(self.encrypted_word))
        test_words_proxy_words_list = self.get_proxy_words_for_test_words()
        proxy_word_list.extend(test_words_proxy_words_list)
        return list(set(proxy_word_list))

    def get_proxy_words_for_test_words(self):
        test_words_list = self.get_test_words()
        test_words_proxy_words_list = []
        for test_word in test_words_list:
            test_words_proxy_words_list.extend(self.spell_checker.candidates(test_word))
        return test_words_proxy_words_list

    def get_test_words(self):
        random_letters = self.get_random_letters()
        test_words_list = []
        for letter in random_letters:
            test_words_list.append(self.get_test_word(letter))
        return test_words_list

    def get_random_letters(self):
        """
        Provides a list of random letters based on self.no_of_random_letters
        """
        return random.sample(self.alphabet, self.no_of_random_letters)

    def get_test_word(self, letter):
        """
        As most of the encrypted_words in the alphabet_soup problem are missing the first letter,
        test_words can be created, where the first index from the zero_list is substituted with a letter.
        This means there may be more accuracy in finding potential_words.
        Note, substituting letters for further index positions may introduce too much noise
        e.g. with words from different languages and non-words
        """
        test_word = self.split_word.copy()
        test_word[self.zeros_list[0]] = letter
        return "".join(test_word)

    def check_if_potential_word(self, potential_word):
        """
        First, index positions in the split_potential_words are checked to
        ensure there are no zeros as these may be returned as a single proxy_word
        if not other proxy_words are found.
        Secondly, non zeros (letters_ from the split encrypted_word are
        checked against those at index positions in the potential_word.
        This is to deduce that the letters are the same, and thus the
        potential_word is truly a potential_word.
        Thirdly, self.check_no_dupes_at_zero_indexes checks that letters
        are not duplicated at zero_indexes
        Overall, returning True, indicates the word is a potential_word.
        """
        split_potential_word = list(potential_word)

        for c, x in enumerate(self.split_word):

            if split_potential_word[c].isalpha() != True:
                return False

            if x.isalpha():
                if x != split_potential_word[c]:
                    return False

        return self.check_no_dupes_at_zero_indexes(split_potential_word)

    def check_no_dupes_at_zero_indexes(self, split_potential_word):
        letters_found = []
        for x in self.zeros_list:
            letters_found.append(split_potential_word[x])
        letters_found = set(letters_found)
        if len(letters_found) < len(self.zeros_list):
            return False
        return True


    def get_potential_words_list(self, proxy_words_list):
        """
        Provides a list of potential_words based on checks.
        """
        potential_words_list = []
        for potential_word in proxy_words_list:
            if len(potential_word) == len(self.encrypted_word):
                if self.check_if_potential_word(potential_word):
                    potential_words_list.append(potential_word)
        return potential_words_list

    def get_potential_words_dict(self, potential_words_list):
        success=False
        if len(potential_words_list) >1:
            success= True
        return {self.encrypted_word: {"potential_words_list": potential_words_list,
                    "zeros_list": self.zeros_list, "success": success}}

"""
potential_words_dict_collection sample
{'0ri0t': {'potential_words_list': ['grist', 'trist', 'drift', 'pritt', 'britt', 'wrist', 'print', 'gritt'], 'zeros_list': [0, 3], 'success': True}, '0ala00': {'potential_words_list': ['palang', 'palate', 'galaxy', 'balaam', 'salaam', 'malady', 'salade', 'calais', 'salads', 'malaka', 'salame', 'malays', 'salami', 'malawi', 'salako', 'ealaoq', 'balazs', 'malaya', 'palais', 'palace', 'falati', 'malais', 'lalage', 'malaga'], 'zeros_list': [0, 4, 5], 'success': True}, '0e00est': {'potential_words_list': ['bequest', 'deepest', 'request', 'sexiest', 'keenest', 'xegfest', 'weakest', 'nearest', 'meanest', 'densest', 'xefeest', 'wettest', 'tempest', 'dearest', 'neatest', 'qeogest', 'reddest', 'yeoeest', 'bestest'], 'zeros_list': [0, 2, 3], 'success': True}, '0e00ry': {'potential_words_list': ['penury', 'gentry', 'oexjry', 'sentry', 'eekgry', 'yezmry', 'memory', 'belfry', 'aefkry', 'yeyzry', 'hendry', 'celery', 'vestry', 'pendry'], 'zeros_list': [0, 2, 3], 'success': True}, '0ra0e0': {'potential_words_list': ['brayed', 'travel', 'braver', 'kramer', 'craves', 'tralee', 'rraoej', 'crazes', 'frazer', 'grapes', 'grapey', 'grated', 'crazed', 'grates', 'krater', 'crates', 'braden', 'brakes', 'uraxev', 'craven', 'grader', 'braces', 'arabel', 'erases', 'grater', 'graben', 'crater', 'braves', 'oradea', 'erased', 'framer', 'frater', 'drapes', 'eraser', 'cranes', 'fraser', 'graced', 'traded', 'kraken', 'trades', 'drawer', 'graver', 'grades', 'braved', 'tracer', 'erades', 'graves', 'grazed', 'traber', 'graded', 'prayed', 'drakes', 'gravel', 'braced', 'crated', 'graven', 'brazen', 'trader', 'braked', 'graces', 'craned', 'xraueb', 'traces', 'qraqex', 'prayer', 'draper', 'grazes', 'frayed', 'gracey', 'jraqev', 'draped', 'cramer'], 'zeros_list': [0, 3, 5], 'success': True}, 's00r0': {'potential_words_list': ['sabri', 'shirt', 'swore', 'sutra', 'sturm', 'sworn', 'stirs', 'spiro', 'shirk', 'scare', 'saarc', 'sabre', 'stork', 'samra', 'supra', 'serra', 'spire', 'scarf', 'swirl', 'shark', 'spark', 'sward', 'stark', 'sirri', 'sours', 'semra', 'sturt', 'sipri', 'score', 'start', 'scary', 'shire', 'swarf', 'shere', 'slurp', 'scars', 'spars', 'sport', 'slorc', 'sairi', 'sperm', 'spurn', 'skaro', 'spare', 'spurr', 'sorry', 'scarp', 'seers', 'soars', 'sacra', 'sherd', 'shore', 'smart', 'skirt', 'snare', 'sayre', 'stare', 'sears', 'starr', 'spurs', 'sabra', 'sopra', 'shirl', 'skirl', 'sword', 'swarm', 'sgurr', 'slurs', 'spora', 'sharp', 'sarre', 'sparc', 'sucre', 'store', 'swart', 'smirk', 'spore', 'spurt', 'scorn', 'sacre', 'scurf', 'shorn', 'snort', 'snarl', 'snore', 'share', 'short', 'skara', 'stars', 'shard', 'swire', 'stern', 'safra'], 'zeros_list': [1, 2, 4], 'success': True}, '00amy': {'potential_words_list': ['seamy', 'foamy', 'loamy'], 'zeros_list': [0, 1], 'success': True}, '0ebr0': {'potential_words_list': ['zebra', 'debra', 'gebre', 'debre'], 'zeros_list': [0, 4], 'success': True}, '0o0ey': {'potential_words_list': ['bogey', 'covey', 'honey', 'holey', 'robey', 'dovey', 'povey', 'pooey', 'dokey', 'gooey', 'coney', 'mobey', 'homey', 'pokey', 'cowey', 'toney', 'josey', 'fowey', 'mosey', 'posey', 'morey', 'money', 'dopey', 'bovey', 'lovey', 'jokey', 'losey', 'soley', 'tovey', 'ropey', 'howey', 'boney', 'corey', 'coley', 'foley', 'nosey', 'fogey'], 'zeros_list': [0, 2], 'success': True}, '0ro0ec0': {'potential_words_list': ['mrozecl', 'mroqecw', 'hroaecj', 'project', 'jroxecb', 'wrokece', 'oroneci', 'hrofecu', 'wrofecr', 'protect', 'yroxecj', 'jroqecu', 'iromecb', 'nroseci', 'qrozecf', 'wrocech', 'qrohecu', 'droueco', 'qroseco', 'wromecl', 'trogecu', 'qrosecl', 'aronecp', 'urofecj', 'xroxecf', 'jroiecq', 'hrowecf', 'vroqeco', 'vrosece', 'vrorecm', 'drohecu', 'lronecp'], 'zeros_list': [0, 3, 6], 'success': True}}
Time taken 0:02:38.063372
Here's the potential_words_dict_collection with 10 words used in substitutions
{'0ri0t': {'potential_words_list': ['print', 'drift', 'wrist', 'trist', 'gritt', 'pritt', 'britt', 'grist'], 'zeros_list': [0, 3], 'success': True}, '0ala00': {'zeros_list': [0, 4, 5], 'success': False}, '0e00est': {'potential_words_list': ['bestest', 'bequest', 'nearest', 'weakest', 'request', 'neatest'], 'zeros_list': [0, 2, 3], 'success': True}, '0e00ry': {'potential_words_list': ['penury', 'gentry', 'pendry'], 'zeros_list': [0, 2, 3], 'success': True}, '0ra0e0': {'potential_words_list': ['cranes', 'traber', 'trades', 'trader', 'travel', 'crazes', 'braden', 'braves', 'tracey', 'erased', 'braces', 'craven', 'eraser', 'brayed', 'erades', 'traces', 'crates', 'craned', 'craves', 'cramer', 'traced', 'crazed', 'tralee', 'braced', 'braked', 'crated', 'tracer', 'braved', 'craved', 'braver', 'brazen', 'crater', 'brakes'], 'zeros_list': [0, 3, 5], 'success': True}, 's00r0': {'potential_words_list': ['score', 'swire', 'stare', 'semra', 'storm', 'slorc', 'sturm', 'swarm', 'slurp', 'swarf', 'scary', 'scarp', 'swart', 'stork', 'story', 'store', 'scare', 'smirk', 'sword', 'stirs', 'swore', 'scars', 'stars', 'storr', 'stark', 'scarf', 'smart', 'sworn', 'stern', 'serra', 'sears', 'swirl', 'starr', 'sward', 'scurf', 'scorn', 'slurs'], 'zeros_list': [1, 2, 4], 'success': True}, '00amy': {'potential_words_list': ['loamy', 'foamy', 'seamy'], 'zeros_list': [0, 1], 'success': True}, '0ebr0': {'potential_words_list': ['debra', 'gebre', 'zebra', 'debre'], 'zeros_list': [0, 4], 'success': True}, '0o0ey': {'potential_words_list': ['fogey', 'nosey', 'coney', 'cowey', 'fowey', 'homey', 'dopey', 'bogey', 'boney', 'povey', 'dovey', 'gooey', 'honey', 'losey', 'bovey', 'tovey', 'robey', 'posey', 'corey', 'foley', 'soley', 'pooey', 'jokey', 'holey', 'dokey', 'mosey', 'mobey', 'money', 'pokey', 'coley', 'covey', 'josey', 'morey', 'howey', 'ropey', 'toney', 'lovey'], 'zeros_list': [0, 2], 'success': True}, '0ro0ec0': {'zeros_list': [0, 3, 6], 'success': False}}
Key 0ri0t
Value {'potential_words_list': ['print', 'drift', 'wrist', 'trist', 'gritt', 'pritt', 'britt', 'grist'], 'zeros_list': [0, 3], 'success': True}
Key 0ala00
Value {'zeros_list': [0, 4, 5], 'success': False}
Key 0e00est
Value {'potential_words_list': ['bestest', 'bequest', 'nearest', 'weakest', 'request', 'neatest'], 'zeros_list': [0, 2, 3], 'success': True}
Key 0e00ry
Value {'potential_words_list': ['penury', 'gentry', 'pendry'], 'zeros_list': [0, 2, 3], 'success': True}
Key 0ra0e0
Value {'potential_words_list': ['cranes', 'traber', 'trades', 'trader', 'travel', 'crazes', 'braden', 'braves', 'tracey', 'erased', 'braces', 'craven', 'eraser', 'brayed', 'erades', 'traces', 'crates', 'craned', 'craves', 'cramer', 'traced', 'crazed', 'tralee', 'braced', 'braked', 'crated', 'tracer', 'braved', 'craved', 'braver', 'brazen', 'crater', 'brakes'], 'zeros_list': [0, 3, 5], 'success': True}
Key s00r0
Value {'potential_words_list': ['score', 'swire', 'stare', 'semra', 'storm', 'slorc', 'sturm', 'swarm', 'slurp', 'swarf', 'scary', 'scarp', 'swart', 'stork', 'story', 'store', 'scare', 'smirk', 'sword', 'stirs', 'swore', 'scars', 'stars', 'storr', 'stark', 'scarf', 'smart', 'sworn', 'stern', 'serra', 'sears', 'swirl', 'starr', 'sward', 'scurf', 'scorn', 'slurs'], 'zeros_list': [1, 2, 4], 'success': True}
Key 00amy
Value {'potential_words_list': ['loamy', 'foamy', 'seamy'], 'zeros_list': [0, 1], 'success': True}
Key 0ebr0
Value {'potential_words_list': ['debra', 'gebre', 'zebra', 'debre'], 'zeros_list': [0, 4], 'success': True}
Key 0o0ey
Value {'potential_words_list': ['fogey', 'nosey', 'coney', 'cowey', 'fowey', 'homey', 'dopey', 'bogey', 'boney', 'povey', 'dovey', 'gooey', 'honey', 'losey', 'bovey', 'tovey', 'robey', 'posey', 'corey', 'foley', 'soley', 'pooey', 'jokey', 'holey', 'dokey', 'mosey', 'mobey', 'money', 'pokey', 'coley', 'covey', 'josey', 'morey', 'howey', 'ropey', 'toney', 'lovey'], 'zeros_list': [0, 2], 'success': True}
Key 0ro0ec0
Value {'zeros_list': [0, 3, 6], 'success': False}


"""