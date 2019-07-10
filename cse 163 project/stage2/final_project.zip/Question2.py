# manage the process of solving question 2
# use tree regressor model to predict the rate of a certain type of crime
# being solved at a giving time and community area
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class Question2:

    def __init__(self):
        """
        _case_count_grouped(DataFrame): the rate of case being solved for each
        community, crime type and hour
        """
        self._case_count_grouped = None
        self._model = None
        self._X_test = None
        self._y_test = None

    def aggregate_data(self, crime_data):
        """
        calculate the rate of case being solved for each community,
        crime type and hour
        """
        def arrest_count(x):
            """
            use to count the solved case
            """
            return x.sum()

        def get_hour(s):
            """
            get the hour from time column
            """
            if s.endswith('PM'):
                return int(s[11:13]) + 12
            return int(s[11:13])

        crime_data['Hour'] = crime_data['Date'].apply(get_hour)
        case_count_grouped = crime_data.groupby(['Community Area',
                                                'Primary Type', 'Hour']).agg(
                           {'Arrest': ['count', arrest_count]}).reset_index()
        case_count_grouped['Solve_rate'] =\
            case_count_grouped['Arrest']['arrest_count'] / \
            case_count_grouped['Arrest']['count']
        case_count_grouped = case_count_grouped.drop(columns='Arrest')
        self._case_count_grouped = case_count_grouped

    def machine_learning(self):
        """
        train a tree regressor model
        """
        if self._case_count_grouped is None:
            raise Exception('Please aggregate data first')
        X = self._case_count_grouped.loc[:, ['Community Area', 'Primary Type',
                                             'Hour']]
        X = pd.get_dummies(X)
        y = self._case_count_grouped['Solve_rate']
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.2)
        model = DecisionTreeRegressor()
        model.fit(X_train, y_train)
        self._model = model
        self._X_test = X_test
        self._y_test = y_test

    def _predict_once(self):
        """
        a helper function to predict once
        """
        if self._model is None:
            raise Exception('Please train ML model first')
        community, crime_type, time = self._ask_for_info()
        crime_type = crime_type.upper()
        community = float(community)
        time = float(time)
        keys = (self._X_test.columns)
        values = [0] * len(keys)
        feature_map = dict(zip(keys, values))
        type_key = "('Primary Type', '')_" + crime_type
        while ((community < 1 or community > 77) or type_key not in feature_map
                or (time < 0 or time > 24)):
            print('Your input is invalid.')
            community, crime_type, time = self._ask_for_info()
            crime_type = crime_type.upper()
            community = float(community)
            time = float(time)
            keys = (self._X_test.columns)
            values = [0] * len(keys)
            feature_map = dict(zip(keys, values))

        feature_map[('Community Area', '')] = community
        feature_map[('Hour', '')] = time
        feature_map[type_key] = 1
        possibility_percentage = self._model.predict(
                                [list(feature_map.values())])[0] * 100
        print('The predicted possibility of the case being solved is: ' +
              str(round(possibility_percentage, 2)) + ' percent')
        return possibility_percentage

    def predict(self):
        """
        do the predict process
        """
        predict_again = 'True'
        while predict_again == 'True':
            self._predict_once()
            print()
            predict_again = input('Please enter True if want to predict agai' +
                                  'n, otherwise False: ')
            while predict_again != 'True' and predict_again != 'False':
                predict_again = input('Please enter True if want to predict ' +
                                      'again, otherwise False: ')

    def _ask_for_info(self):
        """
        a helper function to ask for input of community, crime type
        and hour. return a result as a triple
        """
        community = input('Please enter a community area number: ')
        crime_type = input('Please enter a crime type: ')
        hour = input('Please enter the hour: ')
        return (community, crime_type, hour)

    def mes(self):
        """
        return the mean square error of the ML model
        """
        return mean_squared_error(self._y_test,
                                  self._model.predict(self._X_test))
