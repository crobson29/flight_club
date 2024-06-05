# Flight Club

The intention for this project is to make a python script that finds cheap flights and emails them to you.  This project will use a Google Sheet to keep track of the flights that you want to track and their prices, and the Amadeus Flight Search API to find flights.  When ran, the program will check the Google Sheet for the flights and their previous lowest prices.  It will then use Amadeus to search for these flights from tomorrow to 6 months from now.  If the price is lower than the price listed in the Sheet, it will send an email with the details of the flight and the price.

The API Keys and other sensitive information are kept in a json document, and the values are not populated.  The blank JSON is provided, and the values can be filled and feed the program.