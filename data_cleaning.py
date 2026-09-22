import pandas as pd

# -----------------------------------------------------------------------------
# 1. DATA LOADING & INITIAL AUDIT
# -----------------------------------------------------------------------------
# Первичный анализ и загрузка данных из Google Drive

raw_file_path = 'final_international_sales_with_nan.xlsx'
df = pd.read_excel(raw_file_path)

# Оценка объема, типов данных и доли пропусков (%)
df.head(10)
df.info()
null_percent = (df.isnull().mean() * 100).round(1)
print("Missing values (%):\n", null_percent)

# Создание резервной копии перед обработкой
df_backup = df.copy()

# -----------------------------------------------------------------------------
# 2. DATE STANDARDIZATION & REORDERING
# -----------------------------------------------------------------------------
# Чистим даты, форматируем в единый вид YYYY-MM-DD (без времени)
df['clean_date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
df['clean_date'] = pd.to_datetime(df['clean_date']).dt.date

print("Min date:", df['clean_date'].min())
print("Max date:", df['clean_date'].max())
print("Null dates count:", df['clean_date'].isna().sum())

# Замена колонки Date на очищенную clean_date и перемещение ее на 1-е место
df = df.drop(columns=['Date'])
df = df.rename(columns={'clean_date': 'Date'})
cols = ['Date'] + [col for col in df.columns if col != 'Date']
df = df[cols]

# -----------------------------------------------------------------------------
# 3. CATEGORICAL DATA IMPUTATION (Department)
# -----------------------------------------------------------------------------
# В колонке Department вместо пропусков ставим Unknown
df['Department'] = df['Department'].fillna('Unknown')
print("Department distribution:\n", df['Department'].value_counts(dropna=False))

# -----------------------------------------------------------------------------
# 4. PRICE PARSING & NUMERIC CONVERSION
# -----------------------------------------------------------------------------
# Описание столбцов Raw_Price и Quantity до очистки
df[['Raw_Price', 'Quantity']].describe()

# Превращаем всё в строку для строковой очистки
df['Raw_Price'] = df['Raw_Price'].astype(str)

# Очистка: убираем префиксы "Price:", знаки $, буквенный код GBP и лишние пробелы
df['Raw_Price'] = df['Raw_Price'].str.replace('Price:', '', case=False)
df['Raw_Price'] = df['Raw_Price'].str.replace('$', '', regex=False)
df['Raw_Price'] = df['Raw_Price'].str.replace('GBP', '', case=False)
df['Raw_Price'] = df['Raw_Price'].str.strip()

# Превращаем очищенный текст в числа и удаляем некорректные записи (NaNs)
df['Raw_Price'] = pd.to_numeric(df['Raw_Price'], errors='coerce')
df = df.dropna(subset=['Raw_Price'])

# -----------------------------------------------------------------------------
# 5. MANAGER IMPUTATION & STATS AUDIT
# -----------------------------------------------------------------------------
# Заменяем пропуски в менеджерах на Unknown
df['Manager'] = df['Manager'].fillna('Unknown')

# Считаем количество записей и доли (%) по менеджерам
counts = df['Manager'].value_counts(dropna=False)
percentages = df['Manager'].value_counts(dropna=False, normalize=True) * 100
manager_stats = pd.concat([counts, percentages], axis=1)
print("Manager stats (%):\n", manager_stats.round(1))

# -----------------------------------------------------------------------------
# 6. FEATURE ENGINEERING (Revenue & Customer Type)
# -----------------------------------------------------------------------------
# Переименовываем Raw_Price в Price и рассчитываем итоговую выручку (Revenue)
df = df.rename(columns={'Raw_Price': 'Price'})
df['Revenue'] = df['Price'] * df['Quantity']

# Создаем колонку с маркировкой типа клиента (CARD vs GUEST) из Customer_ID
df['Customer_Type'] = df['Customer_ID'].astype(str).str.split('-').str[0]
print("Customer types distribution:\n", df['Customer_Type'].value_counts())

# -----------------------------------------------------------------------------
# 7. AUTOMATED REPORTING & EXCEL EXPORT
# -----------------------------------------------------------------------------
# Функция для генерации сводных отчетов по направлениям с расчетом доли выручки (%)
def get_share_report(groupby_column):
    report = df.groupby(groupby_column)['Revenue'].sum().reset_index()
    total_revenue = report['Revenue'].sum()
    report['Share (%)'] = ((report['Revenue'] / total_revenue) * 100).round(1)
    report = report.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
    return report

# Генерируем 4 отчета
pivot_manager = get_share_report('Manager')
pivot_dept = get_share_report('Department')
pivot_city = get_share_report('City_Store')
pivot_cust_type = get_share_report('Customer_Type')

# Сохраняем очищенный набор данных и агрегации в отдельные листы Excel
report_path = 'final_sales_report.xlsx'
with pd.ExcelWriter(report_path) as writer:
    df.to_excel(writer, sheet_name='Clean_Data', index=False)
    pivot_manager.to_excel(writer, sheet_name='By_Manager', index=False)
    pivot_dept.to_excel(writer, sheet_name='By_Department', index=False)
    pivot_city.to_excel(writer, sheet_name='By_City', index=False)
    pivot_cust_type.to_excel(writer, sheet_name='By_Customer_Type', index=False)

print("Data processing & Excel export completed successfully!")
