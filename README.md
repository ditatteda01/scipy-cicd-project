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
- Python installed

### Initialize Git Repository `scipy-cicd-project`:
```bash
git init
git branch -M main  # rename the current branch's name to 'main'
```
### Create .gitignore
Here we demonstrate how to create file with heredoc. In terminal, run the following command:
```bash
touch .gitignore            # create file
cat > .gitignore << 'EOF'   # start heredoc
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
...
EOF     # when 'EOF' is captured, end heredoc
```

### Install Dependencies
Make sure the installation is on `.venv`.
```bash
pip install -r requirements.txt
```

### Testing in Docker environment
```bash
# Build Docker image
make build

# Run quality checks
make quality
```

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
- Select "Read and write permissions"
- Save changes

## Obtain Personal Access Token(PAT)
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

# push the current working branch to remote main branch. The PAT is used here
git push -u origin main
```
- Go to GitHub → Actions tab
- Monitor the pipeline execution
- If succeeds:
    - Check GitHub Profile → Packages, for your pushed image
    - Image should be tagged as `latest`

## CI/CD with Feature Branches
1. In `src/data_processor.py`, add:
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
2. In `tests/test_data_processor.py`, add:
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
3. Local Test
```bash
# Clean unused images
make clean

# Create new image and test
make build
make quality
```
4. Push to Remote Feature Branch
```bash
git add .
git commit -m "feat: add advanced statistics function"
git push origin feature
```
5. `Create Pull Request`
- Go to GitHub → Pull requests → New pull request
- Select your feature branch
- Create pull request and watch CI pipeline run on the PR
- Ensure all CI checks pass then approve the PR
- Full CI/CD triggered
- Image is pushed to GHCR

