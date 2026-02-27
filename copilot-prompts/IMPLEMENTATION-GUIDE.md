# Getting Started Implementation Guide

Quick-start guide for implementing Copilot prompt templates and CI/CD integration.

## Phase 1: Setup (Day 1-2)

### Step 1: Understand Your Tech Stack
Document what your team uses:

```
Programming Languages: JavaScript, Python, Java
Frameworks: Express.js, FastAPI, Spring Boot
Test Frameworks: Jest, pytest, JUnit5
CI/CD Platform: GitHub Actions / GitLab CI / Jenkins
Logging Tools: Winston, ELK Stack
Monitoring: Prometheus, Grafana
```

### Step 2: Review Templates
- Read all 5 template files (takes ~30 minutes)
- Identify which are most relevant to your team
- Note parameters you'll need to customize

### Step 3: Team Alignment
- Share templates with team
- Get feedback on priorities
- Agree on adoption timeline
- Assign owners for each area

---

## Phase 2: API Scaffolding (Week 1)

### Task 1: API Template Customization

1. Open [api-scaffolding.md](./api-scaffolding.md)
2. Choose your framework from the examples
3. Create a simple prompt for your first endpoint
4. Test with Copilot in VS Code

**Example customization for your project:**
```
Generate an Express.js POST endpoint for /api/products that:
- Accepts JSON with: name (string), description (string), price (number)
- Validates using joi validator
- Returns product object with id, name, price, createdAt
- Includes error handling for validation failures and database errors
- Has JSDoc documentation
- Follows our REST API standards from docs/api-standards.md
```

### Task 2: Create First Generated API
1. Use the customized prompt
2. Submit to Copilot
3. Review the generated code
4. Test it in your local environment
5. Add to your codebase

### Task 3: Document Your Customization
Save your working prompt as `team-prompts/api-create-endpoint.prompt.txt`

---

## Phase 3: Testing (Week 2)

### Task 1: Implement Unit Test Generation

1. Open [unit-test-generation.md](./unit-test-generation.md)
2. Find your test framework
3. Create a prompt for testing an existing function

**Example:**
```
Generate Jest unit tests for the validateProductName function that:
- Tests valid names (20 chars, unicode, special cases)
- Tests invalid names (empty, too long, special chars)
- Tests edge cases (null, undefined, whitespace)
- Uses expect() assertions
- Follows Arrange-Act-Assert pattern
- Includes parameterized tests
- Targets 100% code coverage
- File name: validateProductName.test.js
```

### Task 2: Generate Tests
1. Pick a function without tests
2. Use the customized template
3. Submit to Copilot
4. Review and integrate tests
5. Verify coverage improved

### Task 3: Create Test Template
Save working prompt as `team-prompts/generate-unit-tests.prompt.txt`

---

## Phase 4: Error Handling (Week 3)

### Task 1: Standardize Error Handling

1. Open [error-handling-patterns.md](./error-handling-patterns.md)
2. Review your current error handling approach
3. Create a prompt matching your standards

**Example:**
```
Generate error handling for the createUser API endpoint that:
- Catches: validation errors, duplicate email, database failures
- Logs warnings with: userId, email, error type, timestamp
- Returns JSON with: { code, message, statusCode, details }
- Implements retry for database timeouts
- Returns 400 for validation, 409 for duplicate, 500 for database
- Follows our error standards from docs/error-handling.md
- Cleans up any partial database transactions
```

### Task 2: Apply to Critical Paths
1. Identify 3-5 critical endpoints without proper error handling
2. Generate error handling using the template
3. Add generated code to your codebase
4. Test error scenarios

---

## Phase 5: Logging & Observability (Week 4)

### Task 1: Setup Structured Logging

1. Open [logging-observability-standards.md](./logging-observability-standards.md)
2. Choose your logging framework
3. Create initialization configuration

**Example:**
```
Generate Winston logging setup for our Node.js API service that:
- Uses Winston with console and file transports
- Log levels: debug, info, warn, error
- Includes context: requestId, userId, serviceName, timestamp
- Formats logs as JSON
- Creates rotating daily file logs
- Logs all HTTP requests with method, path, status, response time
- Exports logs to our ELK stack at logs.company.com
```

### Task 2: Add Logging to Code
1. Import logging into key modules
2. Add structured logging to critical operations
3. Include proper context in all logs
4. Verify logs appear in your logging backend

### Task 3: Create Dashboard
1. Document key metrics to monitor
2. Create Grafana dashboard (or your tool)
3. Set up basic alerts

---

## Phase 6: CI/CD Integration (Week 5)

### Task 1: Choose Your Platform

Review the relevant section in [CI-INTEGRATION-GUIDE.md](./CI-INTEGRATION-GUIDE.md):

- **GitHub Actions**: Use if hosting on GitHub
- **GitLab CI**: Use if hosting on GitLab  
- **Jenkins**: Use if self-hosted

### Task 2: Setup Basic Pipeline

1. Copy the workflow template for your platform
2. Create configuration file in your repo:
   - `.github/workflows/ci.yml` (GitHub)
   - `.gitlab-ci.yml` (GitLab)
   - `Jenkinsfile` (Jenkins)
3. Commit and trigger first run
4. Fix any configuration issues

### Task 3: Add Quality Gates

