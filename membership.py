import streamlit as st
import pandas as pd
from datetime import datetime
from links import cred
import gspread
import os
import re

st.cache_resource()
def member():
    try:
        client = cred()
        spreadsheet = client.open("campus_data")
        worksheet = spreadsheet.worksheet("mem")
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
            selected_region = col1.selectbox("Region", ["Select"] + list(unique_regions), key="region")
            
            # Filter campuses based on the selected region
            if selected_region != "Select":
                filtered_campuses = df[df['Region'] == selected_region]['Campus'].unique()
                selected_campus = col2.selectbox("Campus", ["Select"] + list(filtered_campuses), key="campus")
            else:
                selected_campus = col2.selectbox("Campus", ["Select"], key="campus")

            year = datetime.now().year
            period = col1.selectbox("Period", ["Select", f"First Quarter(Q1) {year}", f"Second Quarter(Q2) {year}", f"Third Quarter(Q3) {year}", f"Last Quarter(4) {year}" ], key="month")
            fullname = col1.text_input("Name", key="fullname", placeholder="Enter your name")
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
            selected_date = col2.text_input("Date of Submission", value=select_date, disabled=True, key="date")

            baptized = col2.text_input("", disabled=True,  key="bap", placeholder="Re-check entries before submission")

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

    st.markdown("**MEMBERSHIP SUMMARY**")
    with st.container(border=True):
        
        col1, col2, col3 = st.columns(3)
        with col1:
            bro = st.number_input("Brothers", min_value=0, value=0, key="broth23")
            sis = st.number_input("Sisters", min_value=0, value=0, key="sist78")
        with col2:
            boys = st.number_input("Children Boys", min_value=0, value=0, key="boy1")
            girls = st.number_input("Children Girls", min_value=0, value=0, key="girl2")
        with col3:
            wkrs_female = st.number_input("Workers Male", min_value=0, value=0, key="wkr2")
            wkrs_male = st.number_input("Workers Female", min_value=0, value=0, key="wkr1")

    submit = st.button("Submit")

    if submit:
        # Validation checks
        if selected_region == "Select":
            st.warning("Select a Region.")
            st.stop()
        if selected_campus == "Select":
            st.warning("Select a Campus.")
            st.stop()
        if period == "Select":
            st.warning("Select the period.")
            st.stop()
        if not fullname:
            st.warning("Enter your Name.")
            st.stop()
        
        # Prepare data for submission
        seers = [
            selected_date, selected_region, selected_campus, period, bro, sis, 
            boys, girls, wkrs_male, wkrs_female, fullname
        ]
        worksheet.append_row(seers)
        st.success("Successfully submitted")
        st.balloons()

        # Clear session state
        for key in st.session_state.keys():
            if key in ["region", "campus", "period", "fullname", "date", "brothers", "sisters", "boys", "girls", "wkrs_male", "wkrs_female"]:
                del st.session_state[key]

if __name__ == "__main__":
    member()