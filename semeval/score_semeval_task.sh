output_dir=results/
jarfile=../data/semeval/original/task2-scorer.jar

for f in $( ls $output_dir ); do
  gold_file=$( echo $f |sed 's/data/gold/g' |sed 's/\.[a-z]-/-/g' |sed 's/\.[a-z]\././g' |sed 's/de-de\./de\./g' )
  if [[ "$gold_file" == *"-"* ]]; then
    gold_dir=../data/semeval/original/test/subtask2-crosslingual/keys/
    gold_file=en-de.test.gold.txt
  else
    gold_dir=../data/semeval/original/test/subtask1-monolingual/keys/
  fi
  echo $f |sed 's/\.test.*//g'
  echo $1 \& $2 \& $( java -jar $jarfile $gold_dir$gold_file $output_dir$f |awk '{print $5" & "$7" \\\\"}' |tr -d ",)" )
done
