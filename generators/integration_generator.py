"""Integration Test Generator - Generates integration tests for multi-component interactions."""

import ast
from pathlib import Path
from typing import Any, Dict, List, Set
from datetime import datetime


class IntegrationTestGenerator:
    """Generates integration tests for multi-component interactions."""
    
    def __init__(self):
        self.test_count = 0
        
    def generate(self, analysis: Dict[str, Any], output_path: Path) -> List[str]:
        """Generate integration tests based on analysis results.
        
        Args:
            analysis: Analysis results containing functions, classes, and imports.
            output_path: Path to output directory for test files.
            
        Returns:
            List of generated test file paths.
        """
        generated_files = []
        
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        imports = analysis.get('imports', [])
        
        # Generate tests for class interactions
        if classes:
            test_file = self._generate_class_integration_tests(classes, output_path)
            if test_file:
                generated_files.append(test_file)
        
        # Generate tests for function workflows
        if functions:
            test_file = self._generate_workflow_tests(functions, classes, output_path)
            if test_file:
                generated_files.append(test_file)
        
        # Generate tests for API/external service interactions
        if imports:
            test_file = self._generate_external_service_tests(imports, output_path)
            if test_file:
                generated_files.append(test_file)
        
        return generated_files
    
    def _generate_class_integration_tests(
        self, 
        classes: List[Dict], 
        output_path: Path
    ) -> str:
        """Generate integration tests for class interactions.
        
        Args:
            classes: List of class information.
            output_path: Path to output directory.
            
        Returns:
            Path to generated test file.
        """
        test_file = output_path / "test_integration_classes.py"
        
        test_content = []
        test_content.append('"""Integration tests for class interactions."""')
        test_content.append('')
        test_content.append('import pytest')
        test_content.append('from unittest.mock import Mock, patch, MagicMock')
        test_content.append('')
        
        # Find class interactions
        class_names = [cls.get('name') for cls in classes]
        
        for i, cls in enumerate(classes):
            class_name = cls.get('name', 'unknown')
            
            # Skip private classes
            if class_name.startswith('_'):
                continue
            
            # Generate tests for interacting with other classes
            for other_cls in classes[i+1:]:
                other_name = other_cls.get('name', 'unknown')
                if other_name.startswith('_'):
                    continue
                    
                test_content.extend(
                    self._generate_class_interaction_test(class_name, other_name)
                )
        
        # Write test file
        with open(test_file, 'w') as f:
            f.write('\n'.join(test_content))
        
        return str(test_file)
    
    def _generate_class_interaction_test(
        self, 
        class1: str, 
        class2: str
    ) -> List[str]:
        """Generate test for interaction between two classes.
        
        Args:
            class1: First class name.
            class2: Second class name.
            
        Returns:
            List of test case code lines.
        """
        test_cases = []
        
        # Test class1 using class2
        test_cases.append(f'def test_{class1}_uses_{class2}():')
        test_cases.append(f'    """Test {class1} using {class2}."""')
        test_cases.append(f'    # Setup')
        test_cases.append(f'    # {class2}_instance = {class2}()')
        test_cases.append(f'    # {class1}_instance = {class1}({class2}_instance)')
        test_cases.append(f'    ')
        test_cases.append(f'    # Test interaction')
        test_cases.append(f'    # Add your assertions')
        test_cases.append('')
        
        # Test class2 using class1
        test_cases.append(f'def test_{class2}_uses_{class1}():')
        test_cases.append(f'    """Test {class2} using {class1}."""')
        test_cases.append(f'    # Setup')
        test_cases.append(f'    # {class1}_instance = {class1}()')
        test_cases.append(f'    # {class2}_instance = {class2}({class1}_instance)')
        test_cases.append(f'    ')
        test_cases.append(f'    # Test interaction')
        test_cases.append(f'    # Add your assertions')
        test_cases.append('')
        
        return test_cases
    
    def _generate_workflow_tests(
        self,
        functions: List[Dict],
        classes: List[Dict],
        output_path: Path
    ) -> str:
        """Generate integration tests for function workflows.
        
        Args:
            functions: List of function information.
            classes: List of class information.
            output_path: Path to output directory.
            
        Returns:
            Path to generated test file.
        """
        test_file = output_path / "test_integration_workflows.py"
        
        test_content = []
        test_content.append('"""Integration tests for function workflows."""')
        test_content.append('')
        test_content.append('import pytest')
        test_content.append('from unittest.mock import Mock, patch, MagicMock')
        test_content.append('')
        
        # Group functions by potential workflow
        function_names = [f.get('name') for f in functions]
        
        # Generate tests for common workflow patterns
        
        # Test: Create -> Process -> Validate workflow
        test_content.extend(self._generate_create_process_validate_workflow(function_names))
        
        # Test: Data flow between functions
        test_content.extend(self._generate_data_flow_tests(function_names))
        
        # Test: Error propagation
        test_content.extend(self._generate_error_propagation_tests(function_names))
        
        # Write test file
        with open(test_file, 'w') as f:
            f.write('\n'.join(test_content))
        
        return str(test_file)
    
    def _generate_create_process_validate_workflow(
        self, 
        function_names: List[str]
    ) -> List[str]:
        """Generate test for create -> process -> validate workflow.
        
        Args:
            function_names: List of function names.
            
        Returns:
            List of test case code lines.
        """
        test_cases = []
        
        # Find create, process, and validate functions
        create_funcs = [f for f in function_names if 'create' in f.lower() or 'init' in f.lower()]
        process_funcs = [f for f in function_names if 'process' in f.lower() or 'transform' in f.lower()]
        validate_funcs = [f for f in function_names if 'validate' in f.lower() or 'check' in f.lower()]
        
        if create_funcs and process_funcs and validate_funcs:
            test_cases.append('def test_create_process_validate_workflow():')
            test_cases.append('    """Test complete create -> process -> validate workflow."""')
            test_cases.append('    # Create')
            test_cases.append(f'    # data = {create_funcs[0]}(...)')
            test_cases.append('    ')
            test_cases.append('    # Process')
            test_cases.append(f'    # processed = {process_funcs[0]}(data)')
            test_cases.append('    ')
            test_cases.append('    # Validate')
            test_cases.append(f'    # result = {validate_funcs[0]}(processed)')
            test_cases.append(f'    # assert result is not None')
            test_cases.append('')
        
        return test_cases
    
    def _generate_data_flow_tests(
        self, 
        function_names: List[str]
    ) -> List[str]:
        """Generate tests for data flow between functions.
        
        Args:
            function_names: List of function names.
            
        Returns:
            List of test case code lines.
        """
        test_cases = []
        
        # Find getter and setter pairs
        getters = [f for f in function_names if 'get' in f.lower() or 'retrieve' in f.lower()]
        setters = [f for f in function_names if 'set' in f.lower() or 'update' in f.lower()]
        
        if getters and setters:
            test_cases.append('def test_data_flow_between_functions():')
            test_cases.append('    """Test data flow between getter and setter functions."""')
            test_cases.append('    # Set data')
            test_cases.append(f'    # {setters[0]}(key, value)')
            test_cases.append('    ')
            test_cases.append('    # Get data')
            test_cases.append(f'    # result = {getters[0]}(key)')
            test_cases.append(f'    # assert result == value')
            test_cases.append('')
        
        return test_cases
    
    def _generate_error_propagation_tests(
        self, 
        function_names: List[str]
    ) -> List[str]:
        """Generate tests for error propagation between functions.
        
        Args:
            function_names: List of function names.
            
        Returns:
            List of test case code lines.
        """
        test_cases = []
        
        test_cases.append('def test_error_propagation():')
        test_cases.append('    """Test that errors are properly propagated."""')
        test_cases.append('    # Test that errors from one function propagate correctly')
        test_cases.append('    # with pytest.raises(Exception):')
        test_cases.append('    #     function1(function2(invalid_input))')
        test_cases.append('')
        
        return test_cases
    
    def _generate_external_service_tests(
        self, 
        imports: List[Dict], 
        output_path: Path
    ) -> str:
        """Generate tests for external service integrations.
        
        Args:
            imports: List of import information.
            output_path: Path to output directory.
            
        Returns:
            Path to generated test file.
        """
        test_file = output_path / "test_integration_external.py"
        
        test_content = []
        test_content.append('"""Integration tests for external service interactions."""')
        test_content.append('')
        test_content.append('import pytest')
        test_content.append('from unittest.mock import Mock, patch, MagicMock')
        test_content.append('')
        
        # Identify external services from imports
        external_services = self._identify_external_services(imports)
        
        for service in external_services:
            test_content.extend(self._generate_external_service_test(service))
        
        # Write test file
        with open(test_file, 'w') as f:
            f.write('\n'.join(test_content))
        
        return str(test_file)
    
    def _identify_external_services(self, imports: List[Dict]) -> Set[str]:
        """Identify external services from imports.
        
        Args:
            imports: List of import information.
            
        Returns:
            Set of external service names.
        """
        external = set()
        
        # Common external service modules
        known_services = {
            'requests', 'urllib', 'httpx', 'aiohttp',  # HTTP
            'boto3', 'botocore',  # AWS
            'google', 'google.cloud',  # Google Cloud
            'azure', 'azure.storage',  # Azure
            'pymongo', 'redis', 'sqlalchemy',  # Databases
            'smtplib', 'email',  # Email
            'stripe', 'paypal',  # Payments
            'twilio', 'slack',  # Communication
            'pusher', 'socketio',  # Real-time
        }
        
        for imp in imports:
            module = imp.get('module', '')
            if any(service in module.lower() for service in known_services):
                # Extract service name
                service_name = module.split('.')[0]
                external.add(service_name)
        
        return external
    
    def _generate_external_service_test(self, service: str) -> List[str]:
        """Generate test for external service interaction.
        
        Args:
            service: Service name.
            
        Returns:
            List of test case code lines.
        """
        test_cases = []
        
        test_cases.append(f'def test_{service}_integration():')
        test_cases.append(f'    """Test integration with {service} service."""')
        test_cases.append(f'    ')
        test_cases.append(f'    # Mock the external service')
        test_cases.append(f'    # with patch("{service}") as mock_{service}:')
        test_cases.append(f'    #     mock_{service}.return_value = ...')
        test_cases.append(f'    ')
        test_cases.append(f'    # Test the integration')
        test_cases.append(f'    # Add your assertions')
        test_cases.append('')
        
        test_cases.append(f'def test_{service}_error_handling():')
        test_cases.append(f'    """Test {service} error handling."""')
        test_cases.append(f'    ')
        test_cases.append(f'    # Test error handling for {service} failures')
        test_cases.append(f'    # with patch("{service}") as mock_{service}:')
        test_cases.append(f'    #     mock_{service}.side_effect = Exception("Service unavailable")')
        test_cases.append(f'    #     with pytest.raises(Exception):')
        test_cases.append(f'    #         call_your_function()')
        test_cases.append('')
        
        return test_cases
