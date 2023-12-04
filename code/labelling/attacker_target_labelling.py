"""
This code labels users in a thread as attackers, targets, or neither.
An attacker is defined as a user who has contributed a comment that has been labelled as "is_attack"=1.
A target is defined as a user who has contributed to the conversation within a 14 day window prior to an attack.
"""

import pandas as pd

# Loading the 2014-2015 thread-wise dataset
df = pd.read_csv('pages_with_at_least_two_threads_2014_2015.tsv', delimiter='\t')

# Sorting comments by timestamp to obtain the order of comments in each thread
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by=['page_id', 'thread', 'timestamp'])

output_data = []

# For each thread on the page, we characterize each user as an attacker, target, or neither
# If an individual is both attacked and targeted in a thread, we treat them as an attacker only.
for page_id in df['page_id'].unique():
    page_data = df[df['page_id'] == page_id]

    for thread in page_data['thread'].unique():
        thread_data = page_data[page_data['thread'] == thread]

        attackers = {}
        targets = {}

        # Iterate through the comments in the thread
        for idx, row in thread_data.iterrows():
            # If the user_id is missing, skip
            if pd.isna(row['user_id']):
                continue

            # User IDs for comments with "is_attack"=1 are labelled as attackers
            if row['is_attack'] == 1:
                attacker_user_id = row['user_id']
                attackers[attacker_user_id] = True

                # Finding 14-day window before the attack
                attack_timestamp = row['timestamp']
                window_start = attack_timestamp - pd.Timedelta(days=14)

                # Labelling users who commented within this window as targets
                window_comments = thread_data[(thread_data['timestamp'] >= window_start) & (thread_data['timestamp'] < attack_timestamp)]
                for _, comment_row in window_comments.iterrows():
                    target_user_id = comment_row['user_id']
                    if target_user_id not in attackers and not pd.isna(target_user_id):
                        targets[target_user_id] = True


        # Combining attackers and targets to the final user ID list
        for user_id in set(list(attackers.keys()) + list(targets.keys())):
            output_data.append({
                'page_id': page_id,
                'thread': thread,
                'user_id': user_id,
                'is_attacker': int(user_id in attackers),
                'is_target': int(user_id in targets and user_id not in attackers)
            })

# Writing output to csv file
output_df = pd.DataFrame(output_data)
output_csv_path = 'threadwise_attack_target_analysis.csv'
output_df.to_csv(output_csv_path, index=False)
