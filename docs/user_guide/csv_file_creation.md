## Instructions

Once you have installed mtg_pynance, the next step is to create a CSV file of the cards in your collection. This is an extremely important step and the following instructions should be read carefully to ensure mtg_pynance can read your file!

mtg_pynance expects the CSV file you feed to it to contain the following four columns with the indicated data types

| **Column**     | **Type** |
|----------------|----------|
| cid            | Integer  |
| id             | String   |
| foiling        | String   |
| purchase_price | Float    |

These four columns *must* appear in your CSV with those exact names (copy and paste them if you want). What's neat is that because mtg_pynance uses Polars to look for these four columns, they can be in any order and you can include other columns in the CSV file. For example, if you want to make a column recording a card's card type, you can do that and mtg_pynance will ignore it! The ability to add extra columns in your CSV file opens the avenue to creating analysis functions that analyze only cards that meet certain conditions, like being a land. See ADVANCED TOPICS for more. Each column will now be explained.

## Column descriptions

### cid

The cid is the collection identifier of a card. It is by nature a unique number you assign to a card that distinguishes it from all other cards in your collection. The cid of a card must be a signed integer. Note that if you have multiple copies of the same card they all must have a different cid. This is intuitive from the standpoint that those cards may all have different purchase prices or other characertistics you add to your CSV file, like the purchase date.

### id

The id is the unique identification string of a card assigned by Scryfall. This id is what connects a card in the CSV file to its price data in the Scryfall bulk data file that is downloaded. To find a card's id, go to [Scryfall](https://scryfall.com/), search the card, and click on "Copy-pasteable JSON".

### foiling

The foiling string lists the type of foiling a card has. Because Magic the Gathering cards have non-foil and foil variants, the foil type must be recorded to ensure an accurate price is retrieved. The foiling string has three potential string values

| **foiling string** | **Card type**                   |
|--------------------|---------------------------------|
| none               | Non-foil                        |
| foil               | All types of foil except etched |
| etched             | Etched foil                     |

The foiling string must have exactly one of these three string values (copy and paste them if you want).

### purchase_price

The purchase_price is the price you paid for a card in USD. It must be a float.

## Example CSV file

To illustrate what a CSV file might look like, imagine you have two cards in your collection.

| **name**           | **cid** | **id**                               | **foiling** | **purchase_price** |
|--------------------|---------|--------------------------------------|-------------|--------------------|
| Tolarian Academy   | 0       | ad7ac9a5-340f-4509-826c-7b9416d47887 | none        | 1.00               |
| Transmute Artifact | 1       | 6eab6765-eba3-4844-81ca-ae37a6e903df | none        | 1.00               |

Notice how the additional "name" column was added to enhance the readability of the collection. Remember, you can add as many extra columns as you want as long as you have the four required columns listed above!