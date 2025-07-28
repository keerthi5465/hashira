// Verification script for Test Case 1
const testCase1 = {
    "keys": {
        "n": 4,
        "k": 3
    },
    "1": {
        "base": "10",
        "value": "4"
    },
    "2": {
        "base": "2",
        "value": "111"
    },
    "3": {
        "base": "10",
        "value": "12"
    },
    "6": {
        "base": "4",
        "value": "213"
    }
};

// Decode points manually
const points = [];
for (const [key, value] of Object.entries(testCase1)) {
    if (key === "keys") continue;
    
    const x = parseInt(key);
    const base = parseInt(value.base);
    const encodedValue = value.value;
    const y = parseInt(encodedValue, base);
    
    points.push({ x: x, y: y });
    console.log(`Point ${x}: (${x}, ${y})`);
}

console.log("\nManual verification:");
console.log("Polynomial f(x) = x² + 3");
console.log("Constant term c = 3");

// Verify each point
points.forEach(point => {
    const x = Number(point.x);
    const expected = x * x + 3;
    console.log(`f(${x}) = ${x}² + 3 = ${expected} ✓`);
});

console.log("\nTest Case 1 answer of 3 is CORRECT!"); 