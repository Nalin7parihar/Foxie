"""
Validation utilities for code quality checks.
Extracted from self_correction.py for better separation of concerns.
"""
import ast
from typing import List
from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """Result of code validation."""
    is_valid: bool = Field(description="Whether the code is valid")
    issues: List[str] = Field(default_factory=list, description="List of issues found")
    severity: str = Field(default="info", description="Severity: critical, warning, info")
    file_path: str = Field(description="Path of the validated file")


class CodeValidator:
    """Validates generated Python code for syntax, structure, and best practices."""
    
    @staticmethod
    def validate_syntax(code: str, file_path: str) -> ValidationResult:
        """Validate Python syntax using AST."""
        try:
            ast.parse(code)
            return ValidationResult(
                is_valid=True,
                issues=[],
                severity="info",
                file_path=file_path
            )
        except SyntaxError as e:
            return ValidationResult(
                is_valid=False,
                issues=[f"Syntax Error at line {e.lineno}: {e.msg}"],
                severity="critical",
                file_path=file_path
            )
    
    @staticmethod
    def validate_imports(code: str, file_path: str) -> ValidationResult:
        """Validate import statements."""
        issues = []
        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Check for circular imports (basic check)
            if file_path and 'app/' in file_path:
                module_parts = file_path.replace('\\', '/').split('/')
                if 'app' in module_parts:
                    app_index = module_parts.index('app')
                    current_module = '.'.join(module_parts[app_index:-1])
                    
                    for imp in imports:
                        if current_module in imp:
                            issues.append(f"Potential circular import detected: {imp}")
            
            severity = "warning" if issues else "info"
            return ValidationResult(
                is_valid=len(issues) == 0,
                issues=issues,
                severity=severity,
                file_path=file_path
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                issues=[f"Import validation error: {str(e)}"],
                severity="warning",
                file_path=file_path
            )
    
    @staticmethod
    def validate_fastapi_patterns(code: str, file_path: str) -> ValidationResult:
        """Validate FastAPI-specific patterns and best practices."""
        issues = []
        
        # Check for APIRouter in endpoint files
        if 'endpoints/' in file_path or 'api/' in file_path:
            if 'APIRouter' not in code:
                issues.append("Endpoint file should use APIRouter")
            if '@router.' not in code and 'router = APIRouter()' in code:
                issues.append("No route decorators found for defined router")
        
        # Check for proper dependency injection
        if 'Depends(' in code:
            if 'from fastapi import' not in code or 'Depends' not in code:
                issues.append("Using Depends but not importing it from fastapi")
        
        # Check for response models in CRUD endpoints
        if '@router.post' in code or '@router.get' in code:
            if 'response_model=' not in code and '-> ' not in code:
                issues.append("Endpoints should define response models or return types")
        
        # Check for proper status codes
        if '@router.post' in code and 'status_code=201' not in code:
            issues.append("POST endpoints should return 201 status code")
        
        severity = "warning" if issues else "info"
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            severity=severity,
            file_path=file_path
        )
    
    @staticmethod
    def validate_sqlalchemy_patterns(code: str, file_path: str) -> ValidationResult:
        """Validate SQLAlchemy patterns."""
        issues = []
        
        if 'models/' in file_path and file_path.endswith('.py'):
            # Check for SQLAlchemy 2.0 syntax
            if 'class ' in code and 'Base' in code:
                if 'Mapped[' not in code and 'Column(' in code:
                    issues.append("Use SQLAlchemy 2.0 syntax with Mapped[] instead of Column()")
                
                if 'mapped_column' not in code and 'Mapped[' in code:
                    issues.append("Use mapped_column() with Mapped[] type hints")
        
        severity = "warning" if issues else "info"
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            severity=severity,
            file_path=file_path
        )
    
    @classmethod
    def validate_all(cls, code: str, file_path: str) -> List[ValidationResult]:
        """Run all validators and return all results."""
        validators = [
            cls.validate_syntax,
            cls.validate_imports,
            cls.validate_fastapi_patterns,
            cls.validate_sqlalchemy_patterns
        ]
        
        results = []
        for validator in validators:
            result = validator(code, file_path)
            if not result.is_valid or result.issues:
                results.append(result)
        
        return results
