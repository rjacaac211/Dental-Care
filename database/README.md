# RJ Dental Care PH — Database

This folder contains the **PostgreSQL** setup used by **RJ Dental Care PH**, including:
- A Dockerfile to build a PostgreSQL container.
- An initialization script (`init.sql`) that creates the database schema for patients and appointments.

## Folder Structure

```
database/
├── Dockerfile    # Docker configuration for PostgreSQL
└── init.sql      # SQL script that sets up the initial schema
```

## How It Works

1. **Dockerfile**  
   - Inherits from the official `postgres:13` image.
   - Copies `init.sql` into `/docker-entrypoint-initdb.d/`, which is automatically run by PostgreSQL when the container starts for the first time.
   - Exposes port `5432` for PostgreSQL connections.

2. **init.sql**  
   - Defines two tables:  
     - **`patients`**: Stores patient information (`id`, `name`, `email`, `phone`, `created_at`).  
     - **`appointments`**: Stores appointment details (`id`, `patient_id`, `appointment_date`, `appointment_time`, `notes`, `created_at`).  
   - Includes a **foreign key** on `appointments.patient_id` referencing `patients(id)`.

## Usage

When used within the broader **RJ Dental Care PH** Docker Compose setup:
1. The PostgreSQL container automatically runs `init.sql` once to create the required tables.
2. The backend connects to this database at `postgres://<user>:<password>@database:5432/rj_dental_db` (or as specified by your environment variables).

If you need to customize the schema or seed data, modify `init.sql` before building and running the container.

---

**Note**: For production usage, remember to set secure passwords and consider using persistent volumes to ensure data is not lost when the container restarts.
