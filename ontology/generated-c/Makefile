# Makefile
ACCESS_TCPIP := TCPIP
ACCESS_NOTA := NOTA
ACCESS_PROTO := $(ACCESS_TCPIP)

APISOURCE = ontology.c
APIHEADER = ontology.h

OBJECT = ontology.o 

THREADS := -pthread
EXPAT_AND_SCEW := -L/usr/lib -L/usr/local/lib -lexpat -lscew -lkpilow
INCLUDES := -I/usr/local/include -I/usr/local/include/scew -I/usr/local/include/smartslog
LIBS := $(THREADS)  $(EXPAT_AND_SCEW) -lsmartslog

CC     = gcc
DEBUG := -g
CFLAGS = -Wall -c $(DEBUG) $(THREADS) -DACCESS_TCPIP -DTHREADS -DEXPAT_AND_SCEW $(INCLUDES)
LFLAGS = -Wall $(DEBUG) $(THREADS)

PROGRAM_NAME = kp

targets = main

pkg_packages := scew

PKG_CFLAGS  := $(shell pkg-config --cflags $(pkg_packages))
PKG_LDFLAGS := $(shell pkg-config --libs $(pkg_packages))

.PHONY: all
all : $(targets)

main: $(OBJECT) kp.o
	$(CC)  $(LFLAGS)  kp.o $(LIBS) $(OBJECT) -o $(PROGRAM_NAME)

.c.o:
	$(CC) $(CFLAGS) $(PKG_CFLAGS) $(LFLAGS) -o $@ $<


.PHONY: clean
clean:
	rm -f $(targets) *.o
	rm $(PROGRAM_NAME)
