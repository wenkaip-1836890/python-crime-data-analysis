import seaborn as sns
import matplotlib.pyplot as plt


class Question1:
    def __init__(self, data, sentence_length, chicago_shape, socio):
        """
        get a dataframe containing all the harm for every community in
        every year
        """
        data = data.merge(sentence_length, left_on='Primary Type',
                          right_on='Criminal Type', how='inner')
        harm_by_community =\
            data[(data['Community Area'] != 0.0) &
                 (data['Year'] != 2001) & (data['Year'] != 2019)].\
            groupby(['Community Area', 'Year']).\
            agg({'Sentence Length in Month': 'sum'}).reset_index()

        chicago_shape = chicago_shape.dissolve(by='commarea_n')
        neighbour_data = {float(i): [] for i in range(1, 78)}
        for i in range(1, 78):
            for j in range(1, 78):
                if chicago_shape['geometry'][float(i)].\
                     touches(chicago_shape['geometry'][float(j)]):
                    neighbour_data[float(i)].append(float(j))
        chicago_shape['commarea'] = chicago_shape['commarea'].astype(float)
        self._total_frame = harm_by_community
        self._neighbour_data = neighbour_data
        self._chicago_shape = chicago_shape
        self._socio = socio

    def _compute_harm_by_community(self, year):
        sum_harm_list = []
        harm_by_community =\
            self._total_frame[self._total_frame['Year'] == year].\
            groupby('Community Area')['Sentence Length in Month'].sum()
        for k in range(1, 78):
            k = float(k)
            harm_itself = harm_by_community[k]
            harm_around_mean = 0
            neigbour_list = self._neighbour_data[k]
            for CA in neigbour_list:
                harm_around_mean += harm_by_community[CA]
            harm_around_mean = harm_around_mean / len(neigbour_list)
            sum_harm_list.append(harm_itself * 0.8 + harm_around_mean * 0.2)
        harm_by_community = harm_by_community.to_frame()
        harm_by_community['sum_harm'] = sum_harm_list
        return harm_by_community

    def _plot_a_single_year(self, year):
        """
        a helper function to plot a single year plot
        """
        harm_by_community = self._compute_harm_by_community(year)
        merged =\
            self._chicago_shape.merge(harm_by_community, left_on='commarea',
                                      right_on='Community Area')
        fig, ax = plt.subplots(1)
        merged.plot(ax=ax, column='sum_harm', legend=True, cmap='Wistia')
        fig.suptitle('Crime Situation in ' + str(year), size=16)
        plt.savefig('safety_ranking_' + str(year) + '.png')

    def plot_communities_single_year(self):
        """
        ask for years and plot the harm situation in those years
        """
        plot_again = 'True'
        while plot_again == 'True':
            year = input('Enter a year you want to plot: ')
            year = int(year)
            self._plot_a_single_year(year)
            print()
            plot_again = input('Please enter True if want to print ano' +
                               'ther, otherwise False: ')
            while plot_again != 'True' and plot_again != 'False':
                plot_again = input('Please enter True if want to print ' +
                                   'another, otherwise False: ')

    def plot_change_through_years(self):
        """
        plot how harm changes through out years for some given communities
        """
        communities_str = input('Enter communities you want to plot: ')
        communities = [float(i) for i in communities_str.split()]
        specific_CA = self._total_frame[self._total_frame['Community Area'].
                                        isin(communities)]
        sns.relplot(data=specific_CA, kind="line", x="Year",
                    y="Sentence Length in Month", style='Community Area')
        plt.savefig('change_through_years.png', bbox_inches='tight')

    def safety_ranking(self):
        """
        return the ranking of safety of communities in a list of a year
        print out the list
        """
        year = input('Enter a year you want to get ranking: ')
        year = int(year)
        harm_by_community = self._compute_harm_by_community(year)
        sorted_df = harm_by_community.sort_values(by='sum_harm',
                                                  ascending=True)
        ranking = list(sorted_df.index.values)
        ranking_name = []
        ranking_name = [self._socio.loc[i - 1, 'COMMUNITY AREA NAME']
                        for i in ranking]
        print('Safety ranking in this year is: ')
        print(ranking_name)
        print('safer places appears earlier')
        return ranking
