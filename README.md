# Food Data Analysis Program

This Python program is designed to analyze food data and generate pie charts to visualize the distribution of various categories. The program uses `matplotlib` for plotting, `numpy` for numerical operations, `pandas` for data manipulation, and `pluralizer` for text processing.

## Features

The program includes the following functions:

- `get_data(func)`: Reads data from an Excel file named after the function calling it, located in the `data` directory.
- `rename_categories(df)`: Renames categories in the DataFrame by combining the first two columns.
- `create_other_category(df, x='x', y='perc', threshold=3)`: Groups categories that make up a small portion of the total into an 'Other' category.
- `pie_cht(df, title, fname, x='x', y='perc', subfolder=None)`: Generates a pie chart from the DataFrame and saves it as a PNG file in the `charts` directory.
- `loc_by_pct()`, `food_by_pct()`, `adult_by_pct()`, `food_by_fail()`, `adult_by_fail()`, `prov_by_food_pct()`, `prov_by_food_count()`, `prov_by_recs()`: These functions read data, process it, and generate pie charts to visualize the distribution of sampled location types, food types, adulterant types, and provinces by various metrics.
- `format_title(title)`: Formats the title for the pie chart.
- `food_by_adult()`, `adult_in_food()`, `prov_by_food()`, `food_in_prov()`, `prov_by_adult()`, `adult_in_prov()`, `adult_in_all_food()`, `food_by_all_adult()`, `food_by_all_prov()`, `prov_by_all_food()`, `adult_in_all_prov()`, `prov_by_all_adult()`: These functions read data, process it, and generate pie charts to visualize the distribution of food types and adulterant types in various categories.

## Usage

To use this program, you need to have Python installed along with the `matplotlib`, `numpy`, `pandas`, and `pluralizer` libraries. You can install these libraries using pip:

```bash
pip install matplotlib numpy pandas pluralizer
```

Once the libraries are installed, you can run the program with Python:

```bash
python main.py
```

The program will read the data, perform the analysis, and generate the pie charts, which will be saved in the `charts` directory.
