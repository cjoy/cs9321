#!/usr/bin/env python3
import pandas
import matplotlib.pyplot as plt


def main():
  dataframe = pandas.read_csv('dataset.csv')
  df_1a = dataframe.query("species == 'Iris-setosa'").plot.scatter(x='sepal_length', y='sepal_width', label='setosa')
  df_2a = dataframe.query("species == 'Iris-versicolor'").plot.scatter(x='sepal_length', y='sepal_width', label='versicolor', color='green', ax=df_1a)
  dataframe.query("species == 'Iris-virginica'").plot.scatter(x='sepal_length', y='sepal_width', label='virginica', color='red',  ax=df_2a)
  df_1b = dataframe.query("species == 'Iris-setosa'").plot.scatter(x='petal_length', y='petal_width', label='setosa')
  df_2b = dataframe.query("species == 'Iris-versicolor'").plot.scatter(x='petal_length', y='petal_width', label='versicolor', color='green', ax=df_1b)
  dataframe.query("species == 'Iris-virginica'").plot.scatter(x='petal_length', y='petal_width', label='virginica', color='red',  ax=df_2b)
  plt.show()

if __name__ == '__main__':
  main()