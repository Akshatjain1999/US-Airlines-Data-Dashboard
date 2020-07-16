import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment Analysis on Tweets about US Airlines ✈️")
st.sidebar.title("Sentiment Analysis on Tweets about US Airlines ✈️")
st.markdown("### By [Akshat Jain](https://github.com/akshatjain1999)")
st.sidebar.markdown("By [Akshat Jain](https://github.com/akshatjain1999)")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv("tweets.csv")
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data()

# Show random tweet
st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
if not st.sidebar.checkbox("Hide", True, key='0'):
    st.sidebar.subheader(f"Random {random_tweet.capitalize()} Tweet")
    st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])

# Number of tweets by sentiment
st.sidebar.subheader("Number of Tweets by Sentiment")
select = st.sidebar.selectbox("Visualization Type", ["Bar Plot", "Pie Chart"])
sentiment_count = data["airline_sentiment"].value_counts()
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets":sentiment_count.values})
if not st.sidebar.checkbox("Hide", True, key='1'):
    st.subheader("Number of Tweets by Sentiment")
    if select == "Bar Plot":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets")
        st.plotly_chart(fig)
    if select == "Pie Chart":
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are users tweeting from ?")
hour = st.sidebar.slider("Hour of a day",min_value=0,max_value=23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close",True,key='1'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets betweet %i:00 and %i:00 "%(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show Raw Data",False):
        st.write(modified_data)

choice = st.sidebar.multiselect("Pick airlines",("US Airways","United",'American',"Southwest",'Delta','Virgin America'),key=0)
if len(choice)>0 :
    choice_data = data[data.airline.isin(choice)] 
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display Word cloud for what sentiment?",('positive','neutral','negative'))

if not st.sidebar.checkbox("Close",True,key='3'):
    st.header("Word Cloud for Sentiment {} ".format(word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = " ".join(df['text'])
    processed_words = " ".join(word for word in words.split() if 'http' not in word and not word.startswith('@') and word !='RT')
    wordcloud = WordCloud(stopwords=STOPWORDS,background_color='white',height=640,width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()