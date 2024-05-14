!pip install kaggle
!kaggle datasets download -d mohamedharris/supermart-grocery-sales-retail-analytics-dataset
!unzip supermart-grocery-sales-retail-analytics-dataset.zip

df = pd.read_csv('Supermart Grocery Sales - Retail Analytics Dataset.csv')

df = df.drop(columns=['State'])
df = df.drop(columns=['Order ID'])
df['Order Date'] = pd.to_datetime(df['Order Date'],format="mixed")

df = df.drop_duplicates()
