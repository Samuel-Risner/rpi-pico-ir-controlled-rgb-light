const MAX_FREQUENCY = 65536-1;
const INVERT = true;
const FREQUENCY_STEP = MAX_FREQUENCY / 255;

const COLORS = [
    // "rgb(255, 0, 0)", "rgb(0, 255, 0)", "rgb(0, 0, 255)", "rgb(255, 255, 255)",
    "rgb(255, 51, 0)", "rgb(13, 145, 42)", "rgb(16, 102, 201)",
    "rgb(255, 145, 0)", "rgb(0, 255, 255)", "rgb(122, 32, 206)",
    "rgb(255, 187, 0)", "rgb(20, 187, 199)", "rgb(119, 35, 168)",
    "rgb(229, 255, 0)", "rgb(32, 103, 105)", "rgb(234, 0, 255)",
];

/**
 * @param {string} color
 * @returns {number[]}
 */
function extractNumbers(color) {
    color = color.replace("rgb(", "");
    color = color.replace(")", "");

    const strs = color.split(",");
    const nums = [];

    for (const s of strs) {
        nums.push(parseInt(s));
    }

    return nums;
}

/**
 * @param {number} num 
 * @returns {number}
 */
function numberToFrequency(num) {
    let n = num * FREQUENCY_STEP;

    if (INVERT)
        n = MAX_FREQUENCY - n;

    return n;
}

const numsToSkip = [11, 15, 19, 23];
let curNum = 8;

function getHex() {
    if (numsToSkip.includes(curNum)) curNum++;

    let hex = Number(curNum++).toString(16);
    if (hex.length === 1) hex = "0" + hex;

    return hex;
}

let finished = "";

for (const color of COLORS) {
    finished += `    "${getHex()}-ef00": [`;

    for (const num of extractNumbers(color)) {
        finished += `${numberToFrequency(num)},`;
    }

    finished = finished.substring(0, finished.length-1);

    finished += "],\n";
}

console.log(finished);