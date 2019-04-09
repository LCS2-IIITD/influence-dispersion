# Code 
This repository houses the code for **Go Wide, Go Deep:  Quantifying the Impact of Scientific Papers through Influence Dispersion Trees**
(accepted at *ACM/IEEE Joint Conference on Digital Libraries* authored by Dattatreya Mohapatra, Abhishek Maiti, Sumit Bhatia & Tanmoy Chakraborty. 

## Instruction
The NID of an paper can be calculated in two ways using this repository. 
* Using Text-Based Dataset: The script will parse the text based dataset and create the citation graph, using which the Influence Dispersion Tree and Influence Disperion Index will be calculated. The format of the text is given below. 

* Using pickled citation graphs: The script will take the path of the pickled NetworkX citation graph. This doesn't require any text-based dataset. More details are in the **data** section. 

The dependencies for this repository are: 
```
cycler==0.10.0
decorator==4.3.0
kiwisolver==1.0.1
matplotlib==2.1.0
networkx==1.11
numpy==1.15.1
pyparsing==2.2.1
python-dateutil==2.7.3
pytz==2018.7
scikit-learn==0.19.2
scipy==1.1.0
six==1.11.0
sklearn==0.0
```

## Directories 
### src
This has 3 has scripts named 
* ```init.py```
This script parses the dataset. It parses for the names, the papers which have cited by other papers, the paper
which has been cited by other papers. This then makes the ```global_citation_graph```. In this, the invalid edges are removed, the Influence Dispersion
Graph (IDG) for each paper is isolated and converted to Influence Dispersion Tree (IDT) and serialised in the form of a dictionary. 
The agruments it takes are (All are mandatory):
    * ```--dataset```: Path to the dataset. 
    * ```--dumps```: Path to dump the serialised pickled files. 
    * ```--graph_path```: Path to the ```global_citation_graph```, if this is used then ```--dataset``` is not required
    * ```--year_dict_path```: Path to the ```year_dict```. This is a dictionary with key as paper-id (as per the citation graph) and value is the publication year. This is mandatory if ```--graph_path``` is used. 

* ```main.py```
This script takes the ID of the paper according to dataset, and the year and gives the __Normalised Influence Dispersion__ (NID) and the 
__Influence Dispersion Index__ (IDI) of the paper. 
The agruments it takes are (All are mandatory):
    * ```--dumps```: Path to dump the serialised pickled files. 
    * ```--id```: ID of the query paper 
    * ```--year```: Year till which the NID and the IDI needs to be calculated. 
    
 * ```utils.py```
 This script houses all the functions used in the other two scripts. all the documentation can be accessed by ```function_name.__doc__```. 
 

### data 
This has the two data developed for this paper. 
* _MAS Datatset_: The data which we have used is the Microsoft Academic Search Dataset (MAS), this dataset was created by crawling the [Microsoft Academic](https://academic.microsoft.com/home) web portal. 
The dataset description are as follows:

|            Number of Papers            | 3,908,805 |
|:--------------------------------------:|-----------|
|         Number of Unique Venues        |   5,149   |
|        Number of unique authors        | 1,186,412 |
|    Avg. number of papers per author    | 5.21      |
|    Avg. number of authors per paper    | 2.57      |
| Min/Max number of references per paper | 1/2,432   |
|  Min/Max number of citations per paper | 1/13,102  |
 
You can find the data [here](https://drive.google.com/drive/folders/1SXmrDoi9F80ojgbU7mHcKgpE9Lje2m7g?usp=sharing). 
  
 * _Test Of Time Dataset_:This is a ```.csv``` file which has the test of time dataset which has been manually curated. 
 

_Note_: We currently only support MAS-style textual datasets but will add support for other datasets later. 
To convert your Citation dataset to MAS-style, please keep in mind the following points. The features which weren't used for this paper but are in the dataset (MAS) we used are omitted. 

* ```#index<paper-id>``` indicates the paper-id of the paper whose information is in the following lines (also referred to as the index paper).
* ```#j<text>``` indicates the journal in which it was puclished. Replace ```j``` with ```c``` to get the conference name.
* ```#y<4-digit no.>``` indicates the year in which the paper was published.
* ```#%*<text>[.]``` indicates a paper which has cited the index paper. This is the paper name and the paper-id in this dataset for the same is enclosed in ```[.]```. 
* ```#%y``` indicates the year in which the paper citing the index paper has been published.
* ```#%j``` indicates the journal in which the paper citing the index paper has been published. Replace ```j``` with ```c``` to get the conference name.
* ```#$*<text>[.]``` indicates a paper which the index paper has cited. This the paper name and the paper-id in this dataset for the same is enclosed in ```[.]```. 
* ```#$y``` indicates the year in which the paper cited by the index paper has been published.
* ```#$j``` indicates the journal in which the paper cited by the index paper has been published. Replace ```j``` with ```c``` to get the conference name.

An example from the dataset 
```
#index29
#*An evolutionary autonomous agents approach to image feature extraction
#jIEEE Transactions on Evolutionary Computation - TEC[0], vol. 1, no. 2, pp. 141-158
#y1997
#%*New Prospects in Line Detection by Dynamic Programming[799913]
#%jIEEE Transactions on Pattern Analysis and Machine Intelligence - PAMI[25], vol. 18, no. 4, pp. 426-431
#%y1996
#%*Automatic Finding of Main Roads in Aerial Images by Using Geometric-Stochastic Models and Estimation[800248]
#%jIEEE Transactions on Pattern Analysis and Machine Intelligence - PAMI[25], vol. 18, no. 7, pp. 707-721
#%y1996
#$*Swarm cognition on off-road autonomous robots[39335482]
#$@Pedro Santana[621081],Luís Correia[2108324],
#$jSwarm Intelligence[40], vol. 5, no. 1, pp. 45-72
#$y2011

```
The end is demarcated by the beginning of another index paper. 
_Please follow the order in which the above points are when converting your dataset._


Incase of any queries you can reach us at lcs2@iiitd.ac.in



