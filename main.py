import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_data(func):
    # Get file name
    fname = 'data/%s.xlsx' % func.__name__
    # Read data
    return pd.read_excel(fname)


def rename_categories(df):
    # Create a new category that renames the two categories
    df['x'] = df.iloc[:, 0] + ' (' + df.iloc[:, 1].astype(str) + ')'
    return df


def create_other_category(df, threshold=3, x='x', y='perc'):
    # Convert threshold to a percentage of the total of the column
    threshold *= df[y].sum() / 100
    # Combine food types that are a small portion of the total
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
    # Create a color map
    cmap = plt.get_cmap('viridis')
    # Create a list of colors
    colors = cmap(np.linspace(1, 0.25, len(df[x])))

    # Set the size of the plot
    plt.figure(figsize=(10, 6))
    # Create a pie chart
    plt.pie(df[y], labels=df[x], colors=colors, autopct='%.1f%%')
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

    # Combine food types that are a small portion of the total
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

    # Combine food types that are a small portion of the total
    df = create_other_category(df, x='prod_category_english_nn', y='fail_rate')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types by Failure Rates', food_by_fail.__name__, 'prod_category_english_nn',
            'fail_rate')


def adult_by_fail():
    # Read data
    df = get_data(adult_by_fail)

    # Combine the category names
    df = rename_categories(df)

    # Combine food types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types by Failure Rates', adult_by_fail.__name__)


def food_pct_by_prov():
    # Read data
    df = pd.read_excel('data/food_test_by_prov.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('data_source_province', as_index=False).sum(numeric_only=True)

    # Combine food types that are a small portion of the total
    df = create_other_category(df, x='data_source_province', y='orig_f_perc')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Test Percentage by Province', food_pct_by_prov.__name__, 'data_source_province',
            'orig_f_perc')


def food_count_by_prov():
    # Read data
    df = pd.read_excel('data/food_test_by_prov.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('data_source_province', as_index=False).sum(numeric_only=True)

    # Combine food types that are a small portion of the total
    df = create_other_category(df, x='data_source_province', y='orig_count')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Test Count by Province', food_count_by_prov.__name__, 'data_source_province',
            'orig_count')


loc_by_pct()
food_by_pct()
adult_by_pct()
food_by_fail()
adult_by_fail()
food_pct_by_prov()
food_count_by_prov()
