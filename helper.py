from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):

    df = df[df['user']!='group_notification']

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]



    num_messages = df.shape[0]


        
    words = []
    for message in df['message']:
        words.extend(message.split())



    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]



    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)





def busiest_users(df):

    df = df[df['user']!='group_notification']

    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns = {'index':'user', 'user':'percent'})
    return x,df




def remove_stop_words(message):

    f = open('hinglish_stopwords.txt', 'r')
    stop_words  = f.read()

    words = []

    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)
    
    return " ".join(words)




def create_wordcloud(selected_user, df):

    df = df[df['user']!='group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['message'] = df['message'].apply(remove_stop_words)

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc
    




def most_common_words(selected_user, df):
    
    df = df[df['user']!='group_notification']
    df = df[df['message'] != '<Media omitted>\n']
    df['message'] = df['message'].apply(remove_stop_words)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    for message in df['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df






def emoji_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    df = df[df['user']!='group_notification']

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10)).rename(
    columns = {0: 'Emoji', 1: 'Frequency'})

    return emoji_df






def get_monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline





def get_daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    
    timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return timeline






def activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts(), df['month'].value_counts()



def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message',
    aggfunc = 'count', fill_value = 0)

    return user_heatmap



