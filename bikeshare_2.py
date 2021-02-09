import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n')
    print('\tHello! Let\'s explore some US bikeshare data!')
    print('\n')
    print('\t***  If you ever want to exit, hit Control-C   ***')
    print('\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ("chicago", "new york city", "washington")
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    while True:
        city = input('\tPlease enter a city - Chicago, New York City or Washington\n')
        if city.lower() not in cities:
            print('\tAww, sorry ', city, 'is not a valid city.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\tPlease enter a month from January to June, or the word all\n')
        if month.lower() not in months:
            print('\tWoah, sorry ', month, 'is not a valid month.')
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\tPlease enter a day as in Monday or the word all\n')
        if day.lower() not in days:
            print('\tOops, sorry ', day, 'is not a valid day.')
            continue
        else:
            break


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
    
    filename = CITY_DATA[city.lower()]
    df = pd.read_csv(f'{filename}')


    # convert the Start Time column to datetime
    # need to convert it to this so we can then extract the hour, month and day of the week
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    month = month.lower()
    day = day.lower()

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

def raw_data_it_is(df):

    """Displays raw data statistics."""

    print(df.head(5))
    more = 0
    while True:
        print('\n')
        want_more_raw_data = input('\tWould you like to view more raw data? Enter yes.\n')
        if want_more_raw_data.lower() == 'yes':
            more = more + 5
            print(df.iloc[more:more+5])
        else:
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    if common_month == 1:
            monthString = "January";
    elif common_month == 2:
            monthString = "February";
    elif common_month == 3:
            monthString = "March";
    elif common_month == 4:
            monthString = "April";
    elif common_month == 5:
            monthString = "May";
    elif common_month == 6:
            monthString = "June";
    else:
        print('\Oh no, that month is not in our files\n')


    print('\nThe most common month is:', monthString)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is:', common_day)


    # display the most common start hour - make sure this isn't the most common start time! ;-)
    # so get the hour field from start time similiar to how we got day

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most common Start Hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_value = df['Start Station'].value_counts()[0]
    common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: ', common_start_station)
    print('\nAnd it has been visited', start_station_value, 'times!')


    # display most commonly used end station
    end_station_value = df['End Station'].value_counts()[0]
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most common End Station is: ', common_end_station)
    print('\nAnd it has been visted', end_station_value, 'times!')

    
    # display the top three most frequent combination of start station and end station trip
    #combo = df.groupby(['Start Station','End Station']).size().nlargest(3)
    combo = df.groupby(['Start Station','End Station']).size().nlargest(3).reset_index(name='Combination count')



    print('\nThe top three frequent combinations of Start Station and End Station trips are: ')
    print('\n', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    print('\nThe total amount of travel time in seconds was: ', total_trip)

    # display mean travel time
    mean_trip = df['Trip Duration'].mean()
    print('\nThe total mean travel time in seconds was: ', mean_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_types(df):
    """Displays user types only because everyone likes user type info."""

    print('\nCalculating User Types...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser types are', user_types)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating Other User Stats...\n')
    start_time = time.time()

    # Display counts of gender
    gender_types = df['Gender'].value_counts()
    print('\nGenders counts are:\n', gender_types)


    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']

    # earliest birth year
    earliest_birth_year = birth_year.min()
    formatted_eby = "{:.0f}".format(earliest_birth_year)
    print('\nThe earliest birth year was: ', formatted_eby)

    # most recent birth year
    most_recent_birth_year = birth_year.max()
    formatted_mrby = "{:.0f}".format(most_recent_birth_year)
    print('\nThe most recent birth year was: ', formatted_mrby)

    # most common birth year
    most_common_birth_year = birth_year.value_counts().idxmax()
    formatted_mcby = "{:.0f}".format(most_common_birth_year)
    print('\nThe most common birth year was: ', formatted_mcby)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        print('\tOK here are some nice stats for you')

        print('-'*40)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_types(df)
        if city.lower() != 'washington':
            user_stats(df)

        raw_data = input('\n\tIf you would like to see raw data, enter yes.\n')
        if raw_data.lower() == 'yes':
            print('\t----- yeehaw raw data -----\n')
            raw_data_it_is(df)
        
        restart = input('\tWould you like to restart? Enter yes.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
