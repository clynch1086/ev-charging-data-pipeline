#This is the final script to run everything automatically

from load_raw_data import load_raw_data
from run_transformation import run_transformation  
from dashboard import show_dashboard

def run_pipeline():
    
#Load raw CSV data
    print("Starting EV Charging Data Pipeline...\n")
    load_raw_data()
    print("Raw data stage complete.\n")

#Run SQL transformation 
    run_transformation()
    print("Transformation stage complete.\n")

#Show dashboard 
    print("Launching dashboard...\n")
    show_dashboard()
    print("Dashboard displayed successfully.\n")

    print("Pipeline executed successfully.")

if __name__ == "__main__":
    run_pipeline()