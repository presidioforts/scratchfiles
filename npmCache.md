# gradle.properties
org.gradle.caching=true
cacheDir=${user.home}/.gradle/caches/${branchName}

// build.gradle
if (project.hasProperty('branchName')) {
    def branchName = project.property('branchName')
    gradle.startParameter.buildCacheDir = new File("${System.getenv('HOME')}/.gradle/caches/${branchName}")
    
}

// build.gradle

// Access the BRANCH_NAME environment variable
ext.branchName = System.getenv('BRANCH_NAME') ?: 'default'

// Configure a custom cache directory based on the branch name
gradle.startParameter.buildCacheDir = new File("${System.getenv('HOME')}/.gradle/caches/${branchName}")

task configureCacheDir {
    doLast {
        def cacheDir = new File("${System.getenv('HOME')}/.gradle/caches/${branchName}")
        if (!cacheDir.exists()) {
            cacheDir.mkdirs()
        }
    }
}

// Ensure the cache directory is configured before any build tasks
tasks.withType(JavaCompile) {
    dependsOn configureCacheDir
}


// build.gradle

// Access the HOME environment variable
def homeDir = System.getenv('HOME') ?: 'default'

// Example usage in a Gradle task
task printHomeDir {
    doLast {
        println "Home directory is: ${homeDir}"
    }
}

