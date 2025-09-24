#!/bin/sh
# Test script untuk memastikan fix-sudo-permissions.sh kompatibel dengan sh

echo "Testing fix-sudo-permissions.sh compatibility with POSIX sh..."

# Test 1: Check shebang
if head -1 fix-sudo-permissions.sh | grep -q "#!/bin/sh"; then
    echo "✅ Shebang correct: #!/bin/sh"
else
    echo "❌ Shebang should be #!/bin/sh"
fi

# Test 2: Check for bash-specific syntax
if grep -q '\[\[' fix-sudo-permissions.sh; then
    echo "❌ Found bash-specific [[ syntax"
else
    echo "✅ No bash-specific [[ syntax found"
fi

# Test 3: Check for $EUID (bash-specific)
if grep -q '$EUID' fix-sudo-permissions.sh; then
    echo "❌ Found bash-specific \$EUID variable"
else
    echo "✅ No bash-specific \$EUID found"
fi

# Test 4: Check for POSIX-compatible $(id -u)
if grep -q '$(id -u)' fix-sudo-permissions.sh; then
    echo "✅ Using POSIX-compatible \$(id -u)"
else
    echo "❌ Should use \$(id -u) instead of \$EUID"
fi

# Test 5: Syntax check with sh
echo "Testing syntax with sh..."
if sh -n fix-sudo-permissions.sh 2>/dev/null; then
    echo "✅ Syntax check passed with sh"
else
    echo "❌ Syntax errors found with sh"
fi

echo "Compatibility test completed!"
