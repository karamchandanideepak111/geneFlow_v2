#!/bin/sh

a="8000"

b=$(lsof -t -i:$a)

if [[ -n "$b" ]]
then
  kill -9 $b
  echo "previous process killed"
else
  echo "no process killed"
fi