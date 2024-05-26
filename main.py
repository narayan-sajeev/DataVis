from random import choice

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pluralizer import Pluralizer


def get_data(func):
    # Get file name
    fname = 'data/%s.xlsx' % func.__name__
    # Read data
    return pd.read_excel(fname)


def rename_categories(df):
    # Create a new category that renames the two categories
    df['x'] = df.iloc[:, 0] + ' (' + df.iloc[:, 1].astype(str) + ')'
    return df


def create_other_category(df, x='x', y='perc', threshold=3):
    # Convert threshold to a percentage of the total of the column
    threshold *= df[y].sum() / 100
    # Combine values that are a small portion of the total
    mask = df[y] < threshold
    # Set the food type to 'Other' if the food type has less than the threshold
    df.loc[mask, x] = 'Other'
    # Group by the food type and sum the percentage
    df = df.groupby(x).sum(numeric_only=True).reset_index()

    # Separate 'Other' from the rest
    df_other = df[df[x] == 'Other']
    df = df[df[x] != 'Other']

    # Sort the DataFrame in descending order after grouping
    df = df.sort_values(y, ascending=False)

    # Add 'Other' at the end regardless of its value
    df = pd.concat([df, df_other], ignore_index=True)

    return df


def pie_cht(df, title, fname, x='x', y='perc'):
    # Define the list of colors
    colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'twilight', 'twilight_shifted', 'turbo', 'cubehelix',
              'cubehelix_r', 'rocket', 'mako', 'mako_r', 'icefire', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG',
              'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r',
              'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r',
              'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn',
              'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r',
              'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1',
              'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn',
              'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r',
              'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis',
              'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r',
              'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r',
              'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg',
              'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv',
              'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r',
              'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r',
              'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20',
              'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r',
              'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter',
              'winter_r', 'vlag', 'vlag_r', 'crest', 'crest_r', 'teal', 'teal_r', 'Greys', 'Purples', 'Blues', 'Greens',
              'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn',
              'BuGn', 'YlGn']

    # Create a color map
    cmap = plt.get_cmap(choice(colors))
    # Create a list of colors
    colors = cmap(np.linspace(0.9, 0.25, len(df[x])))

    # Set the size of the plot
    plt.figure(figsize=(10, 6))
    # Capitalize the labels
    labels = [' '.join(label.split('_')).title() for label in df[x]]
    # Create a pie chart
    plt.pie(df[y], labels=labels, colors=colors, autopct='%.1f%%')
    # Set the title of the plot
    plt.title(title)
    # Save the plot
    plt.savefig('charts/%s.png' % fname)
    plt.show()


def loc_by_pct():
    # Read data
    df = get_data(loc_by_pct)

    # Combine the category names
    df = rename_categories(df)

    # Combine location types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Sampled Location Types by Percentage', loc_by_pct.__name__)


def food_by_pct():
    # Read data
    df = get_data(food_by_pct)

    # Combine the category names
    df = rename_categories(df)

    # Combine values that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types by Percentage', food_by_pct.__name__)


def adult_by_pct():
    # Read data
    df = get_data(adult_by_pct)

    # Combine the category names
    df = rename_categories(df)

    # Combine adulterant types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types by Percentage', adult_by_pct.__name__)


def food_by_fail():
    # Read data
    df = get_data(food_by_fail)

    # Combine values that are a small portion of the total
    df = create_other_category(df, 'prod_category_english_nn', 'fail_rate')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types by Failure Rate', food_by_fail.__name__, 'prod_category_english_nn',
            'fail_rate')


def adult_by_fail():
    # Read data
    df = get_data(adult_by_fail)

    # Combine the category names
    df = rename_categories(df)

    # Combine values that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types by Failure Rate', adult_by_fail.__name__)


def prov_by_food_pct():
    # Read data
    df = pd.read_excel('data/prov_by_food_test.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('data_source_province', as_index=False).sum(numeric_only=True)

    # Combine values that are a small portion of the total
    df = create_other_category(df, 'data_source_province', 'orig_f_perc')

    # Create a pie chart
    pie_cht(df, 'Distribution of Provinces by Food Test Percentage', prov_by_food_pct.__name__, 'data_source_province',
            'orig_f_perc')


def prov_by_food_count():
    # Read data
    df = pd.read_excel('data/prov_by_food_test.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('data_source_province', as_index=False).sum(numeric_only=True)

    # Combine values that are a small portion of the total
    df = create_other_category(df, 'data_source_province', 'orig_count')

    # Create a pie chart
    pie_cht(df, 'Distribution of Provinces by Food Test Count', prov_by_food_count.__name__, 'data_source_province',
            'orig_count')


def prov_by_recs():
    # Read data
    df = get_data(prov_by_recs)

    # Combine the category names
    df = rename_categories(df)

    # Combine values that are a small portion of the total
    df = create_other_category(df, 'province', 'curr_recs')

    # Create a pie chart
    pie_cht(df, 'Distribution of Provinces by Recommendation', prov_by_recs.__name__, 'province',
            'curr_recs')


def food_by_adult():
    # Read data
    df = get_data(food_by_adult)

    # Retrieve first column
    col1 = df.columns[0]

    # Loop through the columns
    for curr_col in df.columns[1:]:
        # Retrieve the 2 columns
        df2 = df[[col1, curr_col]]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, col1, curr_col)

        # Capitalize the current column
        title = ' '.join([_.capitalize() for _ in curr_col.split()])

        # Retrieve column name
        format_col = '_'.join([_.lower() for _ in curr_col.split()])

        # Set file name
        fname = 'food_by_%s' % format_col

        # Create a pie chart
        pie_cht(df2, 'Distribution of Food by %s' % title, fname, col1, curr_col)


loc_by_pct()
food_by_pct()
adult_by_pct()
food_by_fail()
adult_by_fail()
prov_by_food_pct()
prov_by_food_count()
prov_by_recs()
food_by_adult()
