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


def create_other_category(df, x='x', y='perc', threshold=5):
    # Convert threshold to a percentage of the total of the column
    threshold *= df[y].sum() / 100
    # Combine values that are a small portion of the total
    mask = df[y] < threshold
    # Set the food type to 'Other' if the food type has less than the threshold
    df.loc[mask, x] = 'Other'
    # Group by the food type and sum the percentage
    df = df.groupby(x).sum(numeric_only=False).reset_index()

    # Separate 'Other' from the rest
    df_other = df[df[x] == 'Other']
    df = df[df[x] != 'Other']

    # Sort the DataFrame in descending order after grouping
    df = df.sort_values(y, ascending=False)

    # Add 'Other' at the end regardless of its value
    df = pd.concat([df, df_other], ignore_index=True)

    # Remove 'Other' row if it has a value of 0
    if df.iloc[-1][y] == 0:
        df = df.iloc[:-1]

    return df


def pie_cht(df, title, fname, x='x', y='perc', subfolder=None):
    # Create a color map
    cmap = plt.get_cmap()
    # Create a list of colors
    colors = cmap(np.linspace(1, 0.25, len(df[x])))

    # Set the size of the plot
    # plt.figure(figsize=(10, 6))
    # Capitalize the labels
    labels = [' '.join(label.split('_')).title() for label in df[x]]
    # Create a pie chart
    plt.pie(df[y], labels=labels, colors=colors, autopct='%.1f%%', pctdistance=0.85)
    # Set the title of the plot
    plt.title(title)
    # Retrieve the name of the folder to save the plot
    folder = fname.split('_')[0]
    # If there are no special instructions on where to save the plot
    # if not subfolder:
    # Save the plot
    # plt.savefig('charts/%s/%s.png' % (folder, fname))
    # else:
    # Save the plot
    # plt.savefig('charts/%s/%s/%s.png' % (folder, subfolder.__name__, fname))
    # plt.show()
    # Wait before creating the next chart
    # plt.pause(2)


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


def capitalize(s):
    return ' '.join([_.capitalize() for _ in s.split()])


def format(s):
    # Remove underscores
    s = ' '.join(s.split('_'))

    # Remove comma
    s = ''.join(s.split(','))

    # Capitalize
    s = capitalize(s)

    # Split the title into words
    words = s.split()

    # Loop through each word
    for word in words:
        # If that word repeats
        if words.count(word) > 1:
            # Find the index of the word
            i = words.index(word)
            # Remove the repeated words
            new_words = words[:i + 1]
            # Update the new words
            words = list(new_words)

    # Pluralize the last word
    last = Pluralizer().pluralize(words[-1])

    # Replace the last word
    words[-1] = ''.join(last)

    # Update the title
    title = ' '.join(words)

    return title


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
        title = capitalize(curr_col)

        # Retrieve column name
        col_name = '_'.join([_.lower() for _ in curr_col.split()])

        # Set file name
        fname = 'food_by_%s' % col_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Food Types by %s' % title, fname, col1, curr_col, food_by_adult)

    return df


def adult_in_food():
    # Read data
    df = get_data(food_by_adult)

    # Loop through the rows
    for _, row in df.iterrows():
        # Create a new DataFrame
        df2 = pd.DataFrame(row).reset_index()

        # Set the column names
        df2.columns = ['x', 'y']

        # Retrieve the food
        food = df2['y'][0]

        # Remove the first row
        df2 = df2.iloc[1:]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, 'x', 'y')

        # Retrieve the title
        title = format(food)

        # Retrieve row name
        row_name = '_'.join([_.lower() for _ in title.split()])

        # Set file name
        fname = 'adult_in_%s' % row_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Adulterant Types in %s' % title, fname, 'x', 'y', adult_in_food)

    return df


def prov_by_food():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Retrieve first column
    col1 = df.columns[0]

    # Loop through the columns
    for curr_col in df.columns[1:]:

        # Stop once adulterants are reached
        if 'contaminant' in curr_col.lower():
            return

        # Retrieve the 2 columns
        df2 = df[[col1, curr_col]]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, col1, curr_col)

        # Retrieve the title
        title = format(curr_col)

        # Retrieve column name
        col_name = '_'.join([_.lower() for _ in title.split()])

        # Set file name
        fname = 'prov_by_%s' % col_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Provinces by %s' % title, fname, col1, curr_col, prov_by_food)

    # Transpose the DataFrame
    df = df.T

    # Delete the first row
    df = df.iloc[1:]

    # Reset the index
    df.reset_index(inplace=True)

    return df


def food_in_prov():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Loop through the rows
    for _, row in df.iterrows():
        # Create a new DataFrame
        df2 = pd.DataFrame(row).reset_index()

        # Set the column names
        df2.columns = ['x', 'y']

        # Retrieve the food
        food = df2['y'][0]

        # Stop once adulterants are reached
        if 'contaminant' in food.lower():
            return

        # Remove the first rows
        df2 = df2.iloc[2:]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, 'x', 'y')

        # Capitalize the current column
        title = capitalize(food)

        # Retrieve column name
        col_name = '_'.join([_.lower() for _ in food.split()])

        # Set file name
        fname = 'food_in_%s' % col_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Food Types in %s' % title, fname, 'x', 'y', food_in_prov)

    return df


