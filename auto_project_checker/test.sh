#!/usr/bin/env bash
count=0
git show --pretty="" --name-only |
	while IFS= read -r line
	do
		count=$((count+1))
		if [ $count -ge 7 ]
		then
			echo "$line"
		fi
	done


