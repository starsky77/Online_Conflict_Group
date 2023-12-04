"""
This code prepares a reconstruction of threads in a text file for qualitative analysis.
It checks for prior statements to an attack as well as the response and prints each comment in the thread along with the user ID.
"""

import pandas as pd

# Loading the 2014-2015 thread-wise dataset
df = pd.read_csv('pages_with_at_least_two_threads_2014_2015.tsv', delimiter='\t')

# Sorting comments by timestamp to obtain the order of comments in each thread
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by=['page_id', 'timestamp'])

# Replacing the "NEWLINE_TOKEN" and double quotes in the comments for enhanced readability
df['comment'] = df['comment'].str.replace("NEWLINE", " ").str.replace("\"", "")

# Filtering pages to exclude page_id 503055 since this is the MAIN page and has a lot of comments that are not part of any thread, making qualitative analysis difficult
filtered_df = df[(df['page_id'] != 5030553)]

# For each page, we check the threads for comments that are labelled as "is_attack". For these comments, we reconstruct the conversation, including some history and the response.
with open('threads_2014_2015_formatted_final.txt', 'w') as file:
    for page_id in filtered_df['page_id'].unique()[:10000]:  # Limiting to first 10000 for ease of analysis
        page_data = filtered_df[filtered_df['page_id'] == page_id]

        # Checking for attacks on the page
        if page_data['is_attack'].sum() > 0:

            for idx, row in page_data.iterrows():
                if row['is_attack'] == 1:
                    prev_idx = idx - 1
                    if prev_idx in page_data.index:
                        previous_comment = page_data.loc[prev_idx, 'comment']
                        previous_user = page_data.loc[prev_idx, 'user_id']

                        # Finding earlier comments (2 before the conflict, which is idx - 2)
                        beforethat_idx = idx - 2
                        earlier_comment = page_data.loc[beforethat_idx, 'comment'] if beforethat_idx in page_data.index else '[None]'
                        earlier_user = page_data.loc[beforethat_idx, 'user_id'] if beforethat_idx in page_data.index else '[None]'

                        # Finding previous comments (1 before the conflict, which is idx - 1)
                        previous_idx = idx - 1
                        previous_comment = page_data.loc[previous_idx, 'comment'] if previous_idx in page_data.index else '[None]'
                        previous_user = page_data.loc[previous_idx, 'user_id'] if previous_idx in page_data.index else '[None]'

                        # Attack comment (which is idx)
                        attack_comment = row['comment']
                        attack_user = row['user_id']  # Replace 'user_id' with the appropriate column name for user IDs

                        # Following comment to attack or response comment (which is idx + 1)
                        next_idx = idx + 1
                        response_comment = page_data.loc[next_idx, 'comment'] if next_idx in page_data.index else '[None]'
                        response_user = page_data.loc[next_idx, 'user_id'] if next_idx in page_data.index else '[None]'

                        # Writing the earlier, previous, attack, and response comments along with user IDs to the file
                        file.write(f"Earlier Comment (User {earlier_user}): {earlier_comment}\n")
                        file.write(f"Previous Comment (User {previous_user}): {previous_comment}\n")
                        file.write(f"Attack Comment (User {attack_user}): {attack_comment}\n")
                        file.write(f"Response Comment (User {response_user}): {response_comment}\n")
                        file.write('-------------------\n')

            # Writing pageID and page title to label the thread snippets
            file.write(f"Page ID: {page_id}\n")
            file.write(f"Page Title: {page_data['page_title'].iloc[0]}\n")
            file.write('===================\n')
