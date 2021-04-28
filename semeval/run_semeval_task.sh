settings=(baseline random series)
for setting in ${settings[@]}; do
  echo
  echo $setting
  >&2 echo In setting "$setting"

  >&2 echo Tokenizing data 
  ./tokenize_semeval_task.sh $setting

  if [ "$setting" != "baseline" ]; then
    cipher_levels=(f1_ f2_ f3_ f4_)
  else
    cipher_levels=("" )
  fi
  
  for cipher_level in "${cipher_levels[@]}"; do
    >&2 echo Running test $cipher_level
    echo
    echo $cipher_level
    #echo Computing similarity scores
    python compute_semeval_scores.py --embeddings ../data/embeddings/$1/${cipher_level}${setting}_embeddings.pt --input_dir ../data/semeval/tokenized/$setting
    #echo Computing correlations
    ./score_semeval_task.sh $setting $cipher_level
  done
  # clean output directory
  rm results/*.txt 
done > scores/scores.txt
cd scores
./split_tables.sh ./scores.txt
