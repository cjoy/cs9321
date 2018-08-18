#!/usr/bin/env python3
import pandas
import matplotlib.pyplot as plt


def main():
  dataframe = pandas.read_csv('dataset.csv')
  dataframe.groupby('species').mean().plot.bar(rot=0)
  plt.show()

if __name__ == '__main__':
  main()