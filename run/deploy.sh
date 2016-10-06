#! /bin/bash
# copy the contents of this repo to the correct places

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

TOP=${DIR}/../

shopt -s dotglob

echo $DIR
echo $TOP
echo $HOME

if [ ! -d $HOME/scripts ]; then
	mkdir $HOME/scripts
fi


for file in $TOP/home/* ; do
af=`basename $file`
hf=.`basename $file`
if [[ $file -nt $HOME/$hf ]]; then
  cp -f $file $HOME/$hf
  echo deployed $hf
elif [ ! -e $HOME/$hf ]; then
  cp -f $file $HOME/$hf
  echo deployed $hf
fi
done

rsync --exclude="*.pyc" --exclude="*#" --exclude="#*" --exclude="*~" --update -rtaz --progress ${TOP}scripts/* $HOME/scripts

