Here’s a consolidated End User Developer guide for managing npm cache in Gradle builds, including the note about using `'default'` as a fallback value.

---

## **End User Developer Guide: Managing npm Cache in Gradle Builds**

### **Overview**

This guide provides two solutions for managing npm cache in Gradle builds. You can choose between using the `Exec` task or the updated Gradle Node plugin. Each solution ensures compatibility for both local builds and Jenkins builds.

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

### **Note on Fallback Value**

In both solutions, the line:

```groovy
def buildNumber = System.getenv('BUILD_NUMBER') ?: 'default'
```

ensures compatibility for both local and Jenkins builds:

- **Local Builds**: When developers run builds locally, the `BUILD_NUMBER` environment variable may not be set. The fallback value `'default'` is used in such cases.
- **Jenkins Builds**: Jenkins automatically sets the `BUILD_NUMBER` environment variable, so the script uses this value to manage npm caching for each build, providing better separation of cache directories.

### **Summary**

Both solutions effectively manage npm caching in Gradle builds, offering flexibility based on your development environment:

1. **Using `Exec` Task**: Directly executes npm commands to configure and use a custom cache directory.
2. **Using Gradle Node Plugin**: Utilizes the Node plugin to handle npm tasks with integrated cache configuration.

Choose the solution that best fits your needs and development workflow.
