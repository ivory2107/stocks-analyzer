#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <curl/curl.h>

#include "cJSON.h"
#include "request.h"

void parse_response(const char *response, const char *symbol) {
    cJSON *json = cJSON_Parse(response);
    
    if (json == NULL) {
        fprintf(stderr, "Error parsing JSON response\n");
        return;
    }

    // get the "Time series (5min)" object from the JSON response
    cJSON *time_series = cJSON_GetObjectItemCaseSensitive(json, "Time Series (Daily)");
    if (time_series == NULL) {
        fprintf(stderr, "Error: 'Time Series (Daily)' not found in JSON response\n");
        cJSON_Delete(json);
        return;
    }

    char filename[256];
    snprintf(filename, sizeof(filename), "../data/results/%s.csv", symbol);
    FILE *fp = fopen(filename, "w");

    if (!fp) {
        fprintf(stderr, "Failed to open file\n");
        cJSON_Delete(json);
        return;
    }

    //write a header to the CSV file
    fprintf(fp, "timestamp,open,high,low,close,volume\n");

    //loop over the timeseries. time series = JSON object of all dates hence we need 
    //to loop over each
    cJSON *entry = NULL;
    cJSON_ArrayForEach(entry, time_series) {
        const char *timestamp = entry->string;

        //grab each field from the entry, so open, high, low, close, volume
        //so one by one extract each of the data
        cJSON *open = cJSON_GetObjectItemCaseSensitive(entry, "1. open");
        cJSON *high = cJSON_GetObjectItemCaseSensitive(entry, "2. high");
        cJSON *low = cJSON_GetObjectItemCaseSensitive(entry, "3. low");
        cJSON *close = cJSON_GetObjectItemCaseSensitive(entry, "4. close");
        cJSON *volume = cJSON_GetObjectItemCaseSensitive(entry, "5. volume");

        //then write into the CSV file, one row per timestamp
        fprintf(fp, "%s,%s,%s,%s,%s,%s\n", timestamp, 
            open->valuestring, high->valuestring, 
            low->valuestring, close->valuestring, 
            volume->valuestring
        );
    }

    fclose(fp);
    printf("Data written to %s.csv\n", symbol);
    cJSON_Delete(json);

}