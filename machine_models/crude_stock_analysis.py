import sys
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def analyse_crude_stock(year, month, criteria):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'Crude_Oil_Data.csv')
        df = pd.read_csv(csv_path)

        df['Date'] = pd.to_datetime(df['Date'].apply(lambda x: x.split(" ")[0]))
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month

        # Filter data for the given year and month
        yearly_data = df[df['Year'] == int(year)]
        monthly_data = yearly_data[yearly_data['Month'] == int(month)]

        # Plot data for the whole year
        plt.figure(figsize=(10, 6))
        plt.plot(yearly_data['Date'], yearly_data[criteria], label=f'{criteria} (Yearly)', color='blue')
        plt.title(f'{criteria} Trend for {year}')
        plt.xlabel('Date')
        plt.ylabel(criteria)
        plt.legend()
        yearly_plot_path = os.path.join(script_dir, f'plots/yearly_plot.png')
        plt.savefig(yearly_plot_path)
        plt.close()

        # Plot data for the selected month
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_data['Date'], monthly_data[criteria], label=f'{criteria} (Monthly)', color='green')
        plt.title(f'{criteria} Trend for {year} - {month}')
        plt.xlabel('Date')
        plt.ylabel(criteria)
        plt.legend()
        monthly_plot_path = os.path.join(script_dir, f'plots/monthly_plot.png')
        plt.savefig(monthly_plot_path)
        plt.close()

        return json.dumps({
            "yearly_plot": yearly_plot_path,
            "monthly_plot": monthly_plot_path
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    try:
        year = sys.argv[1]
        month = int(sys.argv[2])
        criteria = sys.argv[3]

        result = analyse_crude_stock(year, month, criteria)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
