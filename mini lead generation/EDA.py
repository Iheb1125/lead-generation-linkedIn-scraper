# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Read the cleaned dataset
cleaned_data = pd.read_csv('linkedin.csv')

# Summary statistics for categorical data
summary_statistics = cleaned_data.describe(include='object')
print(summary_statistics)

# Distribution of industries
plt.figure(figsize=(12, 6))
sns.countplot(y='Industry', data=cleaned_data, order=cleaned_data['Industry'].value_counts().index)
plt.title('Distribution of Industries')
plt.xlabel('Count')
plt.ylabel('Industry')
plt.show()



# Distribution of locations
plt.figure(figsize=(12, 6))
sns.countplot(y='Location', data=cleaned_data, order=cleaned_data['Location'].value_counts().index[:10])
plt.title('Top 10 Locations of Companies')
plt.xlabel('Count')
plt.ylabel('Location')
plt.show()

# Word cloud for firm names
industry_names = ' '.join(cleaned_data['Industry'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(industry_names)
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Industries')
plt.axis('off')
plt.show()
