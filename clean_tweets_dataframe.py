
import pandas as pd
import numpy as np
import string
#python library
class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        return self.df
 
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(
            self.df["created_at"], errors="coerce")
        
        return self.df

        df = df[df['created_at'] >= '2020-12-31' ]
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
       #convert columns like polarity, subjectivity, retweet_count
        #favorite_count etc to numbers
       
        df["polarity"] = pd.to_numeric(df["polarity"])
        df["subjectivity"] = pd.to_numeric(df["subjectivity"])
        df["favorite_count"] = pd.to_numeric(df["favorit_count"])
        df["followers_count"] = pd.to_numeric(df["followers_count"])
        df["retweet_count"] = pd.to_numeric(df["retweet_count"])
        df["friends_count"] = pd.to_numeric(df["friends_count"])
        
        return df
   
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        index_name= self.df[self.df['lang']!= 'en'].index
        self.df.drop(index_name, inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        
        return self.df
    def preproce_tweet(self, df:pd.DataFrame)->pd.DataFrame:
        
        self.df["full_text"] = self.df["full_text"].str.lower()      
        self.df["full_text"] = self.df["full_text"].str.replace("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", " ")             
        self.df["full_text"] = self.df["full_text"].astype(str).apply(lambda x: x.encode('latin-1', 'ignore').decode('latin-1'))      
        self.df["full_text"] = self.df["full_text"].str.replace('(\@w+.*?', " ")        
        self.df["full_text"] = self.df["full_text"].apply(lambda x: " ".join([i for i in x if i not in string.punctuation]))        
        stopword_list = stopwords.words('english')
        self.df["full_text"] = self.df["full_text"].apply(lambda x: " ".join([w for w in x.split() if w not in (stopword_list)]))
 
        
        self.df.drop(self.df[self.df["full_text"]== " "].index, inplace= True)

        return self.df
    def fill_nullvalues(self):
        self.df['possibly_sensitive'] = self.df['possibly_sensitive'].fillna(
            False)
        self.df['created_at'] = self.df['created_at'].fillna(" ")
        self.df['place'] = self.df['location'].fillna(" ")
        self.df['retweet_count'] = self.df['retweet_count'].fillna(0)
        self.df['favorite_count'] = self.df['favorite_count'].fillna(0)
        self.df['lang'] = self.df['lang'].fillna(" ")
        self.df['full_text'] = self.df['full_text'].fillna(" ")
        self.df['source'] = self.df['source'].fillna(" ")

        return self.df
#add main function of class
if __name__ == "__main__":
    cleaned_df=pd.read_csv("data/processed_tweet_data.csv")
    Clean_Tweets = Clean_Tweets(cleaned_df)
    cleaned_df = Clean_Tweets.drop_duplicate(cleaned_df)
    cleaned_df = Clean_Tweets.remove_non_english_tweets(cleaned_df)
    cleaned_df = Clean_Tweets.convert_to_datetime(cleaned_df)
    cleaned_df = Clean_Tweets.drop_unwanted_column(cleaned_df)
    cleaned_df = Clean_Tweets.convert_to_numbers(cleaned_df)
    #print the first five row from cleaned tweet
    print(cleaned_df["polarity"].head())


    cleaned_df.to_csv("data/clean_processed_tweet.csv")
    print("Great File is successfully save!") 
