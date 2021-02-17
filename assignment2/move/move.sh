#!/bin/bash

function is_dir() {
  # Check if directories exist. If destination does not, prompt user
  SRC=$1
  DST=$2

  if [ ! -d "$SRC" ]; then
    echo "Source directory not found"
    exit 1
  fi

  if [ ! -d "$DST" ]; then
    echo "Destination directory not found. Make directory? [y/n]"
    read INPUT
    if [ "$INPUT" == "y" ] || [ "$INPUT" == "yes" ]; then
      mkdir -v $DST
    elif [ "$INPUT" == "n" ] || [ "$INPUT" == "no" ]; then
      echo "Aborting."
      exit 1
    else
      echo "Aborting. Please provide [y/n]"
      exit 1
    fi
  fi
}

function move() {
  # Move content from source directory to destination directory
  shopt -s dotglob nullglob
  SRC=$1
  DST=$2

  if [ "$#" == "2" ]; then
    for file in $SRC/*; do
      mv -v "$file" $DST
    done
  elif [ "$#" == "3" ]; then
    FILE_EXT=$3
    for file in $SRC/*.$FILE_EXT; do
      mv -v "$file" $DST
    done
    for file in $SRC/**/*.$FILE_EXT; do
      mv -v "$file" $DST
    done
  fi
}

function mk_date_dir() {
  # Make date- and timestamped directory
  SRC=$1
  DST=$2
  echo "Create date- and timestamped directory in new destination that moved content will be within? [y/n]"
  read INPUT
  if [ "$INPUT" == "y" ] || [ "$INPUT" == "yes" ]; then
    NEW_DST=$DST/$(date +%Y-%m-%d-%H-%M)
    mkdir -p $NEW_DST
    if [ "$#" == "2" ]; then
      move $SRC $NEW_DST
    elif [ "$#" == 3 ]; then
      FILE_EXT=$3
      move $SRC $NEW_DST $FILE_EXT
    else
      echo "Usage: move src_dir dst_dir [file_extension]"
      exit 1
    fi
  elif [ "$INPUT" == "n" ] || [ "$INPUT" == "no" ]; then
    if [ "$#" == "2" ]; then
      move $SRC $DST
    elif [ "$#" == 3 ]; then
      FILE_EXT=$3
      move $SRC $DST $FILE_EXT
    else
      echo "Usage: move src_dir dst_dir [file_extension]"
      exit 1
    fi
  else
    echo "Aborting Please provide [y/n]."
  fi
}


if [ "$#" == "2" ]; then
  is_dir $1 $2
  mk_date_dir $1 $2
elif [ "$#" == "3" ]; then
  is_dir $1 $2
  mk_date_dir $1 $2 $3
else
  echo "Provide source directory, destination directory and optionally file extension"
  exit 1
fi
