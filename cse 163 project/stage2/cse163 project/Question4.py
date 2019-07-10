import Question3
import geopandas


def generate_crime_socioecon_data(crime_data, geo_data,
                                  population_data, socio_econ_data):
    '''
    accepts crime_data, geo_data, population_data and
    socio_econ_data tables as parameters,
    generate a table with crime rate and
    other socio-econ data included in and return it
    '''
    geo_pop_data = Question3.merge_data(geo_data, population_data)
    crime_arrest_rate = Question3.generate_crime_arrest_rate(crime_data,
                                                             geo_pop_data)
    crime_arrest_rate = crime_arrest_rate[crime_arrest_rate['Year'] == 2018]
    crime_socioecon_data =\
        crime_arrest_rate.merge(socio_econ_data,
                                left_on='Community Area',
                                right_on='Community Area Number')
    crime_socioecon_data = crime_socioecon_data.merge(geo_data,
                                                      left_on='Community Area',
                                                      right_on='commarea_n')
    crime_socioecon_data = crime_socioecon_data[['COMMUNITY AREA NAME',
                                                 'Community Area', 'Year',
                                                 'crime_rate',
                                                 'PERCENT HOUSEHOLDS '
                                                 'BELOW POVERTY',
                                                 'PERCENT AGED 16+ UNEMPLOYED',
                                                 'PERCENT AGED 25+ WITHOUT '
                                                 'HIGH SCHOOL DIPLOMA',
                                                 'PERCENT AGED UNDER 18 OR '
                                                 'OVER 64',
                                                 'geometry']].dropna()
    return crime_socioecon_data


def geo_plot(geo_crime_socioecon_ca):
    '''
    accepts a geo_crime_socioecon_ca table as a parameter,
    generate some geo subplots of the Chicago map based on the geometry column
    and other socio-econ data columns
    save these subplots to a single file
    '''
    geo_crime_socioecon_ca['crime_rate'] = \
        geo_crime_socioecon_ca['crime_rate'] * 100
    fig, [[ax1, ax2, ax3], [ax4, ax5, ax6]] = \
        Question3.plt.subplots(2, figsize=(30, 15), ncols=3)
    geo_crime_socioecon_ca.plot(legend=True, ax=ax1)
    geo_crime_socioecon_ca.plot(column='PERCENT HOUSEHOLDS BELOW POVERTY',
                                cmap='plasma', legend=True, ax=ax2)
    geo_crime_socioecon_ca.plot(column='PERCENT AGED 16+ UNEMPLOYED',
                                cmap='inferno', legend=True, ax=ax3)
    geo_crime_socioecon_ca.plot(column='PERCENT AGED 25+ WITHOUT '
                                'HIGH SCHOOL DIPLOMA', cmap='magma',
                                legend=True, ax=ax4)
    geo_crime_socioecon_ca.plot(column='PERCENT AGED UNDER 18 OR OVER 64',
                                cmap='cividis', legend=True, ax=ax5)
    geo_crime_socioecon_ca.plot(column='crime_rate', cmap='viridis',
                                legend=True, ax=ax6)
    ax1.set_title('Community Area', fontsize=30)
    ax2.set_title('poverty rate', fontsize=30)
    ax3.set_title('unemployment rate', fontsize=30)
    ax4.set_title('educational level', fontsize=30)
    ax5.set_title('age distribution', fontsize=30)
    ax6.set_title('crime rate', fontsize=30)
    fig.suptitle("Chicago Map", fontsize=50)
    fig.savefig("geo_plot.png")


def regress_plot(geo_crime_socioecon_ca):
    '''
    accepts a eo_crime_socioecon_ca table as a parameter,
    generate some seaborn subplots showing the relationships between the
    change in crime rate and change in other socio-econ data
    save these subplots to a single file
    '''
    fig, [[ax1, ax2], [ax3, ax4]] = \
        Question3.plt.subplots(2, figsize=(30, 15), ncols=2)
    Question3.sns.regplot(x="PERCENT HOUSEHOLDS BELOW POVERTY", y="crime_rate",
                          data=geo_crime_socioecon_ca, ax=ax1, order=2)
    Question3.sns.regplot(x="PERCENT AGED 16+ UNEMPLOYED", y="crime_rate",
                          data=geo_crime_socioecon_ca, ax=ax2, order=2)
    Question3.sns.regplot(x="PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA",
                          y="crime_rate", data=geo_crime_socioecon_ca,
                          ax=ax3, order=2)
    Question3.sns.regplot(x="PERCENT AGED UNDER 18 OR OVER 64", y="crime_rate",
                          data=geo_crime_socioecon_ca, ax=ax4, order=2)
    ax1.set(ylim=(0, 100))
    ax2.set(ylim=(0, 100))
    ax3.set(ylim=(0, 100))
    ax4.set(ylim=(0, 100))
    fig.savefig("regress_plot.png")


def Question4(crime_data, geo_data, population_data, socio_econ_data):
    crime_socioecon_data = generate_crime_socioecon_data(crime_data, geo_data,
                                                         population_data,
                                                         socio_econ_data)

    geo_crime_socioecon_data = \
        geopandas.GeoDataFrame(crime_socioecon_data,
                               geometry='geometry')
    geo_crime_socioecon_ca = geo_crime_socioecon_data.dissolve(by='Community '
                                                               'Area',
                                                               aggfunc='min')

    geo_plot(geo_crime_socioecon_ca)

    regress_plot(geo_crime_socioecon_ca)
