# Unit Test Generation Prompt Template

## Purpose
Generate comprehensive, well-structured unit tests with proper mocking, assertions, and coverage.

## Prompt Structure

### Basic Template
```
Generate [TEST_FRAMEWORK] unit tests for [CLASS/FUNCTION_NAME] that:
- Cover [HAPPY_PATH, EDGE_CASES, ERROR_SCENARIOS]
- Mock dependencies: [MOCKS_LIST]
- Test [ASSERTION_TYPES]
- Use [ASSERTION_LIBRARY]
- Follow [BDD|TDD|AAA_pattern]
- Achieve [TARGET_COVERAGE]% code coverage
- Include descriptive test names in [naming_convention]
```

---

## Full Example Prompts

### JavaScript/Jest
```
Generate Jest unit tests for the validateEmail function that:
- Tests valid emails (gmail, corporate, edge cases)
- Tests invalid emails (malformed, special chars, missing @)
- Tests edge cases (empty string, null, undefined)
- Uses expect() assertions
- Follows Arrange-Act-Assert pattern
- Includes parameterized tests for multiple email formats
- Uses describe() and it() with clear test descriptions
- Targets 100% code coverage
- Test file name: validateEmail.test.js
```

### Python/pytest
```
Generate pytest tests for the UserService.create_user method that:
- Mock the database repository dependency
- Test successful user creation with valid data
- Test validation errors (duplicate email, invalid password)
- Test database failures (connection error, constraint violation)
- Mock external calls (email verification, analytics)
- Use pytest fixtures for common setup
- Use parametrize for testing multiple scenarios
- Include both sync and async test cases
- Achieve 95%+ code coverage
```

### Java/JUnit5
```
Generate JUnit5 tests for PaymentService.processPayment that:
- Mock PaymentGateway and NotificationService dependencies
- Test successful payment processing
- Test failure scenarios (declined, timeout, insufficient funds)
- Test idempotency with duplicate requests
- Verify service interactions using mockito.verify()
- Use @DisplayName for readable test names
- Use parameterized tests for multiple payment methods
- Test exception handling with assertThrows()
```

### TypeScript with Angular/Jasmine
```
Generate Jasmine tests for the UserComponent that:
- Mock the UserService dependency
- Test component initialization
- Test template binding for user data display
- Mock HTTP requests using HttpClientTestingModule
- Test user form validation
- Test event handlers (submit, delete, update)
- Use spyOn for service method verification
- Test error state and loading state display
- Cover async operations with fakeAsync/tick
```

---

## Key Parameters

| Parameter | Examples | Purpose |
|-----------|----------|---------|
| `[TEST_FRAMEWORK]` | Jest, pytest, JUnit5, Jasmine, NUnit, xUnit | Testing framework |
| `[CLASS/FUNCTION_NAME]` | validateEmail, UserService, PaymentProcessor | Code under test |
| `[HAPPY_PATH, EDGE_CASES, ERROR_SCENARIOS]` | What scenarios to test | Test coverage scope |
| `[MOCKS_LIST]` | Database, API client, Logger, external service | Dependencies to mock |
| `[ASSERTION_TYPES]` | Value assertions, call verification, exception checks | Test validations |
| `[ASSERTION_LIBRARY]` | expect(), assertThat(), Assert.equals() | Assertion syntax |
| `[BDD\|TDD\|AAA_pattern]` | Given-When-Then, Arrange-Act-Assert | Test structure style |
| `[TARGET_COVERAGE]` | 80, 90, 100 | Code coverage goal % |
| `[naming_convention]` | camelCase, snake_case, descriptive | Test name format |

---

## Enhancement Tips

### Add Snapshot Testing
```
... Also:
- Generate snapshot tests for component rendering
- Include snapshot comparisons for complex objects
- Document when snapshots should be updated
```

### Add Performance Tests
```
... Also:
- Include performance benchmarks
- Test function execution time < [X]ms
- Memory usage assertions
```

### Add Integration Tests
```
... Also:
- Test interactions between multiple components
- Mock external service calls with realistic responses
- Test error recovery flows
```

### Add Visual Regression Tests
```
... Also:
- Include screenshot comparison tests
- Test responsive design at different breakpoints
- Document visual testing tools and setup
```

---

## Test Data Patterns

### Factory Pattern
```
Generate test factories/fixtures for [ENTITY]:
- Default instance with standard values
- Builder pattern for customization
- Multiple variant generators (activeUser, suspendedUser, newUser)
```

### Parameterized Data
```
Generate parameterized test data for [SCENARIOS]:
- Valid inputs with expected outputs
- Invalid inputs with expected errors
- Edge cases (min, max, boundary values)
```

---

## Coverage Verification

```
Generate a coverage report configuration that:
- Tracks line, branch, function, statement coverage
- Set minimum thresholds (lines: 80%, branches: 75%)
- Generate HTML and JSON reports
- Fail CI if coverage drops below threshold
```

---

## Integration Workflow

1. **Identify Code Section**: Class, function, or component to test
2. **List Dependencies**: What needs to be mocked
3. **Define Scenarios**: Happy path, edge cases, errors
4. **Use Template**: Customize for your test framework
5. **Generate Tests**: Submit to Copilot
6. **Review & Refine**: Ensure mocks are correct, asserts are meaningful
7. **Run Tests**: Verify all tests pass
8. **Check Coverage**: Ensure adequate code coverage
9. **Add to CI**: Include in automated test suite
