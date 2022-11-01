# [WIP] anki-smart-insert
Add-on for [ankitects/anki](https://github.com/ankitects/anki) that aims at enhancing the ctrl+v experience.

## Features

+ Analysis of pasted content to detect Headlines and separated paragraphs
+ Removal of line breaks to enhance the card's layout on different screen widths
+ Replacement of bullet symbol with a custom one (defaults to -)

## Installation

Since this is in work in progress state, there is neither a convenient way of installation nor any benefit you could get from this addon.

## Known issues

+ Headlines containing two or more lines are interpreted as headline and paragraph
+ Unable to detect headlines in a position other than the first line or more than one headline per paste
    + Workaround: Copy and paste them one after another

## Contribute

+ For feature suggestions and bug reports, use the Issues tab.
+ For development, clone the repository and follow [the official tutorial](https://addon-docs.ankiweb.net/editor-setup.html) in order to connect to your Anki installation. 