# Copilot Prompt Templates & CI/CD Integration

A comprehensive guide for using custom Copilot prompt templates and integrating Copilot-powered code generation into your CI/CD pipelines.

## Overview

This directory contains:
- **Custom prompt templates** for common development tasks
- **CI/CD integration guides** for automating code generation and quality checks
- **Example configurations** for GitHub Actions, GitLab CI, and Jenkins

## Template Files

### 1. [API Scaffolding](./api-scaffolding.md)
Generate well-structured REST/GraphQL API endpoints with:
- Proper routing and middleware
- Input validation
- Error handling
- Documentation (JSDoc/docstrings)
- Framework-agnostic examples (Express, FastAPI, Spring Boot, etc.)

**When to use:**
- Creating new endpoints
- Implementing standard REST APIs
- Ensuring consistent API structure

---

### 2. [Unit Test Generation](./unit-test-generation.md)
Generate comprehensive unit tests with:
- Mocking strategies for dependencies
- Edge case and error scenario coverage
- Proper test structure (AAA pattern, BDD)
- Framework-specific examples (Jest, pytest, JUnit5, Jasmine)
- Coverage tracking and reporting

**When to use:**
- Writing tests for new functions/classes
- Improving code coverage
- Testing edge cases and error paths

---

### 3. [Error-Handling Patterns](./error-handling-patterns.md)
Generate robust error handling code with:
- Consistent error response formats
- Proper logging with context
- Recovery strategies (retry, fallback, circuit breaker)
- Exception hierarchy and custom error types
- Framework-specific implementations

**When to use:**
- Adding error handling to API endpoints
- Implementing resilience patterns
- Ensuring consistent error responses
- Handling external service failures

---

### 4. [Logging and Observability Standards](./logging-observability-standards.md)
Generate production-ready logging and observability code with:
- Structured logging with context propagation
- Distributed tracing setup
- Metrics collection and export
- Dashboard and alerting templates
- Tool-agnostic examples (Winston, structlog, Micrometer, Zap)

**When to use:**
- Setting up observability for new services
- Adding logging to existing code
- Implementing distributed tracing
- Creating monitoring dashboards

---

### 5. [CI Integration Guide](./CI-INTEGRATION-GUIDE.md)
Complete guide for integrating Copilot into CI/CD pipelines with:
- **GitHub Actions** workflow examples
- **GitLab CI** pipeline configuration
- **Jenkins** declarative pipeline setup
- Code quality gates and automation
- Security scanning integration
- Pull request automation and comments
- Metrics and monitoring

**When to use:**
- Setting up automated code generation in CI
- Implementing quality gates
- Automating code reviews
- Integrating security scanning

---

## Quick Start

### For Developers

1. **Choose a task**: API scaffolding, test generation, error handling, or logging
2. **Find the template**: Open the relevant `.md` file
3. **Use the prompt**: Copy the prompt template that matches your needs
4. **Customize**: Update parameters with your specific requirements
5. **Submit to Copilot**: Use the prompt in VS Code or web interface
6. **Review & Integrate**: Review the generated code and merge

Example:
```
// Open: api-scaffolding.md
// Copy: "Express.js REST API" prompt
// Customize: Update endpoint path, validation, response format
// Submit to Copilot
// Review generated code
// Add to your codebase
```

### For DevOps/Platform Teams

1. **Choose CI platform**: GitHub Actions, GitLab CI, or Jenkins
2. **Check CI-INTEGRATION-GUIDE.md**: Find your platform section
3. **Copy configuration**: Use the workflow/pipeline configuration
4. **Set up credentials**: Configure API keys and secrets
5. **Deploy**: Enable CI/CD in your repository
6. **Customize**: Adjust quality gates and thresholds for your project
7. **Monitor**: Set up dashboards and alerts

---

## Usage Patterns

### Pattern 1: Manual Code Generation
```
Developer → Review Templates → Use Prompt → Review Code → Merge
```

Best for: One-off code generation, learning, exploration

### Pattern 2: PR-Triggered Suggestions
```
Push Code → CI Analysis → Generate Suggestions → PR Comments → Review → Merge
```

Best for: Code review assistance, consistency checks

### Pattern 3: Automated Code Generation
```
CI Analysis → Generate Missing Code → Run Tests → Create PR → Review → Merge
```

Best for: Boilerplate generation, test generation, scaffolding

---

## Template Parameters Reference

### Common Parameters Across All Templates

