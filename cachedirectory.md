// Access Jenkins or CI workspace and build number
def workspaceDir = System.getenv('WORKSPACE') ?: './'
def buildNumber = System.getenv('BUILD_NUMBER') ?: 'default'
def branchName = System.getenv('BRANCH_NAME') ?: 'feature-branch'

// Define branches where cache expiration should not be set
def noExpirationBranches = ['master', 'main', 'develop']
def cacheDuration = noExpirationBranches.contains(branchName) ? '0' : '2592000' // 0 means no expiration, 30 days for other branches

// Set a branch-specific cache directory
def npmCacheDir = "${workspaceDir}/npm-cache-${branchName}-${buildNumber}"

// Task to configure npm cache directory, overriding the default set by CI
task configureNpmCache {
    doLast {
        println "Setting npm cache directory for branch ${branchName} in project-specific .npmrc"

        // Override the cache directory in the project's .npmrc
        exec {
            commandLine 'npm', 'config', 'set', 'cache', npmCacheDir, '--userconfig', './.npmrc'
        }

        // Set the cache duration in the project's .npmrc
        exec {
            commandLine 'npm', 'config', 'set', 'cache-min', cacheDuration, '--userconfig', './.npmrc'
        }

        // Print the npm cache settings for verification
        exec {
            commandLine 'npm', 'config', 'get', 'cache', '--userconfig', './.npmrc'
        }
        exec {
            commandLine 'npm', 'config', 'get', 'cache-min', '--userconfig', './.npmrc'
        }
    }
}

// Task to run npm install with the overridden cache settings
task npmInstall(type: Exec) {
    dependsOn configureNpmCache
    workingDir projectDir
    commandLine 'npm', 'install', '--verbose'
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
