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

# Denote user (will later get from auth)
user_email = 'test@gmail.com'

# Filenames for later
dir_path = os.path.dirname(os.path.realpath(__file__))
completed_activities_file = os.path.join(dir_path, 'completed_activities.csv')

# Days since start of quarantine
quarantine_start_date = pd.Timestamp(2020,3,15)
today_date = pd.Timestamp.today()
days_since_start = (today_date - quarantine_start_date).days

# Exerises
'''
All values need to be unique
Naming convention is no spaces, uses '-' between words
'''
exercises = dict()
exercises['push'] = ['pushups','old-spice-push-ups','triangle-push-ups']
exercises['pull'] = ['dips','pullups']
exercises['squat'] = ['squat','lunge','pistol']
exercises['core'] = ['v-up','russian-twist']

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
user_active_today = False
if os.path.exists(completed_activities_file):
    completed_df = pd.read_csv(completed_activities_file, header=0, index_col=False, sep='|', parse_dates=[1], infer_datetime_format=True)
    user_today_df = completed_df[(completed_df.email == user_email) & (completed_df.ts.dt.date == today_date)]
    if user_today_df.shape[0] >= 1:
        user_active_today = True

# Find the 'groups' of those exercises and find the list of possible groups to choose from for the next iteration
if user_active_today:
    # TODO: this needs cleaning up
    a = pd.DataFrame(user_today_df.groupby(['exercise_group']).size())
    a.reset_index(drop=False)
    a.rename(columns = {0:'counts'}, inplace=True)
    have_not_done_yet = set(exercises.keys()) - set(a.index)
    print(a)
    print()
    if len(have_not_done_yet) >= 1:
        groups_to_choose_from = list(have_not_done_yet)
    else:
        min_groups = list(a[a == a.min()].dropna().index)
        groups_to_choose_from = min_groups
else:
    groups_to_choose_from = list(exercises.keys())

# Choose the next group
chosen_exercise_group = choice(groups_to_choose_from)
print(chosen_exercise_group)
print()

# Pick an exercise from that group - but make sure it hasn't already been done
if user_active_today:
    # TODO: this needs cleaning up
    a = pd.DataFrame(user_today_df[user_today_df.exercise_group == chosen_exercise_group].groupby(['exercise']).size())
    a.reset_index(drop=False)
    a.rename(columns = {0:'counts'}, inplace=True)
    have_not_done_yet = set(exercises[chosen_exercise_group]) - set(a.index)
    print(a)
    print()
    if len(have_not_done_yet) >= 1:
        exercises_to_choose_from = list(have_not_done_yet)
    else:
        min_groups = list(a[a == a.min()].dropna().index)
        exercises_to_choose_from = min_groups
else:
    exercises_to_choose_from = exercises[chosen_exercise_group]

# Choose the exercise
chosen_exercise = choice(exercises_to_choose_from)
print(chosen_exercise)
print()


# Print back to user
print_string = f'\nToday is day {days_since_start} of quarantine.  Do {days_since_start} reps of {chosen_exercise}.\n'
print(print_string)

# Keep track of what you've done
'''
Need to record the user, time done, exercise, and reps
When reading back in, truncate time to date & use unique lookup in reps
'''

# Record to write
row = [[user_email, pd.Timestamp.now(), chosen_exercise_group, chosen_exercise, days_since_start]]
df = pd.DataFrame(row, columns = ['email','ts','exercise_group','exercise','reps'])

# Check if file exists
# If it does not - create it with headers
# If it does - append
if os.path.exists(completed_activities_file):
    df.to_csv(completed_activities_file, mode='a', header=False, index=False, sep='|')
else:
    df.to_csv(completed_activities_file, mode='w', header=True, index=False, sep='|')

# Now read them back in before assigning the next exercise
completed_df = pd.read_csv(completed_activities_file, header=0, index_col=False, sep='|', parse_dates=[1], infer_datetime_format=True)
user_today_df = completed_df[(completed_df.email == user_email) & (completed_df.ts.dt.date == today_date)]
user_today_exercises = list(completed_df.exercise)

print(f'You have already completed {user_today_exercises} today. Good work!')