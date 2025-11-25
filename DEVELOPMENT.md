# Band Music - Development Guide

## Development Environment Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git
- Code editor (VS Code recommended)

### Recommended VS Code Extensions
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- ESLint
- Prettier

## Project Setup

### Initial Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd band-music

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Or for pinned versions: pip install -r requirements-pinned.txt
cp .env.example .env

# Frontend setup
cd ../frontend
npm install
cp .env.example .env
```

## Development Workflow

### Starting Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --log-level debug
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Hot Reload
- Backend: Auto-reloads on Python file changes
- Frontend: Auto-reloads on TypeScript/TSX changes

## Code Structure Guidelines

### Backend

#### Adding a New Processor
1. Create processor file in appropriate directory:
   ```python
   # backend/src/new_module/processor.py
   from pathlib import Path
   from typing import Union
   from loguru import logger
   from ..config.settings import settings
   
   class NewProcessor:
       def __init__(self):
           logger.info("Initializing NewProcessor")
       
       def process(self, input_path: Union[str, Path]) -> Path:
           # Implementation
           pass
   ```

2. Add to pipeline if needed:
   ```python
   # backend/src/pipeline/new_pipeline.py
   from ..new_module.processor import NewProcessor
   
   class NewPipeline:
       def __init__(self):
           self.processor = NewProcessor()
   ```

3. Add endpoints in main.py:
   ```python
   @app.post("/api/new/upload")
   async def upload_new(file: UploadFile = File(...)):
       # Implementation
       pass
   ```

#### Adding New Settings
Edit `backend/src/config/settings.py`:
```python
class Settings(BaseSettings):
    # Add new setting
    new_setting: str = "default_value"
```

Then update `.env.example`:
```
NEW_SETTING=default_value
```

### Frontend

#### Adding a New Component
```tsx
// frontend/src/components/NewComponent.tsx
import React from 'react';

interface NewComponentProps {
  title: string;
}

const NewComponent: React.FC<NewComponentProps> = ({ title }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
    </div>
  );
};

export default NewComponent;
```

#### Adding New API Endpoints
Edit `frontend/src/services/api.ts`:
```typescript
export const bandMusicAPI = {
  // Add new endpoint
  newEndpoint: async (data: any): Promise<any> => {
    const response = await api.post('/api/new/endpoint', data);
    return response.data;
  },
};
```

## Testing

### Backend Testing

#### Unit Tests
```bash
cd backend
pytest tests/
```

#### Test Structure
```python
# backend/tests/test_processor.py
import pytest
from src.omr.processor import OMRProcessor

def test_omr_processor_init():
    processor = OMRProcessor()
    assert processor is not None

def test_process_image():
    processor = OMRProcessor()
    # Test implementation
```

#### Manual API Testing
```bash
# Test OMR upload
curl -X POST http://localhost:8000/api/omr/upload \
  -F "file=@test_sheet.png"

# Test AMT upload
curl -X POST http://localhost:8000/api/amt/upload \
  -F "file=@test_audio.mp3"
```

### Frontend Testing

#### Component Tests
```bash
cd frontend
npm test
```

#### Test Example
```typescript
// frontend/src/components/OMRConverter.test.tsx
import { render, screen } from '@testing-library/react';
import OMRConverter from './OMRConverter';

test('renders OMR converter', () => {
  render(<OMRConverter />);
  const heading = screen.getByText(/Sheet Music → Audio/i);
  expect(heading).toBeInTheDocument();
});
```

#### E2E Testing (Future)
- Cypress or Playwright
- Test full conversion workflows
- Mock API responses

## Debugging

### Backend Debugging

#### Using Debugger
Add breakpoint in code:
```python
import pdb; pdb.set_trace()
```

Or use VS Code debugger with launch.json:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

#### Logging
```python
from loguru import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

View logs:
```bash
tail -f backend/logs/app.log
```

### Frontend Debugging

#### Browser DevTools
- Console for errors
- Network tab for API calls
- React DevTools extension

#### Debug Logging
```typescript
console.log('Debug:', data);
console.error('Error:', error);
```

## Common Development Tasks

### Adding a New Library Dependency

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install new-library
# Update flexible requirements (recommended)
pip freeze > requirements.txt
# Or update pinned requirements
pip freeze > requirements-pinned.txt
```

**Frontend:**
```bash
cd frontend
npm install new-library
# Updates package.json automatically
```

### Database Migration (Future)
When adding database:
```bash
# Using Alembic
alembic init migrations
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

### API Documentation
FastAPI auto-generates docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Code Formatting

**Backend (Black):**
```bash
cd backend
pip install black
black src/
```

**Frontend (Prettier):**
```bash
cd frontend
npm install --save-dev prettier
npx prettier --write "src/**/*.{ts,tsx}"
```

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Cache repeated computations
- Stream large files
- Profile with cProfile:
  ```python
  import cProfile
  cProfile.run('function_to_profile()')
  ```

### Frontend
- Use React.memo for expensive components
- Implement virtual scrolling for large lists
- Code splitting with React.lazy
- Optimize images and assets

## Error Handling Best Practices

### Backend
```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise HTTPException(
        status_code=500,
        detail=f"Friendly error message: {str(e)}"
    )
```

### Frontend
```typescript
try {
  const response = await api.call();
  setData(response);
} catch (error: any) {
  console.error('API Error:', error);
  setError(error.response?.data?.detail || 'Unknown error');
}
```

## Git Workflow

### Branch Naming
- `feature/descriptive-name` - New features
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-fix` - Production hotfixes
- `refactor/component-name` - Code refactoring

### Commit Messages
```
type(scope): Brief description

Longer description if needed

- Bullet points for details
- Related issue: #123
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process
1. Create feature branch
2. Make changes
3. Write tests
4. Update documentation
5. Create PR with description
6. Address review comments
7. Merge to main

## CI/CD (Future)

### GitHub Actions Example
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## Deployment

### Docker Development
```dockerfile
# Dockerfile.dev
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
```

## Troubleshooting Development Issues

### Virtual Environment Issues
```bash
# Deactivate and recreate
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node Modules Issues
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Import Errors
- Check virtual environment is activated
- Verify PYTHONPATH includes project root
- Check for circular imports

## Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- music21: https://web.mit.edu/music21/doc/
- Oemer: https://github.com/BreezeWhite/oemer
- Basic Pitch: https://github.com/spotify/basic-pitch

### Community
- Stack Overflow
- GitHub Issues
- Discord/Slack channels (if available)

## Contributing Guidelines

### Code Review Checklist
- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log or print statements (use proper logging)
- [ ] Error handling implemented
- [ ] Type hints added (Python) / TypeScript types correct
- [ ] Performance considerations addressed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Screenshots (if applicable)

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] All tests pass
```

---

Happy coding! 🎵
