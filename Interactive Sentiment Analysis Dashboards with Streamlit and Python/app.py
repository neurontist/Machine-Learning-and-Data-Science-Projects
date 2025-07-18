import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")



# loading data
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('./Tweets.csv')
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['tweet_created'])
    return df

# creating dataframe
df = load_data()

# putting titles and headings
st.title("Sentiment Analysis of Tweets about US Airlines")
st.markdown("This application is a Streamlit dashboard used to analyze sentiments of tweets")

st.sidebar.title("Sentiment Analysis of Tweets")
st.sidebar.markdown("This application is a Streamlit dashboard used to analyze sentiments of tweets")

# randome tweets
st.sidebar.header("show random tweet")
sentiment = st.sidebar.radio('Sentiment',('positive','neutral','negative'))

feedback =  df.query('airline_sentiment == @sentiment')['text'].sample(n=1).iloc[0]
st.sidebar.subheader(feedback)

# number of tweets by sentiment plotting
st.sidebar.header("Number of tweets by sentiment")
sentiment_count = df['airline_sentiment'].value_counts()
# st.write(sentiment_count)
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
if not st.sidebar.checkbox('Hide',True):
    plot_type = st.sidebar.selectbox('Visualization type',['Bar plot','Histogram'])
    if plot_type == 'Bar plot':
        fig = px.pie(sentiment_count,names='Sentiment',values='Tweets')
        st.plotly_chart(fig)
    else:
        fig = px.bar(sentiment_count,x='Sentiment',y='Tweets')
        st.plotly_chart(fig)

# World map
st.sidebar.header("When and where are users tweeting from?")

if not st.sidebar.checkbox('Close',True):
    hour = st.sidebar.slider('Hour to look at',0,23)
    hour_choice = df[df['Time'].dt.hour== hour]

    st.header("Tweet locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00"%(len(hour_choice),hour,(hour+1)%24))
    st.map(hour_choice)


# breakdown airline by sentiment

st.sidebar.header("Breakdown airline by sentiment")
choice = st.sidebar.multiselect('Pick airlines',options=['US Airways','United','American','Southwest','Delta','Virgin America'])

if len(choice)>0:
    choice_data = df[df.airline.isin(choice)]
    fig_0 = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',facet_col='airline_sentiment'
                         , labels={'airline_sentiment':'tweets'},
                          height=600, width=800 ,color='airline_sentiment')
    st.plotly_chart(fig_0)

st.sidebar.header("Word Cloud")
sentiment_choice = st.sidebar.radio('Display word cloud for what sentiment?',('positive','neutral','negative'))

if not st.sidebar.checkbox('Close',True,key='3'):
    df = df[df['airline_sentiment']==sentiment_choice]
    words = ' '.join(df['text'])
    processed_words = ' '.join(word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT')
    word_cloud = WordCloud(stopwords=STOPWORDS,background_color='white',height=600,width=800).generate(processed_words)
    plt.imshow(word_cloud)
    plt.axis('off')
    st.pyplot()
