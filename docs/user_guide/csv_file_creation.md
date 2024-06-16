## Create your collection's CSV file

Once you have installed mtg_pynance, the next step is to create a CSV file of the cards in your collection. This is an extremely important step and the following instructions should be read carefully to ensure mtg_pynance can read your file!

mtg_pynance expects the CSV file you feed to it to contain the following four columns with the indicated data types

| **Column**     | **Type** |
|----------------|----------|
| cid            | Integer  |
| id             | String   |
| foiling        | String   |
| purchase_price | Float    |

These four columns *must* appear in your CSV with those exact names (copy and paste them if you want). What's neat is that because mtg_pynance uses Polars to look for these four columns, it means that they can be in any order and that you can include other columns. For example, if you want to make another column recording a card's card type, you can do that and mtg_pynance will ignore it! The ability to add extra columns in your CSV file opens the avenue to creating analysis functions that analyze only cards that meet certain conditions, like being a land. See ADVANCED TOPICS for more. Each column will now be explained.

## cid

The cid is the collection identification number of a card. It is by nature a unique number you assign to a card that distinguishes it from all other cards in your collection. The cid of a card must be a signed integer.

## id

The id is the unique identification string of a card assigned by Scryfall. This id is what connects a card in the CSV file to its price data in the Scryfall bulk data file that is downloaded. To find a card's id, go to [Scryfall](https://scryfall.com/), search the card, and click on "Copy-pasteable JSON".

## foiling

The foiling string lists the type of foiling a card has. 