import cse163_utils  # noqa: F401
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def draw_rate_change_with_year(crime_arrest_rate, comm_area):
    '''
    accepts the crime_arrest_rate table and community area value as parameters,
    draw the rate of change of crime and arrest with respect to years in two
    separate subplots and then save these two subplots to one file.
    '''
    crime_arrest_rate = crime_arrest_rate[crime_arrest_rate['Community Area']
                                          == comm_area].dropna()
    crime_rate_per_ca = crime_arrest_rate[['Year', 'crime_rate']]
    arrest_rate_per_ca = crime_arrest_rate[['Year', 'arrest_rate']]
    fig, axs = plt.subplots(ncols=2, figsize=(10, 10))
    sns.regplot(x="Year", y="arrest_rate", data=arrest_rate_per_ca,
                ax=axs[0], order=1, label='arrest_rate')
    sns.regplot(x="Year", y="crime_rate", data=crime_rate_per_ca, ax=axs[1],
                order=1, label='crime_rate', color='g')
    axs[0].set_title('Community Area: ' + str(comm_area))
    axs[1].set_title('Community Area: ' + str(comm_area))
    plt.savefig('rate_change_with_year.png')


def merge_data(geo_data, population_data):
    '''
    accepts the geo_data table and population_data table as paraneters,
    merge the two tables to form geo_pop_data table and return it
    '''
    geo_data['geoid10'] = geo_data['geoid10'].astype(int)
    population_data['CENSUS_BLOCK_11_DIGIT'] = population_data
    ['CENSUS BLOCK FULL'] // 10000
    geo_pop_data = geo_data.merge(population_data, left_on='geoid10',
                                  right_on='CENSUS_BLOCK_11_DIGIT')
    return geo_pop_data


def generate_crime_arrest_rate(crime_data, geo_pop_data):
    '''
    accepts the crime_data and geo_pop_data tables as parameters,
    generate a table with crime and arrest rate included in it and return
    '''
    case_num = crime_data.groupby(['Community Area', 'Year'])['ID'].count()
    case_num = case_num.to_frame().reset_index()
    case_num = case_num.rename(columns={'ID': 'case_num'})
    pop_data_per_ca = geo_pop_data.groupby('commarea_n')
    ['TOTAL POPULATION'].sum()
    pop_data_per_ca = pop_data_per_ca.repeat(18)
    pop_data_per_ca = pop_data_per_ca.to_frame().reset_index()
    pop_data_per_ca['Year'] = pd.Series([i for i in range(2002, 2020)] * 77)
    case_num['TOTAL POPULATION'] = pop_data_per_ca['TOTAL POPULATION']
    case_pop_data = case_num
    case_pop_data['crime_rate'] = case_pop_data['case_num'] / case_pop_data
    ['TOTAL POPULATION']
    crime_rate_data = case_pop_data
    case_solved = crime_data.groupby(['Community Area', 'Year']).agg(
      {'Arrest': lambda x: x.sum()})
    case_solved = case_solved['Arrest'].to_frame().reset_index()
    crime_rate_data['case_solved'] = case_solved['Arrest']
    crime_rate_data['arrest_rate'] = \
        crime_rate_data['case_solved'] / crime_rate_data['case_num']
    crime_arrest_rate = crime_rate_data.dropna()
    return crime_arrest_rate


def compute_corr(crime_arrest_rate):
    '''
    accepts the crime_arrest_rate table as a parameter,
    compute a dictionary of correlation between crime rate and arrest
    rate in a particular community area and return it
    '''
    crime_arrest_rate['next_year'] = crime_arrest_rate['Year'] + 1
    crime_rate_curr = crime_arrest_rate[['Community Area',
                                        'Year', 'crime_rate']]
    arrest_rate_prev = crime_arrest_rate[['Community Area', 'next_year',
                                          'arrest_rate']]
    crime_arrest_rate_corr = crime_rate_curr.merge(arrest_rate_prev,
                                                   left_on=['Community Area',
                                                            'Year'],
                                                   right_on=['Community Area',
                                                             'next_year'])
    corr_ca = dict()
    for i in range(1, 77):
        data = crime_arrest_rate_corr[crime_arrest_rate_corr['Community Area']
                                      == (1.0 * i)]
        if len(data) != 0:
            correlation = data['arrest_rate'].corr(data['crime_rate'])
            corr_ca[str(1.0 * i)] = correlation
    corr_ca = pd.DataFrame(corr_ca.items(), columns=['Community Area',
                                                     'correlation']).dropna()
    corr_ca['corr_abs'] = corr_ca['correlation'].abs()
    return corr_ca


def Question3(crime_data, geo_data, population_data):

    geo_pop_data = merge_data(geo_data, population_data)
    crime_arrest_rate = generate_crime_arrest_rate(crime_data, geo_pop_data)
    print('crime and arrest rates:')
    print(crime_arrest_rate)
    print()

    draw_rate_change_with_year(crime_arrest_rate, 1.0)

    corr_ca = compute_corr(crime_arrest_rate)
    print('correlations of arrest and crime rates', end="")
    print(' on different Community Area:')
    print(corr_ca)
    print()

    top_10_corr_ca = corr_ca.nlargest(10, 'corr_abs').drop('corr_abs', 1)

    print('top 10 correlations of arrest and crime rates', end="")
    print(' on different Community Area:')
    print(top_10_corr_ca)
    print()
    plt.clf()
    sns.distplot(corr_ca['correlation'], hist=True)
    plt.savefig('correlation.png')

    percent = corr_ca[corr_ca['correlation'].abs() > 0.5]
    ['correlation'].count() / len(corr_ca)
    print('percentage of Community Area whose crime and arrest rates ', end="")
    print('have a correlation of more than 0.5:')
    print(percent)
    print()
