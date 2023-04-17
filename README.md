
# Smart Insert Anki Add-on


Add-on for [ankitects/anki](https://github.com/ankitects/anki) that aims at enhancing the ctrl+v experience and and simplifying the import of AI-generated flashcards.


[![GPL v3](https://img.shields.io/github/license/swssl/anki-smart-insert)](https://github.com/swssl/anki-smart-insert/blob/main/LICENSE) 
[![Anki](https://img.shields.io/badge/platform-Anki-%23317eac)](https://ankiweb.net/shared/info/1303065007) 


## Installation

Go to [the Add-on's official page](https://ankiweb.net/shared/info/1303065007), scroll down and copy the add-on's number. Open Anki, go to Extra > Add-ons > Download Add-ons and paste the number. After the process finishes, restart Anki.
    
## Features

- Analysis of pasted content to detect Headlines and separated paragraphs
- Removal of line breaks to enhance the card's layout on different screen widths
- Replacement of bullet symbol with a custom one (defaults to -)

### How to generate flashcards with AI

When generating flashcards with ChatGPT, just prefix your input text wit something like this:
> The following is a `[text/wikipedia article/etc]` about `[Topic]`. Create flashcards for use by Anki. Prefix each question with "Q:" and shorten the answers to two sentences.

## Known Issues


+ Headlines containing two or more lines are interpreted as headline and paragraph
+ Unable to detect headlines in a position other than the first line or more than one headline per paste
    + Workaround: Copy and paste the paragraphs one after another
## Contributing

- For feature suggestions and bug reports, use the [Issues tab on Github](https://github.com/swssl/anki-smart-insert/issues).
- For development, clone the repository and follow [the official tutorial](https://addon-docs.ankiweb.net/editor-setup.html) in order to connect to your Anki installation. 
