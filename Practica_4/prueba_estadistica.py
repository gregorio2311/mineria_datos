import pandas as pd
from scipy.stats import f_oneway, ttest_ind, kruskal
import numpy as np
data = pd.read_csv('Datos/Streaming_History_Audio.csv')

# Prepare the data
data['ms_played'] = pd.to_numeric(data['ms_played'], errors='coerce')
data['skipped'] = data['skipped'].astype(str)  # Ensure 'skipped' is treated as a string
data['reason_end'] = data['reason_end'].fillna('Unknown')  # Handle missing values

# Filter out invalid or zero play times
valid_data = data[data['ms_played'] > 0]

# ANOVA: Compare ms_played across different artists
anova_artists = valid_data.groupby('master_metadata_album_artist_name')['ms_played'].apply(list)
anova_result_artists = f_oneway(*anova_artists.values)

# ANOVA: Compare ms_played across different reason_end categories
anova_reasons = valid_data.groupby('reason_end')['ms_played'].apply(list)
anova_result_reasons = f_oneway(*anova_reasons.values)

# T-test: Compare ms_played for skipped vs. not skipped
skipped_group = valid_data[valid_data['skipped'] == 'True']['ms_played']
not_skipped_group = valid_data[valid_data['skipped'] == 'False']['ms_played']
ttest_result = ttest_ind(skipped_group, not_skipped_group, nan_policy='omit')

# Kruskal-Wallis: Compare ms_played across different artists
kruskal_artists = kruskal(*anova_artists.values)

# Kruskal-Wallis: Compare ms_played across different reason_end categories
kruskal_reasons = kruskal(*anova_reasons.values)

# Display the results
anova_artists_result_text = f"ANOVA (ms_played across artists): F = {anova_result_artists.statistic:.2f}, p = {anova_result_artists.pvalue:.3f}"
anova_reasons_result_text = f"ANOVA (ms_played across reason_end): F = {anova_result_reasons.statistic:.2f}, p = {anova_result_reasons.pvalue:.3f}"
ttest_result_text = f"T-Test (ms_played, skipped vs. not skipped): t = {ttest_result.statistic:.2f}, p = {ttest_result.pvalue:.3f}"
kruskal_artists_result_text = f"Kruskal-Wallis (ms_played across artists): H = {kruskal_artists.statistic:.2f}, p = {kruskal_artists.pvalue:.3f}"
kruskal_reasons_result_text = f"Kruskal-Wallis (ms_played across reason_end): H = {kruskal_reasons.statistic:.2f}, p = {kruskal_reasons.pvalue:.3f}"

# Display the results with explanations
print(anova_artists_result_text)
print("A low p-value suggests that there are significant differences in ms_played across different artists.\n")

print(anova_reasons_result_text)
print("A low p-value suggests that there are significant differences in ms_played across different reason_end categories.\n")

print(ttest_result_text)
print("A low p-value suggests that there is a significant difference in ms_played between skipped and not skipped tracks.\n")

print(kruskal_artists_result_text)
print("A low p-value suggests that there are significant differences in ms_played across different artists (non-parametric test).\n")

print(kruskal_reasons_result_text)
print("A low p-value suggests that there are significant differences in ms_played across different reason_end categories (non-parametric test).\n")
