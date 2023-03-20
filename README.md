# HTML-file-translator-to-Hindi
An application that traverses through a directory and all its subdirectories, finding all HTML files and translating their text values into Hindi using Google Translate API.
The translated text is Hardcoded into the HTML file.
I would not advise to translate more than 10 files at a time because of the limit the Google Translate API has, which can result in Google temporariliy blacklisting your IP 
address because of too many requests. Even with adding pauses between sending chunks of data, I was not able to overcome this issue. Another issue is that the program sometimes
crashes due to it not creating a found element in the translated Dictionary, which will hopefully be resolved in the next update.
I've used BeautifulSoup4 for extracting the data from the webpage and putting it back in place.
