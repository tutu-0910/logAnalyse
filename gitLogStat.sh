#!/bin/sh

git log --author="$1" --after="$2" --until="$3" --pretty=oneline $4  | wc -l

exit 0
