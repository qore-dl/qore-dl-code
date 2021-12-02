# Generate Adjustment Solution with Heuristic Algorithm

Since adjusting running jobs is NP-hard, it is efficient and feasible to generate local optimal adjustment solutions using heuristic algorithms. 
Thus, we leverage the genetic algorithm (GA) [1] to generate fine-grained adjustment solutions for target jobs.

## Genotype Coding.

We use a 9-bit binary code to encode candidate solutions. The highest digit of the code represents the two adjustment methods. 
The lower 8 bits are constructed by the sub-codes of each resource type alternately. 
For example, The following figure shows the genotype code when considering CPU and memory:
![Image text](https://raw.githubusercontent.com/qore-dl/qore-dl-code/main/images/GA.png)

## Solution Exploration.
We maintain a set of candidate solutions for each target job $i$, and update the set iteratively based on the fitness of solutions.
We define the fitness $f_{iu}$ of candidate solution $u$ to $i$ according to the four cases as:

The four cases are defined in the section IV.D.2) of the paper manuscript (Page 6):
![Image text](https://raw.githubusercontent.com/qore-dl/qore-dl-code/main/images/Case.png)


[1] D. Whitley. A genetic algorithm tutorial. Statistics and computing, 4(2):65–85, 1994.