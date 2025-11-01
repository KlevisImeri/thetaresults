import { $ } from "bun";

const folder = "PredCart(900, true) -> KInd()";

const sourcePath = `~/Cloud/benchcloud/results/baseline/${folder}`;
const destinationPath = `./results/baseline/`;

console.log(`Copying from ${sourcePath} to ${destinationPath}...`);
await $`cp -r ${sourcePath} ${destinationPath}`;
