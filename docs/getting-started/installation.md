# Installation

## Prerequisites

* Python 3.9 or higher
* Pip (Python package installer)
* Docker (optional, for containerized deployment)

## From Source

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Raoof128/SSPME.git
    cd SSPME/sspm_engine
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the package:**
    ```bash
    pip install -e .
    ```

## Using Docker

1.  **Build the image:**
    ```bash
    docker build -t sspm-engine .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 8000:8000 --env-file .env sspm-engine
    ```

