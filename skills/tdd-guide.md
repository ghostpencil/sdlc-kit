---
name: tdd-guide
description: Comprehensive Test Driven Development guide for engineering subagents with multi-framework support, coverage analysis, and intelligent test generation
---

# TDD Guide - Test Driven Development for Engineering Teams

A comprehensive Test Driven Development skill that provides intelligent test generation, coverage analysis, framework integration, and TDD workflow guidance across multiple languages and testing frameworks.

## Capabilities

### Test Generation
- **Generate Test Cases from Requirements**: Convert user stories, API specs, and business requirements into executable test cases
- **Create Test Stubs**: Generate test function scaffolding with proper naming, imports, and setup/teardown
- **Generate Test Fixtures**: Create realistic test data, mocks, and fixtures for various scenarios

### TDD Workflow Support
- **Guide Red-Green-Refactor**: Step-by-step guidance through TDD cycles with validation
- **Suggest Missing Scenarios**: Identify untested edge cases, error conditions, and boundary scenarios
- **Review Test Quality**: Analyze test isolation, assertions quality, naming conventions, and maintainability

### Coverage & Metrics Analysis
- **Calculate Coverage**: Parse LCOV, JSON, and XML coverage reports for line/branch/function coverage
- **Identify Untested Paths**: Find code paths, branches, and error handlers without test coverage
- **Recommend Improvements**: Prioritized recommendations (P0/P1/P2) for coverage gaps and test quality

### Framework Integration
- **Multi-Framework Support**: Jest, Pytest, JUnit, Vitest, Mocha, RSpec adapters
- **Generate Boilerplate**: Create test files with proper imports, describe blocks, and best practices
- **Configure Test Runners**: Set up test configuration, coverage tools, and CI integration

### Comprehensive Metrics
- **Test Coverage**: Line, branch, function coverage with gap analysis
- **Code Complexity**: Cyclomatic complexity, cognitive complexity, testability scoring
- **Test Quality**: Assertions per test, isolation score, naming quality, test smell detection
- **Test Data**: Boundary value analysis, edge case identification, mock data generation
- **Test Execution**: Timing analysis, slow test detection, flakiness detection
- **Missing Tests**: Uncovered edge cases, error handling gaps, missing integration scenarios

## Input Requirements

The skill supports **automatic format detection** for flexible input:

### Source Code
- **Languages**: TypeScript, JavaScript, Python, Java
- **Format**: Direct file paths or copy-pasted code blocks
- **Detection**: Automatic language/framework detection from syntax and imports

### Test Artifacts
- **Coverage Reports**: LCOV (.lcov), JSON (coverage-final.json), XML (cobertura.xml)
- **Test Results**: JUnit XML, Jest JSON, Pytest JSON, TAP format
- **Format**: File paths or raw coverage data

### Requirements (Optional)
- **User Stories**: Text descriptions of functionality
- **API Specifications**: OpenAPI/Swagger, REST endpoints, GraphQL schemas
- **Business Requirements**: Acceptance criteria, business rules

### Input Methods
- **Option A**: Provide file paths (skill will read files)
- **Option B**: Copy-paste code/data directly
- **Option C**: Mix of both (automatically detected)

## Output Formats

The skill provides **context-aware output** optimized for your environment:

### Code Files
- **Test Files**: Generated tests (Jest/Pytest/JUnit/Vitest) with proper structure
- **Fixtures**: Test data files, mock objects, factory functions
- **Mocks**: Mock implementations, stub functions, test doubles

### Reports
- **Markdown**: Rich coverage reports, recommendations, quality analysis (Claude Desktop)
- **JSON**: Machine-readable metrics, structured data for CI/CD integration
- **Terminal-Friendly**: Simplified output for Claude Code CLI

### Smart Defaults
- **Desktop/Apps**: Rich markdown with tables, code blocks, visual hierarchy
- **CLI**: Concise, terminal-friendly format with clear sections
- **CI/CD**: JSON output for automated processing

### Progressive Disclosure
- **Summary First**: High-level overview (<200 tokens)
- **Details on Demand**: Full analysis available (500-1000 tokens)
- **Prioritized**: P0 (critical) → P1 (important) → P2 (nice-to-have)

## How to Use

### Basic Usage
```
/tdd-guide

I need tests for my authentication module. Here's the code:
[paste code or provide file path]

Generate comprehensive test cases covering happy path, error cases, and edge cases.
```

### Coverage Analysis
```
/tdd-guide

Analyze test coverage for my Python project. Coverage report: coverage/lcov.info

Identify gaps and provide prioritized recommendations.
```

### TDD Workflow
```
/tdd-guide

Guide me through TDD for implementing a password validation function.

Requirements:
- Min 8 characters
- At least 1 uppercase, 1 lowercase, 1 number, 1 special char
- No common passwords
```

## Best Practices

### Test Generation
1. **Start with Requirements**: Write tests from user stories before seeing implementation
2. **Test Behavior, Not Implementation**: Focus on what code does, not how it does it
3. **One Assertion Focus**: Each test should verify one specific behavior
4. **Descriptive Names**: Test names should read like specifications

### TDD Workflow
1. **Red**: Write failing test first
2. **Green**: Write minimal code to make it pass
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Small iterations, frequent commits

### Coverage Goals
1. **Aim for 80%+**: Line coverage baseline for most projects
2. **100% Critical Paths**: Authentication, payments, data validation must be fully covered
3. **Branch Coverage Matters**: Line coverage alone is insufficient
4. **Don't Game Metrics**: Focus on meaningful tests, not coverage numbers

### Test Quality
1. **Independent Tests**: Each test should run in isolation
2. **Fast Execution**: Keep unit tests under 100ms each
3. **Deterministic**: Tests should always produce same results
4. **Clear Failures**: Assertion messages should explain what went wrong

### Framework Selection
1. **Jest**: JavaScript/TypeScript projects (React, Node.js)
2. **Pytest**: Python projects (Django, Flask, FastAPI)
3. **JUnit**: Java projects (Spring, Android)
4. **Vitest**: Modern Vite-based projects

## Multi-Language Support

### Python
- Frameworks: Pytest, unittest, nose2
- Runners: pytest, tox, nox
- Coverage: coverage.py, pytest-cov

### TypeScript/JavaScript
- Frameworks: Jest, Vitest, Mocha, Jasmine
- Runners: Node.js, Karma, Playwright
- Coverage: Istanbul/nyc, c8

### Java
- Frameworks: JUnit 5, TestNG, Mockito
- Runners: Maven Surefire, Gradle Test
- Coverage: JaCoCo, Cobertura

## Limitations

- **Unit Tests Focus**: Primarily optimized for unit tests
- **Report Dependency**: Coverage analysis requires existing coverage reports
- **Version Compatibility**: Targets recent stable versions (Jest 29+, Pytest 7+, JUnit 5+)
- **When NOT to use**: E2E testing, performance testing, security testing

## Version Support

- **Python**: 3.8+ (Pytest 7+)
- **Node.js**: 16+ (Jest 29+, Vitest 0.34+)
- **Java**: 11+ (JUnit 5.9+)
- **TypeScript**: 4.5+
