from __future__ import print_function

from builtins import str
from builtins import input
from builtins import object
from menu import Menu

from datetime import datetime

from adapter.adapter import Functions

class CLI():
    def __init__(self):
        self.db = Functions()

        self.delete_options = [
            ("delete words", self.delete_words),
            ("Quit", Menu.CLOSE)
        ]
        self.update_options = [
            ("Update all words", self.update_words),
            ("Update english word", self.update_words, {'lang': 'eng'}),
            ("Update russian word", self.update_words, {'lang': 'rus'}),
            ("Update chinese word", self.update_words, {'lang': 'cn'}),
            ("quit", Menu.CLOSE)
        ]
        self.delete_menu = Menu(
            options=self.delete_options,
            title='Delete words',
            message='',
            prompt='>',
        )
        self.update_menu = Menu(
            options=self.update_options,
            title='Update words',
            message='',
            prompt='>',
        )
        self.main_options = [
            ("Add words", self.add_words),
            ("Delete words", self.delete_menu.open),
            ("Update words", self.update_menu.open),
            ("Show dict", self.show_dictionary),
            ("Quit", Menu.CLOSE)
        ]
        self.main_menu = Menu(
            options=self.main_options,
            title='Main menu',
            message='',
            prompt='> ',
            auto_clear=True
        )

    def add_words(self):
        while True:
            eng = input("english text: ")
            if eng == 'quit':
                return
            try:
                rus = input("russian text: ") 
                cn = input("chinese text: ")
                self.db.add_words(eng, rus, cn)
                return
            except Exception as err:
                print("CLI add word ERROR: " + str(err))
                input()

    def delete_words(self):
        while True:
            try:
                dictionary = self.db.get_full_dict()
                for el in dictionary:
                    print(el)
                word_id = input("input word id: ")
                if word_id == 'quit':
                    return
                word = self.db.get_words(word_id)
                self.db.delete_words(word_id)
                print('word {} deleted'.format(word))
                input()
            except Exception as err:
                print('CLI delete word ERROR: ' + str(err))
                input()

    def update_words(self, lang='all'):
        while True:
            try:
                dictionary = self.db.get_full_dict()
                for el in dictionary:
                    print(el)

                word_id = input('input word id: ')
                if word_id == 'quit':
                    return
                word = self.db.get_words(word_id)

                if not isinstance(word, dict):
                    print("there is no word with that id")
                    input()
                    return

                if lang == 'all':
                    eng = input("updated english text: ")
                    rus = input("updated russian text: ") 
                    cn = input("updated chinese text: ")
                    self.db.update_words(word_id, eng, rus, cn)
                elif lang == 'eng':
                    upd_text = input("updated english text: ")
                    self.db.update_words(word_id, eng=upd_text)
                elif lang == 'rus':
                    upd_text = input("updated russian text: ")
                    self.db.update_words(word_id, rus=upd_text)
                elif lang == 'cn':
                    upd_text  = input("updated chinese text: ")
                    self.db.update_words(word_id, cn=upd_text)

                upd_word = self.db.get_words(word_id)

                word = word['word_eng'] + " " + word['word_rus'] + " " + word['word_cn']
                upd_word = upd_word['word_eng'] + " " + upd_word['word_rus'] + " " + upd_word['word_cn']

                print('\n {} \n changed to \n{}'.format(word, upd_word))
                input()
            except Exception as err:
                print('CLI update word ERROR: ' + str(err))
                input()

    def show_dictionary(self, lang='all'):
        while True:
            try:
                dictionary = self.db.get_full_dict()
                for el in dictionary:
                    print(el['word_eng'], " ", el['word_rus'], " ", el['word_cn'])
                input()
                return
            except Exception as err:
                print("CLI show dictionary Error: " + str(err))
                input()

    def run(self):
        self.main_menu.open()
