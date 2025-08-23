def reorder_and_format_dict(data: dict, column_order: list, enhance: bool = False) -> dict:
    """
    Reorder a dictionary's keys based on a preferred column order, 
    with an option to prettify key names.

    Args:
        data (dict): The dictionary to reorder.
        column_order (list): List of keys in the desired order.
        enhance (bool, optional): If True, formats keys by replacing underscores 
            with spaces, title-casing them, and renaming "id" to "ID".
            Defaults to False.

    Returns:
        dict: A new dictionary with reordered (and optionally formatted) keys.
    """
    prioritized_keys = [col for col in column_order if col in data]
    other_keys = [col for col in data if col not in prioritized_keys]
    output_dict = {k: data[k] for k in prioritized_keys + other_keys}

    if enhance:
        output_dict = {
            ("ID" if k.lower() == "id" else k.replace("_", " ").title()): v
            for k, v in output_dict.items()
        }

    return output_dict
