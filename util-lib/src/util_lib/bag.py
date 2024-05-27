import json
from datetime import datetime

import jsonschema
import pandas as pd
import requests
from jsonschema import validate

local_ca_certificate_file_path='/opt/conda/lib/python3.10/site-packages/certifi/cacert.pem'

# def reverse_date_format(input_date):
#     # Parse the input date string to a datetime object
#     input_date_obj = datetime.strptime(input_date, '%d-%m-%Y')
#
#     # Format the datetime object as a string in the desired format
#     output_date = input_date_obj.strftime('%Y-%m-%d')
#
#     return output_date


# def show_named_plotly_colours():
#     """
#     function to display to user the colours to match plotly's named
#     css colours.
#
#     Reference:
#         #https://community.plotly.com/t/plotly-colours-list/11730/3
#
#     Returns:
#         plotly dataframe with cell colour to match named colour name
#
#     """
#     s='''
#         aliceblue, antiquewhite, aqua, aquamarine, azure,
#         beige, bisque, black, blanchedalmond, blue,
#         blueviolet, brown, burlywood, cadetblue,
#         chartreuse, chocolate, coral, cornflowerblue,
#         cornsilk, crimson, cyan, darkblue, darkcyan,
#         darkgoldenrod, darkgray, darkgrey, darkgreen,
#         darkkhaki, darkmagenta, darkolivegreen, darkorange,
#         darkorchid, darkred, darksalmon, darkseagreen,
#         darkslateblue, darkslategray, darkslategrey,
#         darkturquoise, darkviolet, deeppink, deepskyblue,
#         dimgray, dimgrey, dodgerblue, firebrick,
#         floralwhite, forestgreen, fuchsia, gainsboro,
#         ghostwhite, gold, goldenrod, gray, grey, green,
#         greenyellow, honeydew, hotpink, indianred, indigo,
#         ivory, khaki, lavender, lavenderblush, lawngreen,
#         lemonchiffon, lightblue, lightcoral, lightcyan,
#         lightgoldenrodyellow, lightgray, lightgrey,
#         lightgreen, lightpink, lightsalmon, lightseagreen,
#         lightskyblue, lightslategray, lightslategrey,
#         lightsteelblue, lightyellow, lime, limegreen,
#         linen, magenta, maroon, mediumaquamarine,
#         mediumblue, mediumorchid, mediumpurple,
#         mediumseagreen, mediumslateblue, mediumspringgreen,
#         mediumturquoise, mediumvioletred, midnightblue,
#         mintcream, mistyrose, moccasin, navajowhite, navy,
#         oldlace, olive, olivedrab, orange, orangered,
#         orchid, palegoldenrod, palegreen, paleturquoise,
#         palevioletred, papayawhip, peachpuff, peru, pink,
#         plum, powderblue, purple, red, rosybrown,
#         royalblue, saddlebrown, salmon, sandybrown,
#         seagreen, seashell, sienna, silver, skyblue,
#         slateblue, slategray, slategrey, snow, springgreen,
#         steelblue, tan, teal, thistle, tomato, turquoise,
#         violet, wheat, white, whitesmoke, yellow,
#         yellowgreen
#         '''
#     li=s.split(',')
#     li=[l.replace('\n','') for l in li]
#     li=[l.replace(' ','') for l in li]
#
#     import pandas as pd
#     import plotly.graph_objects as go
#
#     df=pd.DataFrame.from_dict({'colour': li})
#     fig = go.Figure(data=[go.Table(
#         header=dict(
#             values=["Plotly Named CSS colours"],
#             line_color='black', fill_color='white',
#             align='center', font=dict(color='black', size=14)
#         ),
#         cells=dict(
#             values=[df.colour],
#             line_color=[df.colour], fill_color=[df.colour],
#             align='center', font=dict(color='black', size=11)
#         ))
#     ])
#
#     fig.show()

# class Month(IntEnum):
#     JANUARY = 1
#     FEBRUARY = 2
#     MARCH = 3
#     APRIL = 4
#     MAY = 5
#     JUNE = 6
#     JULY = 7
#     AUGUST = 8
#     SEPTEMBER = 9
#     OCTOBER = 10
#     NOVEMBER = 11
#     DECEMBER = 12


# def print_full(x):
#     pd.set_option('display.max_rows', len(x))
#     print(x)
#     pd.reset_option('display.max_rows')


# def fill_zeros(df, column):
#     """
#     Walks through a pandas dataframe column and sets any zero values to the previous non-zero value in the column.
#
#     Args:
#         df (pandas.DataFrame): The dataframe to modify.
#         column (str): The name of the column to modify.
#
#     Returns:
#         None. The function modifies the dataframe in place.
#     """
#     df[column] = df[column].replace(0, pd.NA).fillna(method='ffill')


