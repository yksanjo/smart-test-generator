# Smart Test Generator

A comprehensive test generation tool that creates intelligent test suites by understanding code behavior, edge cases, and common failure modes. Goes beyond simple unit tests to integration and property-based testing.

## Features

- **Code Analysis**: Understand code behavior through AST parsing and static analysis
- **Unit Test Generation**: Generate comprehensive unit tests for functions and classes
- **Integration Test Generation**: Create tests for multi-component interactions
- **Property-Based Testing**: Generate tests that verify code properties across many inputs
- **Edge Case Detection**: Automatically identify and test edge cases
- **Common Failure Mode Testing**: Test known failure patterns
- **Test Execution & Reporting**: Run tests and generate detailed reports

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Analyze code and generate tests
python smart_test_generator.py --source /path/to/source --output /path/to/tests

# Generate specific test types
python smart_test_generator.py --source /path/to/source --test-type unit
python smart_test_generator.py --source /path/to/source --test-type integration
python smart_test_generator.py --source /path/to/source --test-type property

# Run generated tests
python smart_test_generator.py --run-tests --test-dir /path/to/tests

# Full pipeline
python smart_test_generator.py --source /path/to/source --output /path/to/tests --run-tests
```

## Test Types

### Unit Tests
- Function input/output testing
- Boundary condition testing
- Error handling verification
- Mock-based isolation testing

### Integration Tests
- Multi-component interaction testing
- Database/API integration testing
- Event flow testing
- End-to-end scenario testing

### Property-Based Tests
- Random input generation
- Invariant verification
- Statistical testing
- Fuzzing support

## Architecture

```
smart_test_generator/
├── analyzers/          # Code analysis modules
│   ├── ast_analyzer.py  # AST-based code analysis
│   ├── edge_detector.py # Edge case detection
│   └── failure_detector.py # Failure mode detection
├── generators/          # Test generation modules
│   ├── unit_generator.py
│   ├── integration_generator.py
│   └── property_generator.py
├── runners/            # Test execution
│   └── test_runner.py
├── templates/          # Test templates
│   └── test_templates.py
├── utils/             # Utilities
│   └── code_parser.py
└── smart_test_generator.py  # Main entry point
```

## Supported Languages

- Python (primary)
- JavaScript/TypeScript (beta)
- Java (beta)

## License

MIT
