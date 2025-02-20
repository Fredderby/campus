import streamlit as st
import pandas as pd
from datetime import datetime
from links import cred
import gspread
import os
import re

st.cache_resource()
def campus():
    try:
        client = cred()
        spreadsheet = client.open("campus_data")
        worksheet = spreadsheet.worksheet("atten")
        st.write("Network Active!")
    except gspread.SpreadsheetNotFound:
        st.error("Network Too Bad")
        return
    except gspread.WorksheetNotFound:
        st.error("Network Too Bad")
        return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
    
    with st.container(border=True):
        try:
            # Open and read the CSV file, specifying the encoding
            df = pd.read_csv("./data/campus.csv", encoding="ISO-8859-1")  # Replace with the correct encoding if needed
            col1, col2 = st.columns(2)
            
            # Get unique regions for the first selectbox
            unique_regions = df['Region'].unique()
            selected_region = col1.selectbox("Region", ["Select"] + list(unique_regions))
            
            # Filter campuses based on the selected region
            if selected_region != "Select":
                filtered_campuses = df[df['Region'] == selected_region]['Campus'].unique()
                selected_campus = col2.selectbox("Campus", ["Select"] + list(filtered_campuses))
            else:
                selected_campus = col2.selectbox("Campus", ["Select"])

            current_year = datetime.now().year
            mth = ["Select"] + [f"{datetime(2025, i, 1).strftime('%B')} {current_year}" for i in range(1, 13)]
            month = col1.selectbox("Month", mth, key="month2")
            fullname = col1.text_input("Name", key="fullname")
            if fullname:
                # Use a different key for formatted name storage
                formatted_name = fullname.strip().title()
                
                # Validate name format
                if not re.match(r"^[A-Za-z\- ]+$", formatted_name):
                    st.warning("Names should only contain letters, spaces, or hyphens (-).")
                else:
                    # Store formatted name in separate session state key
                    st.session_state.formatted_fullname = formatted_name

            select_date = datetime.now().isoformat(timespec='seconds')
            selected_date = col2.text_input("Date of Submission", value=select_date, disabled=True)

            baptized = col2.number_input("Number Baptized", min_value=0, value=0, key="bap")

        except UnicodeDecodeError as e:
            st.error(f"Error reading the file: {e}")
        except FileNotFoundError:
            st.error("The campus.csv file was not found.")
        except pd.errors.EmptyDataError:
            st.error("The campus.csv file is empty.")
        except pd.errors.ParserError:
            st.error("Error parsing the campus.csv file. Please check the file format.")
        except KeyError as e:
            st.error(f"Column not found in the CSV file: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    st.markdown("**ATTENDANCE SUMMARY**")
    with st.container(border=True):
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            bro = st.number_input("Brothers", min_value=0, value=0, key="bro1")
            sis = st.number_input("Sisters", min_value=0, value=0, key="bro2")
        with col2:
            boys = st.number_input("Children Boys", min_value=0, value=0, key="boys")
            girls = st.number_input("Children Girls", min_value=0, value=0, key="girls")
        with col3:
            vis_male = st.number_input("Visitors Male", min_value=0, value=0, key="vis1")
            vis_female = st.number_input("Visitors Female", min_value=0, value=0, key="vis2")
        with col4:
            off1 = st.number_input("1st Offering", min_value=0.0, value=0.0, key="off1")
            wkrs = st.number_input("Total Workers", min_value=0, value=0, key="worker12")
    submit = st.button("Submit")

if __name__ == "__main__":
    campus()