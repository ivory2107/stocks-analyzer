### Building the C program
#### 1. Get the API Key 
###### What is API Key?? 
- API = Application Programming Interface, a way for different systems or applications
to communicate with each other. 
- A contract of sort, how to use and what you can expect to be received. 
- API is just the concept of something being sent back when something is requested. 

###### Why do we need APIs?
- Call request response.

Example: let's say you book a resturant reservesation for 3 people but now 
you want to change it to 6 people. You call, make request and the service employee 
will respond yes. However if the service agent was not there you would need to 
know details such as how many people are attending, how many staff are present, 
if tables are free, need more sometimes provate data just to figure out just to see 
if you can feed 3 more people. 

In this scenerio, you are the application trying to get feed. And the service 
agent is the API, through which you can communicate to the resturant's information 
without revaling private data information. 

###### How do API's work?
- Web API send response via the internet in the form of JSON or XML. 
- Each request and response cycle = API call 
- Request = server and point URL and a request method - GET/weather HTTP/2. The request 
method contains the desired API action. 
- The HTTP Response - contains a status code, a header and a response body. HTTP/2 200 OK.
Could be the server resource client needs to access. 
    - Example: 
    JSON {
        "location" : "sydney"
        "temperature" : "-50"
        "wind" : "67"
    }

- In normal programming, something like making all uppercase can be called using 
a function, this is also an example of an API. 

- There is also remote API's 

##### WEB API
In the web brower (client) used to connect to a server through a Universal Resource Locator(URL). 
HTTP - hypertext protocal (protocal - how to respond, the expetectation)
GET - HTTP verb (only receives the data) then from the server the brower is shown. 
POST - posting data to the server.

HTTP VERBS - 
    - GET, POST, PUT, PATCH, DELETE

* Can also be passed through headers. Used to further communicate what is wanted. e.g. 
caching - stating we want a page if it has changed in a certain time (allows for caching). 

* Status code - convey message from the server side 

* REST - representational State Transfer, API that meet the style constraints are considered
to be Restful. 

* JSON - JavaScript Object Notation - content type is something you can request 

* Example -> Spotify for developers

#### 2. C PROGRAM 
##### Writing request.c function
###### Exploring Curl
Curl is an open source tool that is used to send data back and forth and it runs
locally on your computer. 

So curl gets a response from the server, it doesn't arrive all at once - it comes in chucks over 
the network. By default it prints them to stdout which is useless for parsing. 
So in order to parse you need another function telling it to call another function 
instead of printing in the stdout. 

The buffer struct keeps track of the pointer to the data and the size. We cannot 
pass 2 seperate variable to curl so instead we wrap it in a struct. 

##### Writing parse.c function
- This code basically takes the raw data gotten from the curl into JSON and then puts it 
inside a file as a CSV file. 
In order to convert to JSON we need source code for JSON parser engine. This is becuase C does
not know what JSON is by defult. So we can download cJSON.c and cJSON.h from github repo:
https://github.com/DaveGamble/cJSON/ 

So now the cJSON.c and cJSON.h is giving your prgram the exact instructions (the logic) it 
needs to understand and unpack JSON text. The licence needed for those are already inside the 
files. 

*Creating a MakeFile
- Makefile saves the command (similar to the tasks.json using config build) such that it 
removes the need to type the entire gcc command and can just do make.
- It also tracks which files have changed and only recompiles what it needs to .

*Writing in CSV
- It will create new file. 
- However if the file already exists then it overwrites the data inside it. 

*Problems
- Realised gcc was not installed, so had to install it! Website -> https://www.msys2.org/ 
- In C file -> terminal -> build configure can help simply the build command. So basically all 
the gcc main.c -o stocks ... stuff but simplified into one file. 
- Only the daily verison of the time series is free in ALPHA VANTAGE T_T

##### Running the code
- The c-fetcher can be ran using:
    gcc main.c request.c cJSON.c parse.c -lcurl -o stocks-fetcher.exe

    Followed by, where it requires an argument. That argument being the stocks 
    symbol of the company we want:
    .\stocks-fetcher.exe argument