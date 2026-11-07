from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(r'D:\PhotonUser\Shameer\Capstone\data\raw\Metro_Interstate_Traffic_Volume.csv')
OUTPUT_DIR = Path(r'D:\PhotonUser\Shameer\Capstone\phase1\output')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['hour'] = df['date_time'].dt.hour
    df['day_of_week'] = df['date_time'].dt.day_name()
    return df


def plot_hourly_traffic(df: pd.DataFrame):
    hourly = df.groupby('hour', as_index=False)['traffic_volume'].mean().sort_values('hour')
    plt.figure(figsize=(10, 5))
    plt.plot(hourly['hour'], hourly['traffic_volume'], color='navy', marker='o')
    plt.title('Average Traffic Volume by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Traffic Volume')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'hourly_traffic_line.png', dpi=300)
    plt.close()


def plot_day_of_week(df: pd.DataFrame):
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = (
        df.groupby('day_of_week', observed=False)['traffic_volume']
        .mean().reindex(weekday_order)
    )
    plt.figure(figsize=(10, 5))
    daily.plot(kind='bar', color='steelblue')
    plt.title('Average Traffic Volume by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Average Traffic Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'day_of_week_traffic.png', dpi=300)
    plt.close()


def plot_weather_traffic(df: pd.DataFrame):
    weather = df.groupby('weather_main', as_index=False)['traffic_volume'].mean().sort_values('traffic_volume', ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(weather['weather_main'], weather['traffic_volume'], color='darkorange')
    plt.title('Average Traffic Volume by Weather Condition')
    plt.xlabel('Weather Condition')
    plt.ylabel('Average Traffic Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'weather_traffic_bar.png', dpi=300)
    plt.close()


def plot_temperature_vs_traffic(df: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    plt.scatter(df['temp'], df['traffic_volume'], alpha=0.3, s=12, color='forestgreen')
    plt.title('Temperature vs Traffic Volume')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Traffic Volume')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'temp_vs_traffic.png', dpi=300)
    plt.close()


def plot_holiday_traffic(df: pd.DataFrame):
    holiday_map = df['holiday'].fillna('None')
    holiday_group = df.assign(holiday_flag=holiday_map.eq('None').map({True: 'Non-Holiday', False: 'Holiday'}))
    summary = holiday_group.groupby('holiday_flag', as_index=False)['traffic_volume'].mean()
    plt.figure(figsize=(7, 5))
    plt.bar(summary['holiday_flag'], summary['traffic_volume'], color=['steelblue', 'tomato'])
    plt.title('Average Traffic Volume: Holiday vs Non-Holiday')
    plt.xlabel('Category')
    plt.ylabel('Average Traffic Volume')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'holiday_traffic.png', dpi=300)
    plt.close()


def main():
    df = load_data()
    plot_hourly_traffic(df)
    plot_day_of_week(df)
    plot_weather_traffic(df)
    plot_temperature_vs_traffic(df)
    plot_holiday_traffic(df)
    print('Dashboard visuals generated in:', OUTPUT_DIR)


if __name__ == '__main__':
    main()
