# Akinator project (with implementation of Decision Tree and idea of Bayes Entropy)

Overview of the concept:
- It will be like classical Akinator ‘guess’ game with characters of League of Legends. 
- There will be answers like yes/no/idk (I don’t know) to value the probabilities and more smoothly handle the inaccuracies.
- The probabilities will be calculated according to each type of model I want to implement, so it won’t fail on unexpected data.

What models gonna be used?
- Decision Tree Classifier – each branch will be as question and leaves as character guess. 
- Bayes Entropy – theory of probability using the Bayes formula and likelihood estimation.

How it will work?
- For Bayes: By recalculating the probability for all objects in our database after answering a new question, you can see which of them are more similar to the hidden object at the moment and output it. More deep explanation, logic implementation will be taken from this source - http://www.machinelearning.ru/wiki/images/7/78/BayesML-2010-Yangel-Akinator.pdf

- For Decision Tree: Algorithm simply will determine the possible splits that each feature gives, calculate the information gain — pick the common one. Game process will look like descending hierarchy from the node to leaf, but the mistakes or inaccuracies in algorithm might cause some troubles in balancing the tree. 

Game itself:

