import subprocess
import time

# run connection process (async)
def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries=0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host, "-U", "admin"],
                check=True,
                capture_output=True, text=True)
            if "accepting connection" in result.stdout:
                print("Postgres connected")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Postgres error: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay_seconds)
    print("Max retries has reached. Exiting...!")
    return False

if not wait_for_postgres(host="postgres"):
    exit(1)

#debugger
print('script running...!')

# configuration from init (source) postgreSQL
source_config = {
 'dbname': 'source_db',
 'user': 'admin',
 'password': 'admin',
 'host': 'postgres'}

# configuration from last (dest) postgreSQL
dest_config = {
 'dbname': 'jobs_db',
 'user': 'admin',
 'password': 'admin',
 'host': 'last_postgres'}

s_command = [ 'pg_dump',
 '-h', source_config['host'],
 '-U', source_config['user'],
 '-d', source_config['dbname'],
 '-f', 'data_dump.sql',
 '-w'
]

subprocess_env = dict(PGPASSWORD=source_config['password'])

# async process - source
subprocess.run(s_command, env=subprocess_env, check=True)

d_command = [ 'psql',
 '-h', dest_config['host'],
 '-U', dest_config['user'],
 '-d', dest_config['dbname'],
 '-a', '-f', 'data_dump.sql'
]

subprocess_env = dict(PGPASSWORD=dest_config['password'])

# async process - dest
subprocess.run(d_command, env=subprocess_env, check=True)

#debugger
print('Ending script...!')