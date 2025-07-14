"""
Code Quality Analysis Tool

Comprehensive static code analysis for the Car Sales Dashboard project.
Analyzes code complexity, maintainability, and adherence to best practices.
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import time
import json


@dataclass
class CodeMetrics:
    """Code metrics for a single file"""
    file_path: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    function_count: int
    class_count: int
    complexity_score: int
    import_count: int
    docstring_coverage: float
    max_line_length: int
    issues: List[str]


@dataclass
class QualityReport:
    """Overall quality report for the project"""
    total_files: int
    total_lines: int
    total_functions: int
    total_classes: int
    avg_complexity: float
    quality_score: float
    issues_summary: Dict[str, int]
    file_metrics: List[CodeMetrics]


class ComplexityAnalyzer(ast.NodeVisitor):
    """AST visitor to calculate cyclomatic complexity"""
    
    def __init__(self):
        self.complexity = 1  # Base complexity
        self.functions = []
        self.classes = []
        self.imports = []
        self.current_function = None
        self.function_complexities = {}
    
    def visit_FunctionDef(self, node):
        """Visit function definition"""
        self.functions.append(node.name)
        old_function = self.current_function
        old_complexity = self.complexity
        
        self.current_function = node.name
        self.complexity = 1  # Reset for this function
        
        # Check for docstring
        has_docstring = (ast.get_docstring(node) is not None)
        
        self.generic_visit(node)
        
        self.function_complexities[node.name] = {
            'complexity': self.complexity,
            'has_docstring': has_docstring,
            'line_number': node.lineno,
            'arg_count': len(node.args.args)
        }
        
        self.current_function = old_function
        self.complexity = old_complexity
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition"""
        self.visit_FunctionDef(node)
    
    def visit_ClassDef(self, node):
        """Visit class definition"""
        self.classes.append(node.name)
        has_docstring = (ast.get_docstring(node) is not None)
        
        # Count methods in class
        method_count = sum(1 for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
        
        self.function_complexities[f"class_{node.name}"] = {
            'complexity': 1,
            'has_docstring': has_docstring,
            'line_number': node.lineno,
            'method_count': method_count
        }
        
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Visit if statement"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Visit while loop"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Visit for loop"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        """Visit exception handler"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        """Visit with statement"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        """Visit assert statement"""
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Visit boolean operation (and/or)"""
        if isinstance(node.op, (ast.And, ast.Or)):
            self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statement"""
        for alias in node.names:
            self.imports.append(alias.name)
    
    def visit_ImportFrom(self, node):
        """Visit from import statement"""
        if node.module:
            for alias in node.names:
                self.imports.append(f"{node.module}.{alias.name}")


class CodeQualityAnalyzer:
    """Main code quality analysis engine"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.exclude_patterns = [
            "__pycache__",
            ".git",
            ".pytest_cache",
            "htmlcov",
            "venv",
            "env",
            ".tox",
            "build",
            "dist",
            ".vscode",
            "node_modules"
        ]
        self.quality_thresholds = {
            'max_complexity': 15,
            'max_line_length': 100,
            'min_docstring_coverage': 0.8,
            'max_function_length': 50,
            'max_class_length': 300,
            'max_function_args': 6
        }
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        
        for file_path in self.project_root.rglob("*.py"):
            # Skip excluded directories
            if any(pattern in str(file_path) for pattern in self.exclude_patterns):
                continue
            
            # Skip test files for main analysis (analyze separately)
            if file_path.name.startswith("test_"):
                continue
                
            python_files.append(file_path)
        
        return python_files
    
    def analyze_file(self, file_path: Path) -> CodeMetrics:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic line analysis
            lines = content.split('\n')
            total_lines = len(lines)
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            blank_lines = sum(1 for line in lines if not line.strip())
            code_lines = total_lines - comment_lines - blank_lines
            
            # Line length analysis
            max_line_length = max(len(line) for line in lines) if lines else 0
            
            # AST analysis
            try:
                tree = ast.parse(content)
                analyzer = ComplexityAnalyzer()
                analyzer.visit(tree)
                
                complexity_score = analyzer.complexity
                function_count = len(analyzer.functions)
                class_count = len(analyzer.classes)
                import_count = len(analyzer.imports)
                
                # Docstring coverage
                functions_with_docs = sum(
                    1 for func_data in analyzer.function_complexities.values()
                    if func_data.get('has_docstring', False)
                )
                docstring_coverage = (
                    functions_with_docs / max(function_count + class_count, 1)
                )
                
            except SyntaxError:
                # File has syntax errors
                complexity_score = 0
                function_count = 0
                class_count = 0
                import_count = 0
                docstring_coverage = 0.0
                analyzer = None
            
            # Issue detection
            issues = self._detect_issues(
                lines, analyzer, complexity_score, max_line_length,
                docstring_coverage, function_count, class_count
            )
            
            return CodeMetrics(
                file_path=str(file_path.relative_to(self.project_root)),
                total_lines=total_lines,
                code_lines=code_lines,
                comment_lines=comment_lines,
                blank_lines=blank_lines,
                function_count=function_count,
                class_count=class_count,
                complexity_score=complexity_score,
                import_count=import_count,
                docstring_coverage=docstring_coverage,
                max_line_length=max_line_length,
                issues=issues
            )
            
        except Exception as e:
            # Return error metrics
            return CodeMetrics(
                file_path=str(file_path.relative_to(self.project_root)),
                total_lines=0,
                code_lines=0,
                comment_lines=0,
                blank_lines=0,
                function_count=0,
                class_count=0,
                complexity_score=0,
                import_count=0,
                docstring_coverage=0.0,
                max_line_length=0,
                issues=[f"Analysis error: {str(e)}"]
            )
    
    def _detect_issues(
        self, 
        lines: List[str], 
        analyzer: Optional[ComplexityAnalyzer],
        complexity: int,
        max_line_length: int,
        docstring_coverage: float,
        function_count: int,
        class_count: int
    ) -> List[str]:
        """Detect code quality issues"""
        issues = []
        
        # Complexity issues
        if complexity > self.quality_thresholds['max_complexity']:
            issues.append(f"High complexity: {complexity} (max: {self.quality_thresholds['max_complexity']})")
        
        # Line length issues
        if max_line_length > self.quality_thresholds['max_line_length']:
            issues.append(f"Long lines: {max_line_length} chars (max: {self.quality_thresholds['max_line_length']})")
        
        # Documentation issues
        if docstring_coverage < self.quality_thresholds['min_docstring_coverage']:
            issues.append(f"Low docstring coverage: {docstring_coverage:.1%} (min: {self.quality_thresholds['min_docstring_coverage']:.1%})")
        
        # Function/class analysis
        if analyzer:
            for name, data in analyzer.function_complexities.items():
                func_complexity = data.get('complexity', 0)
                if func_complexity > self.quality_thresholds['max_complexity']:
                    issues.append(f"Function '{name}' has high complexity: {func_complexity}")
                
                arg_count = data.get('arg_count', 0)
                if arg_count > self.quality_thresholds['max_function_args']:
                    issues.append(f"Function '{name}' has too many arguments: {arg_count}")
        
        # File size issues
        total_functions_classes = function_count + class_count
        if len(lines) > self.quality_thresholds['max_class_length'] and total_functions_classes > 0:
            avg_lines_per_unit = len(lines) / total_functions_classes
            if avg_lines_per_unit > self.quality_thresholds['max_function_length']:
                issues.append(f"Large file: avg {avg_lines_per_unit:.0f} lines per function/class")
        
        # Code style issues
        for i, line in enumerate(lines, 1):
            # Check for common style issues
            if line.strip().endswith('  ') and line.strip():
                issues.append(f"Trailing whitespace on line {i}")
            
            if re.search(r'\t', line):
                issues.append(f"Tab character on line {i} (use spaces)")
        
        return issues
    
    def calculate_quality_score(self, metrics: List[CodeMetrics]) -> float:
        """Calculate overall quality score (0-100)"""
        if not metrics:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric in metrics:
            file_score = 100.0  # Start with perfect score
            weight = max(metric.code_lines, 1)  # Weight by code size
            
            # Deduct points for issues
            issue_count = len(metric.issues)
            file_score -= min(issue_count * 10, 50)  # Max 50 point deduction for issues
            
            # Complexity penalty
            if metric.complexity_score > self.quality_thresholds['max_complexity']:
                excess_complexity = metric.complexity_score - self.quality_thresholds['max_complexity']
                file_score -= min(excess_complexity * 2, 20)  # Max 20 point deduction
            
            # Documentation bonus/penalty
            if metric.docstring_coverage >= self.quality_thresholds['min_docstring_coverage']:
                file_score += 5  # Bonus for good documentation
            else:
                file_score -= 10  # Penalty for poor documentation
            
            # Ensure score is within bounds
            file_score = max(0.0, min(100.0, file_score))
            
            total_score += file_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def analyze_project(self) -> QualityReport:
        """Analyze the entire project"""
        print("🔍 Analyzing code quality...")
        
        python_files = self.find_python_files()
        file_metrics = []
        
        for file_path in python_files:
            print(f"  Analyzing {file_path.name}...", end=" ")
            metrics = self.analyze_file(file_path)
            file_metrics.append(metrics)
            
            issue_count = len(metrics.issues)
            if issue_count == 0:
                print("✅")
            else:
                print(f"⚠️ ({issue_count} issues)")
        
        # Calculate summary statistics
        total_files = len(file_metrics)
        total_lines = sum(m.total_lines for m in file_metrics)
        total_functions = sum(m.function_count for m in file_metrics)
        total_classes = sum(m.class_count for m in file_metrics)
        
        avg_complexity = (
            sum(m.complexity_score for m in file_metrics) / max(total_files, 1)
        )
        
        quality_score = self.calculate_quality_score(file_metrics)
        
        # Summarize issues
        issues_summary = defaultdict(int)
        for metrics in file_metrics:
            for issue in metrics.issues:
                # Categorize issues
                if "complexity" in issue.lower():
                    issues_summary["High Complexity"] += 1
                elif "docstring" in issue.lower():
                    issues_summary["Documentation"] += 1
                elif "line" in issue.lower():
                    issues_summary["Line Length/Style"] += 1
                elif "argument" in issue.lower():
                    issues_summary["Function Arguments"] += 1
                else:
                    issues_summary["Other"] += 1
        
        return QualityReport(
            total_files=total_files,
            total_lines=total_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            avg_complexity=avg_complexity,
            quality_score=quality_score,
            issues_summary=dict(issues_summary),
            file_metrics=file_metrics
        )
    
    def generate_report(self, report: QualityReport, output_file: str = "code_quality_report.md") -> None:
        """Generate a detailed quality report"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Code Quality Analysis Report\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(f"- **Overall Quality Score**: {report.quality_score:.1f}/100\n")
            f.write(f"- **Total Files Analyzed**: {report.total_files}\n")
            f.write(f"- **Total Lines of Code**: {report.total_lines:,}\n")
            f.write(f"- **Functions**: {report.total_functions}\n")
            f.write(f"- **Classes**: {report.total_classes}\n")
            f.write(f"- **Average Complexity**: {report.avg_complexity:.1f}\n\n")
            
            # Quality Grade
            if report.quality_score >= 90:
                grade = "A (Excellent)"
            elif report.quality_score >= 80:
                grade = "B (Good)"
            elif report.quality_score >= 70:
                grade = "C (Acceptable)"
            elif report.quality_score >= 60:
                grade = "D (Needs Improvement)"
            else:
                grade = "F (Poor)"
            
            f.write(f"**Quality Grade**: {grade}\n\n")
            
            # Issues Summary
            if report.issues_summary:
                f.write("## Issues Summary\n\n")
                for issue_type, count in report.issues_summary.items():
                    f.write(f"- **{issue_type}**: {count} issues\n")
                f.write("\n")
            
            # File-by-File Analysis
            f.write("## File Analysis\n\n")
            
            # Sort files by quality score (worst first)
            sorted_files = sorted(
                report.file_metrics,
                key=lambda m: len(m.issues),
                reverse=True
            )
            
            for metrics in sorted_files:
                f.write(f"### {metrics.file_path}\n\n")
                f.write(f"- **Lines**: {metrics.total_lines} (Code: {metrics.code_lines}, Comments: {metrics.comment_lines})\n")
                f.write(f"- **Functions**: {metrics.function_count}, **Classes**: {metrics.class_count}\n")
                f.write(f"- **Complexity**: {metrics.complexity_score}\n")
                f.write(f"- **Docstring Coverage**: {metrics.docstring_coverage:.1%}\n")
                f.write(f"- **Max Line Length**: {metrics.max_line_length}\n")
                
                if metrics.issues:
                    f.write(f"- **Issues** ({len(metrics.issues)}):\n")
                    for issue in metrics.issues:
                        f.write(f"  - {issue}\n")
                else:
                    f.write("- **Issues**: None ✅\n")
                
                f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            
            if report.quality_score < 70:
                f.write("### High Priority\n")
                f.write("- Address complexity issues in functions with high cyclomatic complexity\n")
                f.write("- Improve documentation coverage for functions and classes\n")
                f.write("- Break down large functions into smaller, more focused units\n\n")
            
            if report.avg_complexity > 10:
                f.write("### Code Complexity\n")
                f.write("- Refactor complex functions using extract method pattern\n")
                f.write("- Consider using early returns to reduce nesting\n")
                f.write("- Split complex conditional logic into separate functions\n\n")
            
            f.write("### General Improvements\n")
            f.write("- Add comprehensive docstrings to all public functions and classes\n")
            f.write("- Ensure consistent code formatting (consider using black or autopep8)\n")
            f.write("- Add type hints for better code clarity and IDE support\n")
            f.write("- Consider using linting tools (pylint, flake8) in CI/CD pipeline\n\n")
            
            # Quality Metrics Thresholds
            f.write("## Quality Thresholds Used\n\n")
            for threshold, value in self.quality_thresholds.items():
                f.write(f"- **{threshold.replace('_', ' ').title()}**: {value}\n")
        
        print(f"📊 Code quality report generated: {output_file}")


def main():
    """Main analysis function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Quality Analysis Tool")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), 
                       help="Project root directory")
    parser.add_argument("--output", default="code_quality_report.md", 
                       help="Output report file")
    parser.add_argument("--json", action="store_true", 
                       help="Also output JSON report")
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = CodeQualityAnalyzer(args.project_root)
    report = analyzer.analyze_project()
    
    # Generate reports
    analyzer.generate_report(report, args.output)
    
    if args.json:
        json_file = args.output.replace('.md', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            # Convert dataclasses to dicts for JSON serialization
            report_dict = {
                'total_files': report.total_files,
                'total_lines': report.total_lines,
                'total_functions': report.total_functions,
                'total_classes': report.total_classes,
                'avg_complexity': report.avg_complexity,
                'quality_score': report.quality_score,
                'issues_summary': report.issues_summary,
                'file_metrics': [
                    {
                        'file_path': m.file_path,
                        'total_lines': m.total_lines,
                        'code_lines': m.code_lines,
                        'complexity_score': m.complexity_score,
                        'docstring_coverage': m.docstring_coverage,
                        'issues': m.issues
                    }
                    for m in report.file_metrics
                ]
            }
            json.dump(report_dict, f, indent=2)
        print(f"📋 JSON report generated: {json_file}")
    
    # Print summary
    print(f"\n🎯 Analysis Complete!")
    print(f"   Quality Score: {report.quality_score:.1f}/100")
    print(f"   Total Issues: {sum(report.issues_summary.values())}")
    
    return report.quality_score >= 70


if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    exit(exit_code)
