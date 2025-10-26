# 🤝 Contributing to MERCUR-E GitHub Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- **Report bugs** - Create detailed issue reports
- **Suggest features** - Propose new functionality
- **Improve documentation** - Fix typos, add examples
- **Write code** - Implement features or fix bugs
- **Review PRs** - Help review pull requests
- **Share feedback** - Tell us how you're using the bot

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/mercur-e.git
cd mercur-e
```

### 2. Set Up Development Environment

```bash
# Run setup
./setup.sh

# Create .env file
cp .env.example .env
# Edit .env with your test GitHub App credentials
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 💻 Development Workflow

### Running Locally

```bash
# Start the bot
./run_local.sh

# In another terminal, start ngrok
ngrok http 8000

# Update your test GitHub App webhook URL
```

### Code Style

We follow PEP 8 with some modifications:

```bash
# Format code with black
./venv/bin/black *.py

# Check with flake8
./venv/bin/flake8 *.py --max-line-length=100
```

### Adding a New Command

1. **Add handler in `commands.py`**:

```python
async def handle_mycommand(self, pr, issue, args):
    """Handle /mycommand"""
    try:
        # Your logic here
        return {
            'success': True,
            'message': '✅ Command executed successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'❌ Error: {str(e)}'
        }
```

2. **Register in `main.py`**:

```python
elif command == 'mycommand':
    result = await handler.handle_mycommand(pr, issue_obj, args)
```

3. **Update documentation**:
- Add to README.md command list
- Add examples to TESTING.md

### Adding MCP Tools

1. **Add tool in `mcp_server.py`**:

```python
@mcp.tool()
async def my_tool(param: str) -> Dict[str, Any]:
    """
    Tool description
    
    Args:
        param: Parameter description
    
    Returns:
        Result dictionary
    """
    return {"success": True, "data": "result"}
```

2. **Document in AI_INTEGRATION.md**

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test command parsing
curl -X POST http://localhost:8000/api/parse-comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "/test"}'
```

### Integration Testing

1. Create a test repository
2. Install your test GitHub App
3. Test commands on PRs and issues
4. Verify webhook deliveries in GitHub App settings

### Writing Tests (Future)

```python
# tests/test_commands.py
import pytest
from commands import CommandParser

def test_parse_command():
    commands = CommandParser.parse_commands("/test ci.yml")
    assert len(commands) == 1
    assert commands[0]['command'] == 'test'
```

## 📝 Commit Guidelines

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(commands): add /deploy command for automated deployments

Implements a new /deploy command that triggers deployment workflows
and posts status updates.

Closes #123
```

```
fix(webhook): handle missing installation_id gracefully

Previously, webhooks without installation_id would crash the bot.
Now we log a warning and continue processing.
```

## 🔍 Code Review Process

### Before Submitting PR

- [ ] Code follows style guidelines
- [ ] All tests pass (if applicable)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No sensitive data in commits

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How to test these changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

### Review Process

1. Automated checks run (if configured)
2. Maintainer reviews code
3. Feedback provided
4. Changes requested or approved
5. Merged to main branch

## 🐛 Bug Reports

### Good Bug Report Includes

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Logs**: Relevant log excerpts (remove sensitive data)

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: Ubuntu 22.04
- Python: 3.11
- Bot Version: 1.0.0

**Logs**
```
Paste relevant logs here
```

**Additional Context**
Any other information.
```

## 💡 Feature Requests

### Good Feature Request Includes

- **Use Case**: Why is this needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Examples**: Similar features elsewhere

### Feature Request Template

```markdown
**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
How should this feature work?

**Alternatives**
Other solutions you've considered.

**Additional Context**
Examples, mockups, etc.
```

## 📚 Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add screenshots where helpful
- Keep it up-to-date
- Test all examples

### Documentation Files

- `README.md` - Main documentation
- `QUICKSTART.md` - Quick setup guide
- `DEPLOYMENT.md` - Production deployment
- `TESTING.md` - Testing guide
- `AI_INTEGRATION.md` - AI integration
- `FAQ.md` - Common questions

## 🎨 Design Principles

### Code Principles

1. **Simplicity** - Keep it simple and readable
2. **Security** - Security first, always
3. **Reliability** - Handle errors gracefully
4. **Performance** - Optimize where it matters
5. **Maintainability** - Write code others can understand

### API Design

- Use clear, descriptive names
- Return consistent response formats
- Include proper error messages
- Document all endpoints

### Error Handling

```python
# Good
try:
    result = risky_operation()
    return {'success': True, 'data': result}
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return {'success': False, 'message': str(e)}

# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure
```

## 🔐 Security

### Security Guidelines

- Never commit secrets or keys
- Validate all inputs
- Use parameterized queries
- Keep dependencies updated
- Follow OWASP guidelines

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead, email: security@yourdomain.com

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## ❓ Questions?

- Check the FAQ.md
- Review existing issues
- Ask in discussions
- Contact maintainers

---

Thank you for contributing to MERCUR-E GitHub Bot! 🚀
