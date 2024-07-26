def source_target_list_to_dict(list_items):
    """
    This function source_target_list_to_dict effectively maps the
    'source' values to the 'target' values from a list of dictionaries,
    where each dictionary has a 'source' and 'target' key.
    For example, given this input:
        list_items = [
            {'source': 'A', 'target': '1'},
            {'source': 'B', 'target': '2'},
            {'source': 'C', 'target': '3'}
            ]
        the function returns:
        {
            'A': '1',
            'B': '2',
            'C': '3'
        }
    :param list_items:
    :return:
    """
    column_name_dict = {}
    for source_target_item in list_items:
        column_name_dict[source_target_item['source']] = source_target_item['target']

    return column_name_dict