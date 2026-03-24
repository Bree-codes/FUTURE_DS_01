from data_cleaning import clean_data
from analysis import analyze_data
from visualization import create_visuals
from ai_insights import generate_ai_insights

def main():
    file_path = "/home/bree/Downloads/sales analysis/data.csv"

    df = clean_data(file_path)
    results = analyze_data(df)

    create_visuals(df, results)

    insights = generate_ai_insights(results)

    print("\n=== AI GENERATED INSIGHTS ===\n")
    print(insights)

if __name__ == "__main__":
    main()