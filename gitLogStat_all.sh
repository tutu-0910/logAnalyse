#!/bin/sh

git log  --after="$1" --until="$2" --oneline  | wc -l

exit 0
