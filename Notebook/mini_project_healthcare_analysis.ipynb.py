import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1200)
pd.set_option("display.max_rows", None)

df = pd.read_csv("Health Care_Patient_survey_source.csv") 


# Cleaning data types, numeric columns contain text. Detect mixed numeric columns. 

# print(df.dtypes)

numeric_cols = [
    "Patient Survey Star Rating",
    "Answer Percent",
    "Linear Mean Value",
    "Number of Completed Surveys",
    "Survey Response Rate Percent"
]

for col in numeric_cols: 
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

#print(df[numeric_cols].isnull().sum())

#convert date columns 
if "Measure Start Date" in df.columns: 
    df["Measure Start Date"] = pd.to_datetime(df["Measure Start Date"], errors= "coerce")

if "Measure End Date" in df.columns: 
    df["Measure End Date"] = pd.to_datetime(df["Measure End Date"], errors ="coerce")


# print(df.dtypes)


# Hospital information repeats many times, i created a summary table with the number of completed surveys and survey response rate percent
# I dropped the duplicated Provider ID's because there's no duplicates between Provider ID and Measure ID, meaning they repeat the same Number of Completed Surveys.
# Would like to see how the coaches approached the grain row or eliminated the duplicates. 


hospital_cols = [
   "Provider ID",
    "Hospital Name",
    "City",
    "State",
    "County Name",
    "Number of Completed Surveys",
    "Survey Response Rate Percent",
    "Patient Survey Star Rating"
]

hospital_df = (
    df[hospital_cols]
    .drop_duplicates(subset=["Provider ID"])
)

print("\nHospital Summary Table:")
print(hospital_df)



# To confirm i have the right grain row(i wanted to see it) _ Method to get to the grain data.
"""
#Another survey check 

survey_check = (
    df.groupby(["Provider ID", "Hospital Name"])["Number of Completed Surveys"]
    .nunique()
    .reset_index(name="solo_counts")
)
print("HEY!!!!!")
print(survey_check["solo_counts"].value_counts())


Suggestion for any dataset: 
df.columns 
df.head(10)
df["Provider ID"].nunique()
print(df.duplicated().sum())
print("rows:", len(df))
df.duplicated(["Provider ID","Measure ID"]).sum() (if i get a zero here means that  is one hospital per measure per answer)
print(df.duplicated(["Provider ID","Measure ID","Number of Completed Surveys"]).sum())

print(df.groupby("Provider ID")["Number of Completed Surveys"].nunique().sort_values(ascending=False).head())
print(df[["Provider ID","Number of Completed Surveys"]])
print(df.groupby("Provider ID").size().head())
print(df.groupby("Provider ID")["Survey Response Rate Percent"].nunique().sort_values(ascending=False).head()) 
"""

# No. 1 == Number of Surveys Completed by different Hospitals 

surveys_by_hospital = (
    hospital_df[
        ["Provider ID", "Hospital Name", "City", "State", "Number of Completed Surveys"]
    ]
    .sort_values("Number of Completed Surveys", ascending=False)
    .head(10)
)

print("\n===========================================")
print("1. NUMBER OF SURVEYS COMPLETED BY HOSPITAL") 
print("===========================================")
print(surveys_by_hospital) 


# No. 2 == Survey Response rate based on Measure id. Plot Measure ID vs Response Percentage where the data will be per Hospital.  
# response rate percent repeats many rows, Just keep one provider id, measure id. 

hospital_measure_rrate = ( 
    df[
        ["Provider ID", "Hospital Name", "Measure ID", "Survey Response Rate Percent"]
    ]
    .dropna(subset=["Survey Response Rate Percent"])
)

# interpretation: Average response rate by Measure ID across Hospitals

measure_response_avg = (
    hospital_measure_rrate
    .groupby("Measure ID", as_index=False)["Survey Response Rate Percent"]
    .mean()
    .sort_values("Survey Response Rate Percent", ascending=False)
)
print("\n==============================================")
print("2. AVERAGE SURVEY RESPONSE RATE BY MEASURE ID")
print("=================================================")
print(measure_response_avg)

""""
plt.figure(figsize=(12, 6))
plt.bar(measure_response_avg["Measure ID"], measure_response_avg["Survey Response Rate Percent"])
plt.title("Average Survey Response Rate by Measure ID")
plt.xlabel("Measure ID")
plt.ylabel("Average Survey Response Rate Percent")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
"""

# Question 3 - Top 3 Counties which have the highest survey rate
top_3_counties = (
    hospital_df.groupby("County Name", as_index=False)["Survey Response Rate Percent"]
    .mean()
    .dropna()
    .sort_values("Survey Response Rate Percent", ascending=False)
    .head(3)
)


