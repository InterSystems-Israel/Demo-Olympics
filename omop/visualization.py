import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the provided Excel file
file_path = 'omop_data_formatted_excel/omop_data2.xlsx'
omop_data = pd.read_excel(file_path, None)  # Load all sheets into a dictionary

# Define a professional color palette
professional_colors = sns.color_palette("Set2", 10)  # You can choose other palettes like "Paired", "Set3", etc.

# Create a figure and a grid of subplots
fig, axs = plt.subplots(3, 2, figsize=(16, 12))  # 3 rows, 2 columns grid

# Age Distribution of Patients
age_distribution = omop_data['person']['year_of_birth'].apply(lambda x: 2024 - x).value_counts().sort_index()
axs[0, 0].bar(age_distribution.index, age_distribution.values, color=professional_colors)
axs[0, 0].set_xlabel('Age')
axs[0, 0].set_ylabel('Number of Patients')
axs[0, 0].set_title('Age Distribution of Patients')

# Gender Distribution of Patients as Pie Chart
gender_distribution = omop_data['person']['gender_concept_id'].value_counts().sort_index()
axs[0, 1].pie(gender_distribution.values, labels=gender_distribution.index.astype(str), autopct='%1.1f%%', startangle=90, colors=professional_colors)
axs[0, 1].set_title('Gender Distribution of Patients')

# Visit Frequency Distribution
visit_frequency = omop_data['visit_occurrence']['person_id'].value_counts()
bars = axs[1, 0].bar(visit_frequency.index, visit_frequency.values, color=professional_colors[:len(visit_frequency)])
axs[1, 0].set_xlabel('Number of Visits')
axs[1, 0].set_ylabel('Number of Patients')
axs[1, 0].set_title('Distribution of Visit Frequency')

# Most Common Medications
common_medications = omop_data['drug_exposure']['drug_concept_id'].value_counts().head(10).sort_index()
axs[1, 1].bar(common_medications.index.astype(str), common_medications.values, color=professional_colors)
axs[1, 1].set_xlabel('Drug Concept ID')
axs[1, 1].set_ylabel('Number of Prescriptions')
axs[1, 1].set_title('Top 10 Most Common Medications')
axs[1, 1].set_xticklabels(common_medications.index.astype(str), rotation=45)

# Number of Measurements per Patient
measurement_data = omop_data['measurement']
measurements_per_patient = measurement_data['person_id'].value_counts()
axs[2, 0].bar(measurements_per_patient.index.astype(str), measurements_per_patient.values, color=professional_colors)
axs[2, 0].set_xlabel('Patient ID')
axs[2, 0].set_ylabel('Number of Measurements')
axs[2, 0].set_title('Number of Measurements per Patient')
axs[2, 0].set_xticklabels(measurements_per_patient.index.astype(str), rotation=90)

# Top Conditions by Age Group
condition_occurrence = omop_data['condition_occurrence']
person = omop_data['person']
condition_person = condition_occurrence.merge(person[['person_id', 'year_of_birth']], on='person_id')
condition_person['age'] = 2024 - condition_person['year_of_birth']
age_group_conditions = condition_person.groupby(['age', 'condition_concept_id']).size().reset_index(name='count')
top_conditions_by_age_group = age_group_conditions.sort_values(['age', 'count'], ascending=[True, False]).groupby('age').head(5)
for age in top_conditions_by_age_group['age'].unique():
    age_group_data = top_conditions_by_age_group[top_conditions_by_age_group['age'] == age]
    axs[2, 1].plot(age_group_data['condition_concept_id'], age_group_data['count'], marker='o', label=f'Age {age}', color=professional_colors[age % len(professional_colors)])
axs[2, 1].set_xlabel('Condition Concept ID')
axs[2, 1].set_ylabel('Count')
axs[2, 1].set_title('Top Conditions by Age Group')
axs[2, 1].legend()
axs[2, 1].grid(True)

# Adjust layout
plt.tight_layout()
plt.show()
