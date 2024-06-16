## The short of it 

The core function of mtg_pynance is to create a local SQL database of the cards in your Magic the Gathering collection. You provide a CSV file of your collection with certain information for each card. For each card in this CSV file mtg_pynance creates a table in the database where each entry record's the price of that card and the timestamp that the price was calculated. The price and timestamp come from Scryfall's bulk data default cards file. With this database made, mtg_pynance has analysis functions that parse it to provide you with information such as the market value and profit of your collection as a function of time!

## The long of it

Many points must be elaborated in the operation of mtg_pynance so that it is clear to the user what to expect from the package. To begin, mtg_pynance operates totally locally with the CSV file of your collection and the SQL database made from it. If you are a privacy junkie, this is a great strength of the package because nobody but you has access to what cards you own and their value. This is opposed to websites and other applications that handle your collection for you and may be privvy to your collection's information. The downside to locally hosting such information is that you must fork over disk space for it. This should not be an issue for most users, but those with extremely large collections and/or many timestamp-price entries in their card tables might find that they need to provide larger amounts of space.

The issue of disk space underlies a more fundamental question: when are timestamp-price entries added to a card's table? The answer is, from the documentation, when the function run_mtg_pynance is called. This is not surprising, but warrants explicitly stating because it means that *you* are in charge of adding timestamp-price entries to *your* database! mtg_pynance will not calculate the price history of a card when ran, *only its current price*. If the thought of running mtg_pynance once a day, week, or whatever schedule you want sounds tedious, no worries! Check out the AUTOMATION SECTION to see an example on Mac for automating it.

Just like any other collection tracker application, you must tell mtg_pynance the cards you own. This is done through the creation of a CSV file. mtg_pynance expects your CSV file to contain certain elements. This is detailed in the GETTING STARTED SECTION.

Need to describe the disk space thing with downloading scryfall

