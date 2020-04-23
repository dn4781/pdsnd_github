import time
import calendar
from datetime import timedelta
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY_LIST = ['chicago', 'new york', 'washington']

MONTH_LIST = ['all', 'january', 'february', 'march', 'april', 'may','june']

DAY_LIST = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():

#def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
#while True:
    while True:
        city = input("What city would you like to research: Chicago, New York or Washington? \n").lower()
        if city in CITY_LIST:
            print(f'You selected {city.upper()}')
            break
        else:
            print("Your selection is invalid.  Please try again.  (Chicago, New York or Washington)")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("What month would you like to research: All or January, February, March, April, May, June? \n").lower()
        if month in MONTH_LIST:
            print(f'You selected {month.upper()}')
            break
        else:
            print("Your selection is invalid.  Please try again.  (All or January, February, March, April, May, June)")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("What day of the week would you like to research: ALL or Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday? \n").lower()
        if day in DAY_LIST:
            print(f'You selected \n City:\t{city.upper()} \n Month:\t{month.upper()} \n Days:\t{day.upper()}')
            break
        else:
            print("Your selection is invalid.  Please try again.  (All or Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day'] = df['Start Time'].dt.day
    df['date'] = df['Start Time'].dt.date
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()

    print(f'Most popular month to ride in\t\t{city}:\t', calendar.month_name[popular_month])

    # display the most common day of week
    popular_day_of_the_week = df['day_of_week'].value_counts().idxmax()

    print(f'Most popular day of the week to ride in\t{city}:\t', popular_day_of_the_week)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].value_counts().idxmax()

    print(f'Most popular hour to ride in\t\t{city}:\t', popular_hour)

    # find most popular day
    popular_day = df['day'].value_counts().idxmax()

    print(f'Most popular day to ride in\t\t{city}:\t', popular_day)

    # find most popular date
    popular_date = df['date'].value_counts().idxmax()

    print(f'Most popular date to ride in\t\t{city}:\t', popular_date)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_starting_point = df['Start Station'].value_counts().idxmax()

    print('Most popular station to start a ride:\t', [popular_starting_point])

    # display most commonly used end station
    popular_ending_point = df['End Station'].value_counts().idxmax()

    print('Most popular station to end a ride:\t', [popular_ending_point])

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " / " + df['End Station']
    popular_trip = df['trip'].value_counts().idxmax()

    print('Most popular station to end a ride:\t', [popular_trip])



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_travel_minutes = int(total_travel_time/60)
    total_travel_hours = int(total_travel_time/3600)
    total_travel_days = int(total_travel_time/86400)
    total_travel = "{:0>8}".format(str(timedelta(seconds=total_travel_time)))
    mean_travel_time = int(df['Trip Duration'].mean()/60)

    print('Total minutes of travel:\t\t', [total_travel_minutes])
    print('Total hours of travel:\t\t\t', [total_travel_hours])
    print('Total days of travel:\t\t\t', [total_travel_days])
    print('Total travel:\t\t\t\t', [total_travel])

    # display mean travel time
    print("\nMean time minutes of Travel:\t\t", [mean_travel_time])

    # display longest trip Duration
    longest_rental_duration = df['Trip Duration'].max()
    longest_rental_duration_minutes = int(df['Trip Duration'].max()/60)
    longest_rental_duration_hours = int(df['Trip Duration'].max()/3600)
    #longest_rental_duration_days = "{:0>8}".format(str(timedelta(seconds=longest_rental_duration)))

    print('\nLongest rental duration in seconds:\t', [longest_rental_duration])
    print('Longest rental duration in minutes:\t', [longest_rental_duration_minutes])
    print('Longest rental duration in hours:\t', [longest_rental_duration_hours])
    #print('Longest rental duration in days/hours/minutes/seconds:', longest_rental_duration_days)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #exclude Washington from user types since it has no user type dataframe
    if city == 'washington':
        print("Sorry, but we do not have user data for Washington.")
    else:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('USER TYPE COUNTS: \n', [user_types])

        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print('\n USER GENDER COUNTS: \n', [gender_types])

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        print('\nThe earliest Birth Year is:\t\t', earliest_birth_year)

        most_recent_birth_year = int(df['Birth Year'].max())
        print('The most recent Birth Year is:\t\t', most_recent_birth_year)

        most_common_birth_year = int(df['Birth Year'].value_counts().idxmax())
        print('The most common Birth Year is:\t\t', most_common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data on bikeshare users."""

    print('\nCalculating Raw Data...\n')
    start_time = time.time()

    #print 5 rows of data at a time per request
    idx = 0
    while True:
        more_data = input('\nWould you like to see 5 rows of raw data? Yes or No: ').lower()
        if more_data == 'yes':
            print(df.iloc[idx:idx+5, :])
            idx += 5
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city.title())
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
