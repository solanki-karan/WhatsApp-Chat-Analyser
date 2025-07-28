import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    #fetching unique users
    user_list = (df['user'].unique().tolist())
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis wrt ', user_list)

    if st.sidebar.button("Show Analysis"):
        
        #fetching stats
        num_messages, num_words, num_media_msg, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Files")
            st.title(num_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(num_links)




        #fetching monthly timeline
        timeline = helper.get_monthly_timeline(selected_user, df)
        fig, ax = plt.subplots();

        ax.plot(timeline['time'], timeline['message'], color = 'violet')
        plt.xticks(rotation = 'vertical')
        st.title("Monthly Timeline")
        st.pyplot(fig)







        #fetch daily timeline
        timeline = helper.get_daily_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(timeline['only_date'], timeline['message'], color = 'black')
        plt.xticks(rotation = 'vertical')
        st.title("Daily Timeline")
        st.pyplot(fig)






        #Activity Graph
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        busy_day, busy_month = helper.activity_map(selected_user, df)

        with col1:
            st.header("Most Busy Day")
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'brown')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)


        with col2:
            st.header("Most Busy Month")
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        



        #Weekly Activity Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)





        #fetching busiest user
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.busiest_users(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)




        #WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)




        #Most common words
        st.title("Most Frequent Words")
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)




        #Emoji analysis
        emoji_df = helper.emoji_stats(selected_user, df)
        

        st.title("Top 10 Emojis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots();
            ax.pie(emoji_df['Frequency'], autopct="%0.2f")
            st.pyplot(fig)



