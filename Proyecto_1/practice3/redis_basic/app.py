from flask import Flask
from redis import Redis
import os

app = Flask(__name__)
# The hostname 'redis-db' matches the service name in docker-compose.yml
redis = Redis(host='redis-db', port=6379)

@app.route('/')
def hello():
    count = redis.incr('hits')
    
    # Read the custom variable (bytes) and decode
    quote = redis.get('daily_quote')
    if quote:
        quote = quote.decode('utf-8')
    else:
        quote = "No quote set yet! Run 'python3 set_redis_var.py'"
        
    return f'''
    <div style="font-family: sans-serif; text-align: center; padding: 20px;">
        <h1>Hello from Practice 3!</h1>
        <p>This page has been viewed <strong>{count}</strong> times.</p>
        <div style="margin-top: 20px; padding: 15px; background-color: #f0f8ff; border-radius: 8px; border: 1px solid #dae1e7;">
            <h3>Quote of the Day:</h3>
            <p style="font-style: italic; font-size: 1.2em;">"{quote}"</p>
        </div>
    </div>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)