print("\n==============================================")
print("3. TOP 3 COUNTIES")
print("================================================")
print(top_3_counties)

# Question 4 - 	Top 10 hospitals based on Survey Response Rating  

top_10_hospitals_rating = ( 
    hospital_df
    .dropna(subset="Survey Response Rate Percent")
    .sort_values("Survey Response Rate Percent", ascending=False)
    .head(10)
)

print("\n==============================================")
print("4. TOP 10 HOSPITALS BY SURVEY STAR RATING")
print("================================================")
print(top_10_hospitals_rating.to_string(index=False))


# Question 5 - County and city wise hospital rating through drill down report(BI) 

county_city_hospital_rating = ( 
    top_10_hospitals_rating[
        ["County Name", "City","Hospital Name", "Patient Survey Star Rating"]  
    ]
    .dropna(subset=["County Name", "City", "Hospital Name", "Patient Survey Star Rating"])
    .sort_values(
        ["County Name", "City", "Patient Survey Star Rating", "Hospital Name"],
        ascending=[True, True, False, True]
    )
    .copy()
)


print("\n=========================================================")
print("5. COUNTY -> CITY -> HOSPITAL RATING DATA_DRILL BI")
print("=========================================================")
print(county_city_hospital_rating.head(10))

#county_city_hospital_rating.to_csv("pbi_healthcarefile.csv", index=False)
print("n\File Saved: pbi_healthcarefile.csv")

# Question 6 - List the hospitals which are in same city 


same_city_hospitals = (
    hospital_df
    .groupby(["City", "State"], as_index=False)["Hospital Name"]
    .agg(
        Hospital_Count="count",
        Hospitals=lambda x:", ".join(sorted(set(x)))
    )   
    .query("Hospital_Count > 1")
    .sort_values("Hospital_Count", ascending=False)
    .head(10)
   
)

#same_city_hospitals.columns = ["City", "State","Hospital Count", "Hospitals"]
#same_city_hospitals = same_city_hospitals[same_city_hospitals["Hospital Count"]>1]
#same_city_hospitals = same_city_hospitals.sort_values("Hospital Count", ascending=False)

print("\n=========================================================")
print("6. HOSPITALS IN THE SAME CITY")
print("=========================================================")
print(same_city_hospitals)

# Was trying this way

""""
same_city_hospitals = (
    hospital_df
    .groupby(["City", "State"])["Hospital Name"]
    .count()
    .sort_values(ascending=False)
    .reset_index()
)

print(same_city_hospitals)
"""
# Question 7 - Total Survey Response rate by all the Hospitals 
# Two Ways - Simple average: each hospital counts equally or Weighted Average: Hospitals with more completed surveys count more. 

# Simple Average 
Survey_Response_Rate_Simple = hospital_df["Survey Response Rate Percent"].mean()

print("\n=========================================================")
print("7A. SIMPLE AVERAGE SURVEY RESPONSE RATE ACROSS ALL HOSPITALS")
print("=========================================================")
print(Survey_Response_Rate_Simple)

# Weighted Average
weighted_df = hospital_df.dropna(subset=["Survey Response Rate Percent", "Number of Completed Surveys"]).copy()

Overall_weighted = (
    (weighted_df["Survey Response Rate Percent"] * weighted_df["Number of Completed Surveys"]).sum()
    /weighted_df["Number of Completed Surveys"].sum()
)

print("\n=========================================================")
print("7B. WEIGHTED SURVEY RESPONSE RATE ACROSS ALL HOSPITALS")
print("=========================================================")
print(Overall_weighted)

#Question 8 - Build a report that will give me some new insight from data. 
#Do hospitals with higher response rates also have higher patient survey star ratings?

response_rate_df =(
    hospital_df[
        [
            "Provider ID",
            "Hospital Name",
            "City",
            "State",
            "County Name",
            "Survey Response Rate Percent"
        ]
    ]
    .dropna(subset=["Survey Response Rate Percent"])

) 

survey_rating_df =(
    hospital_df[ 
        [   "Provider ID",
            "Patient Survey Star Rating"
        ]
    ]
    .dropna(subset=["Patient Survey Star Rating"])
)

response_rating = (
    response_rate_df
    .merge(survey_rating_df, on="Provider ID", how="inner")
    .sort_values(
        by=["Patient Survey Star Rating", "Survey Response Rate Percent"], 
        ascending=[False, False])
)

correlation = response_rating[
    ["Patient Survey Star Rating", "Survey Response Rate Percent"]
].corr().iloc[0,1]


print("\n=========================================================")
print("QUESTION 8 - RESPONSE RATE VS STAR RATING")
print("=========================================================")
print(response_rating.head(20))

print("\nCorrelation between response rate and star rating:")
print(correlation)


#response_rating.to_csv("bi_more_insights.csv", index=False)
