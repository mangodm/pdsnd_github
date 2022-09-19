import time
import pandas as pd
from typing import Tuple, Union

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

VALID_MONTH = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
VALID_DOW = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']
VALID_COLUMNS = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']

def get_filters() -> Tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let\'s explore some US bikeshare data!")

    # Get user input for city (chicago, new york city, washington)
    while True:
        city_message = (
            f"{'-'*50} \n"
            f"There are {len(CITY_DATA)} options available now as below: \n"
            f"{list(CITY_DATA.keys())} \n"
            f"Please enter the city you want to see the data: "
        )
        city = input(city_message).lower()
        if city in CITY_DATA:
            break
        else:
            print(f"Sorry. There is no data for {city} available now. Please try again.")

    # Get user input for month
    while True:
        month_message = (
            f"{'-'*50} \n"
            f"There are {len(VALID_MONTH)} options available now as below: \n"
            f"{VALID_MONTH} \n"
            f"Please enter the month you want to see the data: "
        )
        month = input(month_message)
        if month in VALID_MONTH:
            break
        else:
            print(f"Sorry. There is no data for {month} available now. Please try again.")

    # Get user input for day of week
    while True:
        day_message = (
            f"{'-' * 50} \n"
            f"There are {len(VALID_DOW)} options available now as below: \n"
            f"{VALID_DOW} \n"
            f"Please enter the day you want to see the data: "
        )
        day = input(day_message)
        if day in VALID_DOW:
            break
        else:
            print(f"Sorry. There is no data for {day} available now. Please try again.")

    print('-'*50)
    return city, month, day

def return_mappings(valid_list: object) -> object:
    """
    Returns mappings between an item and an integer value.

    Args:
        (List) valid_list - list of valid values
    Returns:
        (dict) mapped_values - dictionary of <valid element: integer>
    """
    mapping_values_list = [*range(len(valid_list))]
    mapped_values = {valid_list[i]: mapping_values_list[i] for i in range(len(valid_list))}
    return mapped_values

def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (pd.DataFrame) DataFrame containing the city data filtered by month and day
    """

    # Get city data
    df = pd.read_csv(CITY_DATA.get(city))
    # Keep columns only in the list
    df = df[df.columns[df.columns.isin(VALID_COLUMNS)]]
    # Convert `Start Time` column into datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Match month, dow to corresponding integers each
    VALID_MONTH_MAPPED, VALID_DOW_MAPPED = return_mappings(VALID_MONTH), return_mappings(VALID_DOW)
    # Filter data by conditions
    if month == 'all' and day == 'all':
        return df
    elif day == 'all':
        return df[df['Start Time'].dt.month == VALID_MONTH_MAPPED.get(month)]
    elif month == 'all':
        return df[df['Start Time'].dt.dayofweek == VALID_DOW_MAPPED.get(day)]
    else:
        return df[(df['Start Time'].dt.month == VALID_MONTH_MAPPED.get(month)) &
                  (df['Start Time'].dt.dayofweek == VALID_DOW_MAPPED.get(day))]

def calculate_mode(df: pd.DataFrame, field: str, index: str = None) -> Union[int, str, float]:
    """
    Finds the mostly frequently occurring value in the given column.

    Args:
        (pd.DataFrame) df - DataFrame containing the city data filtered
        (str) field - column name where to find the mode value
        (str) index - index, especially used when the field is datetime object
    Returns:
        (int or str or float) - mode value
    """

    # Returns the mode value depending on the field type
    if df[field].dtype == '<M8[ns]':
        return getattr(df[field].dt, index).mode()[0]
    else:
        return df[field].mode()[0]

def time_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (pd.DataFrame) df - DataFrame containing the city data filtered
    """

    print('\n (1) Calculating the most frequent times of travel... \n')
    start_time = time.time()

    # Display the most common month
    print(f"The most common month: {calculate_mode(df, 'Start Time', 'month')}")

    # Display the most common day of week
    print(f"The most common day of week: {calculate_mode(df, 'Start Time', 'dayofweek')}")

    # Display the most common start hour
    print(f"The most common start hour: {calculate_mode(df, 'Start Time', 'hour')}")

    print(f"This took {round(time.time()-start_time, 2)} seconds.")
    print('-'*50)

def stations_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (pd.DataFrame) df - DataFrame containing the city data filtered
    """

    print('\n (2) Calculating the most popular stations and trip... \n')
    start_time = time.time()

    # Display the most commonly used start station
    print(f"The most commonly used start station: {calculate_mode(df, 'Start Station')}")

    # Display the most commonly used end station
    print(f"The most commonly used end station: {calculate_mode(df, 'End Station')}")

    # Display the most frequent combination of start station and end station trip
    frequent_start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start/end station: {frequent_start_end_station}")

    print(f"This took {round(time.time()-start_time, 2)} seconds.")
    print('-'*50)

def trip_duration_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the total and average trip duration.

    Args:
        (pd.DataFrame) df - DataFrame containing the city data filtered
    """

    print('\n (3) Calculating trip duration... \n')
    start_time = time.time()

    # Display total travel time
    print(f"The total travel time: {df['Trip Duration'].sum()}")

    # Display mean travel time
    print(f"The mean travel time: {df['Trip Duration'].mean()}")

    print(f"This took {round(time.time()-start_time, 2)} seconds.")
    print('-'*50)

def user_stats(df: pd.DataFrame, city: str) -> None:
    """
    Displays statistics on bikeshare users.

    Args:
        (pd.DataFrame) df - DataFrame containing the city data filtered
    """

    print('\n (4) Calculating user stats... \n')
    start_time = time.time()

    # Display counts of user types
    print(f"The counts of user types: \n"
          f"{df['User Type'].value_counts()} \n"
          f"{'-'*50}")

    if city == 'washington':
        print(f"This took {round(time.time() - start_time, 2)} seconds.")
        print('-' * 50)
    else:
        # Display counts of gender
        print(f"The counts of gender: \n"
              f"{df['Gender'].value_counts()} \n"
              f"{'-'*50}")

        # Display the earliest, most recent, and most common year of birth
        print(f"The earliest year of birth: {int(df['Birth Year'].min())} \n"
              f"The most recent year of birth: {int(df['Birth Year'].max())} \n"
              f"The most common year of birth: {int(calculate_mode(df, 'Birth Year'))} \n"
              f"{'-'*50}")

        print(f"This took {round(time.time()-start_time, 2)} seconds.")
        print('-'*50)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Run calculations and print them
        time_stats(df)
        stations_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Display 5 lines of raw data if a user wants
        while True:
            show_raw_data = input(f"Do you want to see how the raw data looks like? Enter yes or no: ")
            if show_raw_data == 'yes':
                for i, row in df.iterrows():
                    print(f"Index: {i}")
                    print(f"{row}\n")
                    print('-'*50)
                    if i != 0 and i % 5 == 0:
                        show_raw_data = input(f"Do you wish to continue? Enter yes or no: ")
                        if show_raw_data == 'no':
                            break
                if show_raw_data == 'no':
                    break
            else:
                break

        print(f"Thank you! This is the end of the program. \n")
        while True:
            restart = input(f"Would you like to restart? Enter yes or no \n")
            if restart.lower() in ['yes', 'no']:
                break
            print(f"Please enter yes or no.")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()


