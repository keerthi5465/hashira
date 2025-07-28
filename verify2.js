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

// Lagrange interpolation for constant term
function lagrangeConstant(points) {
    const n = points.length;
    let secret = BigInt(0);
    const prime = BigInt(2) ** BigInt(256) - BigInt(189);
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
        const inverse = modInverse(denominator, prime);
        const term = ((numerator * inverse) % prime * points[i].y) % prime;
        secret = (secret + term) % prime;
    }
    return secret < 0 ? secret + prime : secret;
}

function modInverse(a, m) {
    a = ((a % m) + m) % m;
    let m0 = m, t, q;
    let x0 = BigInt(0), x1 = BigInt(1);
    if (m === BigInt(1)) return BigInt(0);
    while (a > 1) {
        q = a / m;
        t = m;
        m = a % m;
        a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    if (x1 < 0) x1 += m0;
    return x1;
}

// Read and decode testcase2.json
const data = JSON.parse(fs.readFileSync('testcase2.json', 'utf8'));
const points = [];
for (const [key, value] of Object.entries(data)) {
    if (key === 'keys') continue;
    const x = parseInt(key);
    const base = parseInt(value.base);
    const y = parseBigInt(value.value, base);
    points.push({ x: BigInt(x), y });
}

// Print all decoded points
console.log('Decoded points:');
points.forEach(p => console.log(`(${p.x}, ${p.y})`));

// Use the first 7 points for interpolation
const k = data.keys.k;
const comb = points.slice(0, k);
const constant = lagrangeConstant(comb);
console.log(`\nConstant term for first 7 points: ${constant}`); 