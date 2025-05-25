# Align-Analytics-engineering-Assessment-
Assessment for Analytics Engineering done By Carlton

This project outlines the steps to build and test dbt models using Docker. It includes data loading, model creation, testing, documentation, and deployment best practices.

---

## Prerequisites

Ensure the following tools are installed on your local machine:

- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Git](https://git-scm.com/downloads/mac)
- [Visual Studio Code](https://code.visualstudio.com/)

---

## Setup Instructions

- Download the project files to your local machine.
- Start the Docker daemon.
- Open the project folder in VS Code.

---

## Docker Commands

- **Build Docker image**:  
 
- Run `docker build -t dbt_project .` to build the Docker image
- Run `docker run -it -v $(pwd):/app dbt_project` to start the container and mount the project directory
- Run `dbt --version` to verify dbt is installed and working
- Run `dbt debug` to confirm the `profiles.yml` is correctly configured and the database connection works
- Run `dbt seed` to load the `.csv` seed files into the database
- Navigate to the `/models/dim/` folder and edit `dim_patients.sql` to define the patient dimension model
- Navigate to the `/models/fct/` folder and edit `fct_patient_claims.sql` to define the fact model for patient claims
- Add tests and documentation in `schema.yml`:
    - Include column- and model-level tests such as `not_null`, `unique`, etc.
    - Write clear documentation for each model and its columns
- Run `dbt test` to execute the defined tests
- Run `dbt run` to build all dbt models


