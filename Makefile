CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -Iinclude -Dstrncasecmp=_strnicmp -Dstrcasecmp=_stricmp
TARGET = phishguard.exe
SRCS = src/main.c src/email_parser.c src/phish_engine.c src/reporter.c src/utils.c

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

clean:
	rm -f $(TARGET) *.json *.html
