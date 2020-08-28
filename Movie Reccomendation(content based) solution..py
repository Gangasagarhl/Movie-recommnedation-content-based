#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np


# # reading the dataset from ratings and movies files

# In[58]:


movies=pd.read_csv("C:/Users/RAGHAVENDRA/Desktop/mrp/movies.csv")
movies.head()


# In[20]:


ratings=pd.read_csv("C:/Users/RAGHAVENDRA/Desktop/mrp/ratings.csv")


# #  merging dataset into one:
# ### uses:
#       1)used for counting the number of people reviewed one movie
#       2)averaging the rating of each movie by viewers

# In[118]:


data=pd.merge(movies,ratings,on="movieId")


# # defining the properties of dataset

# In[22]:


data.shape


# # checking for the first five values of the dataset

# In[23]:


data.head()


# # creating pivot table,based on the index:movieId,placing rating,userId as values

# In[63]:


movie_pivot=data.pivot_table(index=["movieId"],
                             values=["rating","userId"],
                             aggfunc={"rating":np.mean,"userId":len},
                             fill_value=0);


# # cleansing dataset,retrieving only those movies whose review is more than 10

# In[64]:


movie_pivot=movie_pivot.query('userId>=10')


# # merging based on the movieId from movie dataset and index of pivot table 

# In[80]:


movie_pivot=pd.DataFrame(movie_pivot)
newly_generated_used_for_recommendation=pd.merge(movies,movie_pivot,left_on="movieId",right_on=movie_pivot.index)


# In[81]:


newly_generated_used_for_recommendation.head()


# # now actually the movie recommendation starts,by using sklearn

# In[11]:


#importing the dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[133]:


#defining functions to track the title and index
def get_title_from_index(index):
    return newly_generated_used_for_recommendation[newly_generated_used_for_recommendation.index==index]["title"].values[0]

def get_index_from_title(title):
    return newly_generated_used_for_recommendation[newly_generated_used_for_recommendation.title==title].index.values[0]


# In[120]:


cv=CountVectorizer()
#CountVectorizer():used to count the number of similiar words in genres
count_matrix=cv.fit_transform(newly_generated_used_for_recommendation.genres)
#count_matrix:the transformation is fitted


# In[121]:


#this is so much essential,because,this is nothing but correlation matrix:if the contents in the correlation 
#matrix ,is greater than 70%,we can recommend
cosine_sim=cosine_similarity(count_matrix)


# In[122]:


count=int(input("Enter the number of movies to be recomended for you"))


# In[135]:


for i in range(count):
    try:
    
        movie_user_likes=input("\n\nEnter the movie name:  ")
        
        movie_index=get_index_from_title(movie_user_likes)
        similar_movies=list(enumerate(cosine_sim[movie_index]))
        sorted_similiar_movies=sorted(similar_movies,key=lambda x:x[1],reverse=True)
        i=0
        for movie in sorted_similiar_movies:
            print(get_title_from_index(movie[0]))
            i+=1
            if i>15:
                break
        print("******************************************************************************")
    except:
        print("Sorry!!!,search not found\n","*********************************************")
    


# In[117]:





# In[95]:





# In[101]:


newly_generated_used_for_recommendation["movieId"][102]


# In[89]:


i=0
for movie in sorted_similiar_movies:
    print(get_title_from_index(movie[0]))
    i+=1
    if i>60:
        break


# In[16]:


print(data[data.title=="Heat (1995)"]["movieId"].values[0])

