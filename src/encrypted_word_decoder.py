

import potential_word_tracker
import copy
import random

class EncryptedWordDecoder(potential_word_tracker.PotentialWordTracker):
    def __init__(self, alphabet, encrypted_words, potential_words_dict_collection, max_epochs):
        potential_word_tracker.PotentialWordTracker.__init__(self, alphabet, encrypted_words, potential_words_dict_collection)
        self.execute_potential_word_tracker()
        self.max_epochs = max_epochs


    def execute_encrypted_word_decoder(self):
        decrypted_words_dict_collection = self.get_decrypted_words_dict_collection_for_epochs()
        return decrypted_words_dict_collection

    def get_decrypted_words_dict_collection_for_epochs(self):
        """
        The decrypted_words_dict_collection is a list with a series of dictionaries
        containing encrypted and potential decrypted words as key-value pairs. Here's an example
        of a dictionary which would be nested in the list: {'00amy': 'liamy','0ala00': 'galaxy','0e00est': 'request','0e00ry': 'kefcry',
        '0ebr0': 'sebro','0o0ey': 'dovey','0ra0e0': 'brazen','0ri0t': 'hriet','0ro0ec0': 'project',
        's00r0': 'swarm'}
        """
        decrypted_words_dict_collection = []
        for x in range(1, self.max_epochs +1):
            print("Epoch", x)
            new_words = self.get_decrypted_words_dict_collection_for_epoch()
            decrypted_words_dict_collection.extend(new_words)
        return decrypted_words_dict_collection

    def get_decrypted_words_dict_collection_for_epoch(self):
        """
        For each starting letter, a decrypted word dictionary is built where
        the single corresponding key value pair is the first to be assigned
        to the decrypted word dictionary. e.g. 'g' might only have { 'galaxy': '0ala00'}
        """
        decrypted_words_dict_collection = []
        for starting_letter in self.starting_letters:
            decrypted_words_result_dict = self.get_decrypted_words_result_dict_for_starting_letter(starting_letter)
            decrypted_words_dict = decrypted_words_result_dict['decrypted_words_dict']
            unassigned_letters = decrypted_words_result_dict['unassigned_letters']
            unassigned_words = self.get_unassigned_words(decrypted_words_dict)
            decrypted_words_dict_for_unassigned_words = self.get_decrypted_words_dict_for_unassigned_words(
                unassigned_letters, unassigned_words)
            decrypted_words_dict.update(decrypted_words_dict_for_unassigned_words)
            decrypted_words_dict_collection.append(decrypted_words_dict)
        return decrypted_words_dict_collection

    def get_decrypted_words_result_dict_for_starting_letter(self, starting_letter):
        potential_words_by_alpha_dict_copy = copy.deepcopy(self.potential_words_by_alpha_dict)
        unassigned_letters_copy = self.unassigned_letters.copy()
        decrypted_words_dict = {}
        self.use_starting_letter_bool = True
        while len(potential_words_by_alpha_dict_copy) > 0:
            result_dict = self.get_result_dict_for_letter(starting_letter,
                                                          potential_words_by_alpha_dict_copy,
                                                          unassigned_letters_copy,
                                                          decrypted_words_dict)
            potential_words_by_alpha_dict_copy = result_dict['potential_words_by_alpha_dict']
            unassigned_letters_copy = result_dict["unassigned_letters"]
            decrypted_words_dict = result_dict["decrypted_words_dict"]
        return {"decrypted_words_dict": decrypted_words_dict,
                "unassigned_letters": unassigned_letters_copy}

    def get_result_dict_for_letter(self,
                                   starting_letter,
                                   potential_words_by_alpha_dict,
                                   unassigned_letters,
                                   decrypted_words_dict):
        letter = self.get_letter_for_iteration(starting_letter, potential_words_by_alpha_dict)
        decrypted_word_result_dict_for_letter = self.get_decrypted_word_result_dict_for_letter(letter,
                                                                                        potential_words_by_alpha_dict)
        if decrypted_word_result_dict_for_letter["success"]:
            decrypted_word_dict_for_letter = decrypted_word_result_dict_for_letter['decrypted_word_dict_for_letter']
            result_dict = self.get_result_dict_for_potential_words_by_alpha_dict_and_unassigned_letters(
                unassigned_letters,
                decrypted_word_dict_for_letter,
                potential_words_by_alpha_dict)
            unassigned_letters = result_dict['unassigned_letters']
            potential_words_by_alpha_dict = result_dict['potential_words_by_alpha_dict']
            decrypted_words_dict.update(decrypted_word_dict_for_letter)
        else:
            potential_words_by_alpha_dict.pop(letter)
            unassigned_letters.append(letter)
        return {"decrypted_words_dict": decrypted_words_dict,
                'potential_words_by_alpha_dict': potential_words_by_alpha_dict,
                "unassigned_letters": unassigned_letters}

    def get_letter_for_iteration(self, starting_letter, potential_words_by_alpha_dict):
        if self.use_starting_letter_bool == True:
            self.use_starting_letter_bool = False
            return starting_letter
        else:
            return self.get_next_letter(potential_words_by_alpha_dict)

    def get_next_letter(self, potential_words_by_alpha_dict):
        """
        Randomising the keys in choosing the next letter is important in reducing bias.
        If there are more then 3 potential words per a letter, a random letter is chosen
        to save iterating over the letters again
        """
        counter = 1
        letter_keys = list(potential_words_by_alpha_dict.keys())
        random.shuffle(letter_keys)
        while counter < 4:
            for a_letter in letter_keys:
                if len(potential_words_by_alpha_dict[a_letter]) == counter:
                    return a_letter
            counter += 1
        return random.choice(letter_keys)


    def get_decrypted_word_result_dict_for_letter(self, letter, potential_words_by_alpha_dict):

        decrypted_word_keys = list(potential_words_by_alpha_dict[letter].keys())
        random.shuffle(decrypted_word_keys)
        for decrypted_word in decrypted_word_keys:
            get_another_letter = False
            potential_words_by_alpha_dict[letter][decrypted_word] = potential_words_by_alpha_dict[letter].get(decrypted_word)
            encrypted_word = potential_words_by_alpha_dict[letter][decrypted_word]
            for i in self.potential_words_dict_collection[encrypted_word]['zeros_list']:
                if decrypted_word[i] not in potential_words_by_alpha_dict.keys():
                    get_another_letter = True
                    break
            if get_another_letter == False:
                return {"decrypted_word_dict_for_letter": {encrypted_word: decrypted_word}, "success": True}
        return {"success": False}

    def get_result_dict_for_potential_words_by_alpha_dict_and_unassigned_letters(self,
                                             unassigned_letters,
                                             decrypted_word_dict_for_letter,
                                             potential_words_by_alpha_dict):

        potential_words_by_alpha_dict = self.pop_letters_found_from_alpha_dict(
                                             decrypted_word_dict_for_letter,
                                             potential_words_by_alpha_dict)

        potential_words_by_alpha_dict = self.pop_encrypted_word_from_alpha_dict(decrypted_word_dict_for_letter,
                                                                                potential_words_by_alpha_dict)
        return self.get_unassigned_letters_dict(potential_words_by_alpha_dict, unassigned_letters)

    def pop_letters_found_from_alpha_dict(self, decrypted_word_dict_for_letter, potential_words_by_alpha_dict):
        for encrypted_word, potential_word in decrypted_word_dict_for_letter.items():
            for i in self.potential_words_dict_collection[encrypted_word]['zeros_list']:
                potential_words_by_alpha_dict.pop(potential_word[i])
        return potential_words_by_alpha_dict

    def pop_encrypted_word_from_alpha_dict(self, decrypted_word_dict_for_letter, potential_words_by_alpha_dict):
        potential_words_by_alpha_dict_copy = copy.deepcopy(potential_words_by_alpha_dict)
        for encrypted_word in decrypted_word_dict_for_letter.keys():
            for letter_key, potential_word_dict in potential_words_by_alpha_dict_copy.items():
                for k, v in potential_word_dict.items():
                    if v == encrypted_word:
                        potential_words_by_alpha_dict[letter_key].pop(k)
        return potential_words_by_alpha_dict

    def get_unassigned_letters_dict(self, potential_words_by_alpha_dict, unassigned_letters):
        potential_words_by_alpha_dict_copy = copy.deepcopy(potential_words_by_alpha_dict)
        for k, v in potential_words_by_alpha_dict_copy.items():
            if len(v) ==0:
                unassigned_letters.append(k)
                potential_words_by_alpha_dict.pop(k)
        return {"unassigned_letters" : unassigned_letters, "potential_words_by_alpha_dict": potential_words_by_alpha_dict}

    def get_unassigned_words(self, decrypted_word_dict):
        unassigned_encrypted_words = []
        for encrypted_word in self.encrypted_words:
            if encrypted_word not in decrypted_word_dict.keys():
                unassigned_encrypted_words.append(encrypted_word)
        return unassigned_encrypted_words

    def get_decrypted_words_dict_for_unassigned_words(self, unassigned_letters, unassigned_words):
        """
        Randomly allocate unassigned letters to unassigned_words at zero_list index positions
        """

        decrypted_word_dict = {}
        random.shuffle(unassigned_letters)
        random.shuffle(unassigned_words)
        for encrypted_word in unassigned_words:
            split_decrypted_word = list(encrypted_word)
            for zero_index in self.potential_words_dict_collection[encrypted_word]['zeros_list']:
                random_letter = self.assign_random_letter_to_zero_index(zero_index, unassigned_letters)
                split_decrypted_word[zero_index] = random_letter
                unassigned_letters.remove(random_letter)
            decrypted_word = "".join(split_decrypted_word)
            decrypted_word_dict.update({encrypted_word : decrypted_word})
        return decrypted_word_dict


    def assign_random_letter_to_zero_index(self, zero_index, unassigned_letters):
        vowels = ['a', 'e', 'i', 'o', 'u']
        letter_assigned = None
        for unassigned_letter in unassigned_letters:
            if unassigned_letter in vowels:
                if zero_index > 0:
                    letter_assigned = unassigned_letter
                    break
            elif zero_index == 0:
                letter_assigned = unassigned_letter
                break
        if letter_assigned == None:
            letter_assigned = unassigned_letters[0]
        return letter_assigned
