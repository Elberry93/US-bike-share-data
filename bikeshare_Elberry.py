import time
import pandas as pd



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def main():

    while True:
        y_n_Question = input("Hello! Would you like to explore some US bikeshare data!(yes/no)\n").lower()
        while y_n_Question  not in ("yes", "no"):
            print("Wrong entry!,please re-answer the question\n")
            y_n_Question = input("Hello! Would you like to explore some US bikeshare data!(yes/no)\n").lower()

        if y_n_Question != 'yes':
            print("Thank you for using our software we would like to see you again soon")
            break

        else:
            print(
                'Hello! Let\'s explore some US bikeshare data!\n\nplease answer the following questions to start analyzing the data\n')
            city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
            while city not in ("chicago", "new york city", "washington"):
                print("Wrong entry!,please re-answer the question\n")
                city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()

            def display_raw_data(city):
                """This function is to display the raw data of the chosen city five rows at a time"""
                i = 0
                raw = input("Would you like to see the first five rows of the raw data. Please enter only 'yes' or 'no'\n").lower()
                df = pd.read_csv(CITY_DATA[city])
                while True:
                    if raw == 'no':
                        break
                    elif raw == 'yes':
                        print(pd.DataFrame(df, index = [i,i+1,i+3,i+4,i+5]))
                        raw = input("Would you like to see the next five rows of the raw data. Please enter only 'yes' or 'no'\n").lower()
                        if raw == 'no':
                            break
                        elif raw == 'yes':
                            i += 5
                        else:
                            raw = input("\nWrong entry!, please type only 'yes' or 'no'\n").lower()
                    else:
                        raw = input("\nWrong entry!, please type only 'yes' or 'no'\n").lower()

            display_raw_data(city)
            month = input("If you Would like to filter the data by month please enter the month's name(only the data for the first six months are available), if you want all months, please enter \"all\":\n").title()
            while month not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
                print("Wrong entry!,please re-answer the question\n")
                month = input(
                    "If you Would like to filter the data by month please enter the month's name(only the data for the first six months are available), if you want all months, please enter \"all\":\n").title()
            day = input(
                "If you Would like to filter the data by day please enter the day's name, if you want all days, please enter \"all\":\n").lower()
            while day not in ('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all'):
                print("Wrong entry!,please re-answer the question\n")
                day = input(
                    "If you Would like to filter the data by day please enter the day's name, if you want all days, please enter \"all\":\n").lower()

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
                df = pd.read_csv(CITY_DATA[city])
                df['Start Time'] = pd.to_datetime(df['Start Time'])
                df['Month'] = df['Start Time'].dt.month
                df['Weekday'] = df['Start Time'].dt.day_name()

                if month != 'All':
                    months = ['January', 'February', 'March', 'April', 'May', 'June']
                    mon = months.index(month) + 1
                    df = df[df['Month'] == mon]
                if day != 'all':
                    df = df[df['Weekday'] == day.title()]
                return df, city

            def time_stats(df):
                """Displays statistics on the most frequent times of travel."""
                df['Start Time'] = pd.to_datetime(df['Start Time'])
                df['Month'] = df['Start Time'].dt.month
                df['Weekday'] = df['Start Time'].dt.day_name()
                df['Hour'] = df['Start Time'].dt.hour
                print('\nCalculating The Most Frequent Times of Travel...\n')
                start_time = time.time()

                # display the most common month
                most_common_month = df['Month'].mode()[0]

                # display the most common day of week
                most_common_day = df['Weekday'].mode()[0]
                # display the most common start hour
                most_common_hour = df['Hour'].mode()[0]
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-' * 40)
                return most_common_month, most_common_day, most_common_hour

            def station_stats(df):
                """Displays statistics on the most popular stations and trip."""
                print('\nCalculating The Most Popular Stations and Trip...\n')
                start_time = time.time()

                # display most commonly used start station
                most_commonly_start_station = df['Start Station'].mode()[0]
                # display most commonly used end station
                most_commonly_end_station = df['End Station'].mode()[0]
                # display most frequent combination of start station and end station trip
                most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-' * 40)
                return most_commonly_start_station, most_commonly_end_station, most_frequent_combination

            def trip_duration_stats(df):
                """Displays statistics on the total and average trip duration."""
                print('\nCalculating Trip Duration...\n')
                start_time = time.time()
                df['Start Time'] = pd.to_datetime(df['Start Time'])
                df['End Time'] = pd.to_datetime(df['End Time'])
                # display total travel time
                travel_time = df['End Time'] - df['Start Time']
                total_travel_time = travel_time.sum()
                # display mean travel time
                mean_travel_time = travel_time.mean()
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-' * 40)
                return total_travel_time, mean_travel_time

            def user_stats(df, city):
                """Displays statistics on bikeshare users."""
                print('\nCalculating User Stats...\n')
                start_time = time.time()
                if city != 'washington':
                    # Display counts of user types
                    counts_user_types = df['User Type'].value_counts()
                    # Display counts of gender
                    counts_gender = df['Gender'].value_counts()
                    # Display earliest, most recent, and most common year of birth
                    earliest_birth_year = df['Birth Year'].min()
                    most_recent_birth_year = df['Birth Year'].max()
                    most_common_birth_year = df['Birth Year'].mode()[0]
                    print("\nThis took %s seconds." % (time.time() - start_time))
                    print('-' * 40)
                    return counts_user_types, counts_gender, earliest_birth_year, most_recent_birth_year, most_common_birth_year
                else:
                    return "    "


            x = load_data(city, month, day) #x is the filtered data
            y = time_stats(x[0]) #y is to call the function of Popular times of travel
            z = station_stats(x[0]) #z is to call the function of Popular stations and trip
            q = trip_duration_stats(x[0]) #q is to call  the function of  Trip duration
            ust = user_stats(x[0], x[1]) #ust is to call  the function of User info, x[1] is the city
            print("The Data for {} filtered by month: {} and day: {} are as follows:\n {}".format(city, month, day, x))
            print(
                "\nThe Popular times of travel are as follows:\n\nThe most common month is: {}\nThe most common day of week is: {}\nThe most common hour is: {}".format(
                    y[0], y[1], y[2]))
            print(
                "\nThe statistics on the most popular stations and trip are as follows:\n\nThe most commonly used start station is: {}\nThe most commonly used end station is: {}\nThe most frequent combination of start station and end station trip:\n {}".format(
                    z[0], z[1], z[2]))
            print(
                "\nThe Trip duration stats are as follows:\n\nThe total travel time is: {}\nThe average travel time is: {}\n".format(
                    q[0], q[1]))
            print("\nThe Users info is as follows:\n\nThe counts of user types are as follows:\n{}\nThe counts of gender are as follows:\n{}\nThe earliest birth year is: {}\nThe most recent birth year is: {}\nThe most common year of birth is: {}\n\n".format(ust[0], ust[1], ust[2], ust[3], ust[3]))
            Res_Q = input("Would you like to restart the program?!(yes/no)\n").lower()
            while Res_Q not in ("yes", "no"):
                print("Wrong entry!,please re-answer the question\n")
                Res_Q = input("\n\nWould you like to restart the program?!(yes/no)\n").lower()
            if Res_Q == 'no':
                print("Thank you for using our software we would like to see you again soon")
                break


if __name__ == "__main__":
    main()

print("\nIf your answer was mistyped, please reset the program to be able to use it")
