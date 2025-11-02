import { $ } from "bun";

const folder = "3:PredCart(100, pRes=false) -> KInd()";

const sourcePath = `~/Cloud/benchcloud/results/baseline/${folder}`;
const destinationPath = `./results/baseline/`;

console.log(`Copying from ${sourcePath} to ${destinationPath}...`);
await $`cp -r ${sourcePath} ${destinationPath}`;
