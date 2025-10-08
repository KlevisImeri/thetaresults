#!/usr/bin/env bun
import { $ } from "bun";

const mergedName = "4:PredCart(100, true, true) -> KInd() | 2:PredCart(100, true) -> KInd() | 1:Kind() | 1:PredCart()";


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
