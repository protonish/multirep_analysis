# Requirements
Python 3
```
pip instal sentencepiece
pip install fire
```

# Notes
Embeddings are of shape `(vocab, dim=512)`

### Create Enciphered text
Instructions in __main__ method:
```
Step1:  Set SRCDIR and DSTDIR for reading and writing data.
    set ODET = the 'real' text file name -> [ODET is Orig De Text]
    These arguments create the faker object.

Step 2: faker.generate() generates data. Set a prefix (TRAINPREF). this will generate files named
    'prefix'.a-en.a , 'prefix'.b-en.b incrementally to match the no of keys
```

To run just provide the keylist. 
```
# generates ROT-key fake language  
python faker.py --key 0 --keylist [1,2,3,4,5] --gen --notrgtoken

# generates ROT-key fake language with case preserved 
python faker.py --key 0 --keylist [1,2,3,4,5] --gen --notrgtoken --keepcase

```
### Compute overlap within a ROT-key data configuration (series/spaced/cased)

```
python overlap.py --langs de a b c d e
```

# SemEval Task 2 Evaluation

```
cd semeval
./run_semeval_task.sh
```
