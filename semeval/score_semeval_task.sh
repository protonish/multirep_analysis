output_dir=results/
jarfile=../data/semeval/original/task2-scorer.jar

for f in $( ls $output_dir |grep "^\(en\|de\|en-de\)\." ); do
  gold_file=${f/data/gold}
  if [[ "$f" == *"-"* ]]; then
    gold_dir=../data/semeval/original/test/subtask2-crosslingual/keys/
  else
    gold_dir=../data/semeval/original/test/subtask1-monolingual/keys/
  fi
  echo $f
  java -jar $jarfile $gold_dir$gold_file $output_dir$f
  echo
done
#java -jar task2-scorer.jar trial/subtask1-monolingual/keys/de.trial.gold.txt trial/subtask1-monolingual/output/de.trial.sample.output.txt
