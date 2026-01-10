# Dependency Manager Agent

**Purpose**: Automate installation, updating, and verification of project dependencies for both backend (Python) and frontend (Node.js).

**Capabilities**:
- Install Python dependencies from requirements.txt in virtual environment
- Install Node.js dependencies from package.json
- Update dependencies to latest compatible versions
- Verify dependency integrity and security
- Create/activate virtual environments
- Handle dependency conflicts

## Usage

### Install Backend Dependencies

```bash
# From project root
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
# From project root
cd frontend
npm install
```

### Update All Dependencies

```bash
# Backend
cd backend && source venv/bin/activate && pip install --upgrade -r requirements.txt

# Frontend
cd frontend && npm update
```

## Workflows

### 1. Fresh Project Setup

**Input**: Project with requirements.txt and package.json
**Steps**:
1. Check if virtual environment exists for backend
2. Create venv if missing: `python3 -m venv backend/venv`
3. Activate venv: `source backend/venv/bin/activate`
4. Install Python dependencies: `pip install -r backend/requirements.txt`
5. Install Node dependencies: `npm install` in frontend/
6. Verify installations: `pip list` and `npm list`

**Output**: All dependencies installed and verified

### 2. Dependency Update

**Input**: Updated requirements.txt or package.json
**Steps**:
1. For Python: `pip install --upgrade -r requirements.txt`
2. For Node: `npm update` or `npm install`
3. Run security audit: `pip check` and `npm audit`
4. Test application to verify compatibility

**Output**: Dependencies updated, security issues flagged

### 3. Add New Dependency

**Input**: New package name and version
**Steps**:
1. For Python: Add to requirements.txt, run `pip install package==version`
2. For Node: Run `npm install package@version --save`
3. Update lock files (pip freeze, package-lock.json)
4. Test application

**Output**: New dependency integrated

## Error Handling

**Virtual Environment Not Found**:
- Solution: Create with `python3 -m venv venv`

**Permission Errors**:
- Solution: Use `--user` flag or check directory permissions

**Conflicting Dependencies**:
- Solution: Use `pip install --upgrade --force-reinstall`

**Network Errors**:
- Solution: Check internet connection, try with `--retries 5`

## Integration

This agent can be invoked from:
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Pre-commit hooks
- Development environment setup scripts
- Automated testing workflows

## Configuration

Environment variables:
- `VIRTUAL_ENV`: Path to Python virtual environment
- `NPM_CONFIG_PREFIX`: Node package installation path

## Best Practices

1. **Always use virtual environments** for Python to avoid system package conflicts
2. **Pin dependency versions** in requirements.txt for reproducibility
3. **Run security audits** after updating dependencies
4. **Test thoroughly** after dependency changes
5. **Keep lock files in version control** (requirements.txt, package-lock.json)

## Related Skills

- `/skill:install-backend-deps` - Quick backend dependency installation
- `/skill:install-frontend-deps` - Quick frontend dependency installation
- `/skill:update-all-deps` - Update all project dependencies
- `/skill:audit-security` - Run security audit on dependencies
