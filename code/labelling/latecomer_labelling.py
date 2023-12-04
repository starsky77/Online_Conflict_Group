"""
This code performs labelling of threads as having latecomers or not.
A latecomer is defined as a user who joins the conversation after the conflict has ended.
"""

import pandas as pd

# Loading the 2014-2015 thread-wise dataset
df = pd.read_csv('pages_with_at_least_two_threads_2014_2015.tsv', delimiter='\t')

# Sorting comments by timestamp to obtain the order of comments in each thread
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by=['page_id', 'thread', 'timestamp'])

output_data = []

# For each thread, we check if there is a comment made by a new user after the conflict has ended (latecomer)
for page_id in df['page_id'].unique():
    page_data = df[df['page_id'] == page_id]

    for thread in page_data['thread'].unique():
        thread_data = page_data[page_data['thread'] == thread]

        # Finding the end of the conflict in the thread
        last_attack_idx = thread_data[thread_data['is_attack'] == 1].last_valid_index()

        # If there was no attack in the thread, skip since there cannot be a latecomer
        if last_attack_idx is None:
            continue

        # Getting the set of users involved in the conversation before the end of the conflict in the thread
        users_involved = set(thread_data.loc[:last_attack_idx, 'user_id'])

        # Checking for comments made after the last attack comment by newcomers
        late_comments = thread_data.loc[last_attack_idx + 1:]
        latecomer_exists = any(user not in users_involved for user in late_comments['user_id'])

        # Storing the thread-wise latecomer analysis
        output_data.append({
            'page_id': page_id,
            'page_title': page_data['page_title'].iloc[0],
            'thread': thread,
            'latecomer': int(latecomer_exists)  # 1 if latecomer exists, 0 otherwise
        })

output_df = pd.DataFrame(output_data)
output_df.to_csv('threadwise_latecomers_analysis.csv', index=False)
