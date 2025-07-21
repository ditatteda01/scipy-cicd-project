# SciPy CI/CD Project

A tutorial that builds a CI/CD pipeline with GitHub Actions. Demonstrates an automated CI/CD pipeline that performs quality testing, builds a Docker image as an artifact, and pushes it to the GitHub Container Registry.

## Features

- **Local Tools**: Providing a `Makefile` and `Dockerfile` for local development setup and testing. A `docker-compose.yml` template is also included for future project expansion.
- **Quality Tests**: We use `flake8` for linting, `pytest` for unit testing, and `black` for format checking.
- **Auto CI/CD**: The CI/CD pipeline is triggered automatically by a `git push` to the `main` branch. A feature branch workflow is also supported, and the CI/CD process is tested upon merging into `main`.


## Architecture

```
┌───────────────┐    ┌───────────────┐    ┌───────────────────┐    ┌────────┐
│     Local     │    │  Git Push to  │    │  GitHub Actions   │    │  GHCR  │  
│  Development  │───▶│  main branch  │───▶│  CI/CD Triggered  │───▶│        │
└───────────────┘    └───────────────┘    └───────────────────┘    └────────┘
        │                                        ▲
        │         ┌──────────────────┐           │ Merge triggers CI/CD
        └────────▶│  Git Push to     │───────────┘
                  │  feature branch  │
                  └──────────────────┘
```

## Build Instructions

### Prerequisites
- Docker installed and running
- Git installed
- GitHub Account
- Python3.8+ installed

### 1. Initialize Git Repository:
```bash
mkdir -p path/to/scipy-cicd-project
cd path/to/scipy-cicd-project
git init
git branch -M main  # rename the current branch's name to 'main'
```
### 2. Create .gitignore
Here we demonstrate how to create file with heredoc. In terminal, run the following command:
```bash
touch .gitignore            # create file
cat > .gitignore << 'EOF'   # start heredoc
# python build/runtime artifacts
__pycache__/
*py[cod]
*$py.class
*.so
*.egg
*.egg-info/
MANIFEST

# python virtual environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# build/distribution directories
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/var/
wheels/
.installed.cfg

# testing & coverage artifacts
.coverage
htmlcov/
.pytest_cache/

# os/editor specific
.DS_Store

# image files
*.png
*.jpg
*.jpeg
EOF     # when 'EOF' is captured, end heredoc
```

### 3. Setup Python Virtual Environment & Install Dependencies
```bash
# Create a virtual environment named '.venv'
python -m venv .venv

# Activate the environment
# On Unix like:
source .venv/bin/activate
# On Windows
.venv/Scripts/activate

# Install packages
pip install -r requirements.txt
```

### 4. Testing in Docker environment
```bash
# Build Docker image
make build

# Run quality checks (linting, unit test, format check)
make quality
```
**Note**: If you don't have `make` installed, you can run the raw Docker commands listed in `Makefile` instead.

## Project Structure
```
scipy-cicd-project/
├── .gitignore
├── .github/workflows/
│   └── ci-cd.yml       # Instruction for GitHub Actions
├── src/
│   ├── __init__.py 
│   └── data_processor.py
├── tests/
│   ├── __init__.py 
│   ├── conftest.py 
│   └── test_data_processor.py
├── main.py
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setting GitHub Repository
- Create a GitHub repo named `scipy-cicd-project`
- In repo → Settings → Actions → General
- Scroll to "Workflow permisssions"
- Select "Read and write permissions", this allows GitHub Actions to push the Docker image to GHCR
- Save changes

## Obtain Personal Access Token(PAT)
This token is for the authentication for the local git to push codes into GitHub repo through `https`.
- Account Settings → Developer Settings → Tokens (classic)
- Click: "Generate new token (classic)"
  - Name: `ghcr-push-token`
  - Scopes:
    - `write:packages`
    - `read:packages`
    - `delete:packages`
    - `repo`
- Save the Token

## Test CI/CD pipeline
```bash
# add remote connect to local git
git remote add origin https://github.com/<username>/scipy-cicd-project.git

# local commitment
git add .
git commit -m "Initial commit: SciPy CI/CD pipeline setup"

# push the current working branch to remote main branch through https
# You may need to enter your username and PAT for the first time push
git push -u origin main
```
- Go to GitHub → Actions tab
- Monitor the pipeline execution
- If succeeds:
    - Check GitHub Profile → Packages, for your pushed image
    - Image should be tagged as `latest`

## CI/CD with Feature Branches
1. Add new feature
- In `src/data_processor.py`:
    ```python
    def advanced_statistics(self):
        """Advanced statistical analysis"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        from scipy import stats
        
        # Perform additional statistical tests
        result = {
            'skewness_x': stats.skew(self.data['x']),
            'kurtosis_x': stats.kurtosis(self.data['x']),
            'skewness_y': stats.skew(self.data['y']),
            'kurtosis_y': stats.kurtosis(self.data['y'])
        }
        
        return result
    ```
- In `tests/test_data_processor.py`, add:
    ```python
    def test_advanced_statistics(self):
        """Test advanced statistical analysis"""
        self.processor.load_data()
        stats = self.processor.advanced_statistics()
        
        required_keys = ['skewness_x', 'kurtosis_x', 'skewness_y', 'kurtosis_y']
        for key in required_keys:
            assert key in stats
            assert isinstance(stats[key], (int, float))
    ```
2. Local Test
```bash
# Clean unused images
make clean

# Create new image and test
make build
make quality
```
3. Push to Remote Feature Branch
```bash
# Create and switch to a new feature branch as
# local working branch
git checkout -b feature/add-advanced-stats

# Commit the changes
git add .
git commit -m "feat: add advanced statistics function"

# Create a new feature branch in remote repo and push
# the local working branch to it
git push origin feature/add-advanced-stats
```
4. `Create Pull Request`
- On GitHub, you will see a prompt to create a pull request from your new branch. Click it
- Create the pull request, targeting the `main` branch
- Notice that the GitHub Actions pipeline runs automatically on the PR. This ensures the new code passes all quality checks before merging. No container is pushed at this stage
- Once all checks pass, you can merge the pull request into `main`
- After merging, the pipeline will run again on the `main` branch, and this time it will publish the new version of your Docker image to GHCR