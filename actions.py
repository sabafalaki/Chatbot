
# coding: utf-8

# In[ ]:

from rasa_core_sdk import Action
from rasa_core.events import Restarted

import pandas as pd
import requests

movie_data = pd.read_csv("movie_metadata.csv",encoding="utf-8")

# Doing some data cleaning on "genre" column of dataset
def convert_to_list(x):
    y=x.replace("-","").lower() 
    return y
movie_data["genres"]=movie_data["genres"].apply(convert_to_list)

# Doing some data cleaning on "color" column of dataset
def convert(x):
    y=x.replace(" Black and White","Black and White").lower()
    return y
movie_data["color"].fillna("nothing", inplace = True)
movie_data["color"]= movie_data["color"].apply(convert)


class contentAction(Action):
    def name(self):
        return "action_check_movie_content" # Getting movie Content Rating for specific movie
    
    def run(self, dispatcher, tracker, domain):
        mm = tracker.get_slot('movie')
        # if the entity is not captured, it will gives the fallback message
        if mm is None:
            dispatcher.utter_message("Sorry, I did not get that")
        else:
            movie_data["movie_title"]=movie_data["movie_title"].str.lower()
            # In the dataset all the movie titles have "\xa0" at their end. 
            rr = movie_data[movie_data.movie_title == mm+"\xa0"]
            if len(rr)==0:# if there is no such a movie in the dataset that is mentioned
                dispatcher.utter_message("There is no movie with the name that you mentioned in dataset")
            else:
                #getting content rating for asked movie
                xx=list(rr["content_rating"])
                dispatcher.utter_message("Content rating of {} movie is {} ".format(mm,xx[0]))
            
        
class info(Action):
    def name(self):
        return "action_info" # Getting general information about movie
    
    def run(self, dispatcher, tracker, domain):
        mm = tracker.get_slot('movie')
        # if the entity is not captured, it will gives the fallback message
        if mm is None: # if there is no such a movie in the dataset that is mentioned
            dispatcher.utter_message("Sorry, I did not get that")
        else:
            movie_data["movie_title"]=movie_data["movie_title"].str.lower()
            # In the dataset all the movie titles have "\xa0" at their end. 
            rr = movie_data[movie_data.movie_title == mm+"\xa0"]
            if len(rr)==0:
                dispatcher.utter_message("There is no movie with the name that you mentioned in dataset")
            else:
                # Returning some general information( director name and leading actor\actress name and imdb score)
                Director=list(rr["director_name"])
                Actor=list(rr["actor_1_name"])
                IMDB=list(rr["imdb_score"])
                dispatcher.utter_message("General Information about{} movie:\n Director is {}\n Leading Actor\actress is {} \n IMDB score is {}  ".format(mm,Director[0],Actor[0],IMDB[0]))
            
            

        
class moviesuggestionaction(Action):
    def name(self):
        return "action_best_choices_of_movie" # suggesting top 5 movies according to IMDB
    
    def run(self, dispatcher, tracker, domain):
        gg = tracker.get_slot('genre')
        yy = tracker.get_slot('year')
        ii = tracker.get_slot('imdb')
        cc = tracker.get_slot('themecolor')
        
        if gg is None:
            dispatcher.utter_message("Sorry, I did not get that")
               
        elif yy is not None: #if it is the stories that used year and imdb score as the inputs
            if ii is not None:
                new_results=movie_data[movie_data['genres'].str.contains(gg)]
                yy=float(yy)
                ii=float(ii)
                answer=new_results[(new_results.title_year >= yy)&(new_results.imdb_score >= ii)]
                #doing computation to fnd the profit
                answer["profit"]=answer["gross"]-answer["budget"]
                answer=answer.sort_values('profit',ascending=0)#sort movie by profit
                answer=answer.drop_duplicates()
                b=list(answer.movie_title)[0:5]
                g=list(answer.profit)[0:5]
                p=["%s            %s" %i for i in zip(b,g)]
                if len(answer)==0: # if there is no movie in dataset with the asked conditions
                    dispatcher.utter_message("There is no movie with the criteria that you mentioned in dataset")
                else:
                    dispatcher.utter_message("Top 5 profitable movies with your desired criteria are :\n{0}\n{1}\n{2}\n{3}\n{4}".format(*p))
                        
        elif cc is not None: #if it is the story that used color of movie to suggest the movies
            new_results=movie_data[movie_data['genres'].str.contains(gg)]
            answer = new_results[new_results['color']== cc]
            #doing computation to fnd the profit
            answer["profit"]=answer["gross"]-answer["budget"]
            answer=answer.sort_values('profit',ascending=0)
            answer=answer.drop_duplicates()
            b=list(answer.movie_title)[0:5]
            g=list(answer.profit)[0:5]
            p=["%s            %s" %i for i in zip(b,g)]
            if len(answer)==0:# if there is no movie in dataset with the asked conditions
                dispatcher.utter_message("There is no movie with the criteria that you mentioned in dataset")
            else:
                dispatcher.utter_message("Top 5 profitable movies with your desired criteria are :\n{0}\n{1}\n{2}\n{3}\n{4}".format(*p))                                      
                                         
        else:
            dispatcher.utter_message("Sorry, I did not get that")
            


