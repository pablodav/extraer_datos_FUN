
def create_dataframes_from_sections(text, keyword='Evento '):
    """Creating sections from text and return pandas dataframes of these

    Args:
        text (_type_): Text with a section keyword on an specific line
        keyword (str, optional): keyword for the section. Defaults to 'Evento '.

    Returns:
        list: list of dataframes
    """
    # Split the text into sections
    sections = text.split(keyword)

    # Initialize an empty list to hold the dataframes
    dataframes = []

    # Process each section
    for section in sections:
        # Split the section into lines
        lines = section.splitlines()
        
        # Use the first line as the "evento" data and the rest as the dataframe data
        evento = lines[0]
        # Split each line into columns and store the results in a list of lists
        data = [line.split() for line in lines[1:]]

        # Create a dataframe from the list of lists and add it to the list of dataframes
        df = pd.DataFrame(data)
        
        # Add the "evento" data as a new column
        df['evento'] = evento
        
        dataframes.append(df)

    return dataframes
