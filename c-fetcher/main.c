#include <stdio.h>
#include <stdlib.h>

#include "request.h"
#include "parse.h"

#include <curl/curl.h>

int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Please provide an argument!\n");
        return 1;
    }

    CURLcode global_init = curl_global_init(CURL_GLOBAL_DEFAULT);

    if (global_init != CURLE_OK) {
        fprintf(stderr, "curl_global_init failed\n");
        return 1;
    }

    //fetch the raw JSON
    char *response = get_stock_data(argv[1]);
    if (!response) {
        fprintf(stderr, "Failed to fetch stock data\n");
        curl_global_cleanup();
        return 1;
    }

    printf("Got response sucessfully\n");
    parse_response(response, argv[1]);

    free(response);
    curl_global_cleanup();
    return 0;
}