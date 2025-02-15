# Use the official PostgreSQL 13 image as a base
FROM postgres:13

# Copy the initialization SQL script into the image
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