1. Set up linting step
2. Add test execution step
3. Configure coverage threshold (e.g., 80%)
4. Add failure notifications

### Task 4: Add Copilot Analysis (Optional)

1. Create analysis script (see CI-INTEGRATION-GUIDE.md)
2. Add to pipeline to run on every PR
3. Configure it to comment on PRs with suggestions

---

## Phase 7: Team Training (Week 6)

### Task 1: Create Internal Documentation

Create `docs/copilot-guidelines.md`:
```markdown
# Copilot Usage Guidelines

## When to Use Copilot Templates
- Creating new API endpoints
- Writing unit tests
- Implementing error handling
- Setting up logging

## Code Review Checklist
- [ ] Generated code passes linting
- [ ] All tests pass
- [ ] Code coverage maintained
- [ ] No hardcoded values
- [ ] Follows our naming conventions
- [ ] Proper error handling included

## Common Prompts
- [API Scaffolding](../copilot-prompts/api-scaffolding.md)
- [Unit Tests](../copilot-prompts/unit-test-generation.md)
- [Error Handling](../copilot-prompts/error-handling-patterns.md)
- [Logging](../copilot-prompts/logging-observability-standards.md)
```

### Task 2: Host Team Training

1. Demo templates to the team (30 minutes)
2. Show real examples from your codebase
3. Have team try generating code together
4. Answer questions and collect feedback

### Task 3: Create Team Prompts

Customize templates for your specific projects:

```
team-prompts/
├── api-create-endpoint.prompt.txt
├── generate-unit-tests.prompt.txt
├── add-error-handling.prompt.txt
└── setup-logging.prompt.txt
```

---

## Phase 8: Continuous Improvement (Ongoing)

### Monthly Tasks

- [ ] Review Copilot usage metrics
- [ ] Collect team feedback
- [ ] Update templates based on learnings
- [ ] Share successful examples
- [ ] Identify new use cases

### Metrics to Track

```
Monthly:
- # of Prompts used
- # of Code pieces generated
- % Generated code merged
- Bugs in generated code
- Time saved vs manual coding
- Team satisfaction score

Quarterly:
- Development velocity improvement
- Code coverage trends
- Error handling consistency
- Test quality
```

---

## Quick Reference: Prompt Formula

Use this formula for creating prompts:

```
Generate [LANGUAGE/FRAMEWORK] [CODE_TYPE] that:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]
- [Requirement 4] (error handling)
- [Requirement 5] (logging)
- [Requirement 6] (documentation)
- Follows [YOUR_STANDARDS]
```

**Example:**
```
Generate JavaScript Express.js POST endpoint that:
- Handles /api/users route
- Accepts JSON with: name, email, age
- Validates email format and age > 0
- Returns user with id, createdAt
- Includes error handling for validation and database errors
- Has structured logging with context
- Follows our API standards from docs/api-design.md
```

---

## Troubleshooting

### Issue: Copilot generates code that doesn't compile

**Solution:**
- Specify exact language version: "JavaScript ES2020"
- Reference your package versions: "Express 4.18.2"
- Include linting rules: "Following ESLint airbnb config"

### Issue: Generated tests aren't thorough enough

**Solution:**
- Be specific about edge cases: "test null, undefined, empty string, very long string"
- Request parameterized tests
- Ask for minimum coverage: "Minimum 100% code coverage"
- Request specific assertion counts: "At least 6 assertions per test"

### Issue: CI pipeline is slow

**Solution:**
- Optimize in this order: compile → lint → test → security → coverage
- Run tests in parallel where possible
- Cache dependencies
- Skip optional checks on certain branches

---

## Success Criteria

✅ Phase complete when:

**Phase 1 Setup**
- Team understands all templates
- Tech stack documented
- Everyone has Copilot access

**Phase 2 API**
- Generated at least 2 API endpoints
- Team familiar with api-scaffolding template
- Working prompts documented

**Phase 3 Testing**
- Generated tests for 5+ functions
- Test coverage improved
- Team comfortable with test generation

**Phase 4 Error Handling**
- Added error handling to 3+ endpoints
- Error response format standardized
- Logging includes error context

**Phase 5 Logging**
- Logging configured for service
- Logs flowing to central system
- Basic monitoring dashboard created

**Phase 6 CI/CD**
- Pipeline runs on every PR
- Quality gates preventing regressions
- Team using generated code in CI

**Phase 7 Training**
- Team trained on all templates
- Internal documentation created
- Team prompts saved and shared

**Phase 8 Improvement**
- Monthly metrics tracked
- Feedback collected and reviewed
- Continuous improvement process established

---

## Timeline Summary

```
Week 1-2:  Understand templates + API Generation
Week 3:    Add testing
Week 4:    Error handling + Logging setup
Week 5:    CI/CD pipeline
Week 6:    Team training
Week 7+:   Continuous improvement
```

Estimated total effort: **40-60 developer-hours** over 6 weeks

---

## Next Steps

1. **Today**: Share this document with your team
2. **This week**: Review all templates together
3. **Next week**: Start with API scaffolding template
4. **Week 2**: Add unit testing to workflow
5. **Week 3+**: Build on success with other templates

Choose one template, try it out, and iterate!

---

**Questions?** Each template markdown file has detailed guidance and examples.
