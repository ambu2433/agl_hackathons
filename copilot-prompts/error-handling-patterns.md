# Error-Handling Patterns Prompt Template

## Purpose
Generate consistent, maintainable error handling code that provides clear error information and recovery strategies.

## Prompt Structure

### Basic Template
```
Generate error handling code for [CONTEXT/OPERATION] that:
- Catches [ERROR_TYPES]
- Provides [ERROR_RESPONSE_FORMAT]
- Logs [LOG_LEVEL] with context: [CONTEXT_DATA]
- Implements [RECOVERY_STRATEGY]
- Returns [HTTP_STATUS/ERROR_OBJECT]
- Follows [PROJECT_ERROR_STANDARDS]
- Cleans up [RESOURCES]
```

---

## Full Example Prompts

### Express.js/Node.js
```
Generate error handling for a file upload endpoint that:
- Catches: validation error (file size), file system error, permission denied
- Logs warnings with: userId, filename, file size, error details
- Returns JSON error response with: code, message, field (if validation)
- Implements retry strategy for temporary file system errors
- Returns 400 for validation, 413 for size limit, 500 for internal errors
- Cleans up temporary files on error
- Includes request ID for tracing
- Follows project's unified error response format
```

### Python/FastAPI
```
Generate error handling for database queries that:
- Catches: connection timeout, duplicate key, constraint violation, not found
- Logs info level with: operation (INSERT/UPDATE), table, error type
- Returns appropriate HTTPException (404, 409, 500) with detail message
- Implements exponential backoff retry for connection timeouts
- Rolls back transaction on constraint violation
- Provides user-friendly error messages vs detailed logs
- Uses structured logging with context manager
- Includes correlation ID from request headers
```

### Java/Spring Boot
```
Generate global error handler using @ControllerAdvice that:
- Handles: ValidationException, ResourceNotFoundException, DataIntegrityViolationException
- Maps exceptions to HTTP status codes (400, 404, 409, 500)
- Logs at appropriate levels (warn for client errors, error for server errors)
- Returns consistent ErrorResponse object with: timestamp, status, message, path, traceId
- Masks sensitive information in production
- Includes validation error details with field names
- Implements circuit breaker pattern for downstream service failures
```

### TypeScript/NestJS
```
Generate custom exception filters for API that:
- Create custom exception classes: ValidationFailure, NotFound, Conflict
- Implement ExceptionFilter interface
- Catch both HTTP and custom exceptions
- Log with context: user ID, request ID, operation details
- Return JSON with: error code (e.g., VALIDATION_FAILED), message, details
- Handle database errors and map to appropriate exceptions
- Handle external API timeouts with retry logic
- Include correlation IDs in error responses
```

---

## Key Parameters

| Parameter | Examples | Purpose |
|-----------|----------|---------|
| `[CONTEXT/OPERATION]` | File upload, database query, API call, authentication | Operation being protected |
| `[ERROR_TYPES]` | ValidationError, NotFoundError, TimeoutError, PermissionError | Exceptions to catch |
| `[ERROR_RESPONSE_FORMAT]` | JSON, XML, GraphQL error extension | Response format |
| `[LOG_LEVEL]` | error, warn, info | Logging severity |
| `[CONTEXT_DATA]` | userId, requestId, operationName, timestamp | Data to include in logs |
| `[RECOVERY_STRATEGY]` | retry with backoff, fallback value, circuit breaker, graceful degradation | Error recovery approach |
| `[HTTP_STATUS]` | 400, 401, 403, 404, 409, 500, 503 | HTTP status code |
| `[PROJECT_ERROR_STANDARDS]` | Your company's error format/strategy | Standard to follow |
| `[RESOURCES]` | temp files, database connections, open streams | What to cleanup |

---

## Error Response Formats

### Standard REST Error
```
Generate error response object with:
- code: string (VALIDATION_FAILED, NOT_FOUND, INTERNAL_ERROR)
- message: string (user-friendly error description)
- statusCode: number (HTTP status code)
- details: object (field validation errors, nested error info)
- timestamp: ISO string
- requestId: string (for tracing)
- path: string (request path for logging)
```

### GraphQL Error Extension
```
Generate error handling that:
- Extends GraphQL error with extensions object
- Includes: code, message, statusCode, correlation_id
- Avoids exposing stack traces in production
- Provides field-specific validation errors
```

### Structured Logging Format
```
Generate logs using structured JSON format:
{
  "timestamp": "ISO-8601",
  "level": "ERROR|WARN|INFO",
  "service": "service-name",
  "requestId": "unique-id",
  "userId": "user-context",
  "operation": "operation-name",
  "errorCode": "ERROR_CODE",
  "message": "human-readable",
  "details": { /* error context */ },
  "stackTrace": "prod: hidden, dev: included"
}
```

---

## Common Error Patterns

### Validation Errors
```
Generate validation error handling that:
- Collects ALL validation errors (not just first)
- Returns field-level error details
- Includes validation rules that failed
- Suggests corrected values where applicable
```

### Retry with Exponential Backoff
```
Generate retry logic that:
- Retries [MAX_ATTEMPTS] times
- Uses exponential backoff: delay = base * (multiplier ^ attempt)
- Only retries on [RETRIABLE_ERRORS]
- Logs retry attempts with attempt number
- Fails fast on non-retriable errors
```

### Circuit Breaker Pattern
```
Generate circuit breaker for external service calls that:
- Opens circuit after [FAILURE_THRESHOLD] consecutive failures
- Half-open state after [TIMEOUT_DURATION]
- Closes on successful request from half-open state
- Escalates from external service error to system unavailable
- Logs state transitions (CLOSED → OPEN → HALF_OPEN)
```

### Graceful Degradation
```
Generate fallback strategy for [SERVICE] that:
- Serves cached data if service is unavailable
- Returns default/empty response for non-critical data
- Logs degradation event for monitoring
- Provides UI indicator that data may be stale
```

---

## Integration Workflow

1. **Identify Error Scenarios**: What can go wrong in this operation
2. **Define Response Format**: How errors should be communicated
3. **Plan Recovery**: Retry, fallback, or fail?
4. **Create Error Classes**: Custom exception types if needed
5. **Use Template**: Customize for your framework
6. **Generate Code**: Submit to Copilot
7. **Add Tests**: Test error paths and recovery
8. **Document**: Add runbooks for critical errors
9. **Monitor**: Set up alerts for error thresholds
