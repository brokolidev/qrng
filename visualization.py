from qiskit.visualization import plot_histogram
 
counts1 = {'00': 499, '11': 501}
counts2 = {'00': 511, '11': 489}
data = [counts1, counts2]
 
legend = ['First execution', 'Second execution']
title = 'New histogram'
figsize = (10,10)
color=['crimson','midnightblue']
plot_histogram(data, filename='new_hist.png')
 
hist = plot_histogram(data)
hist.savefig('new_hist.png')