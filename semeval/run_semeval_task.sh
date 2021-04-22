echo Tokenizing semeval data
./tokenize_semeval_task.sh

echo Computing similarity scores
python compute_semeval_scores.py

echo Computing correlations
./score_semeval_task.sh
