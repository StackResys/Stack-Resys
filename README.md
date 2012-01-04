## Overview ##

As the world's most popular programmer Q&amp;A community, StackOverflow.com  is a showcase of the successful usage of the tag system, where each question could have one or more questions to indicate its "topics". Intuitively, We can think of the text as the distribution over tags.
 In this project, our goal is to predict the tags of a questions by mining the large amount of tagged questions.

Furthermore, a tags predictor of high accuracy also enables us to discover user's "taste" of questions. We can estimate users interests(represented by a decimal vector) in each tag by examing questions a user asked/answered/favorited/voted. Thus, we can use this information to recommend new question or discover other user who share the similiar interests.

## Dataset ##
StackOverflow has published their dataset under Common Creative Licence. The dataset includes over 2.2 millions questions, 4.8 million answers and 30 thousands of tags, which provides a rich content for our analysis.

## Methods ##
In this project, we address these problem by Naive Bayes model and k Nearest
Neighbors model. Especially, with the analysis of the strength and weakness of
the original approaches, we proposed improvements on both models, which significantly
promoted the overall performance of the tag prediction. As the experimental
results indicates, the proposed models outperformed the baseline method
by over 20% in both recall and precision.

## Evaluatilon ##
the big challenge of tag prediction is that tags are often quite
subjective and incomplete. As a result, it will be problematic to conclude that a tag is “correctly”
predicted only when it appears in user-defined tags. For example, if a question is tagged with “java”
but predicted tag is “jdk”, we still believe it is a ”good” prediction because in real life, “jdk” is
closed related with “java”.
Thus, instead of measure the “goodness” of a tag with only match/unmatch, we assign each predicted
tag with a relevance score s, where s is between `[0, 1]`. The higher the score, the more relevant two tags are.
To get the relevance score s, we proposed an evaluation method which makes use of the KullbackLeibler
divergence(a.k.a. KL-distance). KL-distance is an asymmetric measure of the difference
between two probability distributions P and Q. In our case, each tag has a corresponding
word distribution and we assume that similar tags will often have similar word distribution. Note
that although KL(P,Q) and KL(Q, P) is asymmetrical, in practical, the value of KL(Q, P) and
KL(P,Q) is often very close.
