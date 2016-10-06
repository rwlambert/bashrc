#! /bin/bash
# collect the content of this repo from modified local files
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

shopt -s dotglob

TOP=${DIR}/../

for file in $TOP/home/* ; do
hf=.`basename $file`
if [[ $HOME/$hf -nt  $file ]]; then
  cp -f $HOME/$hf $file
  echo collected $hf
fi
done

if [ -d $HOME/scripts ]; then
rsync --update -raz --exclude="*.pyc" --exclude="*#" --exclude="#*" --exclude="*~" $HOME/scripts/* ${TOP}scripts
fi

