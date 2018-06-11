import os
import pandas as pd

#### TESTING CODE - IN CONSTRUCTION #####


# global variables
may_file = 'tr-info_15764685_20180611173136_CSV/tr-info_15764685_20180611173136.CSV'
june_file = 'tr-info_15764685_20180611173147_CSV/tr-info_15764685_20180611173147.CSV'
april_file = 'tr-info_15764685_20180611173205_CSV/tr-info_15764685_20180611173205.CSV'
categories_directory = 'categories/'

def import_category_file(filename):

    return [x.strip('\n') for x in open(filename, 'r').readlines()]

def import_categories(category_dir = categories_directory):
    
    return os.listdir(category_dir)

def read_banking_file(in_file, header = None):
    """
    opens a banking file
    """
    info_df = pd.read_csv(in_file, sep = ',', header = header)
    
    return info_df

def compute_statistics_category(info_df, ignore_indices, category_elements, index_cost = 10, description_index = 17):
    descriptors = info_df.iloc[:,description_index].apply(lambda x: x.lower())
    
    category_location_indices = []
    
    for descriptor, index in zip(descriptors, range(len(descriptors))):
        for category_element in category_elements:
            if category_element.lower() in descriptor:
                if index not in ignore_indices:
                    category_location_indices.append(index)
                    break
    

    total_expenses = sum(info_df.iloc[category_location_indices, index_cost])
    # test manual checking
    print(info_df.iloc[category_location_indices, [index_cost, description_index]])
    
    return total_expenses, category_location_indices

def main():
    # Import data
    ### Test - import april data
    info_df = read_banking_file(april_file)
    
    # Import categories
    category_dict = {}
    for category in import_categories():
        category_dict[category.strip('.txt')] = import_category_file(categories_directory + category)
    
    identified_rows = []
    for category, category_values in zip(category_dict.keys(), category_dict.values()):
        total_expenses, category_location_indices = compute_statistics_category(info_df, ignore_indices = identified_rows, category_elements = category_values)
        print(category, total_expenses)
        identified_rows += category_location_indices
    
    print('\n\n\n\n###################### Unidentified transaction ##################')
    print(info_df.iloc[list(set(range(len(info_df.index))) - set(identified_rows)), [10, 17]])
    

if __name__=="__main__":
    main()
