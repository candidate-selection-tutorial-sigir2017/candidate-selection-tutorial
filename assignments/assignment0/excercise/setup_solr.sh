#!/bin/bash
set -e

# Escape code
esc=`echo -en "\033"`

# Set colors
cc_red="${esc}[0;31m"
cc_green="${esc}[0;32m"
cc_yellow="${esc}[0;33m"
cc_blue="${esc}[0;34m"
cc_normal=`echo -en "${esc}[m\017"`

function ec () {
    echo -e "${cc_green}${1}${cc_normal}"
}

cd ~/workspace/candidate-selection-tutorial/finished-product/resources
./setup_solr.sh
cd ~/workspace/candidate-selection-tutorial/assignments/assignment0/excercise
ec "\n\nSolr has been started and collections with specific dataset fields have been created!"
