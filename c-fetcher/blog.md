### Building the C program
#### 1. Get the API Key 
###### What is API Key?? 
- API = Application Programming Interface, a way for different systems or applications
to communicate with each other. 
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

#### 2. C PROGRAM 
###### Writing request.h function

