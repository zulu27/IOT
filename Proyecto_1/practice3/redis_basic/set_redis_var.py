from redis import Redis

# Connect to redis-db service
redis = Redis(host='redis-db', port=6379, decode_responses=True)

def set_config():
    try:
        # Setting a 'cool' variable
        key = "daily_quote"
        value = "'Code is like humor. When you have to explain it, it’s bad.' - Cory House"
        
        print(f"Connecting to redis-db service...")
        redis.set(key, value)
        
        print(f"Successfully set '{key}' to:")
        print(f"{value}")
        
        # Verify it's there
        saved = redis.get(key)
        print(f"\nVerification read: {saved}")
        
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        print("Make sure 'docker-compose up' is running and port 6379 is exposed.")

if __name__ == "__main__":
    set_config()
