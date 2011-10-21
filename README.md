## Overview ##

As the world's most popular programmer Q&amp;A community, StackOverflow.com  is a showcase of the successful usage of the tag system, where each question could have one or more questions to indicate its "topics". Intuitively, We can think of the text as the distribution over tags.
 In this project, our goal is to predict the tags of a questions by mining the large amount of tagged questions.

Furthermore, a tags predictor of high accuracy also enables us to discover user's "taste" of questions. We can estimate users interests(represented by a decimal vector) in each tag by examing questions a user asked/answered/favorited/voted. Thus, we can use this information to recommend new question or discover other user who share the similiar interests.

## Dataset ##
StackOverflow has published their dataset under Common Creative Licence. The dataset includes over 2.2 millions questions, 4.8 million answers and 30 thousands of tags, which provides a rich content for our analysis.

