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
from datetime import date
from datetime import datetime
from random import choice

# Days since start of quarantine
quarantine_start_date = date(2020,3,15)
today_date = date.today()
days_since_start = (today_date - quarantine_start_date).days


# Exerises
'''
All values need to be unique
Naming convention - have no spaces, uses '-' between words
'''
exercises = dict()
exercises['push'] = ['pushups','old-spice-push-ups','triangle-push-ups']
exercises['pull'] = ['dips','pullups']
exercises['squat'] = ['squat','lunge','pistol']
exercises['core'] = ['v-up','russian-twist']

# Pick an exercise
'''
This should be done by picking an exerise group first
That way there's a 'full-body-workout' going on, rather than which group has most variations
'''
chosen_exercise_group = choice(list(exercises.keys()))
chosen_exercise = choice(exercises[chosen_exercise_group])

# Print back to user
print_string = f'\nToday is day {days_since_start} of quarantine.  Do {days_since_start} reps of {chosen_exercise}.\n'
print(print_string)