def convert_dtypes_obj_to_strings(df):
    object_columns = list(df.select_dtypes(include='object').columns)

    for object_column in object_columns:
        df[object_column] = df[object_column].astype(str)

    return df



def hello():
    print("hello")


def debug_this(debug_enabled, message, preview_only=True):
    if debug_enabled:
        if isinstance(message, pd.DataFrame):
            if preview_only:
                display(message.head())
            else:
                display(message)
        else:
            print(message)


def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')


def download_file(from_path, to_path):
    print("downloaded from: " + from_path)

    response = requests.get(from_path, verify=local_ca_certificate_file_path)

    with open(to_path, 'wb') as file:
        file.write(response.content)


def source_target_list_to_dict(list_items):
    colummn_name_dict = {}
    for source_target_item in list_items:
        colummn_name_dict[source_target_item['source']] = source_target_item['target']

    return colummn_name_dict

def get_json_content_from_file(file):
    with open(file, 'r') as file:
        json_content = json.load(file)
    return json_content

def validate_json_file_against_schema_file(json_data_file, json_schema_file):

    json_content = get_json_content_from_file(json_data_file)
    json_schema = get_json_content_from_file(json_schema_file)

    try:
        validate(instance=json_content, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "JSON document is invalid and does not conform to the schema."
        return False, err

    message = "JSON document is valid."
    return True, message

def create_me_a_dict_of_using(key, value, source):
    dict_item = {}
    for item in source:
        dict_item[item[key]] = item[value]

    return dict_item


def read_worksheet_into_df(file_specification):

    worksheet_df = pd.read_excel(file_specification['dest_filepath'],
                                 sheet_name=file_specification['worksheet_name'],
                                 skiprows=file_specification['num_rows_from_top_to_ignore'],
                                 header=0,
                                 nrows=file_specification['num_rows_to_read'],
                                 usecols=file_specification['column_range_to_read']
                                 )
    return worksheet_df


def set_object_columns_to_string(input_df):
    df_to_process = input_df.copy()

    object_columns_list = list(df_to_process.select_dtypes(include='object').columns)

    for object_column in object_columns_list:
        df_to_process[object_column] = df_to_process[object_column].astype(str)

    return df_to_process


def remove_timestamp(date_string):
    return str(datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date())


def mutate_safely(function):
    """
    There are a limited number of pandas transformations that mutate the dataframe
    in place.  These are limited to modifying a column of data (insert, delete or update);
    assigning to the index or column attributes and modifying the values directly in the dataframe.

    The purpose of this function is to perform the mutating functions idempotently by mutating
    local deep copies of dataframes and returning new copies back to the caller.

    We use Python decorators to adopt this pattern without polluting our core functions. We
    decorate any function with @mutate_safely and write a function that mutates the given
    dataframe directly without returning it.
    """
    def mutate(df, **params):
        df = df.copy()
        function(df, **params)
        return df
    return mutate

def rename_columns(df, column_mapping):
    return df.rename(columns=column_mapping, inplace=False)

def inner_join_with(df, df_to_join, columns_to_include, join_key):
    return pd.merge(df, df_to_join[columns_to_include], on=join_key, how='inner')

@mutate_safely
def add_week_ending_date(df, default_date, existing_week_end_date_col_name):

    def calculate_week_ending_date(week_ending, default_date="2020-19-03"):
        if week_ending == '19 Mar 2020 to 20 Mar 2020':
            return default_date
        else:
            if len(week_ending) > 10:
                return remove_timestamp(week_ending)
            else:
                return week_ending
    # Can be: Week Ends (Friday) or: Week_end_Date
    df['Week Ending Date'] = df[existing_week_end_date_col_name].apply(lambda raw_week_ending_date: calculate_week_ending_date(raw_week_ending_date, default_date))
    return

@mutate_safely
def convert_column_to_string(df, colname):
    df[colname] = df[colname].astype(str)
    return

def extract_only_this_year(df, year, rows_to_read):
    tmp_df = df[94:rows_to_read].reset_index(drop=True, inplace=False)
    assert len(tmp_df) == 52, "We must have a complete year of 52 registration weeks for 2022."
    return tmp_df

def extract_columns_of_interest(df):
    return df.iloc[0:, [0, 3]]

def convert_datatypes(df):
    return df.convert_dtypes()

@mutate_safely
def extract_and_cast_as_int(df, column):
    df[column] = df[column].astype(str).str.replace("[a-zA-Z]", "", regex=True).astype(float).astype(int)
    return