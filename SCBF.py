# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 17:11:26 2024

@author: hha0010
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import PhotoImage

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier



feature_names = ['I column (in4)', 'Area column (in2)', 'I brace (in4)', 'Area brace (in2)','Number of Stories', 'PGA (in/s2)', 
                  'PGV (in/s)', 'PGD (in)']

target_names=['T1 (sec)','T2 (sec)','Max top displacemment (in)','Max base shear (kip)']



# Configuration options
configurations = ['Configuration_1', 'Configuration_2', 'Configuration_3']

# Function to update image based on selected configuration
def update_image(*args):
    selected_config = option_var.get()
    image_path = f"{selected_config}.png"
    try:
        image = PhotoImage(file=image_path)
        image_label.configure(image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
    except tk.TclError:
        print(f"Error: Image file '{image_path}' not found. Please check the file path and name.")

# Create a dictionary to hold the output widgets
output_labels = {}
def initialize_output_widgets():
    global output_texts
    for idx, feature in enumerate(target_names):

        frame = tk.Frame(output_frame, bg="lightgreen", relief=tk.RAISED, borderwidth=2)
        frame.grid(row=idx, column=2, sticky="ew")
        
        label = tk.Label(frame, text=feature, width=22, anchor='w', bg="lightgreen", font=('Arial', 10, 'bold'))
        label.pack(side=tk.LEFT, padx=5, pady=5)   
        
        
        
        output_label = tk.Label(frame, text="", font=('Arial', 10), bg="white", fg="blue", relief=tk.GROOVE, borderwidth=2, anchor='w', width=20)
        output_label.pack(fill=tk.X, padx=1, expand=False)
        
        output_labels[feature] = output_label

#create prediction function
def Output():
    try:
        selected_configuration = option_var.get()
        selected_model_name = model_var.get()
        
        Prediction_Model_Name_T1=selected_configuration+"_"+selected_model_name+"_T1"
        Prediction_Model_Name_T2=selected_configuration+"_"+selected_model_name+"_T2"
        Prediction_Model_Name_Max_Top_Dis=selected_configuration+"_"+selected_model_name+"_Max_Top_Dis"
        Prediction_Model_Name_Max_base_shear=selected_configuration+"_"+selected_model_name+"_Max_base_shear"
        # Get input values
        values = [float(entries[feature].get()) for feature in feature_names]
        print('values=',values)
        
        # # Create a DataFrame for prediction for T1 and T2
        feature_names_T1=['I column (in4)', 'Area column (in2)', 'I brace (in4)', 'Area brace (in2)','Number of Stories']
        values_T1=values[:5]
        print('values_T1=',values_T1)
        input_data = pd.DataFrame([values_T1], columns=feature_names_T1)
        # print('input_data=',input_data)
        
        # Load the model for T1
        model_file_path = Prediction_Model_Name_T1+'.pkcls'#'Modal_3.pkcls'
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        # Make prediction
        prediction_T1 = model.predict(input_data)


        # Load the model for T2
        model_file_path = Prediction_Model_Name_T2+'.pkcls'#'Modal_3.pkcls'
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        # Make prediction
        prediction_T2 = model.predict(input_data)

        # Display the result
        output_labels['T1 (sec)'].config(text=prediction_T1[0])
        output_labels['T2 (sec)'].config(text=prediction_T2[0])




        # # Create a DataFrame for prediction for Max top displacement
        feature_names_Max_top_Disp=['I column (in4)', 'Area column (in2)', 'I brace (in4)', 'Area brace (in2)','Number of Stories', 'PGA (in/s2)', 'PGV (in/s)', 'PGD (in)','T1', 'T2']
        values_Max_Top_Dis=values+[prediction_T1[0],prediction_T2[0]]
        print('values_Max_Top_Dis=',values_Max_Top_Dis)
        input_data = pd.DataFrame([values_Max_Top_Dis], columns=feature_names_Max_top_Disp)
        print('input_data=',input_data)

        # Load the model for Max_top_Disp
        model_file_path = Prediction_Model_Name_Max_Top_Dis+'.pkcls'#'Modal_3.pkcls'
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        # Make prediction
        prediction_Max_Top_Dis = model.predict(input_data)
        # Display the result
        output_labels['Max top displacemment (in)'].config(text=prediction_Max_Top_Dis[0])





        # # Create a DataFrame for prediction for Max Base Shear
        feature_names_Max_Base_Shear=['I column (in4)', 'Area column (in2)', 'I brace (in4)', 'Area brace (in2)','Number of Stories', 'PGA (in/s2)', 'PGV (in/s)', 'PGD (in)','T1', 'T2','Max Top Displacement']
        values_Max_Base_Shear=values+[prediction_T1[0],prediction_T2[0],prediction_Max_Top_Dis[0]]
        print('values_Max_Base_Shear=',values_Max_Base_Shear)
        input_data = pd.DataFrame([values_Max_Base_Shear], columns=feature_names_Max_Base_Shear)
        print('input_data=',input_data)

        # Load the model for Max Base Shear
        model_file_path = Prediction_Model_Name_Max_base_shear+'.pkcls'#'Modal_3.pkcls'
        with open(model_file_path, 'rb') as file:
            model = pickle.load(file)
        # Make prediction
        prediction_Max_Base_Shear = model.predict(input_data)

        
        # Display the result
        output_labels['Max base shear (kip)'].config(text=prediction_Max_Base_Shear[0])
        
    except ValueError as e:
        messagebox.showerror("Input error", "Please enter valid numeric values")


# # Create output function
# def Output():
#     for feature in target_names:
#         # Fetch the value from the entry widget and insert it into the output_label widget
#         entered_value = entries[feature].get()
#         output_labels[feature].config(text=entered_value)
        
        
        
        
# Create the main window
root = tk.Tk()
root.title("SCBF Seismic response Prediction")

# Configure rows and columns for the grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create an OptionMenu for selecting configurations with a constant width
option_var = tk.StringVar(root)
option_var.set(configurations[0])  # Set default selection

# Calculate the width based on the longest option
option_menu_configuration = tk.OptionMenu(root, option_var, *configurations, command=update_image)
option_menu_configuration.grid(row=0, column=0, padx=50, pady=5, sticky="w")


# Create a dropdown for model selection
model_var = tk.StringVar(root)
model_var.set("Random_Forest")  # Set the default option
model_options = ["Random_Forest", "AdaBoost", "XGBoost"]
option_menu_Artificial = tk.OptionMenu(root, model_var, *model_options)
option_menu_Artificial.grid(row=0, column=0, padx=50, pady=5, sticky="e")
# model_menu.pack(pady=10)


# Create a frame for input widgets (labels and entries)
input_frame = tk.Frame(root, bg="lightgreen")
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Create a dictionary to hold the entry widgets
entries = {}
for idx, feature in enumerate(feature_names):
    frame = tk.Frame(input_frame, bg="lightgreen", relief=tk.RAISED, borderwidth=2)
    frame.grid(row=idx, column=0, sticky="ew")
    
    label = tk.Label(frame, text=feature, width=20, anchor='w', bg="lightgreen", font=('Arial', 10, 'bold'))
    label.pack(side=tk.LEFT, padx=5, pady=5)
    
    entry = tk.Entry(frame, font=('Arial', 10))
    entry.pack(fill=tk.X, padx=5, expand=True)
    
    entries[feature] = entry

# Load and display the initial image
initial_image_path = f"{configurations[0]}.png"
try:
    image = PhotoImage(file=initial_image_path)
    image_label = tk.Label(root, image=image)
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.grid(row=0, column=1, rowspan=len(feature_names), padx=10, pady=10, sticky="nsew")
except tk.TclError:
    print(f"Error: Image file '{initial_image_path}' not found. Please check the file path and name.")








# Create a frame for input widgets (labels and entries)
output_frame = tk.Frame(root, bg="lightgreen")
output_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Initialize output widgets once
initialize_output_widgets()

# Create a button to trigger prediction
def on_hover(event):
    event.widget.config(bg='lightblue', fg='white')

def on_leave(event):
    event.widget.config(bg='blue', fg='white')
# Create a button with custom font, size, and colors
predict_button = tk.Button(root, text="Predict", font=('Helvetica', 14, 'bold'), bg='blue', fg='white', 
                         activebackground='darkblue', activeforeground='white', relief=tk.RAISED, bd=5, padx=10, pady=5, command=Output)
# predict_button = tk.Button(root, text="Predict", command=Output, font=('Arial', 12, 'bold'))
predict_button.grid(row=0, column=2, padx=50, pady=5)#, sticky="e")
# Add hover effect
predict_button.bind("<Enter>", on_hover)
predict_button.bind("<Leave>", on_leave)

# Run the GUI main loop
root.mainloop()