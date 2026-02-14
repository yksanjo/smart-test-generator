#!/usr/bin/env python3
"""
Smart Test Generator - Main Entry Point

A comprehensive test generation tool that creates intelligent test suites
by understanding code behavior, edge cases, and common failure modes.
"""

import argparse
import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from analyzers.ast_analyzer import ASTAnalyzer
from analyzers.edge_detector import EdgeCaseDetector
from analyzers.failure_detector import FailureModeDetector
from generators.unit_generator import UnitTestGenerator
from generators.integration_generator import IntegrationTestGenerator
from generators.property_generator import PropertyBasedTestGenerator
from runners.test_runner import TestRunner
from utils.code_parser import CodeParser
from utils.report_generator import ReportGenerator


class SmartTestGenerator:
    """Main class for the Smart Test Generator."""
    
    def __init__(self, source_path: str, output_path: str, test_type: str = "all"):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.test_type = test_type
        
        # Initialize components
        self.code_parser = CodeParser()
        self.ast_analyzer = ASTAnalyzer()
        self.edge_detector = EdgeCaseDetector()
        self.failure_detector = FailureModeDetector()
        
        self.unit_generator = UnitTestGenerator()
        self.integration_generator = IntegrationTestGenerator()
        self.property_generator = PropertyBasedTestGenerator()
        
        self.test_runner = TestRunner()
        self.report_generator = ReportGenerator()
        
        # Analysis results
        self.analysis_results: Dict[str, Any] = {}
        self.generated_tests: List[str] = []
        
    def analyze_code(self) -> Dict[str, Any]:
        """Analyze source code to understand its structure and behavior."""
        print(f"🔍 Analyzing code in: {self.source_path}")
        
        if self.source_path.is_file():
            files = [self.source_path]
        else:
            files = list(self.source_path.rglob("*.py"))
        
        analysis_results = {
            "files": [],
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": {},
            "edge_cases": [],
            "failure_modes": []
        }
        
        for file_path in files:
            print(f"  📄 Analyzing: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                # Parse AST
                tree = self.code_parser.parse(source_code)
                
                # Analyze functions and classes
                functions = self.ast_analyzer.extract_functions(tree)
                classes = self.ast_analyzer.extract_classes(tree)
                imports = self.ast_analyzer.extract_imports(tree)
                
                # Detect edge cases
                edge_cases = self.edge_detector.detect(functions, classes)
                
                # Detect failure modes
                failure_modes = self.failure_detector.detect(functions, classes)
                
                analysis_results["files"].append(str(file_path))
                analysis_results["functions"].extend(functions)
                analysis_results["classes"].extend(classes)
                analysis_results["imports"].extend(imports)
                analysis_results["edge_cases"].extend(edge_cases)
                analysis_results["failure_modes"].extend(failure_modes)
                
            except Exception as e:
                print(f"  ⚠️  Error analyzing {file_path}: {e}")
        
        self.analysis_results = analysis_results
        return analysis_results
    
    def generate_tests(self) -> List[str]:
        """Generate test files based on analysis."""
        print(f"\n📝 Generating tests...")
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        generated = []
        
        # Generate unit tests
        if self.test_type in ["all", "unit"]:
            print("  🔧 Generating unit tests...")
            unit_tests = self.unit_generator.generate(
                self.analysis_results,
                self.output_path
            )
            generated.extend(unit_tests)
            
        # Generate integration tests
        if self.test_type in ["all", "integration"]:
            print("  🔧 Generating integration tests...")
            integration_tests = self.integration_generator.generate(
                self.analysis_results,
                self.output_path
            )
            generated.extend(integration_tests)
            
        # Generate property-based tests
        if self.test_type in ["all", "property"]:
            print("  🔧 Generating property-based tests...")
            property_tests = self.property_generator.generate(
                self.analysis_results,
                self.output_path
            )
            generated.extend(property_tests)
        
        self.generated_tests = generated
        print(f"  ✅ Generated {len(generated)} test files")
        
        return generated
    
    def run_tests(self) -> Dict[str, Any]:
        """Run generated tests and collect results."""
        print(f"\n🧪 Running tests...")
        
        results = self.test_runner.run(
            self.output_path,
            self.generated_tests
        )
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a detailed report of the test generation and execution."""
        print(f"\n📊 Generating report...")
        
        report = self.report_generator.generate(
            analysis=self.analysis_results,
            generated_tests=self.generated_tests,
            test_results=results
        )
        
        return report
    
    def run(self, run_tests: bool = False) -> Dict[str, Any]:
        """Run the complete test generation pipeline."""
        print("=" * 60)
        print("🚀 Smart Test Generator")
        print("=" * 60)
        print(f"Source: {self.source_path}")
        print(f"Output: {self.output_path}")
        print(f"Test Type: {self.test_type}")
        print("=" * 60)
        
        # Step 1: Analyze code
        analysis = self.analyze_code()
        
        # Step 2: Generate tests
        generated = self.generate_tests()
        
        results = {}
        
        # Step 3: Run tests if requested
        if run_tests:
            results = self.run_tests()
        
        # Step 4: Generate report
        report = self.generate_report(results)
        
        print("\n" + "=" * 60)
        print("✅ Test Generation Complete!")
        print("=" * 60)
        
        return {
            "analysis": analysis,
            "generated_tests": generated,
            "test_results": results,
            "report": report
        }


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Smart Test Generator - Create comprehensive test suites"
    )
    
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to source code to analyze"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./tests",
        help="Output directory for generated tests"
    )
    
    parser.add_argument(
        "--test-type",
        type=str,
        choices=["all", "unit", "integration", "property"],
        default="all",
        help="Type of tests to generate"
    )
    
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run generated tests after generation"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--report-format",
        type=str,
        choices=["text", "json", "html"],
        default="text",
        help="Report output format"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = SmartTestGenerator(
        source_path=args.source,
        output_path=args.output,
        test_type=args.test_type
    )
    
    # Run pipeline
    try:
        results = generator.run(run_tests=args.run_tests)
        
        # Print summary
        print("\n📋 Summary:")
        print(f"  Files analyzed: {len(results['analysis']['files'])}")
        print(f"  Functions found: {len(results['analysis']['functions'])}")
        print(f"  Classes found: {len(results['analysis']['classes'])}")
        print(f"  Edge cases detected: {len(results['analysis']['edge_cases'])}")
        print(f"  Failure modes detected: {len(results['analysis']['failure_modes'])}")
        print(f"  Tests generated: {len(results['generated_tests'])}")
        
        if results.get('test_results'):
            print(f"  Tests passed: {results['test_results'].get('passed', 0)}")
            print(f"  Tests failed: {results['test_results'].get('failed', 0)}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
