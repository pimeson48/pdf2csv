"""Main module."""

import PySimpleGUI as sg
import os.path
import tabula

# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns
left_col = [[sg.Text('pdf folder'), sg.In(size=(40,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(50,20), key='-FILE LIST-')],
            [sg.Exit()]]

# Second window layout...2 columns
right_col = [[sg.Text('pdf selected:')],
             [sg.Text(size=(50,2), key='-PDF-')],
             [sg.Text('')], # spacer
             [sg.Text('csv to be created:')],
             [sg.Text(size=(50,2), key='-CSV-')],
             [sg.Text('')], # spacer
             [sg.Submit(button_text="Convert pdf", key='-SUBMIT-')],
             [sg.Text('')], # spacer
             [sg.Text(size=(50,2), key='-CONVERT-')]]

# ----- Full layout -----
layout = [[sg.Column(left_col), sg.VSeperator(), sg.Column(right_col)]]

#--------------------------------- Create Window ---------------------------------
window = sg.Window('pdf to csv', layout)

# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == '-FOLDER-':                     # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)      # get list of files in folder
        except:
            file_list = []

        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".pdf"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            pdf = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-PDF-'].update(pdf)

            csv = os.path.join(values['-FOLDER-'], 'converted.csv')
            window['-CSV-'].update(csv)
        except:
            pass        # something weird happened making the full filename

    # TODO add option to change csv file location before creating file
    if event == '-SUBMIT-':
        # create blank csv file if it doesn't exist already
        open(csv, 'a').close()

        # convert pdf to csv
        try:
            tabula.convert_into(pdf, csv, output_format="csv", pages="all", stream=True)
            window['-CONVERT-'].update('converstion complete')
            break
        except:
            print("pdf to csv conversion failed! try another pdf...")

    # TODO open converted csv to show completion

# --------------------------------- Close & Exit ---------------------------------
window.close()
raise SystemExit
