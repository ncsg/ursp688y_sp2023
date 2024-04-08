#A function to measure the distance and create a new 
#column with the weighted "customer" count. 
def dist_decay(origins, dest):
  #a dictionary to contain the lists of distances from each polygon
  dict_of_lists = {}
  for polygon in origins['geometry']:
    #a list to contain the distances from each polygon
    dist_list = []
    for point in dest['geometry']:
      dist_list.append(point.distance(polygon))
    #converting to kilometers
    dist_list = [num / 1000 for num in dist_list]
    #a new list for the weighted values
    dist_list_w = []
    #locations less than 2 kilometers away will have the value 1
    #while others will decay
    for num in dist_list:
      if num <= 2:
        dist_list_w.append(1)
      elif num > 2:
        dist_list_w.append(1/(num - 1))
    #summing the values for each origin polygon
    dist_list_w_sum = sum(dist_list_w)
    #creating a new dictionary key, and adding the sum
    #from above as the value
    dict_of_lists[polygon] = dist_list_w_sum
    #creating a new column that maps the results of the
    #dictionary above by the geometry column
    origins['Customers'] = origins['geometry'].map(dict_of_lists)
  #returns the original table with the new column
  return origins