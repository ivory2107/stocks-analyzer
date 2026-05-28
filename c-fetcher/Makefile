# Makefile for c-fetcher

#gcc since we are using gcc, if we want to use clang, we would change this to clang
CC = gcc  

# Compiler flags, -g for debugging, -Wall for all warnings
#-mconsole is used to prevent the console window from appearing when running the program on Windows. 
CFLAGS = -g -mconsole

#library to link against, in this case, we need to link against the curl library to use its functions
LIBS = -lcurl

TARGET = stocks-analyzer.exe

SRCS = main.c request.c cJSON.c parse.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) $(LIBS) -o $(TARGET)

run: $(TARGET)
	./$(TARGET)

#deletes the exe so we can re-build 
clean: del $(TARGET)
	   del *.o

