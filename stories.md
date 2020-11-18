## Greet
* greet 
    - utter_greet

## Thanks
* thanks
    - utter_np

## Goodbye
* goodbye
    - utter_goodbye

## Path 1
* greet
    - utter_greet
* content_check
    - utter_what_movie
* inform{"movie":"Avatar"}
    - action_check_movie_content
    - action_restart

## Path 2 
* content_check{"movie": "Titanic"}
    - action_check_movie_content
    - action_restart
    
## Path 4 
* General_info{"movie": "Titanic"}
    - action_info
    - action_restart
    
## Path 5
* movie_suggestion{"genre":"Drama"}
    - utter_what_year
* inform{"year":"2010"}
    - utter_what_imdb
* inform{"imdb":"6.5"}
    - action_best_choices_of_movie
    - action_restart

    
## Path 6
* movie_suggestion{"genre":"Horror","year":"2007"}
    - utter_what_imdb
* inform{"imdb":"6"}
    - action_best_choices_of_movie
    - action_restart



## Path 7
*  movie_suggestion{"themecolor":"black and white"}
    - utter_what_genre
* inform{"genre":"Drama"}
    - action_best_choices_of_movie
    - action_restart

    
 
