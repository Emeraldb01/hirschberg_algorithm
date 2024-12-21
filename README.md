# Implementation and Benchmarking of Hirchberg’s Algorithm

Hirchberg’s algorithm is a dynamic programming algorithm introduced during this course. Its space optimization made it an unique algorithm for aligning long sequences, it allows compact space while still retaining the alignment with no loss. 

Development Team:
- Nai-Syuan Chang(nc47@illinois.edu)
- Taisia Kalinina(taisiak2@illinois.edu)


The Aligorithm Implementations can be found in global_align.ipynb. The algorithms can be generally described in the following manner. 
## Needleman–Wunsch Algorithm
This dynamic programming algorithm can be broken down into three main steps. 

Inputs: two strings v and w representing DNA sequences to align and a scoring function. 
1. Create and initialize the first row and column of the scoring matrix. 
2. Fill in each cell of the scoring matrix and keep track of back pointers for each cell. 
3. Do a traceback to reconstruct the alignment.
   
Output: the optimal sequence alignment and the score of the alignment.

## Hirschberg’s Algorithm 
Input: two strings v and w representing DNA sequences to align and a scoring function. 
1. Fill in the scoring matrix to the middle column using the Needleman–Wunsch algorithm but only keep the current and previous columns in memory. The values in the middle column are called the prefixes.    
2. Find the suffixes. Start in the bottom right corner of the matrix, reverse the edge direction (while keeping weights the same) and find the values of the middle column in the same way as step 1.  
3. Sum the prefix and suffix values, the one with the highest value is the index at which is the crossing point and the root of the tree.  
4. Do steps 1 to 3 for the values before and after the crossing point separately, these values make up the children of the root. 
5. Continue this process until the lengths of the inputs are 1. 
6. Do a traceback to reconstruct the alignment.
   
Output: the optimal sequence alignment and the score of the alignment. 

