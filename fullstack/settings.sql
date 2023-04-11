CREATE DATABASE workoutbuddy;
CREATE USER workoutbuddyuser WITH PASSWORD 'workoutbuddy';
ALTER DATABASE workoutbuddy OWNER TO workoutbuddyuser;
GRANT USAGE, CREATE ON SCHEMA public TO workoutbuddyuser;