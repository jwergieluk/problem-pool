#!/bin/bash

set -e; set -u

TMP="/tmp"
TGT="problem-supermarkt"

#if [ $TGT.tex -nt $TGT.pdf ]; then
    pdflatex    -output-directory $TMP $TGT
    biber       --output_directory $TMP $TGT
    pdflatex    -output-directory $TMP $TGT
#    pdflatex    -output-directory $TMP $TGT
    cp $TMP/$TGT.pdf .
#fi





