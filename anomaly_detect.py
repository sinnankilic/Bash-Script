import pandas as pd

def prepare_graph_data():
    df = pd.read_csv('data/requestlogs.logs.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    
    df['hour'] = df['timestamp'].dt.floor('H')

  
    summary = df.groupby('hour').agg(
        total_requests=('timestamp', 'count'),
        error_count=('status', lambda x: (x >= 400).sum()),
        avg_latency=('latency', 'mean')
    ).reset_index()

    return summary


