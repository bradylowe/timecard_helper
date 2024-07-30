import streamlit as st
import random
import pandas as pd


def distribute_hours_two_projects(work_days):
    total_hours = work_days * 8
    proj_1_percent = random.uniform(0.735, 0.805)
    proj_2_percentage = 1 - proj_1_percent
    
    proj_1_hours = round(total_hours * proj_1_percent)
    proj_2_hours = total_hours - proj_1_hours
    
    proj_1_daily = [0] * work_days
    proj_2_daily = [0] * work_days

    for i in range(work_days):
        proj_1_daily[i] = round(random.uniform(3.5, 6.5) * 2) / 2
        proj_2_daily[i] = round((8 - proj_1_daily[i]) * 2) / 2
        
        if sum(proj_1_daily) > proj_1_hours:
            diff = sum(proj_1_daily) - proj_1_hours
            proj_1_daily[i] -= diff
            proj_2_daily[i] += diff
        elif sum(proj_2_daily) > proj_2_hours:
            diff = sum(proj_2_daily) - proj_2_hours
            proj_2_daily[i] -= diff
            proj_1_daily[i] += diff
            
        # Adjust if the constraints go beyond the allowed hours
        if proj_1_daily[i] < 0:
            proj_2_daily[i] += proj_1_daily[i]
            proj_1_daily[i] = 0
        if proj_2_daily[i] < 0:
            proj_1_daily[i] += proj_2_daily[i]
            proj_2_daily[i] = 0

    return proj_1_daily, proj_2_daily


def main():
    PROJECT_NAMES = ["LOS", "PTB"]

    st.title("Timecard Autofill")

    work_days = st.number_input("Number of working days", min_value=1, max_value=7, value=5)
    
    if st.button("Generate Timecard"):
        project_hours = distribute_hours_two_projects(work_days)

        data = {name: hours for name, hours in zip(PROJECT_NAMES, project_hours)}
        df = pd.DataFrame(data)
        df.loc['Total'] = df[PROJECT_NAMES].sum(axis=0)
        df['Totals'] = df.sum(axis=1)
        df.loc['Tot (%)'] = round(100.0 * df.loc['Total'] / df.loc['Total', 'Totals'], 2)
        st.dataframe(df)


if __name__ == '__main__':
    main()
