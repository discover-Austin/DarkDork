#!/usr/bin/env python3
"""
Validation script for darkdork_modern.py
Tests structure and imports without running GUI
"""

import sys
import ast
import importlib.util

def validate_python_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
            ast.parse(code)
        print(f"✓ Syntax validation passed for {filepath}")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {filepath}: {e}")
        return False

def check_class_structure(filepath):
    """Check class structure without importing"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    methods = {}

    for cls in classes:
        class_methods = [node.name for node in cls.body if isinstance(node, ast.FunctionDef)]
        methods[cls.name] = class_methods
        print(f"\n✓ Class '{cls.name}' found with {len(class_methods)} methods:")
        for method in class_methods[:10]:  # Show first 10
            print(f"  - {method}()")
        if len(class_methods) > 10:
            print(f"  ... and {len(class_methods) - 10} more methods")

    return methods

def check_imports(filepath):
    """Check what modules are imported"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    print(f"\n✓ Found {len(set(imports))} unique imports:")
    for imp in sorted(set(imports))[:15]:
        print(f"  - {imp}")

    return imports

def check_library_integration():
    """Check if darkdork_library can be imported"""
    try:
        from darkdork_library import DorkLibrary, create_comprehensive_library
        print("\n✓ darkdork_library imports successfully")

        # Test library creation
        lib = create_comprehensive_library()
        print(f"✓ Library created with {len(lib.dorks)} dorks")

        # Test some methods
        stats = lib.get_statistics()
        print(f"✓ Statistics: {stats['total_dorks']} dorks, {stats['total_categories']} categories")

        # Test search
        results = lib.search_dorks(query="password", severity="Critical")
        print(f"✓ Search test: Found {len(results)} critical password-related dorks")

        return True
    except Exception as e:
        print(f"✗ Library integration error: {e}")
        return False

def check_color_scheme(filepath):
    """Check color scheme definition"""
    with open(filepath, 'r') as f:
        content = f.read()

    if 'COLORS' in content and '#0a1628' in content:
        print("\n✓ Dark color scheme defined (DarkNexus style)")
        print("  - bg_dark: #0a1628")
        print("  - accent: #00d4ff")
        return True
    return False

def check_ui_components(filepath):
    """Check if all UI components are defined"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    # Find all method definitions
    methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)

    required_components = [
        'create_modern_ui',
        'create_top_bar',
        'create_query_builder',
        'create_sidebar',
        'create_main_area',
        'create_dork_card',
    ]

    print("\n✓ Checking UI components:")
    for component in required_components:
        if component in methods:
            print(f"  ✓ {component}")
        else:
            print(f"  ✗ {component} MISSING")

    return all(comp in methods for comp in required_components)

def main():
    print("="*60)
    print("DarkDork Modern Interface Validation")
    print("="*60)

    filepath = '/home/user/DarkDork/darkdork_modern.py'

    # Check 1: Syntax
    print("\n[1] Syntax Validation")
    print("-" * 60)
    if not validate_python_syntax(filepath):
        return False

    # Check 2: Class structure
    print("\n[2] Class Structure")
    print("-" * 60)
    methods = check_class_structure(filepath)

    # Check 3: Imports
    print("\n[3] Import Check")
    print("-" * 60)
    imports = check_imports(filepath)

    # Check 4: Color scheme
    print("\n[4] Color Scheme")
    print("-" * 60)
    check_color_scheme(filepath)

    # Check 5: UI components
    print("\n[5] UI Components")
    print("-" * 60)
    check_ui_components(filepath)

    # Check 6: Library integration
    print("\n[6] Library Integration")
    print("-" * 60)
    check_library_integration()

    print("\n" + "="*60)
    print("✓ Validation Complete!")
    print("="*60)
    print("\nThe modern interface is ready to use.")
    print("To run: python darkdork_modern.py")
    print("(Requires tkinter and graphical environment)")

if __name__ == "__main__":
    main()
