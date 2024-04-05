def find_index_higest_value(DataList : list):
    maximum_value = None
    position_of_max_value = None
    for data in range(len(DataList)):
        if maximum_value == None and position_of_max_value == None:
            maximum_value, position_of_max_value = DataList[data], data
        elif maximum_value < DataList[data]:
            maximum_value, position_of_max_value = DataList[data], data
        else:
            continue 
    return f"max : {maximum_value} \nposition : {position_of_max_value}"





if __name__ == '__main__':
    print(find_index_higest_value([1,2,1,7,5,6,4]))

