#!/usr/bin/env bun
import { $ } from "bun";

// const mergedName = "4:PredCart(900, true, true) -> KInd() | 4:PredCart(100, true, true) -> KInd() | 4:PredCart(100) -> KInd().all | 4:PredCart() | 1:Kind()";
// const mergedName = "4:PredCart(900, true, true) -> KInd() | 4:PredCart(900, true) -> KInd() | 4:PredCart() | 1:Kind()";
// const mergedName = "4:PredCart(100, true, true) -> KInd() | 4:PredCart(100, true) -> KInd() | 4:PredCart() | 1:Kind()";
// const mergedName = "4:PredCart(100, true) -> KInd() | 3:PredCart(100, true) -> KInd() | 2:PredCart(100, true) -> KInd()";
// const mergedName = "3:PredCart(100, true) -> KInd() | 4:PredCart() | 1:Kind()";
const mergedName = "2:PredCart(100, true) -> KInd() | 4:PredCart() | 1:Kind()";


const individualFolders = mergedName.split(' | ');

const inputFiles = individualFolders.map(
  (folder) => `./results/baseline/${folder}/*unreach-call.xml.bz2`
);

const outputFile = `./results/${mergedName}`;

const command = [
    "./benchexec/bin/table-generator",
    ...inputFiles,
    "-o",
    outputFile
];

console.log("Input folders parsed:");
console.log(individualFolders);
console.log(command.join(" "));
await $`${command}`;
