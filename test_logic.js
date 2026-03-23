
function testCalculate(expression, currentInput) {
    let fullExpression = expression;
    if (currentInput !== '0' || !expression.trim().endsWith(')')) {
        fullExpression += currentInput;
    }

    // Basic sanitization and conversion for eval
    let toEval = fullExpression.replace(/÷/g, '/').replace(/×/g, '*').replace(/xʸ/g, '**').replace(/\^/g, '**');

    try {
        let result = new Function('return ' + toEval)();
        return { fullExpression, result };
    } catch (e) {
        return { fullExpression, error: e.message };
    }
}

console.log('Test 1: (5 + 3) with currentInput 0 (after paren closed)');
console.log(testCalculate('(5 + 3) ', '0'));

console.log('\nTest 2: (5 + 3) * 2');
console.log(testCalculate('(5 + 3) * ', '2'));

console.log('\nTest 3: 5 + 3');
console.log(testCalculate('', '5 + 3'));
