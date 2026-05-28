# stocks-analyzer

A C program that fetches live stock data from a free API and logs it to a CSV file.

## A C program that:

Calls a stock API (FROM ALPHA VANTAGE). 
Gets the daily timeseries of the stocks. 
Parses the response and saves it to a CSV like stock_log.csv

##### Running the code
- The c-fetcher can be ran using:
    gcc main.c request.c cJSON.c parse.c -lcurl -o stocks-fetcher.exe

    Followed by, where it requires an argument. That argument being the stocks 
    symbol of the company we want:
    .\stocks-fetcher.exe argument

**LIST OF ALL STOCK TICKER SYMBOLS** - https://stockanalysis.com/stocks/ 
