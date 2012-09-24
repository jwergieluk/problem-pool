#!/bin/bash

set -e; set -u


pdflatex index
bibtex index
pdflatex index
pdflatex index






