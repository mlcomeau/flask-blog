#!/bin/bash

CODE=$(curl -s -I https://megan-comeau.duckdns.org | head -n 1 | cut -d ' ' -f 2)

if [ $CODE = "200" ]
then
    echo "0"
else 
    echo "1"
fi 