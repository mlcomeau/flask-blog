#!/bin/bash

CODE=$(curl -s -I https://megan-comeau.duckdns.org | head -n 1 | cut -d ' ' -f 2)

if [ $CODE = "200" ]
then
    exit 0
else 
    exit 1
fi 