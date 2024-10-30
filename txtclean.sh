cd builds && for m in * ; do
  cd $m ; rm *.txt ; rm *.job ; cd ..
done
