import argparse
import os
import torch

parser = argparse.ArgumentParser("Computes similarity scores for SemEval2017 Task 2 word pairs.")
parser.add_argument(
    "--input_dir", default="../data/semeval/tokenized/", help="directory containing tokenized SemEval test files"
)
parser.add_argument(
    "--output_dir", default="results/", help="directory where output files will be saved"
)
parser.add_argument(
    "--embeddings", default="../data/embeddings/f1_series_embeddings.pt", help="embedding weights"
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
    return bos

if __name__ == "__main__":
    for filename in os.listdir( args.input_dir ):
        with open( os.path.join( args.input_dir, filename ) ) as f_in:
            with open( os.path.join( args.output_dir, filename ) , "w+") as f_out:
                for line in f_in.read().strip().split("\n"):

                    # read word-pair
                    word1, word2 = line.split("\t")
                    word1 = map(int, word1.strip().split(" "))
                    word2 = map(int, word2.strip().split(" "))
            
                    # compute bag-of-subwords embedding for word-pair
                    emb1 = bag_of_subwords( word1, bpe_embeddings )
                    emb2 = bag_of_subwords( word2, bpe_embeddings )
        
                    # compute similarity and output to file
                    cosine_similarity = torch.nn.functional.cosine_similarity(emb1, emb2).item()
                    f_out.write( "%f\n"%(cosine_similarity,) )