def prov_by_adult():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Retrieve first column
    col1 = df.columns[0]

    # Find the index of the column header containing 'contaminant'
    idx = df.columns.get_loc(df.columns[df.columns.str.contains('contaminant')][0])

    # Loop through the columns
    for curr_col in df.columns[idx:]:
        # Retrieve the 2 columns
        df2 = df[[col1, curr_col]]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, col1, curr_col)

        # Retrieve the title
        title = format(curr_col)

        # Retrieve column name
        col_name = '_'.join([_.lower() for _ in title.split()])

        # Set file name
        fname = 'prov_by_%s' % col_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Provinces by %s' % title, fname, col1, curr_col, prov_by_adult)

    # Set the index as the first column
    df.set_index(col1, inplace=True)

    # Slice the DataFrame
    df = df.iloc[:, idx - 1:]

    # Transpose the DataFrame
    df = df.T

    # Reset the index
    df.reset_index(inplace=True)

    return df


def adult_in_prov():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Loop through the rows
    for _, row in df.iterrows():
        # Create a new DataFrame
        df2 = pd.DataFrame(row).reset_index()

        # Set the column names
        df2.columns = ['x', 'y']

        # Retrieve the food
        food = df2['y'][0]

        # Find the index of the cell containing 'contaminant'
        idx = df2[df2['x'].str.contains('contaminant')].index[0]

        # Remove the first rows
        df2 = df2.iloc[idx:]

        # Combine values that are a small portion of the total
        df2 = create_other_category(df2, 'x', 'y')

        # Capitalize the current column
        title = capitalize(food)

        # Retrieve column name
        col_name = '_'.join([_.lower() for _ in food.split()])

        # Set file name
        fname = 'adult_in_%s' % col_name

        # Create a pie chart
        pie_cht(df2, 'Distribution of Adulterant Types in %s' % title, fname, 'x', 'y', adult_in_prov)

    return df


def adult_in_all_food():
    # Read data
    df = get_data(food_by_adult)

    # Find the sum of each column
    df = df.sum().reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Remove the first rows
    df = df.iloc[2:]

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types in All Food', adult_in_all_food.__name__, 'x', 'y')


def food_by_all_adult():
    # Read data
    df = get_data(food_by_adult)

    # Set the index
    df.set_index('prod_category_english_nn', inplace=True)

    # Find the sum of each row
    df = df.sum(axis=1).reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types by All Adulterants', food_by_all_adult.__name__, 'x', 'y')


def food_by_all_prov():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Find the sum of each column
    df = df.sum().reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Remove the first row
    df = df.iloc[1:]

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Food Types by All Provinces', food_by_all_prov.__name__, 'x', 'y')


def prov_by_all_food():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Set the index
    df.set_index('level_1', inplace=True)

    # Find the sum of each row
    df = df.sum(axis=1).reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Remove the first row
    df = df.iloc[1:]

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Provinces by All Foods', prov_by_all_food.__name__, 'x', 'y')


def adult_in_all_prov():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Find the index of the column header containing 'contaminant'
    idx = df.columns.get_loc(df.columns[df.columns.str.contains('contaminant')][0])

    # Slice the DataFrame
    df = df.iloc[:, idx:]

    # Find the sum of each column
    df = df.sum().reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Remove the first row
    df = df.iloc[1:]

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Adulterant Types in All Provinces', adult_in_all_prov.__name__, 'x', 'y')


def prov_by_all_adult():
    # Read data
    df = pd.read_excel('data/prov_by_food_adult.xlsx')

    # Group by province and calculate the sum
    df = df.groupby('level_1', as_index=False).sum(numeric_only=True)

    # Find the index of the column header containing 'contaminant'
    idx = df.columns.get_loc(df.columns[df.columns.str.contains('contaminant')][0])

    # Slice the DataFrame
    df = pd.concat([df.iloc[:, 0], df.iloc[:, idx:]], axis=1)

    # Set the index
    df.set_index('level_1', inplace=True)

    # Find the sum of each row
    df = df.sum(axis=1).reset_index()

    # Set the column names
    df.columns = ['x', 'y']

    # Remove the first row
    df = df.iloc[1:]

    # Combine location types that are a small portion of the total
    df = create_other_category(df, 'x', 'y')

    # Create a pie chart
    pie_cht(df, 'Distribution of Provinces by All Adulterants', prov_by_all_adult.__name__, 'x', 'y')


def get_all_adults():
    # Read data
    df = get_data(adult_by_fail)

    # Return the first column
    return list(df[df.columns[0]])


def get_all_foods():
    # Read data
    df = get_data(food_by_fail)

    # Return the first column
    return list(df[df.columns[0]])


def get_all_provinces():
    # Read data
    df = get_data(prov_by_recs)

    # Return the first column
    return list(df[df.columns[0]])


