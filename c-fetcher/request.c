#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "request.h"

#include <curl/curl.h>

typedef struct
{
    char *data;
    size_t size;
} Response;

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;
    Response *res = (Response *)userp;

    char *ptr = realloc(res->data, res->size + realsize + 1);
    if (!ptr) {
        fprintf(stderr, "Not enough memory (realloc returned NULL)\n");
        return 0;
    }

    res->data = ptr;
    memcpy(&(res->data[res->size]), contents, realsize);
    res->size += realsize;
    res->data[res->size] = '\0';
    return realsize;
}

char *get_stock_data(const char *symbol)
{
    // declare a pointer to a CURL object. It will be used to perform the HTTP request. Acts as a handle
    // that tracks all settings for the specific network.
    CURL *curl;

    // All libCurl returns a status code which can be used to determine if the request was successful or if an error occurred.
    CURLcode res;

    // initialise response
    Response response;
    response.data = malloc(1); // initially allocate 1 byte for the response data
    response.size = 0;         // initialize the size of the response data to 0

    if (!response.data)
    {
        fprintf(stderr, "Failed to allocate memory for response data\n");
        return NULL;
    }
    response.data[0] = '\0'; // null-terminate the response data

    // It alloccates memory and initializes underlying network system across your entire program.
    // Every OS has its own way to handle the internet, so this just wakes up the system and then reserves a small
    // amount of RAM for the libCurl library to use globally so that it can create multiple request later on if they require it.
    //   It should be called once before any other libCurl functions are used.
    //curl_global_init(CURL_GLOBAL_DEFAULT);   ADD TO MAIN

    // starts a new libCurl session and assigns it to your CURL pointer. If it fails to initialize, it will return NULL.
    curl = curl_easy_init();

    if (!curl) {
        fprintf(stderr, "Failed to initialize curl\n");
        free(response.data);
        curl_easy_cleanup(curl);
        return NULL;
    }

    // need a seperate variable for URL becuase we need to pass individual symbol for the site code
    char url[512];

    // snprintf -> is a buffer (buffer is a temporary storgae area in memory)
    snprintf(url, sizeof(url),
             "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=5min&apikey=demo",
             symbol);

    // Tells the handle where to go. Takes in the active curl and the option type which is URL and the target web address
    curl_easy_setopt(curl, CURLOPT_URL, url);

    // Tells curl to follow the HTTP redirects. If the website has moved setting it to 1L will make curl follow the
    // new location.
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    // becuase we want the code to write to a funciton we need to call the write functions!
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&response);

    // pauses your code, connects tot he internet and waits for a response and downloads the data. Outcome code is saved to res.
    res = curl_easy_perform(curl);

    // check
    if (res != CURLE_OK)
    {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        free(response.data);
        curl_global_cleanup();
        return NULL;
    } else 
    {
        printf("Response data:\n%s\n", response.data);
    }

    // closes the specific network
    curl_easy_cleanup(curl);

    // cleans up the global environment that was set up at the beginning.
    //curl_global_cleanup();
    return response.data;
}