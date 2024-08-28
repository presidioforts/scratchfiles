You're right. The `gradle-node-plugin` used to be `com.moowork.node`, but it's been replaced by `com.github.node-gradle.node`. Here’s how you can use the updated Gradle Node plugin to manage npm caching:

### **Updated Version Using Gradle Node Plugin**

This version uses the `com.github.node-gradle.node` plugin for npm tasks and caching.

#### **1. Apply the Updated Node Plugin**

Add the updated Node plugin to your `build.gradle` file:

```groovy
// build.gradle

plugins {
    id 'com.github.node-gradle.node' version '4.0.0' // Use the latest version available
}

node {
    // Define Node and npm versions if needed
    version = '16.20.0' // Specify the Node version you need
    npmVersion = '8.15.0' // Specify the npm version you need
    download = true // Download Node and npm if not already installed
}

// Access Jenkins workspace and build number
def workspaceDir = System.getenv('WORKSPACE') ?: './'
def buildNumber = System.getenv('BUILD_NUMBER') ?: 'default'
def npmCacheDir = "${workspaceDir}/npm-cache-${buildNumber}"

// Task to configure npm cache directory
task configureNpmCache {
    doLast {
        println "Configuring npm cache directory at ${npmCacheDir}"
        
        // Create npm cache directory if it doesn't exist
        def cacheDir = new File(npmCacheDir)
        if (!cacheDir.exists()) {
            cacheDir.mkdirs()
        }

        // Configure npm to use the custom cache directory
        exec {
            commandLine 'npm', 'config', 'set', 'cache', npmCacheDir, '--cache-min=86400'
        }
    }
}

// Task to run npm install using Node plugin
task npmInstall(type: com.github.gradle.node.npm.task.NpmTask) {
    dependsOn configureNpmCache
    description = 'Run npm install'
    args = ['install']
}

// Add npmInstall to the build process
build.dependsOn npmInstall
```

#### **Explanation**
- **Node Plugin Configuration**: Configures the `com.github.node-gradle.node` plugin, specifying Node and npm versions.
- **`configureNpmCache`**: Sets up npm caching similarly to the previous version.
- **`npmInstall`**: Uses `NpmTask` from the Node plugin to run `npm install`.
- **`build`**: The build process depends on `npmInstall`.

### **Summary**

This updated configuration uses the latest Gradle Node plugin, `com.github.node-gradle.node`, to handle npm tasks and caching. This approach ensures compatibility with the latest versions of Node and npm and integrates smoothly into your Gradle build process.
