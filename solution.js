const fs = require('fs');

function parseBigInt(str, base) {
    let result = BigInt(0);
    const chars = str.toLowerCase();
    const digits = '0123456789abcdefghijklmnopqrstuvwxyz';
    for (let i = 0; i < chars.length; i++) {
        const value = digits.indexOf(chars[i]);
        if (value < 0 || value >= base) throw new Error(`Invalid digit '${chars[i]}' for base ${base}`);
        result = result * BigInt(base) + BigInt(value);
    }
    return result;
}

class BaseConverter {
    static parseInt(value, base) {
        return parseBigInt(value, base);
    }
    
    static toString(num, base) {
        return num.toString(base);
    }
}

class LagrangeInterpolation {
    static interpolate(points, prime = null) {
        const n = points.length;
        if (n === 0) return null;
        if (!prime) {
            prime = BigInt(2) ** BigInt(256) - BigInt(189);
        }
        
        let secret = BigInt(0);
        
        for (let i = 0; i < n; i++) {
            let numerator = BigInt(1);
            let denominator = BigInt(1);
            
            for (let j = 0; j < n; j++) {
                if (i !== j) {
                    numerator = (numerator * (-points[j].x)) % prime;
                    denominator = (denominator * (points[i].x - points[j].x)) % prime;
                }
            }
            
            if (denominator === BigInt(0)) continue;
            
            try {
                const inverse = this.modInverse(denominator, prime);
                const term = ((numerator * inverse) % prime * points[i].y) % prime;
                secret = (secret + term) % prime;
            } catch (error) {
                continue;
            }
        }
        
        return secret;
    }
    
    static modInverse(a, m) {
        a = BigInt(a);
        m = BigInt(m);
        
        if (m === BigInt(1)) return BigInt(0);
        if (a === BigInt(0)) throw new Error("No modular inverse exists");
        
        let [old_r, r] = [a, m];
        let [old_s, s] = [BigInt(1), BigInt(0)];
        let [old_t, t] = [BigInt(0), BigInt(1)];

        while (r !== BigInt(0)) {
            const quotient = old_r / r;
            [old_r, r] = [r, old_r - quotient * r];
            [old_s, s] = [s, old_s - quotient * s];
            [old_t, t] = [t, old_t - quotient * t];
        }

        if (old_r !== BigInt(1)) {
            throw new Error("No modular inverse exists");
        }

        return old_s < 0 ? old_s + m : old_s;
    }
}
class PolynomialSecretFinder {
    constructor() {
        this.points = [];
    }

    parseInput(jsonInput) {
        const { keys } = jsonInput;
        this.n = keys.n;
        this.k = keys.k;
        this.degree = this.k - 1;
        
        for (const [key, value] of Object.entries(jsonInput)) {
            if (key === "keys") continue;
            
            const x = parseInt(key);
            const base = parseInt(value.base);
            const encodedValue = value.value;
            const y = BaseConverter.parseInt(encodedValue, base);
            
            this.points.push({ x: BigInt(x), y: y });
        }
        
        return this.points;
    }
    generateCombinations(points, k) {
        const combinations = [];
        
        function backtrack(start, current) {
            if (current.length === k) {
                combinations.push([...current]);
                return;
            }
            
            for (let i = start; i < points.length; i++) {
                current.push(points[i]);
                backtrack(i + 1, current);
                current.pop();
            }
        }
        
        backtrack(0, []);
        return combinations;
    }
    findConstantTerm() {
        const combinations = this.generateCombinations(this.points, this.k);
        const results = new Map();
        const resultCounts = new Map();
        for (let i = 0; i < combinations.length; i++) {
            const combination = combinations[i];
            
            try {
                const constantTerm = LagrangeInterpolation.interpolate(combination);
                if (constantTerm !== null) {
                    const constantStr = constantTerm.toString();
                    results.set(constantStr, combination);
                    resultCounts.set(constantStr, (resultCounts.get(constantStr) || 0) + 1);
                }
            } catch (error) {
                continue;
            }
        }
        let maxCount = 0;
        let correctConstant = null;
        let correctCombination = null;
        
        for (const [constant, count] of resultCounts) {
            if (count > maxCount) {
                maxCount = count;
                correctConstant = constant;
                correctCombination = results.get(constant);
            }
        }
        
        if (!correctConstant) {
            throw new Error("No valid constant term found from any combination");
        }
        
        return {
            constant: correctConstant,
            combination: correctCombination,
            confidence: maxCount,
            totalCombinations: combinations.length
        };
    }
    solve(jsonInput) {
        this.parseInput(jsonInput);
        const result = this.findConstantTerm();
        
        return result;
    }
}

function solveTestCases() {
    const finder = new PolynomialSecretFinder();
    try {
        const testCase1 = JSON.parse(fs.readFileSync('testcase1.json', 'utf8'));
        const result1 = finder.solve(testCase1);
        console.log(`Test Case 1: ${result1.constant}`);
    } catch (error) {
        console.error(`Error in Test Case 1: ${error.message}`);
    }
    try {
        const testCase2 = JSON.parse(fs.readFileSync('testcase2.json', 'utf8'));
        const result2 = finder.solve(testCase2);
        console.log(`Test Case 2: ${result2.constant}`);
    } catch (error) {
        console.error(`Error in Test Case 2: ${error.message}`);
    }
}
module.exports = {
    PolynomialSecretFinder,
    BaseConverter,
    LagrangeInterpolation
};
if (require.main === module) {
    solveTestCases();
} 