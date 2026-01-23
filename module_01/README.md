# Module 1 Homework: Docker & SQL

This repository contains solutions for the Module 1 homework assignment covering Docker, SQL, and Terraform.

## Table of Contents
- [Question 1: Understanding Docker Images](#question-1-understanding-docker-images)
- [Question 2: Understanding Docker Networking](#question-2-understanding-docker-networking)
- [Question 3: Counting Short Trips](#question-3-counting-short-trips)
- [Question 4: Longest Trip for Each Day](#question-4-longest-trip-for-each-day)
- [Question 5: Biggest Pickup Zone](#question-5-biggest-pickup-zone)
- [Question 6: Largest Tip](#question-6-largest-tip)
- [Question 7: Terraform Workflow](#question-7-terraform-workflow)

---

## Question 1: Understanding Docker Images

**Question:** What's the version of pip in the python:3.13 image?

**Command:**
```bash
docker run -it --entrypoint bash python:3.13
pip --version
```

**Output:**
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

**Answer:** `25.3`

---

## Question 2: Understanding Docker Networking

**Question:** Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?


```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

**Explanation:**
In Docker Compose, containers can communicate with each other using service names as hostnames. The internal port (5432) is used for inter-container communication, not the mapped external port (5433).

**Answer:** `db:5432`

**Reasoning:**
- **Hostname:** `db` (the service name in docker-compose.yaml)
- **Port:** `5432` (the internal PostgreSQL port, not the host-mapped port 5433)

---

## Question 3: Counting Short Trips

**Question:** For trips in November 2025, how many trips had a trip_distance ≤ 1 mile?

**SQL Query:**
```sql
SELECT COUNT(*) 
FROM green_tripdata
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**Answer:** `8007`

---

## Question 4: Longest Trip for Each Day

**Question:** Which was the pickup day with the longest trip distance (excluding trip_distance ≥ 100 miles)?

**SQL Query:**
```sql
SELECT
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;
```

**Answer:** `2025-11-14`

---

## Question 5: Biggest Pickup Zone

**Question:** Which pickup zone had the largest total_amount on November 18th, 2025?

**SQL Query:**
```sql
SELECT
    z."Zone",
    SUM(g.total_amount) AS revenue
FROM taxi_zones z
JOIN green_taxi_trips g
    ON z."LocationID" = g."PULocationID"
WHERE g.lpep_pickup_datetime >= '2025-11-18'
  AND g.lpep_pickup_datetime <  '2025-11-19'
GROUP BY z."Zone"
ORDER BY revenue DESC
LIMIT 1;
```

**Answer:** `East Harlem North`

---

## Question 6: Largest Tip

**Question:** For passengers picked up in "East Harlem North" in November 2025, which drop-off zone had the largest tip?

**SQL Query:**
```sql
SELECT
    zdo."Zone" AS dropoff_zone,
    MAX(g.tip_amount) AS largest_tip
FROM green_taxi_trips g
JOIN taxi_zones zdo
    ON zdo."LocationID" = g."DOLocationID"
JOIN taxi_zones zpu
    ON zpu."LocationID" = g."PULocationID"
WHERE zpu."Zone" = 'East Harlem North'
  AND g.lpep_pickup_datetime >= '2025-11-01'
  AND g.lpep_pickup_datetime <  '2025-12-01'
GROUP BY zdo."Zone"
ORDER BY largest_tip DESC
LIMIT 1;
```

**Answer:** `Yorkville West`

---

## Question 7: Terraform Workflow

**Question:** Which sequence describes the workflow for:
1. Downloading provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

**Explanation:**
- `terraform init` - Initializes Terraform, downloads provider plugins, and sets up the backend
- `terraform apply -auto-approve` - Generates an execution plan and automatically applies it without manual confirmation
- `terraform destroy` - Removes all resources managed by Terraform

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed
- Terraform (for Question 7)

### Running the Environment

1. Start the Docker containers:
```bash
docker-compose up -d
```
2. Run the ingest_data.py script:
```bash
uv run ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --year=2025 \
  --month=11
```
3. Access pgAdmin at `http://localhost:8085`
   - Email: admin@admin.com
   - Password: root

4. Connect to PostgreSQL from pgAdmin:
   - Host: `pgdatabase`
   - Port: `5432`
   - Username: `root`
   - Password: `root`
---

## Author
Piero Alcantara

## Date
January 2026
