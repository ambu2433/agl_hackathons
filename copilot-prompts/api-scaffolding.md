# API Scaffolding Prompt Template

## Purpose
Generate well-structured REST/GraphQL API endpoints with proper routing, validation, and documentation.

## Prompt Structure

### Basic Template
```
Generate a [framework] API endpoint that:
- Implements [HTTP_METHOD] /[route_path]
- Accepts [REQUEST_TYPE] with fields: [field1, field2, field3]
- Returns [RESPONSE_TYPE] with fields: [response_field1, response_field2]
- Includes input validation using [VALIDATION_LIBRARY]
- Has error handling for [ERROR_CASES]
- Includes JSDoc/docstring comments
- Follows [PROJECT_STYLE_GUIDE]
```

---

## Full Example Prompts

### Express.js REST API
```
Generate an Express.js POST endpoint for /api/users/create that:
- Accepts JSON with: name (string), email (string), age (number)
- Validates email format and age > 0
- Returns user object with id, name, email, createdAt
- Includes error handling for duplicate emails and validation errors
- Uses joi for validation
- Has descriptive JSDoc comments
- Follows our project's error response format { code, message, details }
```

### FastAPI (Python)
```
Generate a FastAPI endpoint GET /api/products/{product_id} that:
- Takes product_id as path parameter
- Returns product details: id, name, description, price, stock
- Includes proper request/response Pydantic models
- Handles 404 when product not found
- Includes query parameter filters: category (optional), min_price (optional)
- Has OpenAPI documentation tags
```

### GraphQL (Apollo Server)
```
Generate a GraphQL Query resolver for getUser that:
- Takes userId as input argument
- Resolves to User type with fields: id, email, profile, posts
- Implements dataloader for N+1 query prevention
- Includes proper error handling and field-level auth checks
- Has JSDoc describing arguments and return types
```

---

## Key Parameters to Customize

| Parameter | Examples | Purpose |
|-----------|----------|---------|
| `[framework]` | Express, FastAPI, Spring Boot, Django, Node.js/hapi | API framework being used |
| `[HTTP_METHOD]` | GET, POST, PUT, DELETE, PATCH | REST operation type |
| `[route_path]` | /api/users, /api/v1/products, /api/auth/login | API endpoint path |
| `[REQUEST_TYPE]` | JSON body, URL query params, form data | Input data format |
| `[RESPONSE_TYPE]` | JSON object, paginated list, stream | Output data format |
| `[VALIDATION_LIBRARY]` | joi, yup, pydantic, zod, ajv | Validation tool |
| `[ERROR_CASES]` | validation errors, not found, auth failures, rate limit | Expected exceptions |
| `[PROJECT_STYLE_GUIDE]` | Google, Airbnb, PEP8, project conventions | Code style reference |

---

## Enhancement Tips

### Add Database Integration
```
... Also:
- Use TypeORM/Sequelize/SQLAlchemy for database queries
- Return paginated results with limit=10, offset=0 parameters
- Include database error handling
```

### Add Authentication
```
... Also:
- Verify JWT token from Authorization header
- Include role-based access control (admin, user, guest)
- Add rate limiting middleware
```

### Add Caching Strategy
```
... Also:
- Cache responses in Redis for 5 minutes
- Invalidate cache when data is updated
- Add Cache-Control headers
```

---

## Integration Workflow

1. **Identify API Requirements**: Endpoint path, HTTP method, request/response data
2. **Use Template**: Customize prompt with your framework and specifications
3. **Generate Code**: Submit to Copilot
4. **Review**: Check validation, error handling, documentation
5. **Integrate**: Add to your codebase and update OpenAPI/Swagger docs
6. **Test**: Write integration tests for the new endpoint
