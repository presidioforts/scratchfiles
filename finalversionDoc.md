Certainly! Here’s a refined, professional-style document that you could use for open-source projects or internal documentation, following best practices and clarity standards.

---

# **Managing npm Cache in Jenkins with Gradle**

## **Overview**

This document outlines the best practices for managing npm cache configuration in Jenkins CI/CD pipelines using Gradle. It provides two methods to optimize npm caching: one using the Gradle `Exec` task, and the other leveraging the `gradle-node-plugin`. Additionally, it includes guidance on manual cache clearing to support flexible build management.

## **Goals**

- **Optimize Build Performance**: Reduce build times by efficiently managing npm cache across different branches and environments.
- **Maintain Flexibility**: Provide developers with tools to manage cache expiration dynamically, based on branch-specific requirements.
- **Ensure Consistency**: Implement caching strategies that support both local development and Jenkins-based builds, ensuring reliable performance.

## **Solution 1: Using Gradle `Exec` Task**

### **Purpose**

The Gradle `Exec` task provides a straightforward way to configure npm cache settings dynamically within a build script. This approach is particularly useful for teams that require fine-grained control over npm caching and build processes.

### **Implementation**

```groovy
// Access Jenkins workspace and build number
def workspaceDir = System.getenv('WORKSPACE') ?: './'
def buildNumber = System.getenv('BUILD_NUMBER') ?: 'default'
def branchName = System.getenv('BRANCH_NAME') ?: 'feature-branch'

// Define branches where cache expiration should not be set
def noExpirationBranches = ['master', 'main', 'develop']
def cacheDuration = noExpirationBranches.contains(branchName) ? '0' : '2592000' // 0 means no expiration, 30 days for other branches
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
            commandLine 'npm', 'config', 'set', 'cache', npmCacheDir
            commandLine 'npm', 'config', 'set', 'cache-min', cacheDuration
        }
    }
}

// Task to run npm install
task npmInstall(type: Exec) {
    dependsOn configureNpmCache
    workingDir projectDir
    commandLine 'npm', 'install'
}

// Ensure npmInstall is part of the build process
build.dependsOn npmInstall

// Task to clear npm cache manually
task clearNpmCache {
    doLast {
        def cacheDir = new File(npmCacheDir)
        if (cacheDir.exists()) {
            cacheDir.deleteDir()
            println "npm cache cleared at ${npmCacheDir}"
        }
    }
}

// Expose clearNpmCache as a user-triggered task
task clearCache {
    dependsOn clearNpmCache
}
```

### **Key Points**

- **Branch-Specific Cache Duration**: Critical branches (`master`, `main`, `develop`) use `0` seconds for `cache-min`, meaning the cache never expires. Feature branches use a cache duration of 30 days (`2592000` seconds).
- **Flexible Cache Management**: Developers can manually clear the npm cache using the `clearCache` task, providing control over the build environment.
- **Integrated Workflow**: The `npmInstall` task ensures that npm dependencies are installed after configuring the cache, seamlessly integrating with the build process.

## **Solution 2: Using Gradle Node Plugin**

### **Purpose**

The `gradle-node-plugin` simplifies the management of Node.js and npm within Gradle, making it easier to handle npm tasks while maintaining consistent cache management. This approach is ideal for projects that standardize Node.js and npm versions across environments.

### **Implementation**

1. **Apply the Plugin**

   ```groovy
   plugins {
       id 'com.github.node-gradle.node' version '3.3.0'
   }
   ```

2. **Configure Node and npm Settings**

   ```groovy
   def branchName = System.getenv('BRANCH_NAME') ?: 'feature-branch'

   node {
       version = '14.17.0'  // Specify the Node.js version
       npmVersion = '7.19.0' // Specify the npm version
       download = true       // Download Node.js and npm if not already installed
   }

   def noExpirationBranches = ['master', 'main', 'develop']
   def cacheDuration = noExpirationBranches.contains(branchName) ? '0' : '2592000'
   def npmCacheDir = "${project.buildDir}/npm-cache"

   task configureNpmCache(type: Exec) {
       commandLine 'npm', 'config', 'set', 'cache', npmCacheDir
       commandLine 'npm', 'config', 'set', 'cache-min', cacheDuration
   }

   task npmInstall(type: Exec) {
       dependsOn configureNpmCache
       commandLine 'npm', 'install'
   }

   // Ensure npmInstall is part of the build process
   tasks.named('build') {
       dependsOn npmInstall
   }

   // Task to clear npm cache manually
   task clearNpmCache {
       doLast {
           def cacheDir = new File(npmCacheDir)
           if (cacheDir.exists()) {
               cacheDir.deleteDir()
               println "npm cache cleared at ${npmCacheDir}"
           }
       }
   }

   task clearCache {
       dependsOn clearNpmCache
   }
   ```

### **Key Points**

- **Standardized Environment**: The Node plugin ensures consistency across different environments by managing Node.js and npm versions centrally.
- **Dynamic Cache Configuration**: Similar to the `Exec` task approach, this method configures cache settings based on the branch name, optimizing performance and reliability.
- **Manual Cache Clearing**: The `clearCache` task provides an easy way to clear the npm cache when needed, ensuring flexibility in the build process.

## **Manual Cache Clearing**

### **Purpose**

Manual cache clearing provides developers with the flexibility to reset the npm cache when necessary, helping to resolve issues or prepare the environment for significant changes.

### **Jenkins Pipeline Job for Cache Clearing**

```groovy
pipeline {
    agent any

    stages {
        stage('Clear Cache') {
            steps {
                script {
                    def cacheDir = "${env.WORKSPACE}/npm-cache-${env.BUILD_NUMBER}"
                    sh "rm -rf ${cacheDir}"
                    echo "npm cache cleared at ${cacheDir}"
                }
            }
        }
    }
}
```

### **Gradle Task for Cache Clearing**

```groovy
// build.gradle

task clearNpmCache {
    doLast {
        def cacheDir = new File("${project.buildDir}/npm-cache")
        if (cacheDir.exists()) {
            cacheDir.deleteDir()
            println "npm cache cleared at ${cacheDir}"
        }
    }
}
```

### **Key Points**

- **On-Demand Clearing**: Allows users to clear the npm cache manually, ensuring that the build environment can be reset when necessary.
- **Consistency Across Platforms**: Both Jenkins and Gradle provide consistent ways to clear the cache, integrating seamlessly with existing workflows.

## **Conclusion**

This guide provides a comprehensive approach to managing npm cache in Jenkins with Gradle, offering both flexibility and control over the build process. By adopting these strategies, development teams can optimize their CI/CD pipelines, improve build performance, and maintain consistency across environments.

**Key Takeaways**:

- **Feature Branches** benefit from a 30-day cache expiration, reducing the overhead of frequent cache invalidation.
- **Critical Branches (`master`, `main`, `develop`)** ensure reliability by not expiring the cache, supporting continuous and stable development.
- **Manual Cache Management** allows developers to reset the cache on-demand, providing flexibility and control over the build environment.

This document serves as a guide to implementing best practices in npm cache management, ensuring a smooth and efficient development workflow.

---

This document is now structured to provide clear, professional guidance, suitable for open-source projects or detailed internal documentation.
