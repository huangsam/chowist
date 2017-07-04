# chowist

Great places are chosen by great chowists.

Contribute by adding additional places to `places.json`.

## Database Setup

Upload data to your MongoDB instance:

    mongoimport --db chowist --collection places --drop --file ./places.json --jsonArray

Verify that the data exists:

    mongo chowist placesExist.js --quiet

Enter the `chowist` database:

    mongo chowist
