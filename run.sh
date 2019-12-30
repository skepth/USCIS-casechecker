#!/bin/bash
# Tool to run ZScrape

function brew_install {
  brew install $1
  if [ $? -ne 0 ]; then
    echo "could not install $1 - abort"
    exit 1
  fi
}

function pip_install {
  for p in $@; do
    pip3 install -r $p
    if [ $? -ne 0 ]; then
      echo "could not install $p - abort"
      exit 1
    fi
  done
}

function unix_command {
  $@
  if [ $? -ne 0 ]; then
    echo "could not run $@ - abort"
    exit 1
  fi
}

echo "Installing Packages neccessary for ZScrape..."

 /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Minimal installation for a Python ecosystem
# for scientific computing

# Editors
brew install python

# pip_install selenium
# pip_install unidecode
# pip_install pandas
pip_install requirements.txt

#st="$(ls | grep ATWL.csv)"

#if [ "$st" != "" ]
#then
echo "******************* Executing ZScrape... ***************************"
python3 ./webscrape.py
python3 ./parser.py
echo "************** FINISHED EXECUTING OUTPUT ==>> EmployeeData.csv ***************"


