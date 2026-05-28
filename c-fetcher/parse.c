#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <curl/curl.h>

#include "cJSON.h"
#include "request.h"

void parse_response(const char *response) {
    cJSON *json = cJSON_Parse(response);
    FILE *fp = fopen("response.json", "w");
    
    if (json == NULL) {
        fprintf(stderr, "Error parsing JSON response\n");
        return;
    }

    //to write headers : fprintf


}