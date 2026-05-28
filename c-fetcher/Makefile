# Makefile for c-fetcher

#gcc since we are using gcc, if we want to use clang, we would change this to clang
CC = gcc  

# Compiler flags, -g for debugging, -Wall for all warnings
#-mconsole is used to prevent the console window from appearing when running the program on Windows. 
CFLAGS = -g -mconsole

#library to link against, in this case, we need to link against the curl library to use its functions
LIBS = -lcurl

fetcher: stocks-analyzer.exe

#basically checks if the executable is up to date with the source files, if not, it will recompile
stocks-analyzer.exe: main.c request.c cJSON.c parse.c
	$(CC) $(CFLAGS) main.c request.c cJSON.c parse.c $(LIBS) -o stocks-analyzer.exe

#deletes the exe so we can re-build 
clean: del stocks-analyzer.exe

