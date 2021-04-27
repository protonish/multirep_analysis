import argparse
import torch
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    "--embeddings", default="../data/embeddings/f1_series_embeddings.pt", help="embedding weights"
)
parser.add_argument(
    "--data", default="de_toefl_tokenized.txt", help="tokenized file containing similar word-pairs alongside distractors"
)
args = parser.parse_args()

bpe_embeddings = torch.load(args.embeddings)
n_dim = bpe_embeddings.shape[1]

def bag_of_subwords( subwords, embeddings ):
    """
    Given a word represented as a list of subwords
    and a set of subword embeddings, computes the
    bag-of-subwords representation for the input word.
    """
    bos = torch.zeros( (1,n_dim) )
    for subword_id in subwords:
        bos = bos + embeddings[subword_id]
    return bos / len(subwords)

correct = 0
n_questions = 0
with open( args.data ) as fp:
    for line in fp.read().strip().split("\n"):
        wordlist = [word.split(" ") for word in line.split("\t")]
        # combine <de> token with the input word:
        wordlist = [wordlist[0]+wordlist[1]] + wordlist[2:]
        wordlist = [list(map(int, word)) for word in wordlist]

        input = bag_of_subwords( wordlist[0], bpe_embeddings )
        targets = [
                bag_of_subwords( wordlist[i], bpe_embeddings ) 
                for i in range(1,len(wordlist))
            ]

        similarities = [
                torch.nn.functional.cosine_similarity( input, targets[i] ).item()
                for i in range(len(targets))
            ]
        if np.argmax(similarities) == 0:
            correct += 1
        n_questions += 1
print(correct/n_questions)
