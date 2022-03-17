import sys
import requests
from bs4 import BeautifulSoup


languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese', 8: 'Dutch',
             9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}


def get_translation(lan_from, lan_to, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://context.reverso.net/translation/{lan_from.lower()}-{lan_to.lower()}/{word}'
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        translated_words = soup.select("#translations-content > .translation")
        translation_examples = soup.select("#examples-content > .example >  .ltr")

        for i, tr_word in enumerate(translated_words):
            translated_words[i] = tr_word.text.strip()
        for i, example in enumerate(translation_examples):
            translation_examples[i] = example.text.strip()

        with open(word + '.txt', 'a', encoding='utf-8') as word_file:
            print(f"\n{lan_to} Translations:", file=word_file)
            print(translated_words[0], end='\n', file=word_file)

            print(f"\n{lan_to} Example:", file=word_file)
            print(translation_examples[0], file=word_file)
            print(translation_examples[1], file=word_file)
            print(file=word_file)
    elif page.status_code == 404:
        print(f"Sorry, unable to find {word}")
        quit()
    else:
        print("Something wrong with your internet connection")
        quit()


def main():
    arguments = sys.argv
    if len(arguments) != 4:
        quit()

    lan_from = arguments[1]
    lan_to = arguments[2]
    word = arguments[3]

    if lan_to.capitalize() not in languages.values() and lan_to != 'all':
        print(f"Sorry, the program doesn't support {lan_to}")
        quit()
    elif lan_from.capitalize() not in languages.values() and lan_from != 'all':
        print(f"Sorry, the program doesn't support {lan_from}")
        quit()

    """
    print("Hello, you're welcome to the translator. Translator supports:")
    for key, value in languages.items():
        print(str(key) + '. ' + value)
    """

    # empty previous file if it exists
    my_file = open(word + '.txt', 'w')
    my_file.close()

    if lan_to != 'all':
        get_translation(lan_from, lan_to, word)
    else:
        for language in languages.values():
            if language.lower() == lan_from.lower():
                continue
            get_translation(lan_from, language, word)

    with open(word + '.txt', 'r', encoding='utf-8') as translate_file:
        for line in translate_file:
            print(line, end='')


if __name__ == "__main__":
    main()
