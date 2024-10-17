
const { execSync } = require('child_process');
const fs = require('fs');

try {
  // Get the location of the .npmrc file dynamically using npm config
  const npmrcPath = execSync('npm config get userconfig', { encoding: 'utf8' }).trim();

  console.log(`NPM config file is located at: ${npmrcPath}`);

  // Read the .npmrc file to get the auth token
  const npmrcContent = fs.readFileSync(npmrcPath, 'utf8');

  // Extract the auth token
  const lines = npmrcContent.split('\n');
  let npmToken = null;

  for (const line of lines) {
    const trimmedLine = line.trim();

    // Adjust this line if you're using a different registry
    if (trimmedLine.startsWith('//registry.npmjs.org/:_authToken=')) {
      npmToken = trimmedLine.split('=')[1];
      break;
    }
  }

  if (npmToken) {
    console.log('NPM auth token retrieved successfully.');

    // Define the registry URL (replace with your actual registry URL)
    const registryUrl = 'https://registry.npmjs.org/'; // Update this to your private registry if needed

    // Strip protocol for npm config key
    const registryUrlKey = registryUrl.replace(/^https?:/, '');

    // Add the registry URL and token dynamically to the npm config
    execSync(`npm config set ${registryUrlKey}:_authToken ${npmToken}`);
    console.log('NPM registry configuration updated with the token.');

    // Now you can run any npm command, and the token will be used for authentication.
    // For example, to publish a package:
    // execSync('npm publish', { stdio: 'inherit' });

  } else {
    console.error('NPM auth token not found in the .npmrc file!');
  }
} catch (error) {
  console.error(`Error: ${error.message}`);
}


