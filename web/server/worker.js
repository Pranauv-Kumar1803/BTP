const { exec } = require('child_process');
const fs = require('fs');
const fse = require('fs-extra');
const cheerio = require('cheerio');
const path = require('path');

// Keeping parseSkipfishReport and saveAsJson functions as they were

const wapiti = async ({url, savePath}) => {
  console.log('inside wapiti function', url);
  const wapitiPath = path.join(savePath, 'wapiti');
  await fse.ensureDir(wapitiPath);
  const outputPath = path.join(wapitiPath, 'wapiti_output.json');

  return new Promise((resolve, reject) => {
    const command = `wapiti -u "${url}" --flush-session -o "${outputPath}" --format json`;
    console.log('Executing command:', command);

    exec(command, (err, stdout, stderr) => {
      if (err) {
        console.error('Wapiti error:', err);
        console.error('Stderr:', stderr);
        reject(err);
        return;
      }
      console.log('Wapiti stdout:', stdout);
      console.log('Wapiti stderr:', stderr);
      resolve(`Wapiti scan completed for ${url}`);
    });
  });
};

const skipfish = async ({url, savePath}) => {
  console.log('inside skipfish function', url);
  const skipfishPath = path.join(savePath, 'skipfish');
  await fse.ensureDir(skipfishPath);
  
  return new Promise((resolve, reject) => {
    const command = `skipfish -o "${skipfishPath}" "${url}"`;
    console.log('Executing command:', command);

    exec(command, (err, stdout, stderr) => {
      if (err) {
        console.error('Skipfish error:', err);
        console.error('Stderr:', stderr);
        reject(err);
        return;
      }
      console.log('Skipfish stdout:', stdout);
      console.log('Skipfish stderr:', stderr);
      resolve(`Skipfish scan completed for ${url}`);
    });
  });
};

const nuclei = async ({url, savePath}) => {
  console.log('inside nuclei', url);
  const nucleiPath = path.join(savePath, 'nuclei');
  await fse.ensureDir(nucleiPath);
  const outputPath = path.join(nucleiPath, 'nuclei_output.json');

  return new Promise((resolve, reject) => {
    const command = `nuclei -u "${url}" -json -o "${outputPath}"`;
    console.log('Executing command:', command);

    exec(command, (err, stdout, stderr) => {
      if (err) {
        console.error('Nuclei error:', err);
        console.error('Stderr:', stderr);
        reject(err);
        return;
      }
      console.log('Nuclei stdout:', stdout);
      console.log('Nuclei stderr:', stderr);
      resolve(`Nuclei scan completed for ${url}`);
    });
  });
};

export default async (task) => {
  switch (task.functionName) {
    case 'wapiti':
      return wapiti(task.args);
    case 'skipfish':
      return skipfish(task.args);
    case 'nuclei':
      return nuclei(task.args);
    default:
      throw new Error(`Unknown function name: ${task.functionName}`);
  }
};