rm -r __pycache__/
rm *.job
cd builds && for m in * ; do
  rm -r $m
done
#rm -r builds
#build is symbolic link to workdir..
