import requests
import argparse
from bs4 import BeautifulSoup


def simultaneous_trans(l1, w, all_langs):
    try:
        for lang in all_langs.values():
            if lang == l1:
                continue
            opt = f'{lang}'
            url = f'https://context.reverso.net/translation/{l1.lower()}-{lang.lower()}/{w}'
            link = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if link:
                    content = BeautifulSoup(link.content, 'html.parser')
                    words = content.select('.translation')
                    examples = content.select('.example')
                    text_words = [word.text.replace('\n', '').strip('\r') for word in words]
                    text_words = [word.strip(' ') for word in text_words]
                    text_examples = [example.text.replace('\n', '').split('\r') for example in examples]
                    text_examples = [each.strip(' ') for example in text_examples for each in example if each]
                    text_examples = [example.split(".") for example in text_examples]
                    text_examples = [each + '.' for example in text_examples for each in example if each]
                    with open(f'{w}.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{opt} Translations:\n{text_words[0]}')
                        file.write('\n')
                        file.write(f'{opt} Example:\n{text_examples[0]}')
                        file.write(f'\n{text_examples[1]}')
                        file.write('\n')
            else:
                raise WordNotFound(w)
        with open(f'{w}.txt', 'r', encoding='utf-8') as f:
            print(f.read())
    except WordNotFound:
        print(f'Sorry, unable to find {w}')


def translator(l1, l2, w):
    opt = f'{l2}'
    url = f'https://context.reverso.net/translation/{l1.lower()}-{l2.lower()}/{w}'
    link = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        if link:
            print(f'{link.status_code} OK')
            print()
            content = BeautifulSoup(link.content, 'html.parser')
            words = content.select('.translation')
            examples = content.select('.example')
            text_words = [word.text.replace('\n', '').strip('\r') for word in words]
            text_words = [word.strip(' ') for word in text_words]
            text_examples = [example.text.replace('\n', '').split('\r') for example in examples]
            text_examples = [each.strip(' ') for example in text_examples for each in example if each]
            with open(f'{w}.txt', 'a', encoding='utf-8') as file:
                print(f'{opt} Translations:')
                file.write(f'{opt} Translations:\n')
                for word in text_words[:5:]:
                    file.write(word + '\n')
                    print(word)

                print(f'{opt} Examples:')
                file.write(f'{opt} Examples:\n')
                for i in range(0, 10, 2):
                    file.write(text_examples[i])
                    file.write('\n' + text_examples[i + 1] + '\n')
                    print(text_examples[i])
                    print(text_examples[i + 1])
        else:
            raise WordNotFound
    except WordNotFound:
        print(f'Sorry, unable to find {w}')


class WordNotFound(Exception):
    pass


class WrongLang(Exception):
    def __init__(self, lang):
        self.message = f"Sorry, the program doesn't support {lang}"

    def __str__(self):
        return self.message


arguments = argparse.ArgumentParser()
arguments.add_argument("lang1")
arguments.add_argument("lang2")
arguments.add_argument("word")
args = arguments.parse_args()
langs = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}
lang_from = args.lang1.title()
lang_to = args.lang2.title()
word = args.word
try:
    if lang_to in langs.values() and lang_from in langs.values():
        translator(lang_from, lang_to, word)
    elif lang_from in langs.values() and lang_to == 'All':
        simultaneous_trans(lang_from, word, langs)
    else:
        if lang_to not in langs.values():
            raise WrongLang(lang_to)
        else:
            raise WrongLang(lang_from)
except WrongLang as error:
    print(error)
