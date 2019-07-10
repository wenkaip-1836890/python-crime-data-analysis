import cse163_utils  # noqa: F401
import os
import requests
import zipfile
import pandas as pd
import geopandas
import Question1
import seaborn as sns
import Question2
import Question3
import Question4


def save_useful_files():
    """
    save the file needed
    """
    def save_file(url, file_name):
        """
        save a single file
        """
        r = requests.get(url, verify=False)
        with open(file_name, 'wb') as f:
            f.write(r.content)

    save_file('https://drive.google.com/uc?export=download&' +
              'id=1xl4r7d4aeXbN_l5NirFZce-NaEXLcsjp', 'sentence_length.csv')
    save_file('https://data.cityofchicago.org/api/views/kn9c-c2s2/rows.' +
              'csv?accessType=DOWNLOAD', 'socio_econ.csv')
    save_file('https://data.cityofchicago.org/api/geospatial/5jrd-6zik?' +
              'method=export&format=Shapefile', 'Chicago_shape.zip')
    save_file('https://data.cityofchicago.org/api/views/5yjb-v3mj/' +
              'rows.csv?accessType=DOWNLOAD', 'population.csv')


def get_crime_data():
    """
    get crime data frame
    """
    data = pd.read_csv('2001-_crime.csv').dropna()
    useful_columns = ['ID', 'Date', 'Block', 'Primary Type', 'Description',
                      'Location Description', 'Arrest',
                      'District', 'Ward', 'Community Area', 'Year',
                      'Updated On', 'Location',
                      'Census Tracts', 'Wards']
    data = data[useful_columns]
    return data


def get_geo_data():
    """
    get chicago geo data frame
    """
    with zipfile.ZipFile('Chicago_shape.zip', 'r') as zipObj:
        zipObj.extractall()
    file_names = os.listdir()
    for file_name in file_names:
        if file_name.endswith('.shp') and file_name.startswith('geo_'):
            chicago_shape = geopandas.read_file(file_name)
    useful_geo_columns = ['commarea', 'commarea_n', 'geoid10', 'geometry']
    return chicago_shape[useful_geo_columns]


def get_population_data():
    """
    get population data frame
    """
    return pd.read_csv('population.csv')


def get_socio_econ_data():
    """
    get socio_econ data frame
    """
    return pd.read_csv('socio_econ.csv')


def get_sentence_length_data():
    """
    get sentence length data frame
    """
    return pd.read_csv('sentence_length.csv')


def get_crime_sample(data):
    """
    get some sample data for later use
    """
    data_sample1 = data.sample(n=10000)
    data_sample2 = data.sample(n=10000)
    data_sample3 = data.sample(n=10000)
    data_sample4 = data.sample(n=10000)
    data_sample1.to_csv('sample1.csv')
    data_sample2.to_csv('sample2.csv')
    data_sample3.to_csv('sample3.csv')
    data_sample4.to_csv('sample4.csv')


def main():
    sns.set()
    file_names = os.listdir()
    needed_files = ['sentence_length.csv', 'socio_econ.csv',
                    'Chicago_shape.zip', 'population.csv']
    for file_name in needed_files:
        if file_name not in file_names:
            save_useful_files()
    print('file_saved')
    crime_data = get_crime_data()
    print('get crime data')
    geo_data = get_geo_data()
    population_data = get_population_data()
    sentence_length_data = get_sentence_length_data()
    socio_econ_data = get_socio_econ_data()
    get_crime_sample(crime_data)

    q1 = Question1.Question1(crime_data, sentence_length_data,
                             geo_data, socio_econ_data)
    q1._plot_a_single_year(2018)
    q1._plot_change('42 43 45')
    q1._safety_ranking(2018)
    q1._plot_all_Ca()

    q2 = Question2.Question2()
    q2.aggregate_data(crime_data)
    q2.machine_learning()
    q2._report_predict('assault', 43, 23)
    q2._report_predict('theft', 9, 23)
    q2._report_predict('theft', 9, 10)
    q2._report_predict('theft', 9, 13)
    print('The mean square error of the model is ' + str(q2.mes()))

    Question3.Question3(crime_data, geo_data, population_data)
    Question4.Question4(crime_data, geo_data, population_data, socio_econ_data)


if __name__ == "__main__":
    main()
