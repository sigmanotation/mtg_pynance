## Overview

The core function of mtg_pynance is to create a local SQL database of the cards in your Magic the Gathering collection. You provide a CSV file of your collection with certain information for each card. For each card in this CSV file mtg_pynance creates a table in the database where each entry record's the price of that card and the timestamp that the price was calculated. The price and timestamp come from Scryfall's bulk data default cards file. With this database made, mtg_pynance has analysis functions that parse it to provide you with information such as the market value and gain/loss of your collection as a function of time!

## Specifics

### Downloads Scryfall's bulk data file

mtg_pynance does not query the Scryfall API for each card in your collection CSV. The maximum number of times we can query Scryfall per second is 10, and most collections are far larger than 10 cards. To avoid obscenely long run times, mtg_pynance downloads the entire Scryfall bulk data file to your computer and searches it locally for your collection's price data. This file is large, coming in at a little less than 500 Mb.

### Stores information locally

mtg_pynance operates totally locally with the CSV file of your collection, the downloaded Scryfall bulk data file, and the SQL database made from your collection. If you are a privacy junkie, this is a great strength of the package because nobody but you has access to what cards you own and their value. This is opposed to websites and other applications that handle your collection for you and may be privy to your collection's information. 

### Records only current prices

mtg_pynance will not calculate the price history of a card when ran, only its *current* price. The prices come from Scryfall's bulk data default cards file which is updated only a few times a day. This means that mtg_pynance cannot provide real-time price data. Moreover, it only records prices when it is run which is controlled by you, the user. If you want to record price information for each day, *you* will have to run mtg_pynance everyday.