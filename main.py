import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def rename_categories(df):
    # Create a new category that renames the two categories
    df['x'] = df.iloc[:, 0] + ' (' + df.iloc[:, 1].astype(str) + ')'
    return df


def create_other_category(df, threshold=5, x='x', y='perc'):
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


# Create a pie chart
def pie_cht(df, title, x='x', y='perc'):
    # Create a color map
    cmap = plt.get_cmap('viridis')
    # Create a list of colors
    colors = cmap(np.linspace(1, 0, len(df[x])))

    # Set the size of the plot
    plt.figure(figsize=(10, 6))
    # Create a pie chart
    plt.pie(df[y], labels=df[x], colors=colors, autopct='%.1f%%')
    # Set the title of the plot
    plt.title(title)
    plt.show()


def plot_loc_by_pct():
    # Read data
    df = pd.read_excel('loc_by_pct.xlsx')

    # Combine the category names
    df = rename_categories(df)

    # Combine location types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Sampled Location Types')


def plot_food_by_pct():
    # Read data
    df = pd.read_excel('food_by_pct.xlsx')

    # Combine the category names
    df = rename_categories(df)

    # Combine food types that are a small portion of the total
    df = create_other_category(df, 3)

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types')


def plot_adult_by_pct():
    # Read data
    df = pd.read_excel('adult_by_pct.xlsx')

    # Combine the category names
    df = rename_categories(df)

    # Combine adulterant types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types')


def plot_fail_by_food():
    # Read data
    df = pd.read_excel('fail_by_food.xlsx')

    # Combine food types that are a small portion of the total
    df = create_other_category(df, threshold=3, x='prod_category_english_nn', y='fail_rate')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types', x='prod_category_english_nn', y='fail_rate')


def plot_fail_by_adult():
    # Read data
    df = pd.read_excel('fail_by_adult.xlsx')

    # Combine the category names
    df = rename_categories(df)

    # Combine food types that are a small portion of the total
    df = create_other_category(df)

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types')
