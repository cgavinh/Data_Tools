# Imports
from ipywidgets import interactive
import seaborn as sns
import ipywidgets as widgets
import matplotlib.pyplot as plt


class missing_vals:
    def __init__(self, df):
        self.df = df
        self.isna_df = self.find_isna_cols()
        self.make_widget()

    def find_isna_cols(self):
        isna_d = {'Feature': [],
                  'dtype': [],
                  'Missing Vals': [],
                  'Percentage': []}
        for key in self.df:
            if self.df[key].isna().sum() > 0:
                isna_d['Feature'].append(key)
                isna_d['dtype'].append(self.df[key].dtype)
                isna_d['Missing Vals'].append(self.df[key].isna().sum())
                isna_d['Percentage'].append(self.df[key].isna().sum() / len(self.df))
        return pd.DataFrame(isna_d)

    def list_isna(self):
        display(self.isna_df)

    def unique(self, column):
        print(self.isna_df.loc[self.isna_df['Feature'] == column])
        print()
        print(self.df[column].unique())

    def make_widget(self):
        dd = widgets.Dropdown(options=self.isna_df['Feature'].unique(),
                              value=self.isna_df['Feature'].unique()[0],
                              description="Feature")
        self.w = interactive(self.unique, column=dd)

class Countplot:
    def __init__(self, df):
        self.df = df
        self.make_widget()

    def draw_countplot(self, column, hue, check_hue):
        sns.set(font_scale=1.2)
        if check_hue == False:
            p = sns.countplot(data=self.df, x=column)
            if len(self.df[column].unique()) > 4:
                p.tick_params(axis='x', rotation=60)
        else:
            p = sns.countplot(data=self.df, x=column, hue=hue)
            if len(self.df[column].unique()) > 4:
                p.tick_params(axis='x', rotation=60)
        plt.figure(figsize=(20, 20))

    def make_widget(self):
        cat_columns = [column for column in self.df.columns if self.df[column].dtype == 'object']
        dd = widgets.Dropdown(options=cat_columns,
                              value=cat_columns[0],
                              description="Feature")
        dd_hue = widgets.Dropdown(options=cat_columns,
                              value=cat_columns[0],
                              description="Hue")
        check_hue = widgets.Checkbox(False, description='By Hue?')

        self.w = interactive(self.draw_countplot, column=dd, hue=dd_hue, check_hue=check_hue)

class simple_box:
    def __init__(self, df):
        self.df = df
        self.make_widget()

    def draw_bar(self, column):
        sns.set(font_scale=1.2)
        p = sns.boxplot(data=self.df, y = column)
        plt.figure(figsize=(20, 20))

    def make_widget(self):
        num_columns = [column for column in self.df.columns if ((self.df[column].dtype == 'int64')|(self.df[column].dtype == 'float'))]
        dd = widgets.Dropdown(options=num_columns,
                              value=num_columns[0],
                              description="Feature")
        """dd_hue = widgets.Dropdown(options=num_columns,
                                  value=num_columns[0],
                                  description="Hue")
        check_hue = widgets.Checkbox(False, description='By Hue?')"""

        self.w = interactive(self.draw_bar, column=dd)