| Parameter | Purpose | Examples |
|-----------|---------|----------|
| `[framework]` | Development framework | Express, FastAPI, Spring Boot, Django |
| `[language]` | Programming language | JavaScript, Python, Java, Go, TypeScript |
| `[pattern]` | Design or coding pattern | AAA, BDD, DDD, circuit breaker |
| `[tool]` | Specific tool/library | Jest, pytest, SonarQube, Jaeger |
| `[threshold]` | Numeric limit | 80 (coverage %), 100ms (latency), 5 (attempts) |

---

## Best Practices

### 1. Template Consistency
- Keep prompt templates in version control
- Document all custom parameters used
- Review and update templates quarterly
- Share templates with your team

### 2. Code Review Process
- Always review Copilot-generated code
- Check for security issues and performance
- Verify test coverage and error handling
- Test generated code thoroughly

### 3. CI/CD Integration
- Start with analysis-only mode (no auto-generation)
- Gradually enable code generation as you test
- Set appropriate quality gates
- Monitor for false positives/negatives

### 4. Observability
- Log all Copilot suggestions and generations
- Monitor suggestion accuracy and adoption
- Track which templates are most useful
- Gather team feedback regularly

---

## Team Workflow Examples

### Example 1: API Development
```
1. Developer needs new endpoint
2. Opens api-scaffolding.md template
3. Customizes for their framework and specifications
4. Submits prompt to Copilot
5. Reviews generated code
6. Runs tests to verify
7. Merges to codebase
```

### Example 2: Improving Test Coverage
```
1. CI pipeline detects <80% code coverage
2. Identifies untested files
3. Suggests unit-test-generation.md template
4. Generates test file with coverage targeting untested paths
5. Runs generated tests
6. Adds tests to PR if they pass
7. Creates PR for review
```

### Example 3: Adding Observability
```
1. New service deployed without logging
2. Team runs observability analysis
3. Uses logging-observability-standards.md template
4. Generates structured logging setup
5. Configures metrics and tracing
6. Creates monitoring dashboards
7. Deploys with updated observability
```

---

## Integration with Development Tools

### VS Code
```
1. Install GitHub Copilot extension
2. Open template markdown file
3. Copy prompt section
4. Paste in Copilot chat or new file
5. Follow up with refinements as needed
```

### GitHub Copilot CLI
```bash
# Use templates with copilot command
copilot suggest "Use the prompt from api-scaffolding.md for..."
```

### CI/CD Platforms
See [CI-INTEGRATION-GUIDE.md](./CI-INTEGRATION-GUIDE.md) for:
- GitHub Actions workflows
- GitLab CI pipelines
- Jenkins declarative pipelines
- SonarQube integration
- Security scanning setup

---

## Metrics & ROI

Track the impact of Copilot in your workflow:

- **Code Generation Speed**: Measure time from requirement to functional code
- **Code Quality**: Track bugs introduced in Copilot-generated code
- **Test Coverage**: Monitor coverage improvements from generated tests
- **Development Velocity**: Measure features shipped per sprint
- **Developer Satisfaction**: Survey team on productivity gains

---

## Troubleshooting

### Q: Generated code doesn't match my standards
**A:** 
- Review the prompt - it may be too vague
- Add specific style guide references
- Include examples in the prompt
- Reference your project conventions

### Q: Tests aren't comprehensive enough
**A:**
- Specify edge cases and error scenarios in the prompt
- Request parameterized tests for multiple inputs
- Ask for specific assertion types
- Review coverage reports

### Q: CI pipeline fails on generated code
**A:**
- Ensure code passes linting in template prompt
- Add framework/version specifics
- Request code that follows your stack
- Validate generated code before merging

### Q: How to handle framework-specific code?
**A:**
- Always specify framework in your prompt
- Reference your version if critical
- Include any custom middleware/extensions
- Provide examples of your patterns

---

## Contributing to Templates

Help improve these templates:

1. **Report Issues**: Found a problem? Open an issue
2. **Suggest Improvements**: Have better prompts? Share them
3. **Add Examples**: Contribute real-world usage examples
4. **Test Thoroughly**: Validate templates work in your environment
5. **Share Feedback**: Help others learn from your experience

---

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [Prompt Engineering Guide](https://github.com/brexhq/prompt-engineering)
- [Testing Best Practices](https://testingjavascript.com/)
- [Error Handling Patterns](https://www.oreilly.com/library/view/web-api-design/9781492026914/)
- [Observability Guide](https://opentelemetry.io/docs/)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles)

---

## License

These templates and guides are provided as-is for your team's use.

---

## Questions & Support

For questions about these templates:
1. Check the relevant template markdown file
2. Review the CI-INTEGRATION-GUIDE.md
3. Consult your team's Copilot guidelines
4. Reach out to your development lead

---

**Last Updated**: February 2026

**Version**: 1.0

**Maintainer**: Platform Engineering Team
