#!/usr/bin/bash
export OMP_NUM_THREADS=6
for file in ./* ; do
  if [ $file == "./xhpcg" ] || [ $file == "./xhpgmp" ]; then
		echo "$file"
    exec $file
  fi
done
