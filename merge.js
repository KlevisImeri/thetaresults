#!/usr/bin/env bun
import { $ } from "bun";

const mergedName = "4:PredCart(900, true, true) -> KInd() | 4:PredCart(900, true) -> KInd()";


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
