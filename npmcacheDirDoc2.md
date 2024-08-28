Certainly! Here’s a consolidated documentation of both solutions for npm cache management in a Gradle build script, using either the `Exec` task or the Gradle Node plugin.

---

## **npm Cache Management in Gradle Build Script**

### **Solution 1: Using `Exec` Task**

This solution uses Gradle’s `Exec` task to directly run npm commands and configure the cache.

#### **`build.gradle`**

```groovy
// build.gradle

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

// Task to run npm install
task npmInstall(type: Exec) {
    dependsOn configureNpmCache
    workingDir projectDir
    commandLine 'npm', 'install'
}

// Add npmInstall to the build process
build.dependsOn npmInstall
```

#### **Explanation**

- **`configureNpmCache`**: Creates the npm cache directory and configures npm to use it.
- **`npmInstall`**: Runs `npm install` with the configured cache.
- **`build`**: The build process depends on `npmInstall`.

### **Solution 2: Using Gradle Node Plugin**

This solution uses the updated Gradle Node plugin (`com.github.node-gradle.node`) for managing npm tasks and caching.

#### **`build.gradle`**

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

- **Node Plugin Configuration**: Configures the Gradle Node plugin, specifying Node and npm versions.
- **`configureNpmCache`**: Sets up npm caching as in Solution 1.
- **`npmInstall`**: Uses `NpmTask` from the Node plugin to run `npm install`.
- **`build`**: The build process depends on `npmInstall`.

### **Summary**

Both solutions provide effective ways to manage npm caching in a Gradle build script:

1. **Using `Exec` Task**: Directly executes npm commands to configure and use a custom cache directory.
2. **Using Gradle Node Plugin**: Leverages the Node plugin to handle npm tasks, integrating cache configuration similarly.

Choose the solution that best fits your development environment and preferences.
