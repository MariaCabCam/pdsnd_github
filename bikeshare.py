import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Define a constant for city prompt
CITY_PROMPT = 'Please, enter the city you would like to see data for (Chicago, New York City, Washington): '

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input(CITY_PROMPT).lower()
        if city in CITY_DATA:
            break
        else:
            print('The name entered is not a valid city name. Please, try again with one of these city names: Chicago, New York City, Washington.')

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Please, enter the month from January to June you would like to see data for (you can also select "all"!): ').lower()
        if month in months:
            break
        else:
            print ('The month entered is not a valid one. Please, try again with one of these or typing "all": January, February, March, April, May, June')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Please, enter the day of the week you would like to see data for (you can also select "all"!): ').lower()
        if day in days:
            break
        else:
            print('The day of the week entered is not a valid one. Please, try again with one of these or typing "all": Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')

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
    
    # Load data file into a dataframe with all data in CITY_DATA dictionary, handling errors due to missing input files
    try:
        df = pd.read_csv(CITY_DATA[city])
    except:
            print(f'Error: The data file for {city} was not found.')
            return None

    # Convert Start Time into the correct format (datetime) to process dates and times
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time and create a new column for each
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month, if a month is selected
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # Filter by day of week, if a day of the week is selected
    if day != 'all':
        
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Raise an exception if there is no data for the selected city-month-date combination
    if df.empty:
        raise ValueError(f'Oops, there is no data available for the selected city {city}, on the selected dates ({month}, {day}).')
   
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Create a dictionary for month names
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    
    # Display the most popular month of usage
    most_popular_month = month_names[df['month'].mode()[0]]
    print(f'The most popular month of the year for travelling is: {most_popular_month}')

    # Display the most popular day of week of usage
    most_popular_day = df['day_of_week'].mode()[0]
    print(f'The most popular day of the week for travelling is: {most_popular_day}')

    # Display the most common start hour of usage
    most_popular_hour = df['hour'].mode()[0]
    print(f'The most popular hour of the day for travelling is: {most_popular_hour}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {most_common_start_station}')

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is: {most_common_end_station}')

    # Display most frequent combination of start station and end station trip
    most_common_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print(f'The most popular trip starts and ends in these stations: {most_common_trip}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time (units = seconds)
    total_travel_time = df['Trip Duration'].sum()
        
    # Convert total travel time to housrs, minutes and seconds
    total_hours = int(total_travel_time // 3600)
    total_minutes = int((total_travel_time % 3600) // 60)
    total_seconds = int(total_travel_time % 60)
    
    print(f'Total travel time is {total_hours} hours, {total_minutes} minutes and {total_seconds} seconds.')

    # Display mean travel time (units = seconds)
    mean_travel_time = df['Trip Duration'].mean()
    
    # Convert mean travel time to housrs, minutes and seconds
    mean_hours = int(mean_travel_time // 3600)
    mean_minutes = int((mean_travel_time % 3600) // 60)
    mean_seconds = int(mean_travel_time % 60)

    print(f'Mean travel time is {mean_hours} hours, {mean_minutes} minutes and {mean_seconds} seconds.')
    
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types (including Dependent)
    user_types = df['User Type'].value_counts()
    print(f'This is the number of users of each type:\n' + user_types.to_string(index=True) + '\n')
    
    # Display counts of gender (currently, only available for Chicago and New York City, but code projected to support gender data for Washington in the future)    
    if 'Gender' in df.columns:
       df['Gender'] = df['Gender'].fillna('No data')   # Fill in 'Gender' column with 'No Data' for the NaN values
       gender_counts = df['Gender'].value_counts()
       ordered_gender_counts = pd.Series({'Male': gender_counts.get('Male', 0),
                                          'Female': gender_counts.get('Female', 0),
                                          'No data': gender_counts.get('No data', 0)
                                         })
       print(f'Number of users per gender:\n' + ordered_gender_counts.to_string(index=True) + '\n')
    else:
       print('Gender data are not available.')

    # Display earliest, most recent, and most common year of birth in year format (currently, only available for Chicago and New York City, but code projected to support gender data for Washington in the future) 
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        count_birth_year_not_null = df['Birth Year'].count() #NaN values not counted by .count()
        total_count_birth_year = len(df['Birth Year'])
        percentage_birth_year_available = (count_birth_year_not_null / total_count_birth_year)*100
        percentage_birth_year_available = int(round(percentage_birth_year_available))
        print(f'Earliest year of birth: {int(earliest_birth_year)}')
        print(f'Most recent year of birth: {int(most_recent_birth_year)}')
        print(f'Most common year of birth: {int(most_common_birth_year)}')
        print(f'Birth year data available for {percentage_birth_year_available}% of users in this city for the selected dates (which is {count_birth_year_not_null} out of {total_count_birth_year} users).')
    else:
        print('Birth year data are not available.')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        try:
            df = load_data(city, month, day)
            
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
                            
            # Ask the user, if individual trip data should be shown and, in case of positive answer, show the first 5 raw data trips and loop to ask for additional data to show, if there are more trips available                          
            # Define the specific columns to display
            columns_to_display = ['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'User Type', 'Gender', 'Birth Year']
                
            # Define the start of the index to display the trips    
            individual_trip_data_index = 0 
            while True:
                individual_trip_data = input('Would you like to see individual trip data? (yes/no): ').lower()
                if individual_trip_data == 'yes':
                    if individual_trip_data_index < len(df):
                        print ('\nShowing 5 individual trips for the selected city and dates:')
                        print(df[columns_to_display].iloc[individual_trip_data_index: individual_trip_data_index + 5])
                        individual_trip_data_index += 5
                    else:
                        print('That was all! There are no more trips to show.')
                        break
                else:
                    break
            restart = input('\nWould you like to restart and see additional data? (yes/no).\n')
            if restart.lower() != 'yes':
                break
        
        except:            
            print('Oops, there is no data available for the selected city, on the selected period. Would you like to try again? (yes/no)')
            restart = input().lower()
            if restart != 'yes':
                break       


if __name__ == "__main__":
	main()
