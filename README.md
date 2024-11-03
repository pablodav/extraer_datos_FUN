# extraer_datos_FUN
scripts para extraer datos de la FUN Uy y poder ser analizados en Business Analytics

# Prompt:

It is required to extract the .pdf file with swimming competition results.
The output needs to be formated for ml, data analytics ready tools, so something that a machine or BI understands.
The data is complex, the data in the .pdf has some many different formats because it includes different types of categories, styles, by swimmer, by team, and many other things, data groups like: "Evento <N> <Hombre/Mujeres/Niñas/Niños> <Ages> <style>" where the data has "Nombre, Edad, Equipo,,Tiempo" but when its for "Hombres or Mujeres" it adds "Puntos" at the end.
Or then we have the type of event "Mixto", where the "Equipo" is the name of the 4 swimmers, format like "1) swimmer name, <M/W><Age> where M is for men and W Woman"2) Swimmer name, <M/W><Age>,"3) Swimmer Name <M/N><Age>"4) Swimmer Name <M/W><Age>" <N> Team Name,,<A>,"time Points". Also for "Mixto" with similar format you can find "Combinado Relevo" with similar format as Mixto. And also Other <Style> Relevo with same format as "Mixto".

Some times has incorrect format with xNN where the x should not be there.

The script should be python script.
Should be a different pieces of modules and code for easy debug, modification and fixes.
Should has an output in machine possible read, like .csv or sqlite.
It must allow debugging and allow me to continue the chat with claude.ai to fix the future issues.
Please analyze the file example in this project

# Claude:

I'll help you create a Python script to extract and structure this swimming competition data. Given the complexity, let's break it down into modules.

First, let's analyze the structure and create a plan:



Now, let's create a test script to verify the functionality:

This implementation includes:

1. A main module with:
   - Data classes for organizing swimmer and relay team data
   - SwimmingDataExtractor class that handles:
     - Event extraction
     - Individual swimmer data processing
     - Relay team data processing
     - SQLite database output
     - CSV file output

2. A test module to verify the functionality

To use this code:

1. First, save both files in your project directory
2. Install required dependencies (standard library only in this case)
3. Modify the text processing patterns if needed based on your specific data format
4. Use the extractor like this:

```python
extractor = SwimmingDataExtractor(your_text_content)
extractor.extract_events()

# Save to SQLite
extractor.save_to_sqlite('swimming_results.db')

# Save to CSV
extractor.save_to_csv('swimming_results')
```

The output will be:
- A SQLite database with tables for events, swimmers, relay teams, and relay swimmers