echo Tokenizing with $1/sentencepiece.bpe.model

mono_dir=../data/semeval/original/test/subtask1-monolingual/data/
cross_dir=../data/semeval/original/test/subtask2-crosslingual/data/
enciphered_mono_dir=../data/semeval/enciphered/mono/$1/
enciphered_cross_dir=../data/semeval/enciphered/cross/$1/
args="--model ../data/bpe_model/$1/sentencepiece.bpe.model --output_format id"

for f in $( find $mono_dir -type f |grep "\/\(en\|de\)\." ); do
  lang=$( echo $f |sed 's/^.*\///g' |sed 's/\(\..\)\.test.*//g' |sed 's/^.*-//g' )
  python ../spm_encode.py \
    --inputs <( cat $f |sed 's/	.*//g' |sed 's/^/<'$lang'> /g' ) \
    --outputs _tmp_left \
    $args > /dev/null 2>&1
  python ../spm_encode.py \
    --inputs <( cat $f |sed 's/.*	//g' ) \
    --outputs _tmp_right \
    $args > /dev/null 2>&1
  outfile=$( echo $f |sed 's/^.*\///g' )
  paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile
done
for f in $( find $cross_dir -type f |grep "\/en-de\." ); do
  src_lang=$( echo $f |sed 's/^.*\///g' |sed 's/\.test.*//g' |sed 's/-.*//g' )
  tgt_lang=$( echo $f |sed 's/^.*\///g' |sed 's/\.test.*//g' |sed 's/.*-//g' )
  python ../spm_encode.py \
    --inputs <( cat $f |sed 's/	.*//g' |sed 's/^/<'$tgt_lang'> /g') \
    --outputs _tmp_left \
    $args > /dev/null 2>&1
  python ../spm_encode.py \
    --inputs <( cat $f |sed 's/.*	//g' ) \
    --outputs _tmp_right \
    $args > /dev/null 2>&1
  outfile=$( echo $f |sed 's/^.*\///g' )
  paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile
done

if [ "$1" != "baseline" ]; then 
  # make files from en to enciphered de and vice versa
  for f in $( find $enciphered_cross_dir -type f |grep "\/en\(\..\)\?-de\." ); do
    src_lang=en
    tgt_lang=de
    tgt_lang_=$( echo $f |sed 's/^.*\///g' |sed 's/\.test.*//g' |sed 's/.*-//g' )

    # take the English column from the unenciphered data:
    orig_file=${cross_dir}en-de.test.data.txt
    python ../spm_encode.py \
      --inputs <( cat $orig_file |sed 's/	.*//g' |sed 's/^/<'$tgt_lang'> /g') \
      --outputs _tmp_left \
      $args > /dev/null 2>&1
    python ../spm_encode.py \
      --inputs <( cat $f |sed 's/.*	//g' ) \
      --outputs _tmp_right \
      $args > /dev/null 2>&1
    outfile=en-$tgt_lang_.test.data.txt
    paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile

    orig_file=${cross_dir}en-de.test.data.txt
    python ../spm_encode.py \
      --inputs <( cat $orig_file |sed 's/.*	//g' |sed 's/^/<'$src_lang'> /g') \
      --outputs _tmp_left \
      $args > /dev/null 2>&1
    python ../spm_encode.py \
      --inputs <( cat $f |sed 's/	.*//g' ) \
      --outputs _tmp_right \
      $args > /dev/null 2>&1
    outfile=$tgt_lang_-en.test.data.txt
    paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile
  done
  
  # make files from de to enciphered de
  for f in $( find $enciphered_mono_dir -type f |grep "\/de\..\.test" ); do
    src_lang=de
    tgt_lang=de
    tgt_lang_=$( echo $f |sed 's/^.*\///g' |sed 's/\.test.*//g' |sed 's/.*-//g' )
  
    # take the German column from the unenciphered data:
    orig_file=${mono_dir}de.test.data.txt
    python ../spm_encode.py \
      --inputs <( cat $orig_file |sed 's/.*	//g' |sed 's/^/<'$tgt_lang'> /g') \
      --outputs _tmp_left \
      $args > /dev/null 2>&1
    python ../spm_encode.py \
      --inputs <( cat $f |sed 's/.*	//g' ) \
      --outputs _tmp_right \
      $args > /dev/null 2>&1
    outfile=de-$tgt_lang_.test.data.txt
    paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile
  
    orig_file=${mono_dir}de.test.data.txt
    python ../spm_encode.py \
      --inputs <( cat $orig_file |sed 's/	.*//g' |sed 's/^/<'$src_lang'> /g') \
      --outputs _tmp_left \
      $args > /dev/null 2>&1
    python ../spm_encode.py \
      --inputs <( cat $f |sed 's/	.*//g' ) \
      --outputs _tmp_right \
      $args > /dev/null 2>&1
    outfile=$tgt_lang_-de.test.data.txt
    paste _tmp_left _tmp_right > ../data/semeval/tokenized/$1/$outfile
  done
fi
rm _tmp_left _tmp_right
