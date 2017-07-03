# chowist

Great places are chosen by great chowists.

:sunglasses: | :sunglasses: | :sunglasses:

Contribute by adding additional places to `places.json`.

:beer: | :wine_glass: | :cocktail: | :tropical_drink: | :hamburger: | :bento: | :ramen: | :spaghetti: | :meat_on_bone: | :icecream: | :shaved_ice: | :cake:

## Database Setup

Upload data to your MongoDB instance:

    mongoimport --db chowist --collection places --drop --file ./places.json --jsonArray

Verify that the data exists:

    mongo chowist placesExist.js --quiet

Enter the `chowist` database:

    mongo chowist
