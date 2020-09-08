#!/bin/sh

git log --author="$1" --after="$2" --until="$3" --oneline  | wc -l

exit 0
