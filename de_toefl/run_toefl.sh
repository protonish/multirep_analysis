settings=(baseline random series)
for setting in ${settings[@]}; do
  ./tokenize.sh $setting

  if [ "$setting" != "baseline" ]; then
    cipher_levels=(f1_ f2_ f3_ f4_)
  else
    cipher_levels=("" )
  fi
  
  for cipher_level in "${cipher_levels[@]}"; do
    echo $setting \& $cipher_level \& $( python de_toefl.py --embeddings ../data/embeddings/${cipher_level}${setting}_embeddings.pt ) \\\\
  done
  echo
done