def error(msg):
    print('\n%s' % msg)
    input('Press enter to continue.')
    print()


def print_options(options, type):
    usr = ''
    while not usr:
        print('Choose 2 %s:\n' % type)
        # Loop through the options
        for i, option in enumerate(options):
            if type != 'provinces':
                # Format the option
                option = format(option)
            # Print the option
            print('%s. %s' % (i + 1, option))

        usr = input('\nEnter the number of the 2 %s to compare, separated by a space: ' % type)

        # Clean the input
        usr = usr.strip()

        # Split the input
        usr = usr.split()

        # Check if there are 2 numbers
        if len(usr) != 2:
            usr = ''
            error('Please enter 2 numbers separated by a space.')
            continue

        try:
            # Convert the input to integers
            usr = [int(num) for num in usr]

            # Create a range of numbers from 1 to the length of the options
            rng = range(1, len(options) + 1)

            # Check if the numbers are within the range
            if not all(num in rng for num in usr):
                usr = ''
                error('Please enter 2 valid numbers from 1 to %s.' % len(options))
                continue

            # Check if the numbers are not the same
            if usr[0] == usr[1]:
                usr = ''
                error('Please enter 2 different numbers.')
                continue


        except:
            usr = ''
            error('Please enter 2 numbers separated by a space.')
            continue

    # Retrieve the options chosen
    options = [option for i, option in enumerate(options) if i + 1 in usr]

    return options


def get_type(usr):
    for _ in ['adulterants', 'foods']:
        if usr in _:
            return _

    return 'provinces'


def bar_cht(func, selected):
    # Read data
    df = func()

    # Retrieve the first column
    col1 = df[df.columns[0]]

    # If the column does not contain provinces
    if 'level' not in col1.name:
        # Format the column
        col1 = [format(_) for _ in list(col1)]

    # Update the first column
    df[df.columns[0]] = col1

    # Set the first column as the index
    df.set_index(df.columns[0], inplace=True)

    # Retrieve the selected columns
    df = df.loc[:, selected]

    # Clear the plot
    plt.clf()

    # Get the top 2 rows with the greatest values in the first column
    top2_first_col = df.nlargest(2, df.columns[0])

    # Get the top 2 rows with the greatest values in the second column
    top2_second_col = df.nlargest(2, df.columns[1])

    # Concatenate the two dataframes
    df = pd.concat([top2_first_col, top2_second_col])

    # Drop duplicates
    df = df.drop_duplicates()

    # Create a grouped bar chart
    bar_width = 0.4

    index = np.arange(len(df.index))

    # Create the bars
    bar1 = plt.bar(index, df[selected[0]], bar_width, label=selected[0])
    bar2 = plt.bar(index + bar_width, df[selected[1]], bar_width, label=selected[1])

    # Set the title
    title = ' and '.join(selected)

    try:
        # If the column does not contain provinces
        if 'level' not in df.iloc[0].name:
            title = ' and '.join([format(_) for _ in selected])
    except:
        try:
            # If the column does not contain provinces
            if 'level' not in df.iloc[0].index.name:
                title = ' and '.join([format(_) for _ in selected])
        except:
            pass

    # Set the title and labels
    plt.title('Comparison of %s' % title)
    plt.xlabel('Category')
    plt.ylabel('Count')

    # Set the x-axis labels
    plt.xticks(index + bar_width / 2, df.index)

    # Adding legend
    plt.legend()

    # Show the plot
    plt.show()


def comp_2():
    usr = input('Compare 2 adulterants, foods, or provinces? (a/f/p) ')
    if usr == 'a':
        adults = get_all_adults()
        selected = print_options(adults, get_type(usr))
        formatted = [format(_) for _ in selected]
        usr2 = input('Compare \'%s\' across foods or provinces? (f/p) ' % ' & '.join(formatted))
        if usr2 == 'f':
            bar_cht(adult_in_food, selected)
        elif usr2 == 'p':
            bar_cht(adult_in_prov, selected)
        else:
            print('Invalid input.')
            quit()
    elif usr == 'f':
        foods = get_all_foods()
        selected = print_options(foods, get_type(usr))
        formatted = [format(_) for _ in selected]
        usr2 = input('Compare \'%s\' across adulterants or provinces? (a/p) ' % ' & '.join(formatted))
        if usr2 == 'a':
            bar_cht(food_by_adult, selected)
        elif usr2 == 'p':
            bar_cht(food_in_prov, selected)
        else:
            print('Invalid input.')
            quit()
    elif usr == 'p':
        provinces = get_all_provinces()
        selected = print_options(provinces, get_type(usr))
        usr2 = input('Compare \'%s\' across adulterants or foods? (a/f) ' % ' & '.join(selected))
        if usr2 == 'a':
            bar_cht(prov_by_adult, selected)
        elif usr2 == 'f':
            bar_cht(prov_by_food, selected)
        else:
            print('Invalid input.')
            quit()
    else:
        print('Invalid input.')
        quit()
