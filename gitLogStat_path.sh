#!/bin/sh

git log  --after="$1" --until="$2" --pretty=oneline $3  | wc -l

exit 0
