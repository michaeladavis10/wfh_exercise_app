# COVID-19 WFH Between Meeting App
# author: Michael A Davis

# How this works
'''
Count number of days since start of quarantine
For every meeting, choose one exercise (at random?)
Do <the number of days since start of quarantine> reps of that exercise before your next meeting
Keep track of what you've done that day (use a CSV initially, then DB)
'''

# Intiialization
from random import choice
import os
import pandas as pd

from wfh_exercises import exercises

# Denote user (will later get from auth)
user_email = 'test@gmail.com'

# Filenames for later
dir_path = os.path.dirname(os.path.realpath(__file__))
completed_activities_file = os.path.join(dir_path, 'completed_activities.csv')

# Days since start of quarantine
quarantine_start_date = pd.Timestamp(2020,3,15)
today_date = pd.Timestamp.today()
days_since_start = (today_date - quarantine_start_date).days

# Check to see if user has already done exercises that day, and what to choose next
'''
Choose a group - first at random, then by fewest times done
Choose an exercise in that group - first at random, then by fewest times done
This should be done by picking an exerise group first
That way there's a 'full-body-workout' going on, rather than which group has most variations
Edge case: if a user does less than the number of groups, they'll get most complete 'full-body' workout
Edge case: if a user does tons of exercises, they'll eventually run out of new options and start repeating
TODO: This gets moved over to a database type solution
This relies on the uniqueness of names
'''


def load_previous_activity(data_source):
    if os.path.exists(completed_activities_file):
        df = pd.read_csv(data_source, header=0, index_col=False, sep='|', parse_dates=[1], infer_datetime_format=True)
    else:
        df = None
    return df

def get_user_activity_on_date(activity_df, user_email, user_date):
    # TODO: convert to class? so this doesn't have to do None check
    if activity_df is not None:
        df = activity_df[(activity_df.email == user_email) & (activity_df.ts.dt.date == user_date)]
        if df.shape[0] >= 1:
            return df
        else:
            return None
    else:
        return None

def show_previous_activity(user_df, groupby_level, where_cond = None):
    # TODO: convert to class? so this doesn't have to do None check
    if user_df is not None:
        if where_cond is None:
            a = pd.DataFrame(user_df.groupby([groupby_level]).size())
        else:
            a = pd.DataFrame(user_df[eval('user_df' + where_cond)].groupby([groupby_level]).size())
        a.reset_index(drop=False)
        a.rename(columns = {0:'count'}, inplace=True)
        print(a)
        print()
        return a
    else:
        return None

def determine_possible_choices(all_available_choices, previous_activity = None):
    if previous_activity is not None:
        have_not_done_yet = set(all_available_choices) - set(previous_activity.index)
        if len(have_not_done_yet) >= 1:
            possible_choices = list(have_not_done_yet)
        else:
            possible_choices = list(previous_activity[previous_activity == previous_activity.min()].dropna().index)
    else:
        possible_choices = list(all_available_choices)
    return possible_choices

def write_to_history(user_email, exercise_group, exercise, reps):
    '''
    Need to record the user, time completed, exercise, and reps
    When reading back in, truncate time to date & use unique lookup in reps
    '''
    # Record to write
    row = [[user_email, pd.Timestamp.now(), exercise_group, exercise, reps]]
    df = pd.DataFrame(row, columns = ['email','ts','exercise_group','exercise','reps'])

    # Check if file exists
    # If it does not - create it with headers
    # If it does - append
    try:
        if os.path.exists(completed_activities_file):
            df.to_csv(completed_activities_file, mode='a', header=False, index=False, sep='|')
        else:
            df.to_csv(completed_activities_file, mode='w', header=True, index=False, sep='|')
    except Exception as e:
        print(e)
    return None


# Load history
previous_activity = load_previous_activity(completed_activities_file)
user_activity_today = get_user_activity_on_date(previous_activity, user_email, today_date)

# Choose the group
exercise_group_df = show_previous_activity(user_activity_today, 'exercise_group')
groups_to_choose_from = determine_possible_choices(exercises.keys(), exercise_group_df)
chosen_exercise_group = choice(groups_to_choose_from)
print(f'Exercise group for this round: {chosen_exercise_group}\n')

# Choose the exercise
exercise_df = show_previous_activity(user_activity_today, 'exercise', "['exercise_group'] == chosen_exercise_group")
exercises_to_choose_from = determine_possible_choices(exercises[chosen_exercise_group], exercise_df)
chosen_exercise = choice(exercises_to_choose_from)
print(f'Exercise for this round: {chosen_exercise}\n')

# Print back to user
print(f'\nToday is day {days_since_start} of quarantine.  Do {days_since_start} reps of {chosen_exercise}.  Go! \n\n')

# Have user mark completion
exercise_start_time = pd.Timestamp.now()
print('...Hit Enter when done...')
x = input()
exercise_end_time = pd.Timestamp.now()
time_to_complete = (exercise_end_time - exercise_start_time).seconds

# Keep track of what you've done
write_to_history(user_email, chosen_exercise_group, chosen_exercise, days_since_start)
print(f'Good work! It took you {time_to_complete} seconds to complete this round!\n')
