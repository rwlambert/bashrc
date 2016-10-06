#! /bin/bash

echo "usage, migrate wiki from_project_name to_namespace/project_name"
if [ -z "$1" ]
  then
    echo "No argument for source supplied"
    exit
fi
if [ -z "$2" ]
  then
    echo "No argument for target supplied"
    exit
fi

git clone https://github.com/DataAnalyticsOrganization/${1}.wiki.git
cd $1
git remote add gitlab http://gitlab-nl.dna.kpmglab.com/`echo "$2" | tr "[:upper:]" "[:lower:]"`.wiki.git
git push gitlab master
