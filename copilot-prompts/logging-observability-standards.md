# Logging and Observability Standards Prompt Template

## Purpose
Generate consistent logging and observability code for monitoring, debugging, and tracing across your system.

## Prompt Structure

### Basic Template
```
Generate logging configuration for [SERVICE_NAME] that:
- Uses [LOGGING_LIBRARY]
- Logs at [LOG_LEVELS]: debug, info, warn, error
- Includes context: [CONTEXT_FIELDS]
- Formats logs as [FORMAT] (JSON, plain text)
- Records [METRICS_TO_TRACK]
- Traces [TRACE_SPANS]
- Exports to [LOGGING_BACKEND]
- Follows [PROJECT_LOGGING_STANDARDS]
```

---

## Full Example Prompts

### Node.js/Winston
```
Generate Winston logging configuration for API service that:
- Uses Winston with multiple transports (console, file, external service)
- Log levels: debug, info, warn, error
- Includes context: requestId, userId, serviceName, timestamp, hostname
- Formats logs as JSON for machine parsing
- Creates rotating file logs (daily, max 100MB)
- Logs all HTTP requests with method, path, status code, response time
- Logs database operation timing and query count
- Exports logs to ELK stack (Elasticsearch/Kibana)
- Uses correlation IDs to trace requests across services
```

### Python/Structlog + OpenTelemetry
```
Generate logging and tracing configuration for microservice that:
- Uses structlog for structured logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Includes context: trace_id, span_id, service_name, version, environment
- Outputs JSON logs with consistent field naming
- Uses OpenTelemetry for distributed tracing
- Records spans for: database queries, external API calls, message processing
- Traces include: duration, error status, result attributes
- Exports traces to Jaeger collector
- Includes automatic instrumentation for common libraries
```

### Java/Spring Boot with Micrometer
```
Generate observability configuration for Spring Boot application that:
- Uses SLF4J with Logback for logging
- Structured logging with: traceId, spanId, userId, version
- MDC (Mapped Diagnostic Context) for context propagation
- Uses Micrometer for metrics (counters, gauges, timers)
- Tracks: request count, response time, error rate, database connection pool
- Uses Spring Cloud Sleuth for distributed tracing (Zipkin export)
- Logs application startup: version, configuration, environment
- Logs shutdown gracefully with in-flight request counts
```

### Go/Zap + OpenTelemetry
```
Generate logging and tracing for Go microservice that:
- Uses Zap for structured, efficient logging
- Fields: timestamp, level, logger, caller, traceID, spanID, message
- JSON output for aggregation
- Uses OpenTelemetry SDK for tracing
- Exports traces to OTLP endpoint (Jaeger/Prometheus)
- Records metrics: request duration, error counts, system resources
- Implements custom instrumentation for business logic
- Includes sampling strategy for high-volume operations
```

---

## Key Parameters

| Parameter | Examples | Purpose |
|-----------|----------|---------|
| `[SERVICE_NAME]` | auth-service, user-api, payment-processor | Application identifier |
| `[LOGGING_LIBRARY]` | Winston, Bunyan, Pino, Structlog, SLF4J, Serilog, Zap | Logging framework |
| `[LOG_LEVELS]` | trace, debug, info, warn, error, fatal | Severity levels |
| `[CONTEXT_FIELDS]` | requestId, userId, traceId, spanId, version, host | Metadata to include |
| `[FORMAT]` | JSON, JSON-seq, plain text, message pack | Log format type |
| `[METRICS_TO_TRACK]` | latency, errors, throughput, resource usage | Metrics to monitor |
| `[TRACE_SPANS]` | http request, database query, cache lookup, external call | Operations to trace |
| `[LOGGING_BACKEND]` | ELK, Datadog, New Relic, Splunk, CloudWatch, Grafana Loki | Log aggregation tool |
| `[PROJECT_LOGGING_STANDARDS]` | Your company's logging standards/format | Internal guidelines |

---

## Logging Levels Guide

### DEBUG
```
Generate DEBUG level logging for:
- Function entry/exit (expensive, development only)
- Variable values during execution
- Internal state changes
- Conditional branch decisions
- Example: logger.debug('User validation passed', { userId, email })
```

### INFO
```
Generate INFO level logging for:
- Application startup events
- Configuration loaded
- Important business operations (user created, order placed)
- State transitions
- Performance milestone achievements
- Example: logger.info('User registered', { userId, email })
```

### WARN
```
Generate WARN level logging for:
- Recoverable errors that should be investigated
- Degraded performance or service
- Deprecated API usage
- Resource thresholds being approached
- Example: logger.warn('Slow query detected', { duration: '5s', table: 'users' })
```

### ERROR
```
Generate ERROR level logging for:
- Exceptions and failures
- Failed operations that impact users
- Critical business failures
- Always include error details and stack trace
- Example: logger.error('Database connection failed', { error, attemptNumber })
```

---

## Context Propagation

### Request ID / Correlation ID
```
Generate request ID propagation that:
- Generates UUID for each incoming request
- Includes in all logs for that request flow
- Passes to downstream service calls
- Stores in response headers for client reference
- Uses middleware/interceptors for automatic injection
```

### Distributed Tracing
```
Generate distributed tracing configuration that:
- Creates root span for each request
- Creates child spans for: database queries, service calls, cache operations
- Propagates trace context across service boundaries (W3C format)
- Records operation duration, error status, custom attributes
- Samples traces intelligently (e.g., 1% of requests, 100% of errors)
```

---

## Metrics Categories

### Application Metrics
```
Generate metrics tracking:
- Request rate (requests/second)
- Response time (p50, p95, p99 latency)
- Error rate (5xx errors, 4xx errors)
- Business metrics (orders processed, users registered, revenue)
- Cache hit ratio
```

### System Metrics
```
Generate system monitoring:
- CPU utilization
- Memory usage (heap, non-heap)
- Disk I/O and storage
- Network bandwidth
- File descriptors / open connections
```

### Database Metrics
```
Generate database tracking:
- Connection pool utilization
- Query count and duration (by operation type)
- Transaction duration
- Slow query threshold warnings
- Deadlock detection
```

---

## Dashboard & Alerting Templates

### Key Metrics Dashboard
```
Generate dashboard queries for:
- Real-time request rate and latency
- Error rate and top error types
- System resource usage
- Service dependency health
- Business KPI trends
```

### Alert Rules
```
Generate alert rules for:
- High error rate (> 5% in 5 minutes)
- High latency (p99 > 2 seconds)
- Service unavailable (no requests in 2 minutes)
- Resource threshold approaching (memory > 85%)
- Database connection pool near capacity
```

---

## Integration Workflow

1. **Choose Tools**: Select logging, metrics, tracing libraries
2. **Define Context**: What fields to include in every log
3. **Set Log Levels**: When to log what information
4. **Use Template**: Customize for your tech stack
5. **Generate Code**: Submit to Copilot for implementation
6. **Add Instrumentation**: Log key operations and metrics
7. **Configure Export**: Connect to logging backend
8. **Create Dashboards**: Build observability views
9. **Set Alerts**: Define critical conditions
10. **Test & Monitor**: Verify logs and metrics flow correctly
