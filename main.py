import re
import time
import bs4
import unicodedata
import googletrans
import httpx
from googletrans import Translator
from bs4 import BeautifulSoup


def translate_to_hindi(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    a = soup.get_text("**", strip=True)  # Taking all the text inside the html and adding delimiters between nodes
    list_to_translate = a.split("**")  # Splitting the text and adding it to a list for easier formatting
    for phrase in list_to_translate:
        if "\n" in phrase:
            c = phrase.splitlines()
            while "" in c:
                c.remove("")
            while "\u200b" in c:
                c.remove("\u200b")
            for strs in c:
                list_to_translate.append(strs.strip())
            list_to_translate.remove(phrase)

    print(list_to_translate)

    if "The website from which you got to this page is protected by Cloudflare. Email addresses on that page have been hidden in order to keep them from being accessed by malicious bots." in list_to_translate:
        print("too")

    timeout = httpx.Timeout(100)
    translator = Translator(timeout=timeout)

    list_translated = []

    print(len(list_to_translate))
    i = 1

    #a = translator.translate(list_to_translate[414], dest="hi")
    #print(a.text)

    for phrase in list_to_translate:
        if phrase == "" or phrase == "\n":  # skip empty and newlines
            continue
        print(repr(phrase))
        if re.match(r'.(?! )', phrase):  # for some reason google translate doesn't like a dot without a space after it
            phrase = phrase.replace('.', '. ')
            #print(phrase)
        #print(phrase)
        a = translator.translate(phrase, dest="hi")
        print(repr(a.text))

        list_translated.append(a.text)
        print(list_translated)
        print("________________")
        #print(i)
        if i % 25 == 0:
            time.sleep(15)
        #time.sleep(1)
        i += 1

    dic = {list_to_translate[i]: list_translated[i] for i in range(len(list_translated))}  # Dictionary is used to eliminate
                                                                                           # duplicates and give us easier
                                                                                           # access to translated versions

    print(dic)

    #print(dic)

    for el in soup.find_all():  # Logic for replacing text - First we iterate through every node inside the document
        if el.name == "script" or el.name == "style":  # We'll skip through script and style tags because we know
            continue  # we won't modify anything there
        if el.text is not None:
            b = []
            loop = 1
            a = '**'.join(el.find_all(string=True, recursive=False))  # We take all the text in the node we're currently
            a = a.strip()  # observing, without the text in child elements

            if a == "":
                continue
            #print(repr(a))
            #print("____")

            b = a.split("**")

            #print(b)

            list_of_phrases = []

            for phrase in b:
                #print("test")
                #print(phrase)
                #print("______________________")
                if re.match(r'/\s{2,}/', phrase):
                    has_children = len(el.find_all())
                    # is separated by tags and we will break it up into parts
                    # If it doesn't, it just bad formatting on the site and we will leave
                    # it as it is
                    if has_children != 0:
                        phrase = unicodedata.normalize('NFKD', phrase)
                        c = phrase.split("  ")  # Here we break it up into parts that are in our dictionary
                        while "" in c:
                            c.remove("")
                        for strs in c:
                            list_of_phrases.append(strs)
                    #print(phrase)
                    #print("______________________")

                if "\n" in phrase:
                    c = phrase.splitlines()
                    while "" in c:
                        c.remove("")
                    for strs in c:
                        list_of_phrases.append(strs)

                if "\n" not in phrase and not re.match(r'/\s{2,}/', phrase):
                    list_of_phrases.append(phrase)

            while "" in list_of_phrases:
                list_of_phrases.remove("")

            if not list_of_phrases:
                continue

            for phrase in list_of_phrases:
                phrase = phrase.strip()
                if phrase in list_to_translate:
                    #print(repr(phrase))
                    #print("############")
                    if el.string is not None:
                        el.string = el.string.replace(phrase, dic[phrase])
                    else:
                        for content_index in range(len(el.contents)):
                            if type(el.contents[content_index]) == bs4.element.NavigableString:
                                c = el.contents[content_index].string.strip()
                                lines = c.splitlines()
                                i = 0
                                for line in lines:
                                    line = line.strip()
                                    #print(repr(line))
                                    #print("@@@@@@@@@@@@@@@@@@@@")
                                    if phrase == line:
                                        if i == 0:
                                            el.contents[content_index].string.replace_with(dic[phrase])
                                        else:
                                            el.contents[content_index].string = el.contents[content_index].string + dic[phrase]
                                        #print(el.contents[content_index].string)
                                    i += 1

    for item in soup.select('[placeholder]'):  # Changing the values for placeholders on the site
        value = item['placeholder']
        value = translator.translate(value, dest="hi")
        item['placeholder'] = value.text

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))


#translate_to_hindi(r'D:\allstar\classcentral\www.classcentral.com\course\edx-the-art-of-structural-engineering-vaults-12040.html')




