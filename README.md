### Take Home Interview- Store Monitoring

[Link](https://loopxyz.notion.site/Take-home-interview-Store-Monitoring-12664a3c7fdf472883a41457f0c9347d)


Requirements:
```
fastapi==0.95.0
uvicorn==0.21.1
databases==0.7.0
SQLAlchemy==2.0.8
```

Create a csvdb.db of all csv files.

Start serve:
```
uvicorn main:app --reload
```

API:
1. /trigger_report/ endpoint: generates a report from csv files
2. /get_report/ endpoint: creates a csv file in the root directory


#### Interpolation Logic Used:
Linear Interpolation of Expected Value
To find the expected value random variable simply multiply each value of the random variable by its probability and add the products. The expected value turns out to be the mean of the two times as probability distribution for every point in time between two intervals is supposed to be equak.
Hence between any two states of a machine, it can be extrapolated that the half-time,or here, expected value, turns out to be an expected value for the state change.
The problem reduces down to stacking of overplapping intervals on sequential adding of upcoming intervals.

Assuming only two states, 'active' and 'inactive', only activity hours are calculated(use ```return stat``` with /trigger_report/ endpoint to see) and inactive hours are calculated henceforth.
