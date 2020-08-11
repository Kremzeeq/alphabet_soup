
import random

class PotentialWordTracker():
    def __init__(self, alphabet, encrypted_words, potential_words_dict_collection):
        self.alphabet = alphabet
        self.potential_words_dict_collection = potential_words_dict_collection
        self.encrypted_words = encrypted_words
        self.potential_words_by_alpha_dict = {key: {} for key in self.alphabet}
        self.unassigned_letters = []
        self.starting_letters = []

    def execute_potential_word_tracker(self):
        """
        Iterates over the key-pair vals in the self.potential_words_dict_collection.
        That is a dictionary of encrypted_words as keys and a nested dictionary which
        contains a potential_word_list for decrypted versions of the word.
        self.alpha_dict_with_potential_words is updated so that key-pair values consisting
        respectively of the potential_word and the encrypted_word are assigned under each
        letter of the alphabet. This is according to where letters may be found at particular
        indexes of the encrypted_word
        self.alpha_dict_with_potential_words example:
        {'a': {'balaga': '0ala00', 'falaba': '0ala00', 'nearest': '0e00est', 'dearest': '0e00est'... etc.}
        """
        for k, v in self.potential_words_dict_collection.items():
            if v['success']:
                encrypted_word = k
                potential_word_list = v['potential_words_list']
                zeros_list = v['zeros_list']
                self.update_alpha_dict_with_potential_words(encrypted_word, potential_word_list, zeros_list)
        self.get_starting_and_unassigned_letters()

    def update_alpha_dict_with_potential_words(self, encrypted_word, potential_words, zeros_list):
        for potential_word in potential_words:
            self.assign_potential_word_to_letter(encrypted_word, potential_word, zeros_list)

    def assign_potential_word_to_letter(self, encrypted_word, potential_word, zeros_list):
        letters_found_result_dict = self.get_letters_found_result_dict(zeros_list, potential_word)
        if letters_found_result_dict['success']:
            for letter in letters_found_result_dict["letters_found"]:
                val = {potential_word: encrypted_word}
                self.potential_words_by_alpha_dict[letter].update(val)

    def get_letters_found_result_dict(self, zeros_list, potential_word):
        """
        Iterates through letters of the potential_word at indexes of the zero_list.
        Checks that there are no duplicated letters at the indexes.
        Builds a list of letters found

        :return: e.g. {"success": True, "letters_found":['a', 'p', 't']
        """
        letters_found = []
        no_dupe_letters = True
        for i in zeros_list:
            letter = potential_word[i]
            if letter not in letters_found:
                letters_found.append(letter)
            else:
                no_dupe_letters = False
        return {"success": no_dupe_letters, "letters_found":letters_found}

    def get_starting_and_unassigned_letters(self):
        """
        iterates over self.potential_words_by_alpha_dict to find the no. of key-pair vals
        of encrypted_words and potential_words for letters. If len is 0, is appended to
        self.unassigned_letters. If len is 1, is is appended to self.starting_letters.
        The number of starting letters determines which letters will be decoded first,
        each time the EncryptedWordEncoder runs the self.get_decrypted_words_dict_for_epoch
         function as part of a epoch.
         If the len of the self.starting_letters list is <2, then random letters that are not
         unassigned_letters are added to the list. They cannot be duplicated.
        """
        self.starting_letters = []
        for k, v in self.potential_words_by_alpha_dict.items():
            if len(v) == 0:
                self.unassigned_letters.append(k)
            if len(v) ==1:
                self.starting_letters.append(k)
        if len(self.starting_letters) <2:
            random_alphas = [x for x in self.alphabet if x not in self.unassigned_letters]
            random.shuffle(random_alphas)
            while len(self.starting_letters) <2:
                self.starting_letters.append(random_alphas.pop())